---
name: save-playbook
description: Capture a process the user wants to repeat as their own reusable playbook, grounded in the work actually done. Use for requests such as save this way of working or turn this process into a playbook.
---

# Keep a useful way of working

Read `work/index.md`, the relevant project and artifacts, and `docs/playbooks.md` from the Rewired root. Use the current conversation as supporting evidence when available. Recover the actual inputs, decisions, useful outputs, and checks. Distinguish steps that worked from untested suggestions and unfinished parts.

Check for an existing method serving the same outcome. A request to save the current process authorizes creating a local method; it does not necessarily authorize replacing another method. Reuse or narrowly update an existing method when that intent is clear. Otherwise create a distinct draft without overwriting prior work. Do not require another confirmation for an already requested save.

Write a concise method using `templates/playbook.md` where useful. Generalize the repeatable decisions and checks, keeping task-specific names, dates, account identifiers, credentials, and approval grants in the run. Preserve important constraints as rules or named inputs. Identify any required tool capability without assuming the next user has the same product or account. A method may describe untested later checkpoints, but label those as proposed rather than validated practice.

Save user-owned methods under `work/<project>/playbook.md`, `work/methods/<name>.md`, or the user's existing location. Link the method from its project or, for shared methods, from a small method section in `work/index.md`. Add a dated note describing what work supports the method and what remains untested. Use actual references without copying the whole source conversation.

Check that another assistant can identify when to use it, its required inputs, useful checkpoints, and completion evidence. Resolve the saved links and read back the method. Report what was saved and any untested portions. With no write access, return an explicitly unsaved method. This creates portable guidance; it does not install native skills, enable routines, or execute another run.
