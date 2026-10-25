# Rewired OS

**Change your AI. Keep your system.**

A portable personal OS for your life, learning, projects, and work: context, sourced knowledge, working methods, and things to continue. Use it with the assistant and file provider that fit you. Your accumulated work stays in files you control when you change the model that helps you use it.

Built as a general personal OS, with GTM operators and founders as its initial audience; the optional GTM Library adds practical methods and setup guides for selected tools. This checkout is the unpublished 0.6.0-beta.1 replacement candidate. Revised instructions require their own behavioral validation; broader host, provider, and vendor-account pilots remain pending. See [beta scope and evidence](docs/beta-status.md).

## Start here

This candidate has no public download URL yet. Use the maintainer-supplied `rewired-os-0.6.0-beta.1.zip` and checksum, or build a reviewed checkout using [distribution maintenance](docs/distribution.md). The older public beta does not contain these replacements. See [installation](INSTALL.md).

Give your assistant the candidate folder and ask it to follow START-HERE.md.


1. Follow [installation](INSTALL.md) with the provided release ZIP. Extract into a new folder on your laptop or preferred synced drive. Git and GitHub are not required to use it.
2. Give your assistant access locally or through a supported connector. In a host that loads this workspace's guidance, say **“Let's get started”** or **“Let's go.”** If it does not load guidance automatically, point it to START-HERE.md once.
3. Let the assistant guide you through personalizing the OS, one question at a time with suggested answers. Include personal life, work, or both. When relevant, share a website to save explaining your business; review what it finds. Choose a real task only when ready.

An assistant needs actual file access. Uploaded files are snapshots; they do not automatically update originals. Read [START-HERE.md](START-HERE.md) and [portability](docs/portability.md) for the relevant access mode and its limits.

## Use ordinary language

- Let's get started.
- Help me organize a personal project or learning goal.
- Bring this research or handoff into my OS.
- Start a project for this campaign and help me take the first step.
- Where did I leave off on this project?
- Help me think through this decision.
- Review my week and suggest one worthwhile improvement.
- Check my knowledge intake and flag sources that need review.
- Polish this draft for my audience while keeping the facts intact.
- Activate the GTM Library and help me use lemlist.

The visible [workflow index](workflows/index.md) works without a skill installer. Local skill packages are also included. The assistant loads only the method and evidence needed for the task.

For work spanning sessions, [project setup](docs/projects.md) begins with one brief: outcome, selected evidence, deliverable links, dated state, and the next unfinished action. Existing project folders and tools remain authoritative. Add stages only when repeated work needs them.

## How it grows

**Source → Knowledge → Work → Feedback.** Keep originals, derive useful knowledge, apply it to work, and retain accepted corrections. The [native wiki](docs/knowledge.md) supplies a retrieval route instead of filling every conversation with your whole history.

Setup offers on-demand or light assistance. Light assistance makes relevant suggestions during an active session. [Routines](docs/routines.md) need separately verified scheduling support to run in the background. No jobs ship enabled.

The optional [GTM Library](library/README.md) includes original Rewired playbooks and researched profiles for lemlist, FullEnrich, Clay, and Claap, the default meeting recorder. Each use case supports user-selected alternatives through current tool research and guided setup. Activating guidance does not install software or connect accounts. Asking to set up a selected tool starts guided setup, using existing authorization and pausing only for missing material choices or user-controlled sign-in.

The [intake-health report](docs/ingestion-health.md) shows local import outcomes, pending files, and integrity gaps. Source dates stay separate from ingestion dates. The optional [editing workflow](docs/editing.md) uses relevant voice evidence and preserves meaning; it runs when requested, not on every response.

## Optional local helpers

The file-based guidance requires no Python. For local imports, source hashes, and deterministic checks, helpers use Python 3.10+ without third-party packages:

```sh
python3 scripts/knowledge.py health
```

For a selected source, ask the assistant to bring it into your OS. A fictional call is included for an explicitly chosen demo, not automatic onboarding. The assistant interprets; the helper tracks files. Cloud-only assistants without execution can retrieve knowledge and contribute handoffs, but cannot claim these helper checks ran.

## Install and update

The [installation guide](INSTALL.md) supports agent-assisted setup and ordinary ZIP extraction. Packaged releases record their stock version and file hashes. [Updates](UPDATE.md) preview first, preserve personal files, block conflicting product edits, and save recoverable product backups. Python 3.10+ is needed for checked installation and updates; the basic folder remains readable without it.

Use the packaged release ZIP rather than the repository source archive. An agent can retrieve a selected release; the local helper itself does not download updates or run in the background. See [change notes](CHANGELOG.md) and the [private pilot](docs/distribution-testing.md).

## Development and provenance

```sh
python3 scripts/sync_skills.py
python3 scripts/check_package.py
python3 -m unittest discover -s tests -v
```

Build instructions are in [distribution maintenance](docs/distribution.md).

Read the [operating model](docs/operating-model.md), [runtime notes](docs/runtimes.md), [provenance](PROVENANCE.md), and [release requirements](docs/release.md). The current edition's original contributions are licensed under [MIT](LICENSE). Read the [product contract](docs/product-contract.md) for its implementation requirements.
