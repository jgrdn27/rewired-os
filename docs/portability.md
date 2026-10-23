# One system, different assistants

Rewired OS separates what lasts from what executes. The files contain knowledge, methods, preferences, sources, and resume points. The host supplies a model, file access, tool execution, credentials, and optional scheduling. Replacing a model should not require rebuilding the first layer. It can still change reasoning quality and tool behavior.

## The four layers

| Layer | Contents | What changes independently |
|---|---|---|
| Your system | Plain Markdown, JSON preferences, originals, wiki, work | Your knowledge and accepted corrections |
| Libraries | Optional methods and selected tool profiles | Domain expertise and available tools |
| Access | Local filesystem, synced folder, connector, or API | File provider, account permissions, device |
| Intelligence and execution | Assistant host, chosen model, tools, credentials | Model vendor, local/open-weight model, application |

OpenAI, Anthropic, Google, xAI, and local/open-weight runtimes are possible intelligence choices, not certified integrations in this preview. A model alone does not read a folder or run a CLI. Its host must expose those capabilities. Use [START-HERE.md](../START-HERE.md) and the visible [workflow index](../workflows/index.md) where native skill discovery is unavailable.

## File access modes

| Mode | Useful behavior | Limit |
|---|---|---|
| Local folder | Read and write selected files; run helpers where supported | Access is limited to that device and host |
| Synced local folder | Same local operations plus provider synchronization | A local save does not prove the cloud or second device has received it |
| Direct cloud connector/API | Retrieve the same identified cloud files; write only where supported | Search, raw Markdown reads, writes, and folder access vary by host and account |
| Upload/export | Answer from a selected snapshot; return a proposed handoff | No continuing synchronization or writeback implied |

Google documents local/cloud synchronization and offline choices in [Drive for desktop](https://support.google.com/drive/answer/10838124?hl=en). OneDrive's [Files On-Demand](https://support.microsoft.com/en-us/onedrive/save-disk-space-with-onedrive-files-on-demand-for-windows) distinguishes online-only and downloaded files. Box Drive supports [selected offline content](https://support.box.com/hc/en-us/articles/360043697574-Making-Content-Available-Offline) and warns about conflicting edits. These are provider capabilities, not evidence that any particular assistant connector can edit these files.

Store ordinary `.md` and `.json` files, not converted Google Docs or proprietary notebook entries. A connector must return the necessary file content, not just its title or search snippet. Absolute paths, credentials, and installed binaries belong to the device, not the portable instructions.

## Prove two routes reach the same system

Use [the access-record template](../templates/access-record.md) in `connections.md`. Record the intended account/workspace, provider folder ID or URL, local root if relevant, and one non-sensitive anchor file's cloud ID and relative path. Compare complete contents or hashes and provider revision metadata where available. A matching name alone is not proof.

For a write route, use a unique harmless handoff inside the authorized area only when the task includes testing writes. Read it back through the other route after synchronization and record the result. Keep read access, write access, and cross-route synchronization as separate verification states. Do not claim success from merely installing a plugin.

## Continue from a train or another device

Before leaving, save the deliverable and next unfinished step, wait for sync, and make the needed folder available offline. A phone/cloud assistant can read the canonical files through a verified connector while online. Offline files do not make a cloud model or SaaS API work offline. A local model needs a capable local host and enough device resources; this preview does not install one.

Keep one designated wiki writer at a time. Other sessions can read and create unique raw handoffs when authorized. The local helper lock is not a distributed lock and must not be treated as protection against a second synced device. Before editing shared state, confirm the first writer has stopped and synchronization is settled; if that cannot be established, contribute a new handoff instead. Preserve both versions of a conflict and reconcile explicitly. Do not let a last-write-wins sync silently replace an original.

The current canonical ingestion path requires the local helper. Cloud-only contributors leave new handoffs for that writer. A future direct-cloud maintainer needs provider revisions, conditional writes, source hashing, conflict handling, and verified registry access before it can claim equivalent guarantees. This preview does not implement that adapter.

## Keep context and cost bounded

Read a small index, selected pages, and the needed evidence. Load one workflow, then one library playbook or tool profile as needed. Summarize new sources once; do not re-ingest the full archive for each chat. Keep bulky exports and result rows out of general context. Reuse a checked result when freshness is sufficient, and run deterministic checks without a model where possible.

Record model-reported usage or provider billing data when available; measure retrieval quality and correction burden too. Less repeated input is a design objective, not a guaranteed bill reduction. Pricing, caching, reasoning, and the host's own context loading affect actual cost.

## Supported capability levels

- **Reader:** retrieves selected complete files and cites the right source.
- **Contributor:** additionally creates a unique handoff in an authorized location.
- **Maintainer:** additionally runs source checks and updates derived pages through the designated ingestion path.
- **Executor:** additionally performs a specifically authorized operation through a verified tool account.

Record observed capabilities for each route. A powerful model with read-only access remains a reader. Credentials stay in the host's credential store or protected environment outside the synced folder; they are not wiki content. A model switch reuses files, but each new host's access must be established.
