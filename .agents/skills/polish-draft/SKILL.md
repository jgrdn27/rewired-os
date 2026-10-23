---
name: polish-draft
description: Edit a supplied draft for clarity, the user's voice, and its intended channel while preserving factual meaning. Use when the user asks to polish, tighten, humanize, or match their voice; do not run on every answer, rewrite raw evidence, or assume sending permission.
---

# Polish a draft

Resolve OS paths from the root containing `AGENTS.md` and `START-HERE.md`. This is optional editing for a selected draft, independent of GTM Library activation. Load only the draft and relevant voice guidance; never run a whole-library style pass on ordinary responses.

Establish the audience, channel, and desired change from the request. Read `context/index.md` and its voice route if relevant. Use the user's explicit instructions first, then approved samples for this channel, then patterns supported by the draft. If no voice evidence exists, use clear neutral prose or preserve the draft's register; do not claim a personal voice match. Ask for a sample only when needed for the requested outcome. A missing sample should not block a straightforward clarity edit.

Read `docs/editing.md`. Make one focused revision, then compare it against the source for factual preservation. Resolve an ambiguity that could change meaning before rewriting it; leave nonblocking uncertainty intact. Keep direct quotations, numbers, conditions, citations, and material caveats. Do not invent personal experience, emotions, customer proof, performance claims, or urgency to sound human.

Return the revised draft with a brief note only for material changes or unresolved questions. Honor requested length/format without silently dropping essential information; flag an impossible constraint. Edit a file in place when requested, preserving its intentional structure and unrelated content. Otherwise return the draft in chat or the requested destination. Raw originals in `raw/` remain unchanged.

Save a reusable voice profile only when the user asks to establish or update it, using `templates/voice.md` and linking it from `context/index.md`. One accepted edit does not establish a universal rule. A draft/edit request does not authorize publishing or sending, even when the relevant tool is connected.
