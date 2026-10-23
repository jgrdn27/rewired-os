#!/usr/bin/env python3
"""Check the stock foundation manifest, links, skill parity, and known leaks."""
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'release-manifest.json').read_text())
expected = set(manifest['files'])
actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
          if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}
errors = []
if actual != expected:
    errors.append(f'Manifest difference: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
for value in sorted(expected):
    file = root / value
    if not file.is_file():
        continue
    if file.is_symlink():
        errors.append('Symlink in distribution: ' + value)
    text = file.read_text(encoding='utf-8')
    if re.search(r'/Users/|[A-Za-z]:\\Users\\|@capsulehq\.|TC9|SparkStack', text) and value != 'scripts/check_package.py':
        errors.append('Potential personal data: ' + value)
    if value.endswith('.md'):
        body = re.sub(r'```.*?```', '', text, flags=re.S)
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            url = urlsplit(link.strip().strip('<>'))
            if url.scheme or link.startswith('#'):
                continue
            target = (file.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f'Broken package link: {value}: {link}')
    if value not in ('PROVENANCE.md', 'licenses/AIS-OS-MIT.txt', 'scripts/check_package.py'):
        if re.search(r'Three Ms|Four Cs|HerkBrain|/level-up|/grill-me|/onboard|/3d-brain', text):
            errors.append('Upstream product language outside provenance: ' + value)
source = root / '.agents/skills'
target = root / '.claude/skills'
for file in source.rglob('*'):
    if file.is_file():
        mirror = target / file.relative_to(source)
        if not mirror.is_file() or mirror.read_bytes() != file.read_bytes():
            errors.append('Skill mirror mismatch: ' + str(file.relative_to(source)))
if (root / 'CLAUDE.md').read_bytes() != b'@AGENTS.md\n':
    errors.append('Invalid manual bridge')
for skill in source.glob('*/SKILL.md'):
    visible = root / 'workflows' / (skill.parent.name + '.md')
    if not visible.is_file() or visible.read_bytes() != skill.read_bytes():
        errors.append('Visible workflow mismatch: ' + skill.parent.name)
catalog = json.loads((root / 'library/catalog.json').read_text())
ids = set()
for entry in catalog['tools']:
    if entry['id'] in ids:
        errors.append('Duplicate library tool: ' + entry['id'])
    ids.add(entry['id'])
    profile = (root / entry['profile']).resolve()
    if not profile.is_relative_to(root) or not profile.is_file():
        errors.append('Missing or unsafe tool profile: ' + entry['id'])
    if entry['verification'] != 'documentation-reviewed' or entry['live_tested'] is not False:
        errors.append('Unexpected live verification claim in stock catalog: ' + entry['id'])
    if not entry['official_sources'] or any(urlsplit(url).scheme != 'https' for url in entry['official_sources']):
        errors.append('Missing HTTPS sources: ' + entry['id'])
    revision = entry.get('reviewed_skill_commit')
    if entry.get('review_basis') == 'official-documentation-and-repository':
        if not isinstance(revision, str) or not re.fullmatch(r'[0-9a-f]{40}', revision):
            errors.append('Invalid source revision: ' + entry['id'])
    elif entry.get('review_basis') != 'official-documentation' or revision is not None:
        errors.append('Invalid documentation-only review: ' + entry['id'])
use_cases = set()
for entry in catalog['use_cases']:
    if entry['id'] in use_cases:
        errors.append('Duplicate use case: ' + entry['id'])
    use_cases.add(entry['id'])
    if entry['default_tool'] not in ids:
        errors.append('Unknown default tool: ' + entry['id'])
    playbook = (root / entry['playbook']).resolve()
    if not playbook.is_relative_to(root) or not playbook.is_file():
        errors.append('Missing or unsafe playbook: ' + entry['id'])
preferences = json.loads((root / 'preferences.json').read_text())
if preferences['libraries']['gtm']['enabled'] is not False:
    errors.append('Stock GTM Library must be opt-in')
if preferences['libraries']['gtm'].get('tool_overrides') != {}:
    errors.append('Stock package must not include personal tool overrides')
print(json.dumps({'files': len(expected), 'skills': len(list(source.glob('*/SKILL.md'))),
                  'library_tools': len(ids), 'issues': errors,
                  'scope': 'Stock manifest, known-string scan, Markdown links, skill/workflow mirrors, library metadata; manual privacy and live integration review still required'}, indent=2))
raise SystemExit(bool(errors))
