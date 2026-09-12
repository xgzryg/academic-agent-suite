"""Record real manuscript review/revision stages; this does not spawn agents or judge science."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

DEFAULT_GOAL = '实质问题已修正或有证据回应，剩余限制准确披露，当前稿经再审且无新增事实或一致性错误。'
TERMINAL = {'goal_met', 'max_rounds_reached', 'needs_input', 'blocked', 'user_stopped'}


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def resolved(path, base):
    value = Path(path)
    return (base / value).resolve() if not value.is_absolute() else value.resolve()


def require_file(path):
    if not path.is_file():
        raise ValueError(f'File does not exist: {path}')
    return path


def require_bool(value, label):
    if type(value) is not bool:
        raise ValueError(f'{label} must be true or false')
    return value


def identifier(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must contain the actual execution identifier')
    return value


def save(root, state, event):
    state['updated_at'] = now()
    state['history'].append({'at': state['updated_at'], **event})
    # Only the coordinator writes this task-owned state, after reading actual artifacts.
    (root / 'state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return state


def initialize(config_path, root):
    config_path = Path(config_path).resolve()
    cfg = read_json(config_path)
    rounds = cfg.get('max_rounds', 3)
    if type(rounds) is not int or rounds < 0:
        raise ValueError('max_rounds must be a nonnegative integer')
    for key, default in [('novelty', False), ('network_allowed', True), ('human_checkpoint', False)]:
        cfg[key] = require_bool(cfg.get(key, default), key)
    goal = cfg.get('goal', DEFAULT_GOAL)
    if not isinstance(goal, str) or not goal.strip():
        raise ValueError('goal must describe an observable target')
    source = require_file(resolved(cfg['manuscript'], config_path.parent))
    visible = [require_file(resolved(p, config_path.parent)) for p in cfg.get('visible_files', [])]
    if root.exists() and any(root.iterdir()):
        raise ValueError('Run directory must be new or empty; resume the existing state instead')
    root.mkdir(parents=True, exist_ok=True)
    initial = root / 'versions' / ('v000' + source.suffix)
    initial.parent.mkdir()
    shutil.copy2(source, initial)
    cfg.update(max_rounds=rounds, goal=goal)
    cfg['manuscript'] = str(source)
    cfg['visible_files'] = [str(p) for p in visible]
    (root / 'config.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state = {
        'status': 'awaiting_review', 'version': 'v000', 'current_manuscript': str(initial.relative_to(root)),
        'visible_files': [str(p) for p in visible], 'revision_count': 0, 'completed_rounds': 0,
        'review_count': 0, 'last_review': None, 'pending_revision': None, 'issues': [],
        'config': cfg, 'history': [], 'created_at': now(),
    }
    return save(root, state, {'event': 'initialized', 'version': 'v000'})


def record_review(root, report_path):
    state = read_json(root / 'state.json')
    if state['status'] != 'awaiting_review':
        raise ValueError(f"Cannot record review while {state['status']}")
    report_path = require_file(Path(report_path).resolve())
    report = read_json(report_path)
    if report['version'] != state['version']:
        raise ValueError('Review version differs from current manuscript version')
    reviewed = require_file(resolved(report['manuscript'], root))
    if reviewed != resolved(state['current_manuscript'], root):
        raise ValueError('Review must identify the actual current manuscript')
    agent = identifier(report.get('agent_id'), 'agent_id')
    previous_writers = [h.get('agent_id') for h in state['history'] if h['event'] == 'revision_recorded']
    if agent in previous_writers:
        raise ValueError('A reviser cannot act as this loop reviewer')
    met = require_bool(report.get('goal_met'), 'goal_met')
    can_revise = require_bool(report.get('can_revise'), 'can_revise')
    if not isinstance(report.get('reason'), str) or not report['reason'].strip():
        raise ValueError('Review requires an evidence-based reason')
    issues = report.get('issues')
    if not isinstance(issues, list):
        raise ValueError('issues must be a list')
    ids = set()
    for issue in issues:
        issue_id = identifier(issue.get('id'), 'issue id')
        if issue_id in ids:
            raise ValueError('Duplicate issue ID')
        ids.add(issue_id)
        if issue.get('status') not in {'open', 'partial', 'resolved', 'not_applicable', 'accepted_rebuttal'}:
            raise ValueError(f'Invalid issue status: {issue_id}')
        if issue.get('severity') not in {'critical', 'major', 'minor', 'suggestion'}:
            raise ValueError(f'Invalid issue severity: {issue_id}')
        if not issue.get('evidence'):
            raise ValueError(f'Issue requires evidence: {issue_id}')
    missing = {i['id'] for i in state['issues'] if i['status'] in {'open', 'partial'}} - ids
    if missing:
        raise ValueError(f'Re-review omitted prior unresolved issues: {sorted(missing)}')
    blocking = [i['id'] for i in issues if i['status'] in {'open', 'partial'} and i['severity'] in {'critical', 'major'} and i.get('in_scope', True)]
    if met and blocking:
        raise ValueError(f'Goal cannot pass with open material issues: {blocking}')
    novelty = report.get('novelty_status', 'not_requested')
    if novelty not in {'complete', 'partial', 'offline', 'failed', 'not_requested'}:
        raise ValueError('Unknown novelty_status')
    if state['config']['novelty'] and met and novelty != 'complete':
        raise ValueError('Requested novelty evidence remains incomplete')
    state['review_count'] += 1
    state['completed_rounds'] = state['revision_count']
    state['last_review'] = {'path': str(report_path), 'agent_id': agent, 'version': state['version'], 'reason': report['reason'], 'novelty_status': novelty}
    state['issues'] = issues
    state['pending_revision'] = None
    if met:
        state['status'] = 'goal_met'
    elif state['revision_count'] >= state['config']['max_rounds']:
        state['status'] = 'max_rounds_reached'
    elif not can_revise:
        state['status'] = 'needs_input'
    else:
        state['status'] = 'awaiting_revision'
    return save(root, state, {'event': 'review_recorded', 'agent_id': agent, 'version': state['version'], 'report': str(report_path), 'status': state['status']})


def record_revision(root, report_path, approved=False):
    state = read_json(root / 'state.json')
    if state['status'] != 'awaiting_revision':
        raise ValueError(f"Cannot record revision while {state['status']}")
    if state['config']['human_checkpoint'] and not approved:
        raise ValueError('Human checkpoint requires actual user approval before revision')
    report_path = require_file(Path(report_path).resolve())
    report = read_json(report_path)
    if report['from_version'] != state['version']:
        raise ValueError('Revision must start from the current reviewed version')
    agent = identifier(report.get('agent_id'), 'agent_id')
    reviewers = [h.get('agent_id') for h in state['history'] if h['event'] == 'review_recorded']
    if agent in reviewers:
        raise ValueError('Reviewer and reviser must be distinct actual agents')
    current = require_file(resolved(state['current_manuscript'], root))
    updated = require_file(resolved(report['manuscript'], root))
    if updated == current or not updated.is_relative_to(root / 'versions'):
        raise ValueError('Write a new manuscript file within this run versions directory')
    responses = require_file(resolved(report['responses'], root))
    if not report.get('summary'):
        raise ValueError('Revision needs an actual change summary')
    if current.read_bytes() == updated.read_bytes() and not report.get('updated_visible_files'):
        raise ValueError('No manuscript changes; resolve the issue or stop instead of counting an empty revision')
    updated_visible = report.get('updated_visible_files')
    if updated_visible is not None:
        if not isinstance(updated_visible, list):
            raise ValueError('updated_visible_files must be the complete current attachment list')
        state['visible_files'] = [str(require_file(resolved(p, root))) for p in updated_visible]
    state['revision_count'] += 1
    state['version'] = f"v{state['revision_count']:03d}"
    state['current_manuscript'] = str(updated.relative_to(root))
    state['status'] = 'awaiting_review'
    state['pending_revision'] = {'path': str(report_path), 'responses': str(responses), 'agent_id': agent, 'version': state['version']}
    return save(root, state, {'event': 'revision_recorded', 'agent_id': agent, 'version': state['version'], 'report': str(report_path), 'summary': report['summary']})


def stop(root, reason, status):
    state = read_json(root / 'state.json')
    if status not in {'blocked', 'needs_input', 'user_stopped'}:
        raise ValueError('Only a review can set quality success or max-round status')
    if not reason.strip():
        raise ValueError('A concrete reason is required')
    state['status'] = status
    state['stop_reason'] = reason
    return save(root, state, {'event': 'stopped', 'reason': reason, 'status': status})


def resume(root, reason):
    state = read_json(root / 'state.json')
    if state['status'] not in {'blocked', 'needs_input', 'user_stopped'}:
        raise ValueError('This state does not require resume; do not reset completed rounds')
    if not reason.strip():
        raise ValueError('State the new information or authorization allowing continuation')
    last = state['last_review']
    if last is None or last['version'] != state['version']:
        state['status'] = 'awaiting_review'
    elif state['revision_count'] >= state['config']['max_rounds']:
        state['status'] = 'max_rounds_reached'
    else:
        state['status'] = 'awaiting_revision'
    state.pop('stop_reason', None)
    return save(root, state, {'event': 'resumed', 'reason': reason, 'status': state['status']})


def extend(root, maximum, reason):
    state = read_json(root / 'state.json')
    if state['status'] != 'max_rounds_reached':
        raise ValueError('Extend only after the reviewed round limit was reached')
    if maximum <= state['config']['max_rounds'] or not reason.strip():
        raise ValueError('Supply a larger user-authorized total and the authorization reason')
    previous = state['config']['max_rounds']
    state['config']['max_rounds'] = maximum
    state['status'] = 'awaiting_revision'
    (root / 'config.json').write_text(json.dumps(state['config'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return save(root, state, {'event': 'limit_extended', 'old_max_rounds': previous, 'max_rounds': maximum, 'reason': reason})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', required=True, type=Path)
    subs = parser.add_subparsers(dest='command', required=True)
    subs.add_parser('init').add_argument('--config', required=True, type=Path)
    subs.add_parser('review').add_argument('--report', required=True, type=Path)
    revision = subs.add_parser('revision')
    revision.add_argument('--report', required=True, type=Path)
    revision.add_argument('--approved', action='store_true', help='Use only after actual requested user approval')
    stopping = subs.add_parser('stop')
    stopping.add_argument('--status', choices=['blocked', 'needs_input', 'user_stopped'], required=True)
    stopping.add_argument('--reason', required=True)
    subs.add_parser('resume').add_argument('--reason', required=True)
    extension = subs.add_parser('extend')
    extension.add_argument('--max-rounds', required=True, type=int)
    extension.add_argument('--reason', required=True)
    subs.add_parser('status')
    args = parser.parse_args()
    root = args.run_dir.resolve()
    try:
        if args.command == 'init': result = initialize(args.config, root)
        elif args.command == 'review': result = record_review(root, args.report)
        elif args.command == 'revision': result = record_revision(root, args.report, args.approved)
        elif args.command == 'stop': result = stop(root, args.reason, args.status)
        elif args.command == 'resume': result = resume(root, args.reason)
        elif args.command == 'extend': result = extend(root, args.max_rounds, args.reason)
        else: result = read_json(root / 'state.json')
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
