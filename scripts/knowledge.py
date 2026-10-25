#!/usr/bin/env python3
"""Local UTF-8 source import and registry checks. No model or network calls."""
import argparse
from contextlib import contextmanager
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def source_dates(event_date=None, captured_at=None):
    """Validate declared dates without inventing them from file timestamps."""
    if event_date is not None:
        if not isinstance(event_date, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', event_date):
            raise ValueError('Event date must be YYYY-MM-DD')
        date.fromisoformat(event_date)
    if captured_at is not None:
        if not isinstance(captured_at, str):
            raise ValueError('Capture time must be an ISO timestamp with timezone')
        value = datetime.fromisoformat(captured_at.replace('Z', '+00:00'))
        if value.tzinfo is None:
            raise ValueError('Capture time must include a timezone')
    return {'event_date': event_date, 'captured_at': captured_at}


def inside(root, value, area=None):
    relative = Path(value)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Expected an in-workspace relative path')
    target = root / relative
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f'Symlink not supported: {value}')
    boundary = root / area if area else root
    if not target.resolve().is_relative_to(boundary.resolve()):
        raise ValueError(f'Path outside permitted area: {value}')
    return target


@contextmanager
def writing(root):
    state = inside(root, '.state')
    state.mkdir(exist_ok=True)
    lock = inside(root, '.state/write.lock')
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError('Write lock exists; wait or verify a terminated writer before recovery')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(json.dumps({'pid': os.getpid(), 'created_at': stamp()}))
        yield
    finally:
        lock.unlink()


def registry(root):
    file = inside(root, '.state/sources.json')
    if not file.exists():
        return {'schema': 1, 'sources': []}
    data = json.loads(file.read_text(encoding='utf-8'))
    if data.get('schema') != 1 or not isinstance(data.get('sources'), list):
        raise ValueError('Unsupported registry schema')
    ids, paths = set(), set()
    for entry in data['sources']:
        if not isinstance(entry, dict):
            raise ValueError('Malformed source entry')
        digest = entry.get('sha256', '')
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('Malformed source hash')
        if entry.get('id') != digest or digest in ids:
            raise ValueError('Invalid or duplicate source identity')
        if not isinstance(entry.get('path'), str) or entry['path'] in paths:
            raise ValueError('Invalid or duplicate source path')
        inside(root, entry['path'], 'raw')
        pages = entry.get('pages')
        if not isinstance(pages, list) or not pages or not all(isinstance(p, str) for p in pages):
            raise ValueError('Invalid page references')
        for page in pages:
            inside(root, page, 'wiki')
        if not isinstance(entry.get('ingested_at'), str):
            raise ValueError('Missing ingestion date')
        source_dates(entry.get('event_date'), entry.get('captured_at'))
        ids.add(digest)
        paths.add(entry['path'])
    for entry in data['sources']:
        if entry.get('revises') and (entry['revises'] not in ids or entry['revises'] == entry['id']):
            raise ValueError('Invalid revision reference')
    return data


def save(root, data, filename='.state/sources.json'):
    destination = inside(root, filename, '.state')
    fd, temporary = tempfile.mkstemp(prefix='registry-', suffix='.tmp', dir=destination.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, destination)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()


def raw_files(root):
    folder = inside(root, 'raw')
    if not folder.exists():
        return
    for file in sorted(folder.rglob('*')):
        if file.name == 'README.md' and file.parent == folder:
            continue
        inside(root, file.relative_to(root), 'raw')
        if file.is_file():
            yield file


def inspect(root):
    data = registry(root)
    issues, pending, duplicates = [], [], []
    entries = data['sources']
    registered = {e['path']: e for e in entries}
    hashes = {e['sha256']: e['path'] for e in entries}
    for entry in entries:
        file = inside(root, entry['path'], 'raw')
        if not file.is_file():
            issues.append('Missing original: ' + entry['path'])
        elif sha(file.read_bytes()) != entry['sha256']:
            issues.append('Changed original: ' + entry['path'])
        for page in entry['pages']:
            target = inside(root, page, 'wiki')
            if not target.is_file() or not target.read_text(encoding='utf-8').strip():
                issues.append('Missing or empty derived page: ' + page)
    for file in raw_files(root):
        rel = file.relative_to(root).as_posix()
        if rel in registered:
            continue
        digest = sha(file.read_bytes())
        if digest in hashes:
            duplicates.append({'path': rel, 'same_as': hashes[digest]})
        else:
            reason = None
            try:
                content = file.read_bytes()
                content.decode('utf-8')
                if not content.strip():
                    reason = 'empty source'
            except UnicodeDecodeError:
                reason = 'not UTF-8 text'
            if file.suffix.lower() not in ('.md', '.txt'):
                reason = 'requires a supported reader/export'
            pending.append({'path': rel, 'sha256': digest,
                            'supported': reason is None, 'reason': reason})
            hashes[digest] = rel
    return {'registered': len(entries), 'pending': pending, 'duplicates': duplicates, 'issues': issues}


