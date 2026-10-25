# Rewired GTM Library

Optional GTM methods, tool setup guides, and reusable skills. Start with a business outcome, use the user's preferred tools where they fit, and carry the resulting knowledge back into the OS.

The starter includes original Rewired instructions. Third-party skill collections are linked, not copied or installed. No accounts, paid plans, or sponsorships are bundled. Tool documentation was researched on 2026-10-05; no live account connection was tested.

## Activate only what helps

Say **Activate the GTM Library** to enable its guidance. The assistant sets `libraries.gtm.enabled` in `preferences.json`, preserving other settings, then loads the relevant method on demand. An explicit request for one tool can use that profile for the current task without enabling persistent recommendations. Activation alone performs no installation, authentication, or credit-consuming operation.

Say **Set up lemlist for my OS** to start its setup route. The assistant checks the host, existing installation, intended account, current official setup instructions, and a useful read-only probe. It acts within the setup request and only asks for missing material choices or a user-controlled sign-in step. If the host cannot run a CLI, it offers a documented MCP/API route or a precise handoff.

Say **Turn off the GTM Library** to stop its proactive routing by setting the preference to false. This does not uninstall third-party tools, revoke credentials, or stop independently scheduled jobs; those are separate actions.

## Your tool choice comes first

Each GTM use case has a default recommendation. Claap is included as the default meeting recorder. If you prefer another tool for any use case, say so: Rewired researches the exact product, maps its capabilities to the same method, guides setup, and verifies access. It saves the choice when you ask to use it going forward. Read [tool choice and alternative setup](tool-choice.md). Equivalent outcomes are the goal; identical integrations are not assumed.

## Start from the work

| Need | Rewired method | Candidate tool, only if needed |
|---|---|---|
| Capture meeting evidence and continue the work | [Meeting to knowledge](playbooks/meeting-to-knowledge.md) | Claap by default, or your chosen recorder |
| Decide which accounts merit attention | [Choose a target](playbooks/choose-a-target.md) | Existing evidence first; Clay for scalable research |
| Fill missing fields in a selected list | [Enrich a useful sample](playbooks/enrich-a-sample.md) | FullEnrich; existing enrichment workflow if sufficient |
| Prepare a grounded outbound experiment | [Prepare and learn](playbooks/prepare-and-learn.md) | lemlist for campaign preparation and results |

These are original Rewired methods, proposed for pilot validation. They do not promise conversion rates or replace the user's judgment. Avoid requiring multiple tools for a job one existing tool can handle.

## Tool profiles

- [Claap](tools/claap.md): meeting recording setup, MCP/API retrieval, transcript export fallback.
- [lemlist](tools/lemlist.md): outreach workflow, CLI/MCP routes, optional official skills.
- [FullEnrich](tools/fullenrich.md): contact enrichment/search, MCP/API routes, optional official skills.
- [Clay](tools/clay.md): research and enrichment orchestration, plugin/CLI route, separate MCP considerations.

The small [catalog](catalog.json) records where each profile lives and what has been verified. It is stock documentation, not a customer's connection registry. User-specific setup evidence belongs in `connections.md`, using [this template](../templates/tool-connection.md). Read the [execution contract](execution.md) before setup or tool execution and [editorial policy](editorial-policy.md) when selecting or adding listings.
