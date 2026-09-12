"""Page-indexed PDF extraction and rendering. Writes only new task-local outputs."""
import argparse
import json
from pathlib import Path


def page_numbers(spec, total):
    if not spec:
        return list(range(1, total + 1))
    result = []
    for part in spec.split(','):
        bounds = part.strip().split('-')
        if len(bounds) == 1:
            values = [int(bounds[0])]
        elif len(bounds) == 2:
            first, last = map(int, bounds)
            if first > last:
                raise ValueError('Page range must be ascending')
            values = range(first, last + 1)
        else:
            raise ValueError('Use pages such as 1,3-5')
        for page in values:
            if not 1 <= page <= total:
                raise ValueError(f'Page {page} outside 1..{total}')
            if page not in result:
                result.append(page)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    extract = sub.add_parser('extract')
    extract.add_argument('input', type=Path)
    extract.add_argument('--output', type=Path, required=True)
    render = sub.add_parser('render')
    render.add_argument('input', type=Path)
    render.add_argument('--output-dir', type=Path, required=True)
    render.add_argument('--pages')
    render.add_argument('--scale', type=float, default=1.5)
    args = parser.parse_args()
    if args.command == 'extract':
        from pypdf import PdfReader
        reader = PdfReader(args.input)
        pages = []
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ''
            pages.append({'page': i, 'text': text, 'characters': len(text.strip()),
                          'needs_visual_or_ocr_check': len(text.strip()) < 80})
        data = {'source': str(args.input.resolve()), 'page_count': len(pages),
                'status': 'text_extracted_not_visually_verified', 'pages': pages}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'Extracted {len(pages)} pages: {args.output.resolve()}')
    else:
        import pypdfium2 as pdfium
        if args.scale <= 0:
            raise ValueError('Scale must be positive')
        with pdfium.PdfDocument(args.input) as doc:
            selected = page_numbers(args.pages, len(doc))
            targets = [args.output_dir / f'page-{n:03}.png' for n in selected]
            for target in targets:
                if target.exists():
                    raise FileExistsError(target)
            args.output_dir.mkdir(parents=True, exist_ok=True)
            for number, target in zip(selected, targets):
                page = doc[number - 1]
                bitmap = page.render(scale=args.scale)
                try:
                    with target.open('xb') as f:
                        bitmap.to_pil().save(f, format='PNG')
                finally:
                    bitmap.close()
                    page.close()
        print(f'Rendered {len(selected)} pages; images still require visual inspection: {args.output_dir.resolve()}')


if __name__ == '__main__':
    main()
