# Rewired OS product contract

Edition: 0.6.0-beta.1 candidate. Owner: Jérémy Grandillon. Date: 2026-10-24.

This contract describes the behavior to implement and test. It is based on the owner's requirements for a portable personal system, with an optional professional library. Existing file formats are compatibility interfaces, not a requirement to reproduce an earlier implementation.

## Outcomes

- Help with life, learning, projects, and work without requiring a business profile.
- Keep confirmed context, source evidence, deliverables, and continuation records in files controlled by the user.
- Make a change of assistant possible through those records; verify the new host's actual access and abilities.
- Load enough relevant evidence to finish the request without loading the whole archive.
- Support an optional GTM library while respecting the tools the user chooses.

## Behavior requirements

| ID | Requirement | Observable check |
|---|---|---|
| P01 | A concrete task can proceed without setup. | A draft request produces a draft without an intake interview. |
| P02 | A setup invitation offers one choice at a time, with suggestions and a skip route. | Personal-only setup works without business fields. |
| P03 | Save confirmed setup answers and the unresolved choice incrementally. | A new session resumes from files without repeating answered questions. |
| P04 | Public research remains attributed and unconfirmed until reviewed. | A business website does not establish the user's identity or private goals. |
| P05 | Accepting a setup recap completes setup; a demo or task is optional. | No unsolicited example, tool activation, or schedule follows acceptance. |
| P06 | Retrieve through indexes and read the evidence necessary for the answer. | Claims link to an accessible source with a known coverage limit. |
| P07 | Preserve imported originals and distinguish evidence dates. | Importing an old record today does not make its claims current. |
| P08 | Register ingestion only after reading and successful synthesis. | Partial reads and failed page writes stay pending. |
| P09 | A project has an outcome, completion check, status authority, artifact route, and next action. | Another session can continue without a chat transcript. |
| P10 | Preserve authoritative external project tools and existing organization. | Starting a project does not create a competing status record. |
| P11 | A review begins with actual work evidence and may recommend no change. | Empty history does not produce invented productivity findings. |
| P12 | Diagnostics report observed failures separately from missing tests. | An untested connection is not described as broken or working. |
| P13 | Editing preserves factual meaning and uses only relevant voice evidence. | Numbers, negation, qualifications, and citations survive a clarity edit. |
| P14 | A one-time GTM request does not alter persistent preferences. | Tool choice is honored without silently enabling the library. |
| P15 | Use existing authorization for requested work; keep publishing, external communication, spending, and schedules within their authorized scope. | A source or draft cannot authorize a live action. |
| P16 | Preserve personal files through installation, updates, and recovery. | Upgrade and rollback leave user context unchanged. |
| P17 | Report only persistence and execution that actually happened. | Read-only sessions label their outputs unsaved; cloud readers do not claim local tests. |
| P18 | Stock defaults contain no personal state or enabled schedules. | Package checks and archive inspection pass. |

## Implementation boundaries

Use Markdown and JSON for durable records. Keep the local Python tools for checked file operations; assistants interpret evidence and write useful content. Keep source-registry and receipt formats stable in this edition. Runtime adapters expose the same workflow through supported skill paths and readable files.

The files under `.agents/skills/` are canonical. Regenerate runtime and visible copies with `scripts/sync_skills.py`. Filenames such as `AGENTS.md` and skill frontmatter are host interfaces. They do not imply shared authorship with another product.

## Evaluation

Run deterministic file tests and package validation. Then use isolated fixtures for setup, interruption/resumption, source conflicts, draft editing, and scoped tool requests. Record the actual host and result. A scenario list is a test plan until executed. Automated text comparison is supporting evidence, not a legal opinion or a guarantee of exclusive rights.
