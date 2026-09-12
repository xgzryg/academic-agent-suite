#!/usr/bin/env python3
"""Heuristic reviewer/comment splitting with source line positions and draft scaffolds."""
import argparse, json, re
from pathlib import Path

HEADER=re.compile(r'^(?:Reviewer\s*\d+|Referee\s*\d+|审稿人\s*\d+|(?:Associate\s+)?Editor)(?:\s*[:：-]\s*)?$',re.I)
COMMENT=re.compile(r'^\s*(?:(?:Comment|Point)\s*\d+(?:\.\d+)?[.:：)]?|\d+(?:\.\d+)?[.)、：])(?:\s+|$)',re.I)

def parse(text):
    groups=[];group={'reviewer':'Unassigned','comments':[]};lines=[];start=1
    def flush():
        nonlocal lines
        if any(x.strip() for x in lines):
            group['comments'].append({'source_line':start,'text':'\n'.join(lines).strip()})
        lines=[]
    for num,line in enumerate(text.splitlines(),1):
        if HEADER.fullmatch(line.strip()):
            flush()
            if group['comments']:groups.append(group)
            group={'reviewer':line.strip().rstrip(':：-').strip(),'comments':[]};start=num+1
        elif COMMENT.match(line):
            flush();start=num;lines=[line]
        else:
            if not lines:start=num
            lines.append(line)
    flush()
    if group['comments']:groups.append(group)
    return {'status':'heuristic_requires_source_check','reviewers':groups,'comment_count':sum(len(g['comments']) for g in groups)}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--scaffold',type=Path)
    a=p.parse_args()
    try:
        if a.out.exists() or (a.scaffold and a.scaffold.exists()):raise FileExistsError('Output exists; no overwrite')
        data=parse(a.input.read_text(encoding='utf-8-sig'))
        if not data['comment_count']:raise ValueError('No review text found')
        if a.scaffold and a.scaffold.resolve()==a.out.resolve():raise ValueError('JSON and scaffold paths must differ')
        scaffold=[]
        for g in data['reviewers']:
            scaffold+=['# '+g['reviewer'],'']
            for i,c in enumerate(g['comments'],1):
                scaffold+=['## Comment '+str(i),c['text'],'','Response: [AUTHOR_INPUT_NEEDED]','Reason/evidence: [AUTHOR_INPUT_NEEDED]','Concrete revision: [AUTHOR_INPUT_NEEDED]','Location: [AUTHOR_INPUT_NEEDED]','Author action: [AUTHOR_INPUT_NEEDED]','']
        a.out.parent.mkdir(parents=True,exist_ok=True)
        with a.out.open('x',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2)
        if a.scaffold:
            a.scaffold.parent.mkdir(parents=True,exist_ok=True)
            with a.scaffold.open('x',encoding='utf-8') as f:f.write('\n'.join(scaffold))
        print(json.dumps({'comment_count':data['comment_count'],'status':data['status']},ensure_ascii=False))
        return 0
    except (ValueError,OSError) as exc:p.exit(1,f'{exc}\n')
if __name__=='__main__':raise SystemExit(main())
