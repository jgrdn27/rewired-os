# Claap

Rewired's default recommendation for meeting recording and reusable meeting knowledge. Included guidance does not mean an account is connected or meetings are being recorded. Use [turn a meeting into useful knowledge](../playbooks/meeting-to-knowledge.md). A user's chosen recorder takes precedence through [tool choice](../tool-choice.md).

Status: official documentation reviewed 2026-10-05. No live account, recording, transcript retrieval, or host integration tested. Read [the execution contract](../execution.md) before setup.

## Capture and retrieve are separate setup steps

For recording setup, inspect the user's existing calendar connection and preferences. Claap documents Google/Outlook calendar connections and configurable meeting selection, recap sharing, and processing in [meeting preferences](https://help.claap.io/en/articles/10149930-how-to-set-your-meeting-preferences). Its [bot guide](https://help.claap.io/en/articles/10502268-using-the-claap-bot-recorder) explains admission and one-off recording. Configure only the requested meeting scope and sharing behavior; do not enable recording of every meeting or automatic participant emails merely to connect the OS. Observe the user's meeting recording policy and participant notification practices.

For retrieving existing meeting knowledge, the [official MCP guide](https://help.claap.io/en/articles/11786373-use-claap-mcp-server-for-advanced-workflows) documents `https://api.claap.io/mcp`, OAuth by default, and API-key authentication as an alternative. Use the current host's supported connection flow. Inspect discovered tools, list accessible workspaces, select the intended workspace, then read a bounded recording list and one user-selected transcript. Keep recording/search/summary access and full-transcript access as separately verified capabilities. MCP also exposes writes; reading meetings does not authorize those actions. The guide restricts retrievable recordings by workspace/folder visibility, so missing results do not establish that no meeting exists.

## Alternatives and prerequisites

The [API overview](https://help.claap.io/en/articles/11833785-claap-api-overview) covers recordings and transcripts, with API-key management restricted to workspace Admins/Owners. Its access rules exclude private recordings unavailable to workspace search. Recheck the [current plan information](https://www.claap.io/product/mcp-api): the researched page lists MCP across plans and the API on Enterprise. Verify actual entitlement before choosing the API route; do not infer it from a successful MCP connection.

If a connector is unavailable, Claap's [meeting-page guide](https://help.claap.io/en/articles/16600260-what-you-can-do-with-a-claap-meeting) documents **Copy transcript**. Save the authorized export with its meeting URL, date, speakers where supplied, and coverage. Label an AI summary as a summary, not a transcript. A manual export can support the same knowledge workflow while automated access remains unverified.

## Useful verification and recovery

A read test should answer one factual question about a selected meeting with an attributable passage or timestamp. A login alone is insufficient. If processing is incomplete or a recording is inaccessible, report that state; do not broaden sharing settings to make the test pass. Keep the recording ID and observed revision/content hash to avoid duplicate ingestion; preserve a corrected transcript as a new source version.

Meeting content flows through the normal raw → wiki → work process. Do not send follow-ups, update CRM records, publish recordings, or configure background imports under a retrieval request. Record the successful route and limits in `connections.md`.

This profile is original Rewired guidance based on official documentation. No first-party Claap CLI or distributable skill repository was verified in this research; no vendor code or skill text is bundled.
