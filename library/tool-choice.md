# Keep the method, choose the tool

The library is organized by GTM use case. `catalog.json` supplies a default recommendation and a reusable playbook for each one. Defaults reduce setup effort; they do not override the user's stack.

## Resolve the user's choice

Use the exact tool requested for the current task first, then a saved preference for this use case and business scope, then a suitable existing verified connection. Offer the catalog default when no preference or usable connection is known. Do not force a migration, require a listed vendor, or install two competing tools for one outcome.

When the user says to use a tool going forward, save an entry in `preferences.json` under `libraries.gtm.tool_overrides`, keyed by the use-case ID. Preserve unrelated preferences. The entry holds `tool`, `profile` (a root-relative path), and `business_scope` (the user's supplied scope, or null if general). A one-off request does not silently change the persistent default. Authentication/capability evidence belongs in `connections.md`, not in the preference.

Stock use-case IDs are `meeting-recording`, `account-research`, `contact-enrichment`, and `outreach`. A user's custom tool need not already appear in the stock catalog. If business scopes differ, keep the preference confined to its recorded scope and use the intended connection for the current task; do not assume one account serves every activity.

## Research an unlisted or stale tool

1. Identify the exact product and official website; disambiguate only when needed. Read the use-case playbook and identify the capabilities this task requires.
2. Inspect current primary sources for available connectors, MCP, CLI, API, or export paths; host/plan requirements; authentication; permissions; costs; retrieval/write limits; and failure behavior. Search for official skills if useful. Do not invent an installer or infer feature parity from the vendor category.
3. Map the required outcome to supported capabilities. For a recorder, separately assess capture, meeting discovery, transcript access, speaker/timestamp fidelity, and export. For other categories, map the corresponding inputs, outputs, costs, and mutations. State gaps concretely.
4. Create original guidance using [the tool-profile template](../templates/tool-profile.md). Save it under `library/custom/<tool-slug>.md` only when the request calls for persistent setup or a saved preference; keep one-off research in the task otherwise. Record official URLs, check date, evidence level, and any reviewed source revision. Do not fabricate a commit for a documentation-only review. Link the custom profile from the saved preference or `connections.md` so it can be found later.
5. Continue through [the execution contract](execution.md): inspect existing setup, use an appropriate verified route, secure sign-in, and perform a bounded useful probe. Existing authorization carries forward. Record unsupported capabilities rather than pretending the recommended tool's commands also work here.

If no integration is available, use a documented export/manual route when it satisfies the task. If information cannot be verified online, keep the route unverified and request only the missing official reference or needed input. Do not fall back to the default vendor or buy a higher plan without the user's choice.

The result is the same kind of work artifact and evidence, with honest differences in automation. Custom profiles are private installation data and excluded from the stock release manifest. They do not become public recommendations or sponsored listings. Deactivating a library or selecting another tool does not revoke accounts, migrate historical data, or delete existing sources.
