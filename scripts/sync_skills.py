#!/usr/bin/env python3
"""Generate host packages and visible workflows from canonical skills."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
source = root / '.agents/skills'
target = root / '.claude/skills'
expected = {p.relative_to(source) for p in source.rglob('*') if p.is_file()}
existing = {p.relative_to(target) for p in target.rglob('*') if p.is_file()}
extras = existing - expected
if extras:
    raise SystemExit('Unrecognized generated files; inspect before syncing: ' + ', '.join(map(str, sorted(extras))))
visible = root / 'workflows'
workflow_sources = {p.parent.name + '.md': p for p in source.glob('*/SKILL.md')}
visible_extras = {p.name for p in visible.glob('*.md')} - set(workflow_sources) - {'index.md'}
if visible_extras:
    raise SystemExit('Unrecognized visible workflows; inspect before syncing: ' + ', '.join(sorted(visible_extras)))
for relative in sorted(expected):
    destination = target / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / relative, destination)
visible.mkdir(exist_ok=True)
for name, origin in sorted(workflow_sources.items()):
    shutil.copyfile(origin, visible / name)
print(f'Synced {len(expected)} host files and {len(workflow_sources)} visible workflows without path rewriting.')
