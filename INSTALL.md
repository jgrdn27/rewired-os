# Install Rewired OS

**Change your AI. Keep your system.** Download once, keep your OS in a shared folder you control, and give each assistant access to that same folder.

**[Download the installable ZIP](https://github.com/jgrdn27/rewired-os/releases/download/v0.6.0-beta.3/rewired-os-0.6.0-beta.3.zip)** and get its checksum from the [release page](https://github.com/jgrdn27/rewired-os/releases/tag/v0.6.0-beta.3). The packaged ZIP includes the installation receipt used for safe updates. You do not need Git or a GitHub account.

Choose Google Drive, OneDrive, Box, or another storage service you prefer. The folder can remain private to you. What matters is that the assistants and devices you use can reach the same saved context and work through a synced local folder or a supported connector.

## Give this to your assistant

> Help me install this Rewired OS ZIP in a new folder in my preferred shared storage. Follow INSTALL.md. If I already have a Rewired OS folder, help me connect to it instead of creating another copy.

Use the release asset linked above and its checksum. Identify the user's intended shared folder and actual file access before installing or saving personal context. Reuse an existing OS. For a first install, extract into a new location there and follow START-HERE.md. Do not create a separate OS in each assistant's default project folder. If the package cannot be retrieved, give the user the download link and a manual extraction route; do not silently substitute a source clone.

Once the installed folder is open in a host that loads workspace guidance, “Let's get started” or “Let's go” starts setup. Other hosts need an explicit reference to START-HERE.md. A chat attachment is a snapshot, not write access to its original.

## Choose the route that works here

| Your assistant can… | Setup route |
|---|---|
| Read and write local files and execute commands | Install or extract the ZIP into a new folder in the local synced drive, then work there. |
| Read and write local files without execution | You extract the ZIP into your preferred shared storage, then give the assistant access to that folder. |
| Read or write cloud files through a connector | Extract into the synced drive, wait for sync, then verify access to those same files through the connector. Capabilities vary. |
| Only chat or read uploaded attachments | Extract the ZIP yourself. Upload selected files as snapshots for help; changes must be saved back explicitly. Do not claim the original folder was updated. |

The readable OS needs no Git, GitHub account, Python, or vendor subscription. The optional checked installer and updater require Python 3.10+ on a local filesystem. They install no dependencies. Do not install a runtime or change machine settings implicitly.

## The simple folder route

1. Obtain the ZIP and SHA-256 value from the intended maintainer/release. Compare the downloaded file's checksum when tooling is available. A checksum from the same untrusted source does not establish authenticity.
2. Extract into a **new folder in your preferred shared storage**, such as Google Drive, OneDrive, or Box. The ZIP contains one `Rewired-OS` folder. Never extract over an existing OS or merge folders.
3. Keep the complete folder together, including hidden `.rewired`, `.agents`, and `.claude` folders. `.rewired/installed.json` records the original stock version and hashes for future updates. You can choose a name such as `My Rewired OS` when placing the new folder.
4. Let synchronization finish. For local assistants and helpers, make the folder available on the device rather than leaving its files online-only.
5. Point your first assistant to this folder and ask it to **read START-HERE.md and help you get started**. Confirmed personalization and work are saved here.
6. Point your next assistant to the **same folder** through its supported local or cloud access route. Check that it sees the saved context before continuing. Finish one writer's work and let sync settle before another assistant writes.

A local-only folder is also usable if you choose it; other devices need an access route to reach it. A repository link, separate agent checkout, or uploaded copy does not automatically share changes with your personal OS. If an assistant can only read snapshots, save its accepted changes back to the shared folder explicitly.

Keep the original ZIP and its checksum outside the working OS. No repository, account connection, telemetry, or scheduled job is created by extraction.

## Checked installation for a local agent

Read the instructions and obtain the helper from the trusted package first. Run it from the extracted stock folder, with the ZIP kept separately. Replace the sample names and use quoted absolute paths for paths containing spaces:

```sh
python3 scripts/distribution.py install --package "/path/to/rewired-os-0.6.0-beta.3.zip" --destination "/path/to/synced-drive/My Rewired OS" --sha256 "EXPECTED_SHA256"
```

The destination's parent must exist; the destination must not exist, even as an empty folder. The helper validates the inventory and hashes, rejects unsafe archive paths and symlinks, stages the files, and installs the complete folder. A failed validation creates no destination. Do not pass the literal placeholder checksum; use the supplied 64-character digest.

For Windows, use the available Python 3.10+ launcher and native quoted paths. Windows and cloud-provider pilots remain pending; no platform support is inferred merely from portable code.

## Assistant: guide personalization

- Identify the intended shared folder and actual read/write access, then read START-HERE.md and the canonical AGENTS.md. Reuse a confirmed existing folder; changing assistant is not a reason to reinstall or restart setup.
- Follow Get started (`first-win` internally): one focused question at a time, suggested answers/examples, and free response/skip. Learn about personal life, work, or both as the user chooses.
- Offer a website or public profile as a shortcut when work context is relevant. Read only accessible selected pages, label claims, link sources, and ask the user to confirm. Use pasted text or a brief explanation if browsing is unavailable or a social platform blocks access.
- Save confirmed context and a small resumable setup record. Respect existing files. Confirm saved content by reading it back. Do not claim persistence with read-only access.
- Offer assistance preferences and relevant routines during setup. GTM guidance is optional; no schedules, vendor tools, or accounts are enabled implicitly.
- Recap the personalization for the user to accept or correct. Then offer a real task, optional demo, or stop for now. The fictional call must never run merely because setup began.

Already have a Rewired OS? Connect this assistant to it. Use [safe updates](UPDATE.md) when an update is requested. If you are moving from a different system, keep it intact and bring only selected information into a new Rewired folder through the source-preserving workflow.

For later releases, use [safe updates](UPDATE.md). For file-provider and host limits, use [portability](docs/portability.md).
