# Beta scope and evidence · 2026-10-23

Rewired OS is being released as an early beta. The author tested the revised onboarding in a new Codex project and accepted it for release on 2026-10-23. This is a user-reported result; the exact model/app version and full transcript were not recorded in this package.

| Area | Evidence | Limit |
|---|---|---|
| Guided onboarding | Author's positive fresh-project trial of 0.5.1 | No claim that every host/model follows the flow identically |
| Local ingestion and distribution helpers | 51 deterministic tests pass on macOS arm64, Python 3.12.14 | Does not establish semantic quality or all operating-system compatibility |
| Package integrity | Explicit stock inventory, per-file hashes, ZIP checksum, stock link/mirror/privacy-marker checks | Checksums are not publisher signatures; scans are not a security audit |
| Updates and recovery | Fresh installation, preview, upgrade, personal-file preservation, conflict blocking, and rollback checked locally | One writer required; no distributed cloud lock or universal migration engine |
| Native skills and visible workflows | Nine skills with matched Claude/visible copies | Full discovery and behavior across hosts remain to be piloted |
| GTM Library | Original guides and dated official-documentation research for four recommended tools | Live account setups and vendor actions are not verified merely by including a profile |
| File-provider portability | Documented local/sync/connector access contract | Windows, direct cloud ingestion, and each sync/provider route need their own pilots |

## What to expect

Open the installed folder and say “Let's get started” in an assistant that loads its workspace guidance. Otherwise point it to START-HERE.md once. Personalize around life, learning, projects, and work. A website and a business are optional. The fictional example is an explicitly chosen demonstration.

The OS is readable without Python. Local helpers need Python 3.10+. Your assistant supplies reasoning, browsing, file access, and tool execution. Rewired does not provide model subscriptions, install a local model, connect accounts, schedule background work, or promise quantified token/cost savings.

Use a separate folder for a first trial, and keep normal backups of your own work. The updater's backup covers changed product files, not all personal data.

## Feedback

Report the release version, host/model if known, what you asked, what happened, and what you expected. Use fictional or redacted examples in public issues; do not upload your personal OS, transcripts, credentials, or private business records.

The [release checklist](release.md) records further acceptance scenarios. Pending scenarios remain useful testing work; their presence is not a claim that they have passed.
