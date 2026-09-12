"""Install this entire skill folder into an explicitly supplied skills directory."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True, help='Existing or new parent skills directory')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    target = (args.destination / 'paper-writing-agent').resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Destination must be separate from this source folder')
    if target.exists():
        raise FileExistsError(f'Existing installation is preserved: {target}')
    if not (source / 'SKILL.md').is_file():
        raise FileNotFoundError('Source SKILL.md missing')
    print(f'Source: {source}\nDestination: {target}')
    if args.dry_run:
        print('Dry run only; no files changed.')
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    print('Installed one independent folder. No global configuration, services, dependencies or other skills were changed.')


if __name__ == '__main__':
    main()
