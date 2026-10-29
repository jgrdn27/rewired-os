# Projects that are easy to continue

A project needs enough saved context for another assistant to continue useful work. Start with the smallest structure that achieves that. Read this guide for project creation or a requested organization repair, not every conversation.

## Choose the right amount of structure

| Work | Starting structure |
|---|---|
| Quick answer or one-off draft | Conversation or requested artifact |
| Work spanning sessions | One project brief with evidence and deliverable links |
| Repeated process with real stages | Brief plus reusable method and per-run artifacts, added when needed |

For a new project the default is `work/<name>/PROJECT.md`. Use [the brief template](../templates/project.md). If a repository, CRM, task system, or existing folder already owns the project, preserve that location and link it. Do not move files, duplicate changing status, or create nested operating manuals simply for consistency.

## What the brief keeps

Record the intended result, completion criteria, scope, selected evidence, latest deliverable, dated state, and next unfinished action. Identify owners and deadlines only when known. Distinguish confirmed criteria from assistant proposals. Link current state to its authoritative source; if the brief owns local state, say so. A dated observation of external state does not establish its current state when the external system is unavailable.

Use relative links inside the OS and stable provider references outside it. Reuse the wiki and raw sources. A project brief provides work context; the wiki holds reusable knowledge. Neither should become another copy of the user's full business context or live CRM.

Keep approvals and execution explicit. A draft may be ready for review while the project remains unfinished. Record completion only against the defined outcome and supporting evidence. An existing file, successful API submission, or earlier assistant claim alone does not prove the requested outcome happened.

## Grow when the work calls for it

Add an output folder when there are actual outputs to organize. For a repeated process, keep the reusable method separate from dated run artifacts. Describe each needed stage's input, intended output, and completion check. Introduce a human review point where the user's preference or action scope requires one; do not add a permission stop between every reversible internal step.

Use [playbook runs](playbooks.md) when those stages need evidence, waiting conditions, or continuation across sessions. Link each run from the brief. Keep its progress in that run or the existing authoritative tool, rather than repeating checkpoint status in the brief and index.

Project setup and resumption preserve existing authorization. Sending, spending, publishing, and changing external records still depend on the task's scope. Closing a project does not silently delete its evidence or create recurring automation.

Use one writer for a project brief at a time. When a sync conflict or another active writer is unresolved, preserve a separate handoff instead of overwriting state. Follow [portability](portability.md) for cloud write limits. With no write access, provide an unsaved brief without claiming it is registered.

## Fresh-reader check

From `work/index.md`, follow the selected project link and its relevant deliverable/source. Without relying on conversation history, verify that the files answer:

- What result is this project trying to produce, and what counts as done?
- What evidence or deliverable exists, and what remains unverified?
- Where does authoritative status live, and when was it observed?
- What is the next unfinished action, and does it need missing input or authorization?

Check that referenced local files exist and selected external references are accessible when access is available. If a link cannot be checked, label it unverified. Inspect the content as well as the path; a placeholder is not a completed deliverable. This manual review is useful but does not prove a new model/session can follow the route. Use the pilot scenarios in [release readiness](release.md) for that stronger test.

See [the fictional project](../examples/fictional-project/PROJECT.md) for a draft-ready project whose customer commitment remains unverified.
