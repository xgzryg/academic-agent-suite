"""Build a lookup index from an explicitly supplied journal spreadsheet.

Usage: python build_index.py --data-file project/journals.xlsx
           --output project/journals_index.json
No data is bundled and importing this module does not read or write files.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict


def normalize_text(s):
    if s is None:
        return ''
    s = str(s).upper()
    s = re.sub(r'[^A-Z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def normalize_issn(s):
    if s is None:
        return ''
    return re.sub(r'[^0-9X]', '', str(s)).upper()


def acronym_of(name_norm):
    """Build acronym from a normalized uppercase journal name.

    Rules: take first letter of each word; for hyphenated compounds, take first
    letter of each segment; ignore tiny words ('J', 'OF', 'THE', 'AND', 'AN',
    'A', 'IN', 'ON', 'FOR', 'TO', '&') from the start? We keep them so that
    'JAMA' (Journal of the American Medical Association) still works.
    """
    # normalized name uses single spaces
    words = name_norm.split()
    # Split hyphenated words further
    parts = []
    for w in words:
        for sub in w.split('-'):
            if sub:
                parts.append(sub)
    acr = ''.join(p[0] for p in parts if p)
    return acr


def build_index(src, out_path, sheet='Journals', jif_column=None, source_label=None):
    if not os.path.isfile(src):
        raise FileNotFoundError('The supplied spreadsheet is missing. Provide a file you are entitled to use, or use official online verification.')
    if os.path.exists(out_path):
        raise FileExistsError('The output already exists; choose a new output path to preserve it.')
    import openpyxl
    print(f'Loading workbook: {src}')
    wb = openpyxl.load_workbook(src, data_only=True, read_only=True)
    if sheet not in wb.sheetnames:
        wb.close()
        raise ValueError(f'No worksheet named {sheet!r}; select the correct --sheet.')
    ws = wb[sheet]
    headers = [c.value for c in ws[1]]
    if 'Journal name' not in headers:
        wb.close()
        raise ValueError('The spreadsheet must include a Journal name column.')
    if jif_column is None:
        possible = [h for h in headers if isinstance(h, str) and re.fullmatch(r'(?:\d{4} )?JIF', h)]
        if len(possible) > 1:
            wb.close()
            raise ValueError('Multiple JIF columns exist; choose one with --jif-column.')
        jif_column = possible[0] if possible else None
    elif jif_column not in headers:
        wb.close()
        raise ValueError(f'The requested JIF column {jif_column!r} does not exist.')
    year_match = re.fullmatch(r'(\d{4}) JIF', jif_column or '')
    jif_year = int(year_match.group(1)) if year_match else None

    journals = []
    acronym_index = defaultdict(list)  # acronym -> [journal_idx, ...]
    issn_index = {}  # issn -> journal_idx
    eissn_index = {}
    name_norm_index = {}  # normalized name -> journal_idx (first hit only; we keep all but use first)
    abbr_norm_index = {}

    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
        d = dict(zip(headers, row))
        if not d.get('Journal name'):
            continue
        # Build a compact record — keep fields that are useful for display
        rec = {
            'rank': d.get('Rank'),
            'name': d.get('Journal name'),
            'abbr': d.get('Abbreviated journal'),
            'publisher': d.get('Publisher'),
            'issn': d.get('ISSN'),
            'eissn': d.get('eISSN'),
            'categories': d.get('Categories'),  # may be 'Multiple' or a single string
            'editions': d.get('Editions'),
            'jcr_year': d.get('JCR year'),
            'jif': d.get(jif_column) if jif_column else None,
            'jif_year': jif_year,
            'jif_source_column': jif_column,
            'jif_5y': d.get('5-year JIF'),
            'jif_no_self': d.get('JIF without self cites'),
            'jif_quartile': d.get('JIF quartile'),
            'jif_percentile': d.get('JIF percentile'),
            'jif_rank': d.get('JIF rank'),
            'jci': d.get('JCI'),
            'jci_quartile': d.get('JCI quartile'),
            'jci_percentile': d.get('JCI percentile'),
            'jci_rank': d.get('JCI rank'),
            'total_citations': d.get('Total citations'),
            'total_articles': d.get('Total articles'),
            'citable_items': d.get('Citable items'),
            'pct_oa_gold': d.get('% OA gold'),
            'immediacy_index': d.get('Immediacy index'),
            'eigenfactor': d.get('Eigenfactor'),
            'norm_eigenfactor': d.get('Normalized eigenfactor'),
            'article_influence_score': d.get('Article influence score'),
            'ais_quartile': d.get('AIS quartile'),
            'ais_rank': d.get('AIS rank'),
            'cited_half_life': d.get('Cited half-life'),
            'citing_half_life': d.get('Citing half-life'),
            'category_quartiles_json': d.get('Category quartiles JSON'),
            # internal lookups
            '_name_norm': normalize_text(d.get('Journal name')),
            '_abbr_norm': normalize_text(d.get('Abbreviated journal')),
        }
        idx = len(journals)
        journals.append(rec)

        # Index by acronym
        acr = acronym_of(rec['_name_norm'])
        if acr:
            acronym_index[acr].append(idx)
        # Also index by any all-caps token in the name (length >= 3) — this
        # covers cases like 'JAMA' in 'JAMA-JOURNAL OF THE AMERICAN MEDICAL
        # ASSOCIATION', which a strict first-letter acronym would miss.
        for token in rec['_name_norm'].split():
            tok = re.sub(r'[^A-Z0-9]', '', token)
            if len(tok) >= 3 and tok.isalpha() and tok.isupper() and re.match(r'^[A-Z]+$', tok):
                acronym_index.setdefault(tok, []).append(idx)

        # Index by ISSN
        issn_n = normalize_issn(d.get('ISSN'))
        eissn_n = normalize_issn(d.get('eISSN'))
        if issn_n and issn_n not in issn_index:
            issn_index[issn_n] = idx
        if eissn_n and eissn_n not in eissn_index:
            eissn_index[eissn_n] = idx

        # Index by normalized name (first hit wins)
        nn = rec['_name_norm']
        if nn and nn not in name_norm_index:
            name_norm_index[nn] = idx
        an = rec['_abbr_norm']
        if an and an not in abbr_norm_index:
            abbr_norm_index[an] = idx

    wb.close()
    if not journals:
        raise ValueError('No named journal records were found; no index was written.')
    for key, values in acronym_index.items():
        acronym_index[key] = list(dict.fromkeys(values))
    print(f'Indexed {len(journals)} journals')
    print(f'Unique acronyms: {len(acronym_index)}')
    print(f'Unique ISSNs: {len(issn_index)} + {len(eissn_index)} eISSN')

    out = {
        'meta': {
            'source': source_label or 'User-provided journal spreadsheet',
            'rows': len(journals),
            'jif_source_column': jif_column,
            'jif_year': jif_year,
            'note': 'Values are copied from the selected spreadsheet; no live verification was performed.',
        },
        'journals': journals,
        'index': {
            'acronym': acronym_index,
            'issn': issn_index,
            'eissn': eissn_index,
            'name_norm': name_norm_index,
            'abbr_norm': abbr_norm_index,
        },
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, 'x', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f'Wrote {out_path} ({size_mb:.1f} MB)')
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description='Index your own journal spreadsheet; no data is bundled.')
    parser.add_argument('--data-file', required=True, help='Input XLSX file you are entitled to use')
    parser.add_argument('--output', required=True, help='New JSON output path, preferably in the current project')
    parser.add_argument('--sheet', default='Journals', help='Worksheet name (default: Journals)')
    parser.add_argument('--jif-column', help='Exact metric column name, e.g. 2024 JIF; required if several exist')
    parser.add_argument('--source-label', help='Optional label for the data supplied by the user')
    args = parser.parse_args(argv)
    try:
        build_index(args.data_file, args.output, args.sheet, args.jif_column, args.source_label)
    except (OSError, ValueError, ImportError) as exc:
        print(f'Index not created: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
