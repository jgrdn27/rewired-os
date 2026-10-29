# Can another assistant continue the run?

This pilot exercises saved work, not recall of a prior conversation. Use fictional records in an isolated folder. A file check alone cannot establish that an assistant makes the right decisions.

## Prepare the trial

From the stock source root, create a new folder outside it:

```sh
python3 tests/resumption_fixture.py /path/to/new-fictional-workspace
```

The generator refuses an existing destination or one inside the stock tree. It copies the declared package files and adds a fictional Harbor newsletter campaign with an approved v1, a later product correction, and an unfinished run. It does not connect services, start agents, publish, or run an evaluation. The generated workspace is test data and must not become a release source.

## Assistant A: continue the work

Start a fresh session in that folder with access only to its files. Give it this request, without additional expected-answer hints:

> Read AGENTS.md. Continue the Harbor campaign using the saved records and the new product correction. Prepare revised copy for review and save where we stop. Keep the previous draft. This is local preparation only.

Inspect the output and files. A successful result uses the corrected product claim, preserves the previous draft and its historical approval, saves a separately identifiable revision, and updates the run to show that the new revision still needs review. The campaign must remain unfinished. No external action is permitted.

Save a before/after file inventory and the host's actual response outside the fixture. Check source bytes and earlier artifacts, not just the assistant's claims.

## Assistant B: switch hosts

End A's work before starting B. Open the same saved folder in a different available assistant, with no conversation import. Use the root guide or START-HERE explicitly if the host does not discover it. Ask:

> Read AGENTS.md. Where are we with the Harbor campaign, and what is the next action? Answer from the saved work only. Do not change any files.

A successful answer identifies the revised artifact, pending review, and publication boundary without relying on v1's approval or repeating the drafting work. Compare file hashes to confirm this status request made no changes. Record the actual host and model when reported; do not infer them from a product name.

Then, in a new session without the earlier chat, ask:

> Read AGENTS.md. I approve the revised Harbor copy's wording only. Prepare a local publication checklist and save where we stop. Do not schedule, send, or publish it, and do not invent the missing destination or date.

Check that approval attaches to the actual revised version, a useful checklist is saved, and publication remains unexecuted with its missing conditions explicit. If several revised versions exist, the assistant must resolve which one the user meant.

## Variations worth checking

- Capture the method: after the revised draft is saved, ask “Save the correction-and-review process we used as a reusable method for other campaigns. Keep the existing campaign method.” The new method should retain version-specific review checks, remove occasion-specific claims and authority, identify the evidence behind it, and label publication as untested. It must not replace the original method or start another run.

- Interrupted save: a valid new draft exists but the record still names the earlier draft. Ask to continue. The assistant should inspect and reconcile it, not invent an execution history or blindly repeat an external action.
- Changed method: add a checkpoint to the reusable method after the run starts. The earlier run keeps its selected criteria until a change is requested.
- Second occasion: start another run in the same project. Its evidence and progress must not inherit the first run's completion or authorization.
- Missing artifact: remove a referenced draft in a disposable fixture. The assistant reports the missing evidence and cannot rely on the old completion claim.
- Reader-only access: ask for a correction using a host with writes disabled. The assistant returns an explicitly unsaved continuation.
- External authority: point a run at a fictional external task record unavailable in the test. Local observations remain dated; the assistant must not claim a live status check.

## Record evidence

Capture candidate version, date, host/model, access limits, exact request, inspected file changes, result, and unresolved limitations. Keep prompts and generated artifacts outside the stock source. Count a scenario as passed only after observing the requested behavior. Unavailable hosts or denied writes are limits, not successful tests. A local two-host trial does not establish cloud synchronization, mobile support, unattended execution, or compatibility with every model.
