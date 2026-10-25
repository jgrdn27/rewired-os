#!/usr/bin/env python3
"""Build, install, preview, update and restore Rewired folders. Python 3.10+, stdlib."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import uuid
import zipfile

RECEIPT = '.rewired/installed.json'
PENDING = '.rewired/pending.json'
LOCK = '.rewired/update.lock'
PREFIX = 'Rewired-OS/'
MAX_FILE = 20 * 1024 * 1024
MAX_TOTAL = 50 * 1024 * 1024
SEED_FILES = {'preferences.json', 'connections.md', 'decisions.md'}
SEED_DIRS = {'context', 'wiki', 'raw', 'work'}


class DistributionError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode('utf-8')


def path_name(name):
    if not isinstance(name, str) or not name or len(name) > 240:
        raise DistributionError('Invalid package path')
    parts = name.split('/')
    if any(p in ('', '.', '..') or p.endswith((' ', '.')) or
           re.search(r'[\\:*?"<>|\x00-\x1f]', p) or
           re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?', p)
           for p in parts):
        raise DistributionError('Unsafe or nonportable path: ' + name)
    return name


def stock_path(name):
    path_name(name)
    parts = name.split('/')
    if (parts[0].lower() in SEED_DIRS and parts[0] != parts[0].lower()) or (name.lower() in SEED_FILES and name != name.lower()):
        raise DistributionError('Use canonical spelling for user-owned paths: ' + name)
    if any(p.lower() in {'.git', '.rewired', '.state', '__pycache__', 'dist', 'reviews'}
           or p.lower().startswith('.env') for p in parts) or name.lower().startswith('library/custom/'):
        raise DistributionError('Private/runtime path cannot ship: ' + name)
    return name


def policy(name):
    return 'seed' if name in SEED_FILES or name.split('/')[0] in SEED_DIRS else 'managed'


def version_key(version):
    if not isinstance(version, str):
        raise DistributionError('Invalid version')
    match = re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?', version)
    if not match:
        raise DistributionError('Use a semantic version without build metadata')
    suffix = match[4]
    identifiers = suffix.split('.') if suffix else []
    if any(not s or (s.isdigit() and len(s) > 1 and s[0] == '0') for s in identifiers):
        raise DistributionError('Invalid prerelease version')
    return (int(match[1]), int(match[2]), int(match[3]), suffix is None,
            tuple((0, int(s)) if s.isdigit() else (1, s) for s in identifiers))


def validate_receipt(value):
    if not isinstance(value, dict) or value.get('schema') != 1 or value.get('product') != 'rewired-os':
        raise DistributionError('Unrecognized Rewired receipt')
    version_key(value.get('version'))
    files = value.get('files')
    if not isinstance(files, dict) or not files or len(files) > 2000:
        raise DistributionError('Invalid release inventory')
    folded = set()
    for name, entry in files.items():
        stock_path(name)
        if name.casefold() in folded:
            raise DistributionError('Case-colliding paths')
        folded.add(name.casefold())
        if (not isinstance(entry, dict) or entry.get('policy') != policy(name) or
                not re.fullmatch(r'[0-9a-f]{64}', str(entry.get('sha256', '')))):
            raise DistributionError('Invalid ownership/hash: ' + name)
    for name in files:
        if any(str(parent).casefold() in folded for parent in PurePosixPath(name).parents if str(parent) != '.'):
            raise DistributionError('File/directory path collision')
    return value


def root_path(value):
    root = Path(os.path.abspath(value))
    for part in (root, *root.parents):
        if part.is_symlink():
            raise DistributionError('Use a real folder path, not a symlink: ' + str(part))
    return root


def safe(root, name):
    path_name(name)
    target = root / name
    for part in (target, *target.parents):
        if part == root:
            break
        if part.is_symlink():
            raise DistributionError('Symlink blocked: ' + name)
        if part != target and part.exists() and not part.is_dir():
            raise DistributionError('Parent is not a folder: ' + name)
    if target.exists() and not target.is_file():
        raise DistributionError('Expected a file: ' + name)
    return target


def read(root, name):
    p = safe(root, name)
    if not p.exists():
        return None
    if p.stat().st_size > MAX_FILE:
        raise DistributionError('File exceeds size limit: ' + name)
    return p.read_bytes()


def hash_at(root, name):
    data = read(root, name)
    return digest(data) if data is not None else None


def atomic(root, name, data):
    target = safe(root, name)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.rewired-', dir=target.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        safe(root, name)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def remove(root, name):
    safe(root, name).unlink(missing_ok=True)


def load_json(data):
    try:
        return json.loads(data)
    except (ValueError, TypeError, UnicodeError) as exc:
        raise DistributionError('Unreadable JSON metadata') from exc


def receipt(root):
    data = read(root, RECEIPT)
    if data is None:
        raise DistributionError('No installation receipt. Do not adopt an existing workspace by guessing its baseline; use a fresh packaged install.')
    return validate_receipt(load_json(data)), data


def build(source, output):
    source, output = root_path(source), Path(output).absolute()
    if output.is_relative_to(source):
        raise DistributionError('Build outside the starter folder')
    if (source / '.rewired').exists() or (source / '.state').exists():
        raise DistributionError('Build only from the stock development template, never an installed OS')
    manifest = load_json(read(source, 'release-manifest.json'))
    names = manifest.get('files', [])
    if not names or len(names) != len(set(names)):
        raise DistributionError('Invalid stock allowlist')
    actual = {p.relative_to(source).as_posix() for p in source.rglob('*')
              if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts}
    if actual != set(names):
        raise DistributionError('Stock folder differs from the release allowlist')
    contents = {}
    for name in names:
        stock_path(name)
        data = read(source, name)
        if data is None:
            raise DistributionError('Missing stock file: ' + name)
        contents[name] = data
    if sum(map(len, contents.values())) > MAX_TOTAL:
        raise DistributionError('Package exceeds size limit')
    meta = validate_receipt({'schema': 1, 'product': 'rewired-os', 'version': manifest['version'],
                            'files': {n: {'sha256': digest(b), 'policy': policy(n)} for n, b in contents.items()}})
    contents[RECEIPT] = encoded(meta)
    if output.exists() or Path(str(output) + '.sha256').exists():
        raise DistributionError('Output or checksum already exists; choose a new build path')
    output.parent.mkdir(parents=True, exist_ok=True)
    # Deterministic bytes and no overwrite of an existing release asset.
    try:
        with output.open('xb') as stream:
            with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
                for name, data in sorted(contents.items()):
                    info = zipfile.ZipInfo(PREFIX + name, (2026, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = (stat.S_IFREG | 0o644) << 16
                    archive.writestr(info, data)
    except FileExistsError as exc:
        raise DistributionError('Output already exists; choose a new build path') from exc
    sha = digest(output.read_bytes())
    with Path(str(output) + '.sha256').open('x', encoding='utf-8') as stream:
        stream.write(sha + '  ' + output.name + '\n')
    return {'version': meta['version'], 'zip': str(output), 'sha256': sha, 'stock_files': len(names)}


def package(path, expected=None):
    archive_path = Path(path)
    if archive_path.stat().st_size > MAX_TOTAL:
        raise DistributionError('Archive exceeds size limit')
    sha = digest(archive_path.read_bytes())
    if expected is not None and sha != expected.lower():
        raise DistributionError('Archive SHA-256 does not match')
    contents = {}
    with zipfile.ZipFile(archive_path) as archive:
        entries = archive.infolist()
        if len(entries) > 2001 or sum(i.file_size for i in entries) > MAX_TOTAL:
            raise DistributionError('Archive exceeds inventory/expanded-size limit')
        for info in entries:
            if not info.filename.startswith(PREFIX):
                raise DistributionError('Unexpected archive root')
            name = path_name(info.filename[len(PREFIX):])
            mode = info.external_attr >> 16
            if (name in contents or info.is_dir() or info.file_size > MAX_FILE or
                    stat.S_IFMT(mode) not in (0, stat.S_IFREG)):
                raise DistributionError('Duplicate, oversized or nonregular archive entry')
            contents[name] = archive.read(info)
    meta_bytes = contents.pop(RECEIPT, None)
    meta = validate_receipt(load_json(meta_bytes))
    if set(contents) != set(meta['files']):
        raise DistributionError('Archive inventory does not match receipt')
    for name, data in contents.items():
        if digest(data) != meta['files'][name]['sha256']:
            raise DistributionError('Package hash mismatch: ' + name)
    manifest = load_json(contents.get('release-manifest.json'))
    if manifest.get('version') != meta['version'] or sorted(manifest.get('files', [])) != sorted(contents):
        raise DistributionError('Release manifest differs from receipt')
    return meta, contents, sha


def install(archive, destination, expected=None):
    meta, contents, sha = package(archive, expected)
    destination = root_path(destination)
    if destination.exists():
        raise DistributionError('Destination already exists; choose a new folder. No merge install.')
    if not destination.parent.is_dir():
        raise DistributionError('Destination parent must exist')
    with tempfile.TemporaryDirectory(prefix='.rewired-install-', dir=destination.parent) as temporary:
        stage = Path(temporary) / 'folder'
        stage.mkdir()
        for name, data in contents.items():
            atomic(stage, name, data)
        atomic(stage, RECEIPT, encoded(meta))
        if destination.exists():
            raise DistributionError('Destination appeared during installation')
        stage.rename(destination)
    return {'installed': meta['version'], 'folder': str(destination), 'sha256': sha,
            'next': 'Read START-HERE.md with your assistant'}


def check_pending(root):
    if read(root, PENDING) is not None:
        raise DistributionError('Interrupted transaction exists. Run restore before another update.')


def plan(root, incoming):
    check_pending(root)
    old, _ = receipt(root)
    if version_key(incoming['version']) <= version_key(old['version']):
        raise DistributionError('Updates must be newer than the installed release; use restore for rollback')
    changes, conflicts, preserved = [], [], []
    for name in sorted(set(old['files']) | set(incoming['files'])):
        before, after = old['files'].get(name), incoming['files'].get(name)
        if policy(name) == 'seed':
            preserved.append(name)
            continue
        previous = before['sha256'] if before else None
        desired = after['sha256'] if after else None
        if previous == desired:
            continue  # User edits/deletions survive when upstream has no change.
        current = hash_at(root, name)
        if current == desired:
            continue
        if current != previous:
            conflicts.append(name)
        else:
            changes.append({'path': name, 'before': current, 'after': desired})
    return {'from': old['version'], 'to': incoming['version'], 'changes': changes,
            'conflicts': conflicts, 'preserved_user_files': preserved,
            'can_apply': not conflicts}


@contextmanager
def locked(root, recover=False):
    lock = safe(root, LOCK)
    lock.parent.mkdir(parents=True, exist_ok=True)
    if recover and lock.exists():
        # Only explicit recovery may clear a stale lock. Caller must stop other writers.
        lock.unlink()
    try:
        with lock.open('x', encoding='utf-8') as stream:
            stream.write(str(os.getpid()) + '\n')
    except FileExistsError as exc:
        raise DistributionError('Update lock exists. Stop other writers; use restore with --recover-lock only after an interrupted process has ended.') from exc
    try:
        if (root / '.state/write.lock').exists():
            raise DistributionError('Knowledge writer is active; finish it before updating')
        yield
    finally:
        lock.unlink(missing_ok=True)


def apply(root, incoming, contents, sha):
    with locked(root):
        result = plan(root, incoming)
        if result['conflicts']:
            raise DistributionError('Update blocked by local edits: ' + ', '.join(result['conflicts']))
        _, old_bytes = receipt(root)
        ident = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:12]
        base = '.rewired/backups/' + ident
        for change in result['changes']:
            if hash_at(root, change['path']) != change['before']:
                raise DistributionError('File changed during planning: ' + change['path'])
            if change['before'] is not None:
                saved = read(root, change['path'])
                if saved is None or digest(saved) != change['before']:
                    raise DistributionError('File changed while backing up: ' + change['path'])
                atomic(root, base + '/files/' + change['path'], saved)
        atomic(root, base + '/installed-before.json', old_bytes)
        new_bytes = encoded(incoming)
        atomic(root, base + '/installed-after.json', new_bytes)
        journal = {'schema': 1, 'transaction': ident, 'status': 'prepared', 'archive_sha256': sha,
                   'receipt_before': digest(old_bytes), 'receipt_after': digest(new_bytes),
                   'changes': result['changes']}
        atomic(root, base + '/transaction.json', encoded(journal))
        atomic(root, PENDING, encoded({'transaction': ident}))
        # On interruption leave the pending journal intact for explicit recovery.
        for change in result['changes']:
            if hash_at(root, change['path']) != change['before']:
                raise DistributionError('Concurrent edit detected; stop and restore: ' + change['path'])
            if change['after'] is None:
                remove(root, change['path'])
            else:
                atomic(root, change['path'], contents[change['path']])
        if hash_at(root, RECEIPT) != digest(old_bytes):
            raise DistributionError('Receipt changed during update; stop and restore')
        atomic(root, RECEIPT, new_bytes)
        journal['status'] = 'complete'
        atomic(root, base + '/transaction.json', encoded(journal))
        remove(root, PENDING)
        return {**result, 'applied': True, 'backup': ident}


def restore(root, ident=None, recover_lock=False):
    pending = read(root, PENDING)
    pending_id = load_json(pending).get('transaction') if pending else None
    ident = ident or pending_id
    if not isinstance(ident, str) or not re.fullmatch(r'\d{8}T\d{6}Z-[0-9a-f]{12}', ident):
        raise DistributionError('Specify a backup transaction ID, or recover an existing pending transaction')
    if pending_id and pending_id != ident:
        raise DistributionError('Restore the pending transaction first')
    with locked(root, recover_lock):
        base = '.rewired/backups/' + ident
        journal = load_json(read(root, base + '/transaction.json'))
        if journal.get('schema') != 1 or journal.get('transaction') != ident or (journal.get('status') == 'restored' and pending_id != ident):
            raise DistributionError('Invalid or already restored transaction')
        old_bytes = read(root, base + '/installed-before.json')
        new_bytes = read(root, base + '/installed-after.json')
        if digest(old_bytes or b'') != journal['receipt_before'] or digest(new_bytes or b'') != journal['receipt_after']:
            raise DistributionError('Backup receipt is damaged')
        old = validate_receipt(load_json(old_bytes))
        new = validate_receipt(load_json(new_bytes))
        if hash_at(root, RECEIPT) not in (journal['receipt_before'], journal['receipt_after']):
            raise DistributionError('A different version is installed; restore newer updates first')
        snapshots = {}
        seen = set()
        for change in journal['changes']:
            name = stock_path(change['path'])
            if name in seen or policy(name) != 'managed':
                raise DistributionError('Invalid restore path')
            seen.add(name)
            # Bind the journal to the original inventories, not arbitrary paths/hashes.
            if (change['before'] != old['files'].get(name, {}).get('sha256') or
                    change['after'] != new['files'].get(name, {}).get('sha256')):
                raise DistributionError('Backup journal differs from release inventories')
            current = hash_at(root, name)
            if current not in (change['before'], change['after']):
                raise DistributionError('File edited since update; preserve and reconcile before restoring: ' + name)
            data = read(root, base + '/files/' + name) if change['before'] else None
            if (digest(data) if data is not None else None) != change['before']:
                raise DistributionError('Backup file is damaged: ' + name)
            snapshots[name] = (current, data)
        atomic(root, PENDING, encoded({'transaction': ident}))
        for name, (previous, data) in snapshots.items():
            if hash_at(root, name) != previous:
                raise DistributionError('Concurrent edit detected during restore: ' + name)
            if data is None:
                remove(root, name)
            else:
                atomic(root, name, data)
        atomic(root, RECEIPT, old_bytes)
        journal['status'] = 'restored'
        atomic(root, base + '/transaction.json', encoded(journal))
        remove(root, PENDING)
        return {'restored': old['version'], 'backup': ident, 'personal_files': 'untouched'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    builder = commands.add_parser('build', help='Build a private test release from a clean stock template')
    builder.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    builder.add_argument('--output', type=Path, required=True)
    installer = commands.add_parser('install', help='Install into a new, nonexistent folder')
    installer.add_argument('--package', type=Path, required=True)
    installer.add_argument('--destination', type=Path, required=True)
    installer.add_argument('--sha256')
    updater = commands.add_parser('update', help='Preview by default; --apply writes after conflict checks')
    updater.add_argument('--root', type=Path, default=Path.cwd())
    updater.add_argument('--package', type=Path, required=True)
    updater.add_argument('--sha256')
    updater.add_argument('--apply', action='store_true')
    restorer = commands.add_parser('restore', help='Restore a backup or recover a pending transaction')
    restorer.add_argument('--root', type=Path, default=Path.cwd())
    restorer.add_argument('--transaction')
    restorer.add_argument('--recover-lock', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'build':
            result = build(args.source, args.output)
        elif args.command == 'install':
            result = install(args.package, args.destination, args.sha256)
        elif args.command == 'update':
            incoming, contents, sha = package(args.package, args.sha256)
            root = root_path(args.root)
            if not root.is_dir():
                raise DistributionError('OS folder does not exist')
            result = apply(root, incoming, contents, sha) if args.apply else plan(root, incoming)
            result['archive_sha256'] = sha
        else:
            result = restore(root_path(args.root), args.transaction, args.recover_lock)
        print(json.dumps(result, indent=2))
        return 2 if result.get('conflicts') else 0
    except (DistributionError, OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(json.dumps({'error': str(exc), 'action': 'Stop. Preserve files and inspect the issue; do not force overwrite.'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
