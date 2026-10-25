# Clay

Use for research, enrichment orchestration, and repeatable GTM data work when that scope justifies the platform. Start with [choose a target](../playbooks/choose-a-target.md) or [enrich a useful sample](../playbooks/enrich-a-sample.md). A small existing list may need neither a new workflow nor another tool.

Status: official documentation and public plugin source reviewed 2026-10-05. No installation, sign-in, paid run, or account entitlement was tested. Read [the execution contract](../execution.md) before setup.

## Setup and first probe

The reviewed [getting-started guide](https://github.com/clay-run/agent-plugins/blob/802a1ab5ee6e76e039c75c98e2fde0429a968472/GETTING_STARTED.md) provides host-specific plugin routes and a setup workflow for the separate CLI. It supports a native executable or an npm route. Review the current setup source and installed state before executing anything. A user does not need GitHub to use the Rewired folder; a vendor adapter may still download its software from an official repository.

Use current documented sign-in, then `clay whoami` to check the intended account/workspace. Read the live help before task execution. A successful identity probe verifies sign-in, not every API capability.

## Material boundaries

The detailed [Clay API and CLI documentation](https://university.clay.com/docs/clay-api-cli) states:

- The plugin supplies CLI/skills; MCP for Reps is a separate connection.
- Windows CLI use requires WSL; macOS/Linux have native routes.
- Developer platform access spans plans, but entitlements and limits differ.
- Tables API is read-only; advanced table queries require Enterprise table sync.
- Workflows CLI is beta. Evaluate the documented stable primitive for production work.
- Usage consumes normal platform credits/actions; developer credit budgets are not currently provided as a hard cap.
- Sequencer launch/pause/resume remains in the Clay app.

Recheck these limits at use time. Do not promise table writes, automatic campaign launch, or a vendor-enforced spending ceiling based on a general integration claim.

## Plugin hooks and provenance

Source reviewed at [commit 802a1ab](https://github.com/clay-run/agent-plugins/tree/802a1ab5ee6e76e039c75c98e2fde0429a968472). The [CLI approval hook](https://github.com/clay-run/agent-plugins/blob/802a1ab5ee6e76e039c75c98e2fde0429a968472/clay/hooks/approve-cli.sh) automatically approves many Clay commands while gating certain credential/billing operations. Inspect host-specific hook configuration during setup. Hook permission is not user authorization for paid jobs or external writes. Prefer a documented CLI-only route when the plugin's broader behavior is unnecessary; do not silently weaken host policy.

No license file was found in the reviewed public repository. Rewired links to official setup and includes original guidance; it does not redistribute Clay plugin code or skill text. Resolve redistribution terms before any future bundling. Public availability alone is not a redistribution license.

## Recovery and continuation

Keep run IDs and a bounded work scope. After a timeout, inspect the existing run before creating another one. Store bulky result tables outside general conversation context and link the relevant findings. If a required action is unsupported through the selected API, prepare an app handoff and state the limit instead of claiming completion.