def import_file(root, source):
    source = Path(source)
    if source.suffix.lower() not in ('.md', '.txt') or not source.is_file():
        raise ValueError('Import requires a selected Markdown or plain-text file')
    content = source.read_bytes()
    content.decode('utf-8')
    if not content.strip():
        raise ValueError('Empty sources are not useful imports')
    digest = sha(content)
    with writing(root):
        if inspect(root)['issues']:
            raise ValueError('Resolve existing source integrity issues before importing')
        for file in raw_files(root):
            if sha(file.read_bytes()) == digest:
                return {'path': file.relative_to(root).as_posix(), 'sha256': digest, 'duplicate': True}
        safe_name = re.sub(r'[^a-zA-Z0-9_-]+', '-', source.stem).strip('-')[:60] or 'source'
        relative = f'raw/{digest[:16]}-{safe_name}{source.suffix.lower()}'
        output = inside(root, relative, 'raw')
        output.parent.mkdir(exist_ok=True)
        with output.open('xb') as f:
            f.write(content)
        return {'path': relative, 'sha256': digest, 'duplicate': False}


def register(root, source, observed_hash, pages, revises=None, event_date=None, captured_at=None):
    dates = source_dates(event_date, captured_at)
    with writing(root):
        data = registry(root)
        file = inside(root, source, 'raw')
        if file.suffix.lower() not in ('.md', '.txt') or file.name == 'README.md':
            raise ValueError('Only source Markdown/text files can be registered')
        content = file.read_bytes()
        content.decode('utf-8')
        actual = sha(content)
        if actual != observed_hash:
            raise ValueError('Source changed since it was read; preserve and investigate')
        if not content.strip():
            raise ValueError('Empty source')
        if inspect(root)['issues']:
            raise ValueError('Existing registry integrity failure; do not replace earlier evidence')
        rel = file.relative_to(root).as_posix()
        for entry in data['sources']:
            if entry['sha256'] == actual:
                return {'id': entry['id'], 'already_registered': True, 'path': entry['path']}
            if entry['path'] == rel:
                raise ValueError('Cannot overwrite an earlier source registration')
        if revises and revises not in {e['id'] for e in data['sources']}:
            raise ValueError('Unknown earlier source for revision')
        clean_pages = []
        for page in dict.fromkeys(pages):
            target = inside(root, page, 'wiki')
            if target.suffix != '.md' or not target.is_file() or not target.read_text(encoding='utf-8').strip():
                raise ValueError('Derived page must be an existing nonempty Markdown file')
            clean_pages.append(target.relative_to(root).as_posix())
        if not clean_pages:
            raise ValueError('At least one completed derived page is required')
        entry = {'id': actual, 'path': rel, 'sha256': actual, 'pages': clean_pages,
                 'ingested_at': stamp(), 'revises': revises, **dates}
        data['sources'].append(entry)
        save(root, data)
        return entry


