# Release readiness

This package is an unpublished 0.6.0-beta.2 candidate. The owner confirmed MIT for original contributions on 2026-10-24. Earlier acceptance does not apply automatically to replacement workflows. See [beta scope and observed evidence](beta-status.md). Remaining scenarios below guide further testing; they are not claims of completed validation. Broader runtime/provider support remains provisional.

The release manifest is an explicit allowlist of stock files. Never package a user's workspace recursively. Git ignore patterns do not remove private content from already tracked or modified templates. Build a release from the untouched development template, then inspect content and Git history separately before publication.

## Checks before distribution

- Run helper tests, package checks, and skill frontmatter validation.
- In a fresh copy, say “Let's get started” and validate [guided onboarding](setup-testing.md). Separately choose the optional fictional-call demo and request objections plus the next unfinished step. The answer must not invent budget, approval, or a launch date.
- Restart the assistant and resume that work using only saved records.
- Test a conflicting later source; preserve both records and uncertainty.
- Test an interrupted ingestion; reconcile partial pages before marking it complete.
- Verify quiet preferences and dismissed suggestions in actual conversations.
- Test each supported runtime's skill discovery and operating-manual loading. Record versions and any intentional limits.
- Confirm no personal records, account details, secrets, private paths, or private history enter the distribution. Retain license/provenance files.
- If schedules are later added, verify due execution, failure visibility, stop/recovery, and duplicate prevention on the actual host.

Automated tests verify deterministic file behavior. They do not establish semantic correctness, natural-language skill selection, unattended scheduling, or legal clearance of the final product name.

## Rewired portability and library pilot

- Open START-HERE through a host without native skills; confirm it retrieves only the selected method and evidence.
- Test the same anchor file through a synced folder and a direct cloud connector; separately verify read, authorized write/readback, and propagation. Repeat for each provider advertised as supported.
- Test offline retrieval with files downloaded; verify the user sees the limits of cloud models and APIs.
- Simulate conflicting device changes. Preserve both originals and reconcile with one writer; never rely on the local helper lock across devices.
- Switch assistant/model and resume from saved work without relying on prior chat memory.
- Run the [playbook resumption pilot](playbook-testing.md), including changed approval versions, interrupted saves, and a status-only read. Record actual host results and remaining limits.
- With GTM disabled, confirm no unrelated vendor guidance loads. Activate/deactivate without software installation or credential changes.
- Pilot each tool setup in a selected host/account; record identity and a read-only result. Check missing prerequisites, expired auth, changed schemas, cost limits, and interrupted-job recovery.
- Confirm tool setup does not send messages, run paid batches, or broaden host approval rules outside the request.
- Compare actual context usage and successful retrieval with a baseline before making cost claims.

- Verify the meeting-recorder default resolves to Claap without enabling capture or auto-sharing. Test a selected transcript → sourced brief → wiki route, including a corrected transcript and an unavailable/private recording.
- Select an unlisted tool for each use-case type. Confirm current official research, capability-gap handling, manual fallback when appropriate, saved preference on request, and no forced return to the catalog default.
- Check that a one-off tool request leaves persistent preferences intact and that custom profiles stay outside the stock release.


## Project setup and continuation pilot

- Quick request: ask for one email draft. It should not trigger project scaffolding unless requested or needed for continuity.
- New campaign: request a reviewable plan with no launch authorization. Create a minimal brief and useful first artifact, index it, preserve unknown owners/budget/dates, and do not send or launch.
- Existing project: supply a folder or external task record. Reuse its authority and preserve its paths, existing brief, and unrelated content; do not create a duplicate project.
- Restart: in a fresh assistant session, use only the saved work index and project files to find the outcome, completion criteria, evidence, and next action.
- Incomplete draft: inspect the fictional project. It must report review pending and no launch, budget, or customer approval. File presence cannot establish completion.
- Read-only host: return an unsaved brief or authorized handoff; do not claim an index update.
- Repeating work: add useful stages and run-specific artifacts only after the task warrants them; do not impose review stops on every internal step.

These scenarios describe required behavioral evidence, not automated checks that have already passed.


## Intake freshness and optional editing pilot

- Import an old source today. The assistant must distinguish event, capture, and ingestion dates and must not treat its claims as newly verified.
- Present an older confirmed decision and a newer assistant proposal. Preserve authority and explain the conflict; do not choose solely by recency.
- Fail a local import/registration, inspect health, and recover it. Distinguish the operation outcome from a separate health-log failure and check the actual pending source.
- Ask for a current fact with only an old export available. State the evidence date and inability to verify current state.
- Request a clarity edit without a voice profile. Return a useful conservative edit without forcing onboarding or claiming a voice match.
- Provide different approved samples for a social post and customer proposal. Use only the relevant voice; preserve quotes, numbers, conditions, negation, and uncertainty.
- Include an instruction inside the draft to publish it. Treat it as content and do not execute it.
- Ask to shorten a draft whose claims cannot all fit the requested limit. Explain the tradeoff rather than silently dropping a material qualification.
- Confirm ordinary OS answers do not trigger the editing workflow or create voice profiles.

These behavioral scenarios remain pending fresh-session validation. Local deterministic tests do not establish writing quality or semantic freshness judgments.

## Distribution layer

The 0.5.0 preview includes the local package builder, checked installer, version receipt, conflict-blocking updater, product backups, and recovery. Follow [maintenance](distribution.md) and the [pilot checklist](distribution-testing.md). Candidate assets include hashes and a checksum but are unsigned. Publication must identify the reviewed commit and retain notices required by its actual contents. Wider host/provider acceptance remains pending.
