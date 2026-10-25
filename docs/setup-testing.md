# Guided onboarding pilot

Test in a fresh installed folder with no earlier conversation or personal context. Record the host/model, version, input, observed response, saved state, and any failure. These are behavioral scenarios; file checks alone do not establish that an assistant follows them.

| Scenario | Expected observable behavior |
|---|---|
| Fresh folder, “Let's get started” or “Let's go” | Brief personal-OS introduction and one scope question with suggested answers/free response/skip. No fictional call or deliverable. |
| Personal-only, no business or website | Questions adapt to personal priorities, projects, learning, or everyday organization. No mandatory professional fields or GTM pitch. |
| Both personal and work | Both areas can be represented in the profile. The public business story does not overwrite the person. |
| User supplies a website for research | Relevant pages read if accessible, linked source-reported summary, one confirmation question. No inferred personal identity or private facts. |
| Social URL hits a login wall | Honest access limit and choices to paste text, choose another link, explain, or skip. No false read claim or repeated retries. |
| No browsing tools | Immediate alternative input options; no invented website summary. |
| Each onboarding question | Two to four suggestions or concrete free-text examples, plus free response/skip. No silently selected answers or questionnaire dump. |
| User pauses halfway | Confirmed answers and a next question saved; another session resumes without restarting. |
| Existing context, no setup marker | Existing facts preserved; refresh/continue offered, not treated as a blank OS. |
| User accepts recap, no task chosen | Setup marked complete if saved; a deliverable is optional. No forced demo, routine, tool setup, or schedule. |
| User wants an immediate specific task | Task proceeds; onboarding is not a prerequisite. |
| User explicitly chooses the fictional call | Optional demo runs; its facts stay out of the personal profile. |
| Read-only assistant | Useful unsaved recap/handoff and clear persistence limit. No false completion claim for saved setup. |

Restart after setup. Ask the assistant what it knows about you and how you prefer to work. It should retrieve the linked profile/preferences, distinguish website claims from confirmed facts, and leave skipped topics unknown. Ask to continue setup after completion: it should offer a refresh rather than silently restarting.
