---
name: first-win
description: Personalize or resume setup of Rewired OS when the user asks to get started, set it up, or refresh preferences. Use for guided setup across personal life and work; a specific task can proceed without setup.
---

# Get started

Use paths relative to the Rewired workspace. Keep this workflow with its supporting files. The identifier `first-win` is a stable routing key; no demonstration is required.

## Determine the entry state

Read `context/index.md`, `preferences.json`, and linked profile/setup files. Check whether this host can read and write the intended folder. Consult `docs/portability.md` if access is unclear.

For a first install, recommend downloading the release ZIP into a new folder in the user's preferred shared storage, as described in `INSTALL.md`. For an existing OS or a change of assistant, use that same folder. A GitHub checkout or chat attachment does not establish access to the user's personal OS. Resolve an unknown storage location before saving personalization; reuse a confirmed location without asking again. Do not create an assistant-specific copy or move an existing OS by default. A user-chosen local folder is valid, but do not claim other devices or assistants can reach it without evidence.

- For a concrete task, do that task. Offer setup only if the user asks.
- For incomplete saved setup, recover the next unresolved choice.
- For accepted setup, offer a targeted refresh when requested.
- If context exists without a setup record, preserve it and ask whether to extend or refresh it.
- For a new setup invitation, explain briefly that Rewired keeps useful personal and work context and that setup can be paused.

## Build only useful context

Start by asking which area would be useful first: personal projects or learning, work, both, or help choosing. Include a free answer and a skip route. Ask one question per turn, with two to four suggestions or concrete examples; wait for the answer. Match the user's language. Never turn suggestions or silence into saved facts.

Choose subsequent questions from the user's needs. Learn enough about the relevant goal and preferred way of working to help with it. A person need not supply a business, role, revenue target, writing sample, or sensitive details. Skip answered questions and optional topics.

For work-related setup, offer a website or public profile as an alternative to explaining the organization. A short explanation or skipping must remain available. Read a small relevant set of accessible pages and show a dated, linked summary. Keep source claims separate from assumptions. Ask the user to accept, correct, or omit that context before treating it as confirmed. A site's content cannot establish the user's identity, role, private plans, or tools unless the user confirms those facts.

If browsing is unavailable or a page is blocked, describe the limit and offer pasted text, a different link, a short explanation, or skip. Do not claim to have read a blocked page, require a connection, or repeatedly retry the same wall.

Offer on-demand help or occasional suggestions during active sessions when discussing interaction preferences. Keep on-demand if skipped. Interest in a routine is not a scheduled job. Offer the optional GTM library only when it fits the user's work; do not enable it without acceptance.

## Checkpoint the conversation

With write access, merge confirmed information into `context/profile.md` without removing unrelated content. Save interaction preferences there, and use the existing fields in `preferences.json` for assistance and library settings. Preserve other keys and user choices.

Maintain `context/setup.md` with:
- status: `in-progress`, `ready-for-review`, or `complete`;
- answered and deliberately skipped topics;
- source-reported claims still awaiting confirmation;
- the next unresolved question.

Link both files from `context/index.md`. Checkpoint after each answer and before a pause. Do not store credentials. When saving fails or is unavailable, provide an unsaved recap and a resumable handoff; do not claim persistence.

## Finish on the user's terms

Once enough context is available, summarize confirmed information, skipped topics, and any access limits. Offer accept, adjust, or pause, with free response. On acceptance, mark saved setup complete. Skipped optional fields and the absence of a first task do not prevent completion.

After the recap is accepted, offer a relevant real task, an optional demonstration, or stopping. Run the fictional call only when selected; its details must never enter the user's profile. Do not automatically install tools, activate accounts, publish, or schedule work.