def activity(root):
    file = inside(root, '.state/ingestion-health.json')
    if not file.exists():
        return {'schema': 1, 'operations': {}}
    data = json.loads(file.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('schema') != 1 or not isinstance(data.get('operations'), dict):
        raise ValueError('Invalid ingestion health log')
    for operation, record in data['operations'].items():
        if operation not in ('import-file', 'register') or not isinstance(record, dict):
            raise ValueError('Invalid ingestion operation')
        attempt = record.get('last_attempt', {})
        if not isinstance(attempt, dict) or type(attempt.get('ok')) is not bool:
            raise ValueError('Invalid ingestion attempt')
        for value in (attempt.get('at'), record.get('last_success_at'), record.get('last_failure_at')):
            if value is not None:
                source_dates(captured_at=value)
        if attempt.get('at') is None:
            raise ValueError('Missing attempt timestamp')
    return data


def record_attempt(root, operation, ok):
    """CLI observations only; no source text, secrets, or command arguments."""
    with writing(root):
        data = activity(root)
        record = data['operations'].setdefault(operation, {})
        at = stamp()
        record['last_attempt'] = {'at': at, 'ok': ok}
        record['last_success_at' if ok else 'last_failure_at'] = at
        save(root, data, '.state/ingestion-health.json')


def health(root, review_before=None):
    if review_before is not None:
        source_dates(event_date=review_before)
    result = inspect(root)
    data = registry(root)
    result['operations'] = activity(root)['operations']
    result['latest_registered_at'] = max((e['ingested_at'] for e in data['sources']), default=None)
    revised = {e['revises'] for e in data['sources'] if e.get('revises')}
    result['sources'] = [
        {'path': e['path'], 'event_date': e.get('event_date'),
         'captured_at': e.get('captured_at'), 'ingested_at': e['ingested_at'],
         'has_later_revision': e['id'] in revised,
         'review_candidate': bool(review_before and e.get('event_date') and
                                  e['event_date'] < review_before)}
        for e in data['sources']]
    failed = any(not record['last_attempt']['ok'] for record in result['operations'].values())
    result['state'] = ('needs-attention' if result['issues'] or failed else
                       'pending' if result['pending'] else
                       'review-needed' if any(e['review_candidate'] for e in result['sources']) else
                       'no-local-issues' if data['sources'] or result['operations'] else 'not-started')
    result['freshness_unknown'] = sum(e.get('event_date') is None for e in data['sources'])
    result['review_before'] = review_before
    result['scope'] = ('Local files and observed CLI attempts only. Dates are declared source metadata; '
                       'age flags are review candidates, not invalid facts. No connector, sync, '
                       'schedule, or claim freshness has been verified.')
    return result


def check(root):
    root = root.resolve()
    result = inspect(root)
    files = [root / 'AGENTS.md', root / 'connections.md']
    for folder in ('wiki', 'context', 'work'):
        base = inside(root, folder)
        files.extend(base.rglob('*.md'))
    for file in files:
        inside(root, file.relative_to(root))
        if not file.is_file():
            result['issues'].append('Missing entry point: ' + file.relative_to(root).as_posix())
            continue
        text = re.sub(r'```.*?```', '', file.read_text(encoding='utf-8'), flags=re.S)
        for match in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = match.strip().strip('<>')
            url = urlsplit(target)
            if url.scheme or target.startswith(('#', '//')):
                continue
            resolved = (file.parent / unquote(url.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                result['issues'].append(f'Broken or external local link: {file.relative_to(root)} → {target}')
    bridge = inside(root, 'CLAUDE.md')
    if not bridge.is_file() or bridge.read_bytes() != b'@AGENTS.md\n':
        result['issues'].append('CLAUDE.md must import AGENTS.md')
    result['scope'] = 'Source hashes, page existence, local link paths, manual import; not meaning, anchors, remote access, or run success'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('status')
    commands.add_parser('check')
    health_cmd = commands.add_parser('health')
    health_cmd.add_argument('--review-before', help='Optional event-date cutoff (YYYY-MM-DD); no default expiry')
    imp = commands.add_parser('import-file')
    imp.add_argument('source')
    reg = commands.add_parser('register')
    reg.add_argument('source')
    reg.add_argument('--sha256', required=True)
    reg.add_argument('--pages', nargs='+', required=True)
    reg.add_argument('--revises')
    reg.add_argument('--event-date')
    reg.add_argument('--captured-at')
    args = parser.parse_args()
    root = args.root.resolve()
    mutation = args.command in ('import-file', 'register')

    def observe(ok, result):
        if mutation:
            try:
                record_attempt(root, args.command, ok)
            except (OSError, ValueError, TypeError, KeyError) as error:
                result['health_log_warning'] = 'Attempt could not be recorded: ' + str(error)
        return result

    try:
        if args.command == 'import-file':
            result = import_file(root, args.source)
        elif args.command == 'register':
            result = register(root, args.source, args.sha256, args.pages, args.revises,
                              args.event_date, args.captured_at)
        elif args.command == 'health':
            result = health(root, args.review_before)
        else:
            result = check(root) if args.command == 'check' else inspect(root)
        print(json.dumps(observe(True, result), ensure_ascii=False, indent=2))
        return 1 if result.get('issues') or result.get('state') == 'needs-attention' else 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps(observe(False, {'error': str(error)}), ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
