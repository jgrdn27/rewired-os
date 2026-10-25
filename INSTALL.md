# Install Rewired OS

**Change your AI. Keep your system.** Start with a folder you control and guided personalization around your life and work.

Source repository: [jgrdn27/rewired-os](https://github.com/jgrdn27/rewired-os). This checkout describes the **unpublished 0.6.0-beta.1 candidate**. No public release URL is asserted for it. Use the exact candidate ZIP and checksum supplied by the maintainer, or build a reviewed checkout using [distribution maintenance](docs/distribution.md). An earlier public beta is not a substitute for this edition. See [candidate scope](docs/beta-status.md).

## Give this to your assistant

> Use this Rewired OS candidate package. Follow INSTALL.md, then help me get started.

Identify the actual supplied ZIP and its checksum. Check file access, install into a new folder, and follow START-HERE.md. Do not guess a download URL from the version number. If no package is available, build only from an identified reviewed checkout or report the missing input. A source clone has no generated installation receipt.

Once the installed folder is open in a host that loads workspace guidance, “Let's get started” or “Let's go” starts setup. Other hosts need an explicit reference to START-HERE.md. A chat attachment is a snapshot, not write access to its original.

## Choose the route that works here

| Your assistant can… | Setup route |
|---|---|
| Read and write local files and execute commands | Use the verified release and installer below, or extract into a new folder. |
| Read and write local files without execution | You extract the ZIP into a new folder, then give the assistant access. |
| Read or write cloud files through a connector | Extract locally, sync the folder, then verify access to the same canonical files. Connector capabilities vary. |
| Only chat or read uploaded attachments | Extract the ZIP yourself. Upload selected files as snapshots for help; changes must be saved back explicitly. Do not claim the original folder was updated. |

The readable OS needs no Git, GitHub account, Python, or vendor subscription. The optional checked installer and updater require Python 3.10+ on a local filesystem. They install no dependencies. Do not install a runtime or change machine settings implicitly.

## The simple folder route

1. Obtain the ZIP and SHA-256 value from the intended maintainer/release. Compare the downloaded file's checksum when tooling is available. A checksum from the same untrusted source does not establish authenticity.
2. Extract into a **new location**. The ZIP contains one `Rewired-OS` folder. Never extract over an existing OS or merge folders.
3. Move/rename the complete extracted folder to your preferred location. Keep hidden folders, including `.rewired`, `.agents`, and `.claude`. `.rewired/installed.json` records the original stock version and hashes for future updates.
4. Choose a laptop folder or a downloaded, synchronized folder. Confirm cloud files are available locally before using local helpers.
5. Open that folder with your assistant and say: **Let's get started.** If the host does not automatically load the folder's guidance, ask it to read START-HERE.md once.

Keep the original ZIP and its checksum outside the working OS. No repository, account connection, telemetry, or scheduled job is created by extraction.

## Checked installation for a local agent

Read the instructions and obtain the helper from the trusted package first. Run it from the extracted stock folder, with the ZIP kept separately. Replace the sample names and use quoted absolute paths for paths containing spaces:

```sh
python3 scripts/distribution.py install --package "/path/to/rewired-os-0.6.0-beta.1.zip" --destination "/path/to/My Rewired OS" --sha256 "EXPECTED_SHA256"
```

The destination's parent must exist; the destination must not exist, even as an empty folder. The helper validates the inventory and hashes, rejects unsafe archive paths and symlinks, stages the files, and installs the complete folder. A failed validation creates no destination. Do not pass the literal placeholder checksum; use the supplied 64-character digest.

For Windows, use the available Python 3.10+ launcher and native quoted paths. Windows and cloud-provider pilots remain pending; no platform support is inferred merely from portable code.

## Assistant: guide personalization

- Identify the intended folder and actual read/write access, then read START-HERE.md and the canonical AGENTS.md.
- Follow Get started (`first-win` internally): one focused question at a time, suggested answers/examples, and free response/skip. Learn about personal life, work, or both as the user chooses.
- Offer a website or public profile as a shortcut when work context is relevant. Read only accessible selected pages, label claims, link sources, and ask the user to confirm. Use pasted text or a brief explanation if browsing is unavailable or a social platform blocks access.
- Save confirmed context and a small resumable setup record. Respect existing files. Confirm saved content by reading it back. Do not claim persistence with read-only access.
- Offer assistance preferences and relevant routines during setup. GTM guidance is optional; no schedules, vendor tools, or accounts are enabled implicitly.
- Recap the personalization for the user to accept or correct. Then offer a real task, optional demo, or stop for now. The fictional call must never run merely because setup began.

Already have an OS? Keep it intact. Install Rewired in a fresh folder, then move only selected information through the normal source-preserving workflow. This preview does not infer an old installation's version or replace an existing operating manual.

For later releases, use [safe updates](UPDATE.md). For file-provider and host limits, use [portability](docs/portability.md).
