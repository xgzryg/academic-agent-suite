"""journal-if-lookup query core.

Usage from the agent:
    from journal_if_lookup.query import lookup
    result = lookup("nat rev mol cell bio", top=5)  # bundled 2025 index
    result = lookup("nat rev mol cell bio", top=5, data_file="project/journals_index.json")

The function NEVER fabricates a journal. If the input is ambiguous, it
returns a `candidates` list and `status="ambiguous"`. If nothing matches,
returns `status="not_found"` plus a list of closest hits for the user to pick
from (sorted by similarity). If the input is unambiguous, returns
`status="ok"` plus the single best match.

"Input may be a full name, an abbreviation, a fragment of either, or an ISSN."
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

_BUNDLED_DATA_FILE = Path(__file__).resolve().parent / 'data' / 'journals_index.json'

def _load(data_file):
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        idx = json.load(f)
    if not isinstance(idx, dict) or not isinstance(idx.get('journals'), list):
        raise ValueError('Expected an index created by build_index.py (journals list missing).')
    index = idx.get('index')
    if not isinstance(index, dict) or any(
        not isinstance(index.get(key), dict)
        for key in ('name_norm', 'abbr_norm', 'issn', 'eissn', 'acronym')
    ):
        raise ValueError('Expected the lookup maps created by build_index.py.')
    if any(not isinstance(row, dict) or '_name_norm' not in row or '_abbr_norm' not in row
           for row in idx['journals']):
        raise ValueError('Journal rows are missing lookup fields; rebuild this index.')
    return idx


# ---------- text helpers ----------

_PUNCT_RE = re.compile(r'[^A-Z0-9 ]+')
_SPACE_RE = re.compile(r'\s+')
_ISSN_RE = re.compile(r'^[0-9Xx\-]+$')
_STOP = {'J', 'OF', 'THE', 'AND', 'AN', 'A', 'IN', 'ON', 'FOR', 'TO'}


def norm(s: str) -> str:
    if s is None:
        return ''
    s = str(s).upper()
    s = _PUNCT_RE.sub(' ', s)
    s = _SPACE_RE.sub(' ', s).strip()
    return s


def norm_issn(s: str) -> str:
    return re.sub(r'[^0-9X]', '', str(s or '')).upper()


def acronym_of(name_norm: str) -> str:
    parts = []
    for w in name_norm.split():
        for sub in w.split('-'):
            if sub:
                parts.append(sub)
    return ''.join(p[0] for p in parts)


def tokens(s: str) -> list[str]:
    return [t for t in s.split() if t]


def _char_overlap(a: str, b: str) -> float:
    """Jaccard similarity over character sets."""
    if not a or not b:
        return 0.0
    ca, cb = set(a), set(b)
    union = ca | cb
    return (len(ca & cb) / len(union)) if union else 0.0


def _combined_ratio(a: str, b: str) -> float:
    """Edit-distance-style ratio blended with character overlap.

    SequenceMatcher.ratio is biased toward very short strings in a 24k-key
    index (e.g. 'JMAM' vs 'JAM' scores 0.857, beating 'JMAM' vs 'JAMA' 0.75)
    because the denominator is `len(a) + len(b)`. We counter that by mixing
    in a Jaccard character overlap, weighted heavier for short strings.
    """
    if not a or not b:
        return 0.0
    sm = SequenceMatcher(None, a, b).ratio()
    co = _char_overlap(a, b)
    if min(len(a), len(b)) <= 6:
        return 0.55 * sm + 0.45 * co
    return 0.8 * sm + 0.2 * co


# ---------- score a candidate ----------

def _score(idx_data, j: dict, qn: str, qn_compact: str) -> int:
    """Higher = better. The function must NOT return 0 for a real match;
    if it can't justify a hit it returns 0 so the row is skipped."""
    score = 0
    name = j['_name_norm']
    abbr = j['_abbr_norm']
    issn = norm_issn(j.get('issn'))
    eissn = norm_issn(j.get('eissn'))

    # ISSN exact (with or without hyphens) — strongest signal
    if qn_compact.isdigit() and 7 <= len(qn_compact) <= 9:
        if issn == qn_compact or eissn == qn_compact:
            return 1000
        if issn.endswith(qn_compact) or eissn.endswith(qn_compact):
            score += 500

    # Exact normalized name
    if qn == name:
        score += 900
    elif qn and qn in name:
        score += 600

    # Exact normalized abbreviation
    if qn == abbr:
        score += 950
    elif qn and qn in abbr:
        score += 700

    # Acronym match (user typed the letters that make up the name)
    acr = acronym_of(name)
    if acr and qn_compact == re.sub(r'[^A-Z0-9]', '', acr):
        score += 850

    # Stop-word-tolerant acronym: e.g. user types 'JAMA' which == acronym_of('JAMA ...')
    # Already covered. But also: user types 'JAM' or 'JMAM' (typo) — see typo path below.

    # Token set: every query token must appear in the name (or abbreviation)
    qt = set(qn.split())
    if qt:
        nt_name = set(name.split())
        if qt.issubset(nt_name):
            score += 200
        # allow abbreviation tokens to satisfy
        nt_abbr = set(abbr.split())
        if qt.issubset(nt_abbr):
            score += 250

    # Length-aware typo tolerance: only when nothing above matched strongly.
    # SequenceMatcher.ratio() is too punitive on short acronyms like
    # 'JMAM' vs 'JAMA' (0.67). We blend in a length-normalized character
    # overlap so single-character typos on 4-6 letter acronyms still score.
    if score < 500 and qn_compact and 3 <= len(qn_compact) <= 12:
        if name and abs(len(name) - len(qn)) <= max(4, len(qn) // 2):
            ratio = _combined_ratio(qn, name)
            if ratio >= 0.65:
                score += int(ratio * 130)
        if abbr and abs(len(abbr) - len(qn)) <= max(4, len(qn) // 2):
            ratio = _combined_ratio(qn, abbr)
            if ratio >= 0.65:
                score += int(ratio * 130)
        # acronym-side typo: edit distance small — most useful for short
        # abbreviations where the user typed them slightly wrong.
        acr_clean = re.sub(r'[^A-Z0-9]', '', acr) if acr else ''
        if acr_clean and abs(len(acr_clean) - len(qn_compact)) <= 3:
            ratio = _combined_ratio(qn_compact, acr_clean)
            if ratio >= 0.6:
                score += int(ratio * 120)

    return score


# ---------- public API ----------

def lookup(query: str, top: int = 5, data_file: Optional[str] = None) -> dict:
    """Look up a journal using the bundled index unless a replacement is supplied."""
    if not query or not str(query).strip():
        return {
            'status': 'error',
            'message': 'Empty query. Please provide a journal name, abbreviation, or ISSN.',
        }

    selected_file = str(data_file) if data_file else str(_BUNDLED_DATA_FILE)
    if not os.path.isfile(selected_file):
        missing_kind = 'the selected replacement index' if data_file else 'the bundled journal index'
        return {
            'status': 'data_unavailable',
            'message': (
                f'No local journal index is available: {missing_kind} is missing. '
                'Import a spreadsheet you are entitled to use with build_index.py, then pass --data-file INDEX.json; '
                'or ask the agent to verify the journal on an accessible official website. '
                'The local lookup has not been performed; this is not a zero-match result.'
            ),
        }
    try:
        idx = _load(selected_file)
    except (OSError, ValueError) as exc:
        return {'status': 'data_error', 'message': f'Cannot read the selected journal index: {exc}'}
    return _lookup_loaded(query, top, idx)


def _lookup_loaded(query, top, idx):
    journals = idx['journals']
    index = idx['index']
    qn = norm(query)
    qn_compact = re.sub(r'[^A-Z0-9]', '', qn)

    # --- Fast path: ISSN (only digits and X, length 7-9) ---
    if qn_compact and 7 <= len(qn_compact) <= 9 and qn_compact.replace('X', '').isdigit():
        # Also try the last-8 / last-7 suffix because the source Excel sometimes
        # stores 8-digit ISSNs starting with a leading zero.
        candidates = [qn_compact]
        if len(qn_compact) == 8:
            candidates.append(qn_compact[1:])  # drop leading 0
        for cand in candidates:
            hit = index['issn'].get(cand)
            if hit is None:
                hit = index['eissn'].get(cand)
            if hit is not None:
                return {
                    'status': 'ok',
                    'matched_by': 'ISSN',
                    'journal': _clean(journals[hit]),
                }

    # --- Fast path: exact name / abbreviation ---
    if qn in index['name_norm']:
        hit = index['name_norm'][qn]
        return {'status': 'ok', 'matched_by': 'name', 'journal': _clean(journals[hit])}
    if qn in index['abbr_norm']:
        hit = index['abbr_norm'][qn]
        return {'status': 'ok', 'matched_by': 'abbreviation', 'journal': _clean(journals[hit])}

    # --- Fast path: acronym index (full string) ---
    if qn_compact in index['acronym']:
        cands = index['acronym'][qn_compact]
        if len(cands) == 1:
            return {'status': 'ok', 'matched_by': 'acronym', 'journal': _clean(journals[cands[0]])}
        # multiple journals share this acronym — return candidates
        return {
            'status': 'ambiguous',
            'matched_by': 'acronym',
            'message': f"Acronym '{query}' matches {len(cands)} journals. Pick one:",
            'candidates': [_clean(journals[i]) for i in cands[:top]],
        }

    # --- Slow path: score all rows ---
    scored = []
    for j in journals:
        s = _score(index, j, qn, qn_compact)
        if s > 0:
            scored.append((s, j))
    scored.sort(key=lambda x: (-x[0], x[1].get('rank') or 9_999_999))

    if not scored:
        # Nothing matches. Compute a similarity-based "closest misses" list.
        closest = _closest_misses(journals, qn, qn_compact, k=top)
        # Also check acronym fuzzy for short queries (e.g. 'JMAM' -> 'JAMA').
        # We use a custom scorer instead of difflib.get_close_matches because
        # SequenceMatcher.ratio is biased toward short keys in a 24k-key index
        # (e.g. 'JMAM' vs 'JAM' scores 0.857, beating 'JMAM' vs 'JAMA' 0.75).
        acr_close = []
        if 3 <= len(qn_compact) <= 6:
            acr_keys = list(index['acronym'].keys())
            qlen = len(qn_compact)
            scored_acr = []
            for ac in acr_keys:
                # Length filter — can't typo-edit 2 chars in a 4-char string
                if abs(len(ac) - qlen) > 2:
                    continue
                r = _combined_ratio(qn_compact, ac)
                if r >= 0.75:
                    scored_acr.append((r, ac))
            scored_acr.sort(key=lambda x: -x[0])
            acr_close = [ac for _, ac in scored_acr[:top]]
        if acr_close:
            seen = set(c.get('rank') for c in closest)
            extra = []
            for ac in acr_close:
                for i in index['acronym'][ac]:
                    j = journals[i]
                    if j.get('rank') not in seen:
                        seen.add(j.get('rank'))
                        extra.append(_clean(j))
            return {
                'status': 'ambiguous',
                'matched_by': 'acronym-fuzzy',
                'message': (
                    f"'{query}' didn't match any journal exactly. Closest "
                    f"abbreviation(s): {', '.join(acr_close)}. Please confirm:"
                ),
                'candidates': (closest + extra)[:top],
            }
        return {
            'status': 'not_found',
            'message': (
                f"No journal in the selected local index matches '{query}'. "
                "Here are the closest titles by string similarity — confirm the "
                "exact spelling/abbreviation, or try an ISSN."
            ),
            'closest': closest,
        }

    best_score, best_j = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0
    gap = best_score - second_score

    # Decide ambiguity
    if best_score < 200:
        # Weak match — treat as "did you mean"
        weak_closest = [_clean(j) for _, j in scored[:top]]
        # Also surface acronym-fuzzy for short queries
        if 3 <= len(qn_compact) <= 6:
            acr_keys = list(index['acronym'].keys())
            qlen = len(qn_compact)
            scored_acr = []
            for ac in acr_keys:
                if abs(len(ac) - qlen) > 2:
                    continue
                r = _combined_ratio(qn_compact, ac)
                if r >= 0.75:
                    scored_acr.append((r, ac))
            scored_acr.sort(key=lambda x: -x[0])
            acr_close = [ac for _, ac in scored_acr[:top]]
            if acr_close:
                seen = set(c.get('rank') for c in weak_closest)
                extra = []
                for ac in acr_close:
                    for i in index['acronym'][ac]:
                        j = journals[i]
                        if j.get('rank') not in seen:
                            seen.add(j.get('rank'))
                            extra.append(_clean(j))
                # Put acronym-fuzzy candidates first — they are the user's
                # intended abbreviation (e.g. JAMA for 'jmam'); the weak
                # name-similarity hits are mostly noise.
                combined = extra + weak_closest
                return {
                    'status': 'ambiguous',
                    'matched_by': 'acronym-fuzzy',
                    'message': (
                        f"'{query}' did not match any journal confidently. "
                        f"Closest abbreviation(s): {', '.join(acr_close)}. "
                        "Please confirm:"
                    ),
                    'candidates': combined[:top],
                }
        return {
            'status': 'not_found',
            'message': (
                f"'{query}' did not match any journal in the selected index confidently. "
                "Closest candidates below — confirm spelling or try the full title."
            ),
            'closest': weak_closest,
        }

    if gap < 80 and len(scored) > 1:
        # Top two are close — surface as ambiguous
        return {
            'status': 'ambiguous',
            'message': (
                f"'{query}' matches several journals with similar scores. "
                "Please confirm which one you meant:"
            ),
            'candidates': [_clean(j) for _, j in scored[:top]],
        }

    return {
        'status': 'ok',
        'matched_by': _match_kind(best_j, qn, qn_compact),
        'journal': _clean(best_j),
    }


def _match_kind(j: dict, qn: str, qn_compact: str) -> str:
    if qn == j['_name_norm']:
        return 'name'
    if qn == j['_abbr_norm']:
        return 'abbreviation'
    if qn_compact == re.sub(r'[^A-Z0-9]', '', acronym_of(j['_name_norm'])):
        return 'acronym'
    return 'fuzzy'


def _clean(j: dict) -> dict:
    """Drop internal lookup keys before returning."""
    if not j:
        return j
    out = {k: v for k, v in j.items() if not k.startswith('_')}
    return out


def _closest_misses(journals, qn: str, qn_compact: str, k: int = 5) -> list[dict]:
    """For 'not_found' responses, return a few titles with the highest
    SequenceMatcher ratio against the normalized name."""
    scored = []
    for j in journals[:5000]:  # cap for speed; covers the most-cited half
        name = j['_name_norm']
        if not name:
            continue
        r = SequenceMatcher(None, qn, name).ratio()
        if r > 0.4:
            scored.append((r, j))
    scored.sort(key=lambda x: -x[0])
    return [_clean(j) for _, j in scored[:k]]


# ---------- CLI ----------

def _format_journal(j: dict) -> str:
    """Human-readable single-record summary."""
    if not j:
        return '(no record)'
    parts = []
    parts.append(f"📘 {j.get('name') or '(no name)'}")
    parts.append('─' * 50)
    parts.append(f"Abbreviation:   {j.get('abbr') or '—'}")
    parts.append(f"Publisher:      {j.get('publisher') or '—'}")
    parts.append(f"ISSN / eISSN:   {j.get('issn') or '—'} / {j.get('eissn') or '—'}")
    parts.append(f"Edition:        {j.get('editions') or '—'}")
    parts.append(f"Categories:     {j.get('categories') or '—'}")
    parts.append('')
    parts.append('── Impact ─────────────────────────────────────────')
    parts.append(f"JIF ({j.get('jif_year') or 'year unspecified'}):     {j.get('jif') if j.get('jif') is not None else '—'}")
    parts.append(f"Data release year: {j.get('jcr_year') or '—'}")
    parts.append(f"5-year JIF:     {j.get('jif_5y') if j.get('jif_5y') is not None else '—'}")
    parts.append(f"JIF quartile:   {j.get('jif_quartile') or '—'}   percentile: {j.get('jif_percentile') or '—'}")
    parts.append(f"JIF rank:       {j.get('jif_rank') or '—'}")
    parts.append(f"JCI:            {j.get('jci') if j.get('jci') is not None else '—'}  ({j.get('jci_quartile') or '—'})")
    parts.append(f"AIS:            {j.get('article_influence_score') if j.get('article_influence_score') is not None else '—'}  ({j.get('ais_quartile') or '—'})")
    parts.append('')
    parts.append('── Volume ─────────────────────────────────────────')
    parts.append(f"Total cites:    {j.get('total_citations') or '—'}")
    parts.append(f"Articles (yr):  {j.get('total_articles') or '—'}   Citable items: {j.get('citable_items') or '—'}")
    parts.append(f"% OA Gold:      {j.get('pct_oa_gold') if j.get('pct_oa_gold') is not None else '—'}")
    parts.append(f"Immediacy idx:  {j.get('immediacy_index') if j.get('immediacy_index') is not None else '—'}")
    parts.append(f"Eigenfactor:    {j.get('eigenfactor') if j.get('eigenfactor') is not None else '—'}")
    parts.append(f"Norm Eigenf.:   {j.get('norm_eigenfactor') if j.get('norm_eigenfactor') is not None else '—'}")
    parts.append(f"Cited ½-life:   {j.get('cited_half_life') or '—'} yr   Citing ½-life: {j.get('citing_half_life') or '—'} yr")

    # Per-category breakdown
    cq = j.get('category_quartiles_json')
    if cq and cq.strip() not in ('', '[]'):
        try:
            cats = json.loads(cq)
            if cats:
                parts.append('')
                parts.append('── Per-category breakdown ──────────────────────────')
                for c in cats:
                    parts.append(
                        f"  • {c.get('category')} ({c.get('edition')}): "
                        f"JIF {c.get('quartile') or '—'} "
                        f"({c.get('jifPercentile') or '—'}%, rank {c.get('jifRank') or '—'})  "
                        f"| JCI {c.get('jciQuartile') or '—'} "
                        f"| AIS {c.get('aisQuartile') or '—'}"
                    )
        except Exception:
            pass
    return '\n'.join(parts)


def _format_result(r: dict) -> str:
    """CLI-friendly formatter."""
    status = r.get('status')
    if status in ('error', 'data_unavailable', 'data_error'):
        return f"❌ {r.get('message')}"
    if status == 'ok':
        matched = r.get('matched_by') or 'match'
        return f"✅ Match ({matched})\n\n" + _format_journal(r.get('journal') or {})
    if status == 'ambiguous':
        out = [f"🤔 {r.get('message') or 'Multiple matches — please confirm:'}"]
        for i, c in enumerate(r.get('candidates') or [], 1):
            out.append(f"\n  [{i}] {c.get('name')}  ({c.get('abbr')})  — JIF {c.get('jif')}, {c.get('jif_quartile')}/{c.get('categories')}")
        return '\n'.join(out)
    if status == 'not_found':
        out = [f"❌ {r.get('message') or 'No match.'}"]
        for i, c in enumerate(r.get('closest') or [], 1):
            out.append(f"\n  [{i}] {c.get('name')}  ({c.get('abbr')})  — JIF {c.get('jif')}, {c.get('jif_quartile')}")
        return '\n'.join(out)
    return json.dumps(r, ensure_ascii=False, indent=2)


def main(argv):
    parser = argparse.ArgumentParser(description='Look up journals in the bundled 2025 index or an explicit replacement index.')
    parser.add_argument('query', nargs='+', help='Journal title, abbreviation, or ISSN')
    parser.add_argument('--data-file', help='Explicit path to an index created by build_index.py')
    parser.add_argument('--top', type=int, default=5, help='Maximum candidate count (default: 5)')
    parser.add_argument('--json', action='store_true', help='Print the structured result as JSON')
    args = parser.parse_args(argv[1:])
    if args.top < 1:
        parser.error('--top must be at least 1')
    r = lookup(' '.join(args.query), top=args.top, data_file=args.data_file)
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else _format_result(r))
    if r.get('status') == 'data_unavailable':
        return 3
    return 0 if r.get('status') in ('ok', 'ambiguous', 'not_found') else 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
