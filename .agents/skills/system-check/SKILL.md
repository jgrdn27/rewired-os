---
name: system-check
description: Check OS retrieval, ingestion health, source integrity, freshness evidence, skill routes, and evidence of useful execution. Use for health reviews or a suspected failure; this checks the system without automatically repairing it.
---

# System check

These are project workflows. Resolve paths from the OS workspace root containing `AGENTS.md` and `START-HERE.md`; do not install this skill alone.

When local execution is available, run `python3 scripts/knowledge.py check` and read its precise scope. Otherwise inspect accessible routes manually and label source hash/registry checks unverified. For intake or freshness questions, also read `docs/ingestion-health.md` and run `python3 scripts/knowledge.py health` when available. Use an event-date cutoff only for a requested, scoped review. Report local attempts separately from actual connector evidence in `connections.md`; no log or run evidence means unverified. Do not interpret ingestion timestamps or file dates as verified current facts. Inspect the relevant manual/index routes and one real priority-related retrieval chain. For a deeper requested check, sample source access, work continuation, and any enabled routine with available run evidence.

Report each area as working, needs attention, or unverified, with the exact source/check and its limitation. Separate a failed operation from a missing test. The absence of user data in a fresh installation is expected. There is no numeric score, stage ladder, or required tool count.

For a project check, use the fresh-reader questions in `docs/projects.md` and distinguish your manual review from an independent session test. Check whether a fresh session can reach a deliverable and a next step; whether source summaries resolve to originals; whether conflicting or dated claims are labeled; and whether an allegedly running routine has an actual due result. A configured connection is not authenticated access. Do not perform live writes just to prove capability.

For a model/device change, verify access to the same identified folder and one source-backed resume point using `docs/portability.md`. If the GTM Library is enabled, inspect only relevant connection evidence; listing, installation, authentication, and tested action are distinct states. Do not install or authenticate merely to finish a health check.

Rank at most three consequential findings. Each gets a practical consequence, a specific repair or verification step, and a completion check. Never invent problems to fill the list. A requested fix can be handled afterward within its own scope.

Default output is a concise chat report. If the user requested a durable report, save a unique dated file under `reviews/` and link it. Do not edit sources, install software, change schedules, or publish during the check.
