#!/usr/bin/env python3
"""Collect PubMed evidence with Python's standard library.

Search/fetch/related metadata is explicit; failures are never zero-hit claims.
This retrieves public records, not the supplied manuscript. No automatic installs,
credential files, or writes to the installed skill directory are used.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'


class EvidenceError(Exception):
    def __init__(self, code, endpoint, message):
        self.code, self.endpoint, self.message = code, endpoint, message
        super().__init__(message)


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def flatten(element):
    return ''.join(element.itertext()).strip() if element is not None else ''


def normalize_ids(values):
    ids = list(dict.fromkeys(v.strip() for v in values.split(',') if v.strip()))
    if not ids or any(not re.fullmatch(r'[1-9][0-9]*', v) for v in ids):
        raise ValueError('Provide one or more numeric positive PMIDs, separated by commas.')
    return ids


class NCBIClient:
    """One process handles network calls in order, at <=2.5 requests/s."""
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.last_call = 0.0

    def request(self, endpoint, params, mode='xml'):
        # Credentials enter only the request body. Do not echo request bodies,
        # full exception objects, or environment values into reports.
        body = dict(params)
        body['tool'] = 'paper-writing-agent'
        key = os.environ.get('NCBI_API_KEY')
        email = os.environ.get('NCBI_EMAIL')
        if key:
            body['api_key'] = key
        if email:
            body['email'] = email
        raw = None
        for attempt in range(3):
            time.sleep(max(0.0, 0.4 - (time.monotonic() - self.last_call)))
            self.last_call = time.monotonic()
            request = urllib.request.Request(BASE+endpoint, data=urllib.parse.urlencode(body).encode('utf-8'), headers={'User-Agent':'paper-writing-agent/1.1 (PubMed evidence)', 'Content-Type':'application/x-www-form-urlencoded'})
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw = response.read()
                break
            except urllib.error.HTTPError as exc:
                if exc.code in {429, 500, 502, 503, 504} and attempt < 2:
                    time.sleep(2 ** (attempt+1))
                    continue
                raise EvidenceError('http_error', endpoint, f'NCBI returned HTTP {exc.code}; no search conclusion follows.') from None
            except (urllib.error.URLError, TimeoutError, OSError):
                if attempt < 2:
                    time.sleep(2 ** (attempt+1))
                    continue
                raise EvidenceError('network_error', endpoint, 'Network request failed after bounded retries; no search conclusion follows.') from None
        try:
            if mode == 'json':
                parsed = json.loads(raw)
                if isinstance(parsed, dict) and ('error' in parsed or 'ERROR' in parsed):
                    raise EvidenceError('api_error', endpoint, 'NCBI returned an API error; inspect query or service state.')
                return parsed
            parsed = ET.fromstring(raw)
            errors = [x for x in parsed.iter() if x.tag.upper() == 'ERROR']
            if errors:
                raise EvidenceError('api_error', endpoint, 'NCBI returned an API error; inspect query or service state.')
            return parsed
        except (json.JSONDecodeError, ET.ParseError, UnicodeError):
            raise EvidenceError('parse_error', endpoint, 'NCBI response could not be parsed; no zero-hit conclusion follows.') from None


def parse_articles(root):
    articles = []
    for record in root.findall('PubmedArticle'):
        citation = record.find('MedlineCitation')
        article = citation.find('Article') if citation is not None else None
        if article is None:
            continue
        pmid = flatten(citation.find('PMID'))
        ids = {node.get('IdType'):flatten(node) for node in record.findall('PubmedData/ArticleIdList/ArticleId')}
        doi = ids.get('doi')
        if not doi:
            doi = next((flatten(node) for node in article.findall('ELocationID') if node.get('EIdType') == 'doi'), None)
        sections = [{'label':node.get('Label') or node.get('NlmCategory') or None, 'text':flatten(node)} for node in article.findall('Abstract/AbstractText')]
        sections = [s for s in sections if s['text']]
        abstract = '\n'.join((s['label']+': ' if s['label'] else '')+s['text'] for s in sections) or None
        authors = []
        for author in article.findall('AuthorList/Author'):
            group = flatten(author.find('CollectiveName'))
            name = group or ' '.join(filter(None,[flatten(author.find('LastName')),flatten(author.find('Initials'))]))
            if name:
                authors.append(name)
        pubdate_node = article.find('Journal/JournalIssue/PubDate')
        pubdate = {name:flatten(pubdate_node.find(name)) for name in ['Year','Month','Day','MedlineDate']} if pubdate_node is not None else {}
        pubdate = {k:v for k,v in pubdate.items() if v}
        articles.append({'pmid':pmid, 'doi':doi or None, 'pmcid':ids.get('pmc'), 'title':flatten(article.find('ArticleTitle')) or None, 'authors':authors, 'journal':flatten(article.find('Journal/Title')) or None, 'journal_abbreviation':flatten(article.find('Journal/ISOAbbreviation')) or None, 'publication_date':pubdate, 'publication_types':[flatten(node) for node in article.findall('PublicationTypeList/PublicationType')], 'abstract':abstract, 'abstract_sections':sections, 'abstract_status':'available' if abstract else 'not_in_returned_record', 'abstract_truncated':False, 'mesh_terms':[flatten(node) for node in citation.findall('MeshHeadingList/MeshHeading/DescriptorName')], 'publication_status':flatten(record.find('PubmedData/PublicationStatus')) or None, 'comments_corrections':[{'type':node.get('RefType'),'pmid':flatten(node.find('PMID')) or None,'reference':flatten(node.find('RefSource')) or None} for node in citation.findall('CommentsCorrectionsList/CommentsCorrections')], 'url':f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/', 'read_level':'record_and_abstract_only', 'full_text_retrieved':False})
    return articles


def fetch_records(client, ids):
    records, failures = [], []
    for start in range(0, len(ids), 100):
        batch = ids[start:start+100]
        try:
            root = client.request('efetch.fcgi', {'db':'pubmed','id':','.join(batch),'retmode':'xml','rettype':'abstract'})
            if root.tag != 'PubmedArticleSet':
                raise EvidenceError('unexpected_response','efetch.fcgi','Expected PubmedArticleSet, received a different response.')
            records.extend(parse_articles(root))
        except EvidenceError as exc:
            failures.append({'pmids':batch,'code':exc.code,'endpoint':exc.endpoint,'message':exc.message})
    requested = set(ids)
    records = [r for r in records if r['pmid'] in requested]
    by_id = {r['pmid']:r for r in records}
    missing = [pmid for pmid in ids if pmid not in by_id]
    records = [by_id[pmid] for pmid in ids if pmid in by_id]
    return {'status':'ok' if not missing and not failures else ('partial' if records else 'error'), 'requested_pmids':ids, 'returned_count':len(records), 'missing_pmids':missing,'failures':failures,'articles':records, 'missing_note':'Missing records or unsupported book records do not prove that a publication never existed.' if missing else None}


def search(client, query, limit, start=0, sort='relevance'):
    raw = client.request('esearch.fcgi', {'db':'pubmed','term':query,'retmode':'json','retmax':limit,'retstart':start,'sort':sort}, mode='json')
    result = raw.get('esearchresult') if isinstance(raw, dict) else None
    if not isinstance(result, dict) or 'count' not in result or not isinstance(result.get('idlist'),list):
        raise EvidenceError('unexpected_response','esearch.fcgi','Search response lacked count or ID list.')
    if result.get('ERROR') or result.get('error'):
        raise EvidenceError('api_error','esearch.fcgi','NCBI reported a query error.')
    try:
        count = int(result['count'])
    except (ValueError,TypeError):
        raise EvidenceError('unexpected_response','esearch.fcgi','Search total was not a valid count.') from None
    ids = result['idlist']
    search_meta={'query':query,'query_translation':result.get('querytranslation'),'database':'pubmed','sort':sort,'total_hits':count,'retstart':start,'requested_limit':limit,'returned_ids':ids,'returned_count':len(ids),'results_truncated':start>0 or start+len(ids)<count,'warnings':result.get('warninglist',{}),'query_errors':result.get('errorlist',{}),'search_url':'https://pubmed.ncbi.nlm.nih.gov/?'+urllib.parse.urlencode({'term':query})}
    if result.get('errorlist'):
        return {'status':'error','search':search_meta,'articles':[],'failures':[{'code':'query_error','endpoint':'esearch.fcgi','message':'NCBI returned query errors; do not interpret as an absence of literature.'}]}
    if count == 0:
        return {'status':'no_hits','search':search_meta,'articles':[],'failures':[]}
    if not ids:
        return {'status':'partial','search':search_meta,'articles':[],'failures':[{'code':'empty_result_window','endpoint':'esearch.fcgi','message':'Search count is positive, but this requested result window returned no IDs.'}]}
    fetched = fetch_records(client,ids)
    return {'status':fetched['status'],'search':search_meta,'fetch':{k:v for k,v in fetched.items() if k!='articles'},'articles':fetched['articles'],'failures':fetched['failures']}


def parse_related(root, seed, limit):
    if root.tag != 'eLinkResult':
        raise EvidenceError('unexpected_response','elink.fcgi','Expected eLinkResult response.')
    matches = []
    seed_present = False
    for linkset in root.findall('LinkSet'):
        if seed not in [flatten(node) for node in linkset.findall('IdList/Id')]:
            continue
        seed_present = True
        for linked in linkset.findall('LinkSetDb'):
            if flatten(linked.find('LinkName')) != 'pubmed_pubmed':
                continue
            for node in linked.findall('Link'):
                pmid = flatten(node.find('Id'))
                if pmid and pmid != seed:
                    rawscore=flatten(node.find('Score'))
                    matches.append({'pmid':pmid,'similarity_score':int(rawscore) if rawscore.isdigit() else None})
    if not seed_present:
        raise EvidenceError('unexpected_response','elink.fcgi','ELink response did not identify the requested seed.')
    unique={item['pmid']:item for item in matches}
    matches=list(unique.values())
    # Sort only to choose similar records, never to score the manuscript.
    if any(item['similarity_score'] is not None for item in matches):
        matches.sort(key=lambda item:-(item['similarity_score'] or 0))
    return {'seed_pmid':seed,'status':'ok' if matches else 'no_links','linkname':'pubmed_pubmed','returned_by_ncbi':len(matches),'selected_count':min(limit,len(matches)),'selected_limit':limit,'results_truncated':len(matches)>limit,'links':matches[:limit],'score_interpretation':'PubMed similarity ranking for retrieval; not novelty, validity, or research quality.'}


def related(client, seeds, limit):
    seed_records=fetch_records(client,seeds)
    found={r['pmid'] for r in seed_records['articles']}
    groups, failures = [], list(seed_records['failures'])
    for seed in seeds:
        if seed not in found:
            groups.append({'seed_pmid':seed,'status':'error','links':[],'message':'Seed record was not retrieved; no similarity conclusion.'})
            continue
        try:
            root=client.request('elink.fcgi',{'dbfrom':'pubmed','db':'pubmed','id':seed,'linkname':'pubmed_pubmed','cmd':'neighbor_score','retmode':'xml'})
            groups.append(parse_related(root,seed,limit))
        except EvidenceError as exc:
            failures.append({'seed_pmid':seed,'code':exc.code,'endpoint':exc.endpoint,'message':exc.message})
            groups.append({'seed_pmid':seed,'status':'error','links':[]})
    ids=list(dict.fromkeys(item['pmid'] for group in groups for item in group['links']))
    fetched=fetch_records(client,ids) if ids else {'status':'ok','articles':[],'failures':[],'missing_pmids':[]}
    failures.extend(fetched['failures'])
    has_errors=any(g['status']=='error' for g in groups) or fetched['status'] != 'ok'
    status=('partial' if found else 'error') if has_errors else ('ok' if ids else 'no_links')
    return {'status':status,'seed_records':seed_records['articles'],'seed_results':groups,'articles':fetched['articles'],'missing_related_pmids':fetched['missing_pmids'],'failures':failures}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True,help='Explicit new JSON output path in the task directory')
    subs=parser.add_subparsers(dest='command',required=True)
    s=subs.add_parser('search'); s.add_argument('--query',required=True); s.add_argument('--limit',type=int,default=20); s.add_argument('--start',type=int,default=0); s.add_argument('--sort',choices=['relevance','pub_date'],default='relevance')
    f=subs.add_parser('fetch'); f.add_argument('--pmids',required=True)
    r=subs.add_parser('related'); r.add_argument('--seeds',required=True); r.add_argument('--limit',type=int,default=10)
    args=parser.parse_args(argv)
    output=args.output.expanduser().resolve()
    install=Path(__file__).resolve().parents[1]
    if output==install or install in output.parents:
        parser.error('Output must be in the user task directory, outside the installed package.')
    if output.exists():
        parser.error('Output already exists; choose a new file path.')
    if args.command in {'search','related'} and not 1 <= args.limit <= 100:
        parser.error('--limit must be 1..100; larger studies require a planned batch strategy.')
    if args.command=='search' and (not args.query.strip() or args.start<0 or args.start+args.limit>9999):
        parser.error('Query must be non-empty and the requested PubMed window must stay within 0..9998.')
    try:
        ids=normalize_ids(args.pmids) if args.command=='fetch' else normalize_ids(args.seeds) if args.command=='related' else None
    except ValueError as exc:
        parser.error(str(exc))
    started=utcnow()
    client=NCBIClient()
    try:
        if args.command=='search':
            result=search(client,args.query,args.limit,args.start,args.sort)
        elif args.command=='fetch':
            result=fetch_records(client,ids)
        else:
            result=related(client,ids,args.limit)
    except EvidenceError as exc:
        result={'status':'error','failures':[{'code':exc.code,'endpoint':exc.endpoint,'message':exc.message}],'articles':[]}
        if args.command=='search':
            result['search']={'query':args.query,'total_hits':None,'requested_limit':args.limit,'retstart':args.start,'sort':args.sort}
    result={'source':'NCBI PubMed E-utilities','command':args.command,'started_at_utc':started,'finished_at_utc':utcnow(),'request_interval_seconds':0.4,**result}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8') as handle:
        json.dump(result,handle,ensure_ascii=False,indent=2)
        handle.write('\n')
    print(json.dumps({'status':result['status'],'article_count':len(result.get('articles',[])),'output':str(output)},ensure_ascii=False))
    return 1 if result['status'] in {'error','partial'} else 0


if __name__=='__main__':
    sys.exit(main())
