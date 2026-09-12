"""Project-local entrypoint for selected editable slide tools. No installation or network actions."""
from __future__ import annotations
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
from xml.etree import ElementTree as ET

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def target(path, overwrite=False):
    p = Path(path).resolve()
    if p.exists() and not overwrite:
        raise FileExistsError(f'Output exists; use a new path or authorized --overwrite: {p}')
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def temp_at(directory):
    p = Path(directory).resolve() / '.engine-tmp'
    p.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(p)
    for name in ['TEMP','TMP','TMPDIR']:
        os.environ[name] = str(p)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def patch_runs(source, plan, output):
    """Edit requested native text runs only; all other package bytes are retained."""
    from template_fill_pptx import _slide_refs
    with zipfile.ZipFile(source) as z:
        entries = {n:z.read(n) for n in z.namelist()}
    refs = _slide_refs(entries)
    ns = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
          'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    modified = {}
    for item in plan.get('edits', []):
        slide = int(item['slide'])
        if slide not in refs:
            raise ValueError(f'Unknown presentation slide: {slide}')
        part = refs[slide][0]
        root = modified.setdefault(part, ET.fromstring(entries[part]))
        shapes = [s for s in root.findall('.//p:sp',ns)
                  if (s.find('p:nvSpPr/p:cNvPr',ns) is not None and
                      s.find('p:nvSpPr/p:cNvPr',ns).get('id') == str(item['shape_id']))]
        if len(shapes) != 1:
            raise ValueError(f'Expected one text shape for slide {slide}, shape {item["shape_id"]}')
        runs = shapes[0].findall('./p:txBody/a:p/a:r',ns)
        index = int(item['run_index'])
        if index < 0 or index >= len(runs):
            raise ValueError(f'Run index {index} outside this shape; inspect the current PPTX first.')
        text = runs[index].find('a:t',ns)
        if text is None:
            raise ValueError('Requested run has no text')
        if 'expected_text' in item and text.text != item['expected_text']:
            raise ValueError('Current run differs from expected_text; re-read the current deck.')
        text.text = str(item['text'])
    for part, root in modified.items():
        entries[part] = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in entries.items():
            z.writestr(name,data)

def parser():
    p = argparse.ArgumentParser(description='Bundled native SVG, template and PPTX editing tools')
    sub = p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('svg',help='SVG project folder -> editable native PPTX, without animation')
    s.add_argument('project');s.add_argument('--output',required=True)
    s.add_argument('--source',default='output')
    s=sub.add_parser('template-inspect',help='Read slide IDs, text slots, tables and charts')
    s.add_argument('input');s.add_argument('--output',required=True)
    s=sub.add_parser('template-plan',help='Create an editable fill plan from inspected library')
    s.add_argument('library');s.add_argument('--output',required=True);s.add_argument('--slides')
    s=sub.add_parser('template-assets',help='Extract source template media, themes and layout metadata')
    s.add_argument('input');s.add_argument('--output',required=True)
    s=sub.add_parser('template-fill',help='Apply a reviewed fill plan; retains geometry and base text style')
    s.add_argument('plan');s.add_argument('--output',required=True)
    s=sub.add_parser('patch-runs',help='Change selected text runs while retaining per-run formatting')
    s.add_argument('input');s.add_argument('plan');s.add_argument('--output',required=True)
    s=sub.add_parser('notes-init',help='Create a notes enhancement project inside a specified work directory')
    s.add_argument('input');s.add_argument('--output',required=True);s.add_argument('--name',default='notes')
    s=sub.add_parser('notes-apply',help='Apply explicitly prepared notes/audio/timing plan')
    s.add_argument('project');s.add_argument('--output',required=True)
    s=sub.add_parser('text-check',help='Read native text geometry and generate a layout report')
    s.add_argument('input');s.add_argument('--output',required=True)
    for s in sub.choices.values():
        s.add_argument('--overwrite',action='store_true',help='Update this generated output when authorized')
    return p

def main():
    args=parser().parse_args()
    if args.command in ['template-assets','notes-init']:
        out=Path(args.output).resolve()
        if out.exists() and any(out.iterdir()):
            raise FileExistsError(f'Choose an empty task output directory: {out}')
        out.mkdir(parents=True,exist_ok=True)
        temp_at(out.parent)
    else:
        out=target(args.output,args.overwrite)
        temp_at(out.parent)
    if args.command=='svg':
        project=Path(args.project).resolve()
        source=project/('svg_'+args.source if args.source in ['output','final'] else args.source)
        for svg in source.glob('*.svg'):
            if 'data-icon=' in svg.read_text(encoding='utf-8'):
                raise ValueError('Inline icon paths in SVG before export; the original external icon archive is not bundled.')
        cmd=[sys.executable,str(ROOT/'scripts/svg_to_pptx.py'),str(project),'--only','native',
             '-t','none','-a','none','-s',args.source,'-o',str(out)]
        subprocess.run(cmd,check=True)
    elif args.command in ['template-inspect','template-plan','template-fill']:
        import template_fill_pptx as fill
        if args.command=='template-inspect':
            write_json(out,fill.analyze_pptx(Path(args.input).resolve()))
        elif args.command=='template-plan':
            write_json(out,fill.scaffold_plan(load(args.library),slides=args.slides))
        else:
            plan=load(args.plan)
            source=Path(plan['source_pptx'])
            if not source.is_absolute():
                plan['source_pptx']=str((Path(args.plan).resolve().parent/source).resolve())
            if Path(plan['source_pptx']).resolve()==out:
                raise ValueError('Template source and output must differ.')
            errors,warnings=fill.validate_plan(plan,fill.analyze_pptx(plan['source_pptx']))
            if errors:
                raise ValueError('\n'.join(errors))
            for warning in warnings:
                print('Note:',warning)
            fill.apply_plan(plan,out)
    elif args.command=='template-assets':
        from template_import.manifest import build_manifest
        write_json(out/'manifest.json',build_manifest(Path(args.input).resolve(),out))
    elif args.command=='patch-runs':
        if Path(args.input).resolve()==out:
            raise ValueError('Input and output must differ.')
        patch_runs(Path(args.input).resolve(),load(args.plan),out)
    elif args.command=='notes-init':
        import native_enhance_pptx as notes
        result=notes.init_project(Path(args.input).resolve(),name=args.name,base_dir=out)
        print('Notes project:',result)
    elif args.command=='notes-apply':
        import native_enhance_pptx as notes
        errors,warnings=notes.validate(args.project)
        if errors:
            raise ValueError('\n'.join(errors))
        notes.apply(args.project,output=out,overwrite=args.overwrite)
    elif args.command=='text-check':
        subprocess.run([sys.executable,str(ROOT/'scripts/validate_pptx_text_layout.py'),
                        str(Path(args.input).resolve()),'--report',str(out)],check=True)
    print('Output:',out)

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        raise SystemExit(1)
