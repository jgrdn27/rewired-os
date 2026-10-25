# Keep Rewired OS up to date

Ask your assistant: **Check this Rewired release and show me what would change in my OS.**

Updates run on request. The local helper accepts a supplied ZIP; it does not fetch releases or run in the background. Ask a capable agent to check the [official releases](https://github.com/jgrdn27/rewired-os/releases), or download a selected release yourself. Read its release notes and checksum before following the preview/apply steps below.

## What belongs to you

| Files | Update behavior |
|---|---|
| `context/`, `wiki/`, `raw/`, `work/`, `preferences.json`, `connections.md`, `decisions.md` | Seeded on fresh install only. Never replaced, deleted, or recreated by an update. Future additions to these areas require an explicit migration. |
| Your extra files, `.state/`, `library/custom/` | Outside the stock update inventory. Left alone. |
| Shipped workflows, guides, scripts, templates, examples, and root operating instructions | Updated only where the upstream file changed and the local file still matches its recorded original, or already matches the new release. |
| Your edits/deletions to a shipped file | Preserved when upstream did not change it. If upstream also changes it, the entire update stops and lists the conflict. |

`.rewired/installed.json` stores the current release's stock baseline, not a hash inventory of your personal files. Do not edit it to force an update. Retain `.rewired/` when moving the OS.

## Preview, then apply

1. Obtain the intended newer release ZIP and checksum from the trusted release source. Read its [change notes](CHANGELOG.md) from the new package. Use the already installed updater for compatible releases. Keep a trusted copy of the helper and ZIP outside the OS for recovery.
2. Finish other agent work. Use one writer and wait for file sync to settle. Local locks cannot coordinate other devices or all editors. Do not update a cloud-only folder through this helper.
3. From your OS folder, preview the update. This command does not write files:

```sh
python3 scripts/distribution.py update --root "/path/to/My Rewired OS" --package "/path/to/new-release.zip" --sha256 "EXPECTED_SHA256"
```

4. Explain the version change, changed paths, preserved user files, and any conflicts. `can_apply: true` means the file checks pass, not that the new workflows have been independently tested. A preview request alone does not authorize applying changes. When the user requested the update, continue within that authorization after reviewing the result; otherwise present the preview.
5. Apply the same package and checksum when authorized:

```sh
python3 scripts/distribution.py update --root "/path/to/My Rewired OS" --package "/path/to/new-release.zip" --sha256 "EXPECTED_SHA256" --apply
```

The helper rechecks files under a local lock, saves the affected product files and old version receipt, writes a recovery journal, and applies the update. It returns a backup transaction ID. No personal-folder backup is needed for the updater's writes because it never writes there; the update backup is **not a general backup of your OS**. Maintain your usual data backup separately.

Restart/reopen the assistant session after an update so it reloads guidance. Read `START-HERE.md`, resume a known project, and check that the user's preferences and links still work. Only report an update as complete after the command succeeds and the relevant post-update check passes.

## If there is a conflict

No update files are applied. Keep using the existing version. Show the locally edited file and the incoming version side by side and identify the useful custom behavior to preserve. Never reset the file, replace the baseline receipt, or use `git pull` as a shortcut.

For this preview there is no automatic merge or force flag. A maintainer or capable agent can propose an explicit reconciliation with the user's custom content preserved separately, then rerun the preview. Do not automatically run skill synchronization to overwrite locally edited mirrors. If reconciliation is unclear, defer the update.

A new release with a required schema/data migration must ship migration instructions and receive separate testing. This updater does not migrate personal state or guarantee compatibility with arbitrary future helper versions.

## Undo or recover

To undo a completed update, use the transaction ID returned by the apply command:

```sh
python3 scripts/distribution.py restore --root "/path/to/My Rewired OS" --transaction "BACKUP_TRANSACTION_ID"
```

An interrupted apply leaves `.rewired/pending.json`. Finish/stop the interrupted process and recover it with:

```sh
python3 scripts/distribution.py restore --root "/path/to/My Rewired OS"
```

If a killed process left the update lock, first verify that no updater or writer is still running. Then add `--recover-lock` to the restore command. This flag is an explicit stale-lock override; never use it to bypass an active writer. If the process died before it created a pending journal, no product writes started: after checking the process is gone, remove only the stale `.rewired/update.lock` and retry the preview.

Restore checks the backup hashes and current files before writing. If a file was edited after the update, restore stops rather than deleting those edits. Preserve that work and reconcile it first. Restore multiple updates in reverse order. Keep backup directories until satisfied with the new release; there is no automatic pruning.

An interruption during restore can also be recovered with the same command. Backups and pending state must remain together with the folder. Filesystem failures, manual deletion of backups, and simultaneous cloud writes are outside the guarantees of the local helper.
