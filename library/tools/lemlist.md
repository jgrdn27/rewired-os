# lemlist

Use for a selected outreach workflow: campaign preparation, grounded drafting, and reviewing results. Prefer the user's existing sequencer if it already meets the need. Start with [prepare and learn](../playbooks/prepare-and-learn.md).

Status: official documentation and public skill source reviewed 2026-10-05. Installation, authentication, account entitlement, and live operations are untested in this preview. Read [the execution contract](../execution.md) before setup.

## Choose an access route

The [official CLI guide](https://developer.lemlist.com/cli/overview) documents Node 20+, installation with `npm install -g @lemlist-official/cli`, browser sign-in with `lemlist auth login`, and endpoint discovery through `lemlist endpoints`. For a local assistant, inspect existing installation and current help before using that route. Global installation is a host change, not something library activation performs.

A host supporting authenticated remote MCP can instead use `https://app.lemlist.com/mcp`. The [official MCP setup guide](https://help.lemlist.com/en/articles/13728466-set-up-the-lemlist-mcp-server-in-your-llm-client-oauth-or-api-key) describes OAuth and API-key options. Use the host's supported connection flow; do not transplant a Claude-specific command into another app.

## First useful verification

After the requested setup and secure sign-in, confirm the intended account. Inspect `lemlist campaigns list --help`, then use a bounded campaign-list read if supported, or the equivalent discovered MCP read tool. An empty successful list can verify access, but not campaign writing or sending. If identity is not returned, leave account identity unverified until established.

Inspect the [MCP tool reference](https://help.lemlist.com/en/articles/15565943-lemlist-mcp-full-tools-reference) or live CLI schema for the requested operation. List, search/enrichment, campaign changes, and launch have different effects. Do not infer that every available read is free or every mutation is authorized. Check entitlement, rate limits, cost, and destination before acting.

## Optional vendor skills

The [official collection](https://github.com/l3mpire/claude-skills/tree/f3a97eae61b12b77d09a72d605087f76f8e19ba3) was reviewed at `f3a97eae61b12b77d09a72d605087f76f8e19ba3`. Its installer targets Claude skills, defaults to a global location, and supports selected project-local skills with `--project`. Rewired does not install the whole collection. Select only relevant skills after checking compatibility, destination, and existing files; avoid blanket overwrite flags.

README and package metadata declare MIT, but no standalone license file was found at that revision. Rewired bundles only its own instructions and links. Obtain the complete applicable notice before redistributing vendor material. No cross-host skill compatibility is claimed from the collection's existence alone.

## Recovery and continuation

On an expired session, use the documented sign-in flow. On a timeout after a campaign mutation, inspect the campaign before retrying; do not create duplicate contacts or drafts. Preserve a campaign ID, dated result, and next step in the work record. Use source-backed observations, not vendor performance promises, when assessing results.
