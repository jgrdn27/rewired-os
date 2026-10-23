# FullEnrich

Use when a defined task requires missing contact or company information. Start with [enrich a useful sample](../playbooks/enrich-a-sample.md); reuse existing verified data and avoid paying twice for overlapping enrichment routes.

Status: official documentation and public skill source reviewed 2026-10-05. Live account behavior and plan entitlement remain untested. Read [the execution contract](../execution.md) before setup.

## Choose an access route

The [official MCP guide](https://help.fullenrich.com/en/articles/14190120-mcp-server) documents `https://mcp.fullenrich.com/mcp` with browser OAuth. It supports search, enrichment, and exports. Use a supported host connection flow. First discover the available tools and request a credit-balance read, without starting an enrichment. Confirm the intended account separately if the result does not identify it.

The guide distinguishes a free search preview from paid exports/enrichment. Check the current operation's cost before expanding a preview; a successful preview does not authorize exporting the complete result. No first-party CLI was verified in this research; do not invent an npm package.

For a host with secure HTTP tooling, [API v2](https://docs.fullenrich.com/api/v2/general/introduction) is another documented route. Its [authentication guide](https://docs.fullenrich.com/api/v2/general/authentication) uses a Bearer API key. Keep it in protected host storage. Use the documented [key-verification endpoint](https://docs.fullenrich.com/api/v2/account/keys/verify/get) or balance read for a probe, and inspect current [rate limits](https://docs.fullenrich.com/api/v2/general/ratelimit) before batch work. This preview does not include an API client.

## Optional vendor skills

The [official skill repository](https://github.com/FullEnrich/fullenrich-skills/tree/5c727120c6ca6ef89d3b17dbd6916b1bee73fdcb) was reviewed at `5c727120c6ca6ef89d3b17dbd6916b1bee73fdcb`. It includes prospecting, CSV enrichment, outreach preparation, and CRM-oriented methods. Its Claude installation uses the marketplace `FullEnrich/fullenrich-skills` and plugin `fullenrich@fullenrich`; use current host-specific instructions for other apps.

The CRM method requires another CRM connection: FullEnrich's MCP does not supply CRM write tools. Do not imply that installing this skill grants CRM access. The repository includes an [MIT license](https://github.com/FullEnrich/fullenrich-skills/blob/5c727120c6ca6ef89d3b17dbd6916b1bee73fdcb/LICENSE); retain its notice if vendor material is redistributed. No vendor skill text is bundled here.

## Recovery and continuation

Map fields and stable record keys before enrichment. Record job identifiers, inspect completion, and reconcile results before retrying after interruption. Keep a separate output with match/verification status and source date; do not replace stronger existing data. API acceptance is not a completed enrichment. Save quality and actual consumption evidence, then recommend whether the selected scope merits expansion.
