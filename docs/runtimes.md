# Runtime adapters, portable methods

Rewired OS is a normal folder, usable without Git or GitHub. Start with `START-HERE.md` in any assistant that can read the selected files. The visible `workflows/` copies make methods accessible without native skill discovery. A read-only or upload-based session has narrower capabilities than a local executor; see [portability](portability.md).

For development, `.agents/skills` is the authoring source. `scripts/sync_skills.py` generates byte-identical `.claude/skills` packages and visible `workflows/<name>.md` files. Do not hand-edit generated copies. These methods resolve paths from the OS root, never from the skill's own folder.

Codex reads root `AGENTS.md`; Claude's root `CLAUDE.md` imports it. Open this folder as the workspace root. Do not copy only the skill folders: the workflows depend on the manual, indexes, library, and optional helpers.

Documentation checked 2026-10-05:

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex plugins](https://learn.chatgpt.com/docs/plugins)
- [Claude skills](https://code.claude.com/docs/en/skills)
- [Claude memory imports](https://code.claude.com/docs/en/memory)

Matching files establish packaging parity, not equivalent reasoning or tool behavior. Local Python ingestion requires Python 3.10+. Direct cloud ingestion, universal connector installation, and cross-device locking are not implemented. A host may require explicit instructions to read START-HERE rather than automatically loading a manual.

Before claiming supported runtimes, test fresh sessions for manual loading, all nine workflow routes, source retrieval, resume points, and library activation. Record app/tool versions and differences. No global skills, accounts, hooks, or schedules are installed by this package.
