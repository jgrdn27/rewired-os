# Private distribution pilot

Use disposable folders, fictional evidence, and a package built from the clean starter. Do not test updates on a personal production OS. Keep a record of the package hash, host/model, runtime, OS, date, outcome, and observed failures. Technical tests and conversation pilots are different evidence.

## Local package checks

1. Run the stock checker and all tests. Build the ZIP and compare its SHA-256 with the sidecar.
2. Install into a new folder with spaces in its path. Confirm an existing destination is refused without changes. Separately extract the ZIP with an archive utility and confirm the hidden receipt and skill folders survived.
3. Open the folder with the chosen assistant and say “Let's get started.” Follow the [onboarding scenarios](setup-testing.md), personalize, and confirm the recap. Separately choose a real task or the optional fictional demo. Save a result and next step, then restart and resume from files only.
4. Add fictional personal content, preferences, a custom tool profile, and a modified operating instruction.
5. In a second clean source copy, bump the version and change a managed guide. Build a trial next release, preview, and apply. Confirm every personal byte and the unrelated customized instruction survives.
6. Edit the same managed guide in both the local OS and next release. The preview must list the conflict; apply must refuse the whole update. Do not force a resolution.
7. Restore a successful update. Verify its added files disappear, replaced/deleted files return, and personal changes made after installation survive. Edit an affected product file after updating and confirm restore refuses to discard it.
8. Use the automated failure-injection tests to check interrupted apply/restore, corrupted backups, locks, path traversal, symlinks, invalid hashes, and version ordering. Do not simulate power loss on a real user folder.

Tests create synthetic next versions solely to exercise updater mechanics. They are not product releases or independent assessments of the next version's content.

## Human/agent experience

- Can a new user start with only the package and installation prompt?
- Does a short greeting begin guided personal/work setup with suggested answers, without requiring a business, Git expertise, or the GTM stack?
- Does a read-only assistant clearly state its limits and leave an explicit handoff?
- Does a second assistant retrieve the same project state without relying on chat history?
- Does the assistant explain an update preview clearly and preserve the user's edits?
- For each advertised synced provider, do hidden files, downloaded availability, and same-file identity work? Use one writer; test conflicts separately without promising distributed locking.

Do not mark these conversational or provider checks passed merely because unit tests passed. Record observed results before claiming supported hosts, providers, or a time-to-first-result target.
