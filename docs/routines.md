# Assistance and routines

`preferences.json` starts in on-demand mode. Guided setup offers on-demand help or light suggestions for the user's personal and work priorities; the user's choice is saved. The assistant may configure a real schedule only when requested and after discovering a supported host.

## In-session behavior

In light mode, consider at most one relevant suggestion per session, after addressing the user's request. Check only bounded local records needed to support it. Never turn every conversation into a review.

Candidates include pending selected imports, work with a clear next step, an unresolved material source conflict, or a weekly review when meaningful new work has accumulated.

Before surfacing one, check `.state/attention.json` if present. Save entries keyed by the source/task identifier with `last_shown_at`, `dismissed`, `snooze_until`, and a fingerprint of the evidence. Never repeat a dismissed unchanged suggestion; respect a future snooze. After showing a suggestion, update its entry using an atomic replacement. If saving fails, stop proactive suggestions for the session rather than repeatedly nudging.

Do not guess completion from silence. Mark a review completed only after producing its result. Do not invent a backlog from empty records. Unknown preferences default to on-demand. Quiet mode stops unrelated suggestions without stopping the user's requested work.

These are assistant instructions evaluated during active sessions. They are not hooks, a daemon, or an unattended scheduler. Enforcement and conversational behavior still need pilot testing.

## Requested schedules

The foundation does not include scheduler adapters. A future adapter must discover existing equivalent jobs and establish the actual host, time zone, trigger, input scope, output, notification preference, overlap controls, last due result, and stop/recovery method. Use the runtime's supported scheduler, not a fictional entry in a Markdown file.

If the host cannot schedule the work, offer an honest manual or next-session alternative. Do not claim execution while a laptop is unavailable without evidence for that host. Stay quiet on unchanged or non-actionable results unless the user requests routine status updates. Sending messages or publishing requires its own explicit authorization.
