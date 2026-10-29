# Candidate scope and evidence · 2026-10-29

This source tree is the **0.6.0-beta.2 candidate**, not a claim of a published release. It adds playbook execution and method capture to the existing nine workflows, following [the product contract](product-contract.md). Previous onboarding acceptance does not establish acceptance of every revised instruction.

| Area | Evidence and limit |
|---|---|
| Product instructions | Eleven canonical workflows with matching host and visible copies. Playbook runs extend the existing project records using plain files. |
| Local helpers | 52 deterministic tests passed on 2026-10-29, including preservation of personal playbooks, run evidence, and post-update user edits through update and restore. |
| Content provenance | Playbook workflows, templates, example, and test fixture independently authored for Rewired. Prior component review remains historical evidence, not legal certification. |
| Compatibility | Existing skill identifiers, user-state formats, and installation receipt schema retained. Actual upgrade and rollback require release validation. |
| Assistant behavior | Fresh-context Codex trials passed correction/version handling and method capture. Separate Codex CLI 0.147.0 sessions recovered the pending review without file changes, then recorded explicit v2 content approval and prepared a checklist without publication. Model identifiers were not captured. |
| Cross-vendor resumption | Claude Code 2.1.280 was attempted on 2026-10-29 but returned an expired-login error before running. Claude resumption remains unverified. No credentials or account settings were changed. |
| External services | Vendor account setups, cloud-provider write routes, Windows, and background execution remain unverified. |

## Use and reporting

Read the installation guide for the exact candidate package. Do not substitute a previous public release when testing this candidate. A repository checkout needs a package build before it can be used as a receipt-tracked installation.

Start with “Let's get started” when the host loads workspace instructions; otherwise open START-HERE.md explicitly. Personal life, learning, and work are supported. Public-source research, the GTM library, tools, and routines are optional.

Use fictional or redacted records in public feedback. Include the exact version, host, request, observed behavior, and expected result. Keep personal OS folders, credentials, and private business records out of public issues.

The [release checklist](release.md) remains a set of required checks. Only observed results count as completed validation. A future public release must update this record with actual package and runtime evidence.

The [resumption protocol](playbook-testing.md) describes the reproducible fictional trial. Status-only reads were checked against file hashes; write trials preserved sources and earlier drafts. Other listed variations remain test cases, not observed passes. Local results do not establish cross-provider synchronization or every model's behavior.
