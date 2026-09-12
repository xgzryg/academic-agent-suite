"""Audit supplied citation identities without editing prose or inventing metadata."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path


def normalize_doi(value):
    value = str(value or '').strip().lower()
    for prefix in ('https://doi.org/', 'http://doi.org/', 'doi:'):
        if value.startswith(prefix):
            value = value[len(prefix):].strip()
    return value


def audit(data):
    refs = data['references']
    citations = data['citations']
    if not isinstance(refs, list) or not isinstance(citations, list):
        raise ValueError('references and citations must be arrays')
    ids = [str(r.get('id', '')).strip() for r in refs]
    cited = [str(c).strip() for c in citations]
    duplicate_ids = [key for key, count in Counter(ids).items() if key and count > 1]
    duplicates = {}
    for field in ('doi', 'pmid'):
        groups = defaultdict(list)
        for index, ref in enumerate(refs):
            key = normalize_doi(ref.get(field)) if field == 'doi' else str(ref.get(field) or '').strip()
            if key:
                groups[key].append({'index': index + 1, 'id': ids[index]})
        duplicates[field] = {key: items for key, items in groups.items() if len(items) > 1}
    items = []
    for index, ref in enumerate(refs):
        missing = [f for f in ('id', 'title', 'authors', 'year') if not ref.get(f)]
        verification = ref.get('verification') or {}
        if not isinstance(verification, dict):
            raise ValueError('verification must be an object when supplied')
        traceable = bool(verification.get('source') and verification.get('checked_at') and verification.get('note'))
        items.append({'index': index + 1, 'id': ids[index], 'missing_fields': missing,
                      'verification_status': 'user_reported_verification' if traceable else 'unverified',
                      'verification_note': 'Supplied record only; this script did not verify online.'})
    known = set(ids) - {''}
    return {'status': 'structural_audit_only', 'missing_citation_ids': sorted(set(cited) - known),
            'duplicate_ids': duplicate_ids, 'duplicate_identities': duplicates,
            'uncited_reference_ids': sorted(known - set(cited)), 'references': items,
            'limitations': 'No automatic deletion, renumbering, metadata repair, online validation or claim-support judgment.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(json.loads(args.input.read_text(encoding='utf-8-sig')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(f'Wrote structural audit: {args.output.resolve()}')


if __name__ == '__main__':
    main()
