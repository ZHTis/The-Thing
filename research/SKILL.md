---
name: research
description: Investigate a question against high-trust primary sources and update the existing related Markdown note
  in place; ask before creating a separate note for a new topic branch. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated
  to a background agent.
compatibility: Primary-source access; background subagent support when research is delegated.
license: MIT
metadata:
  the-thing.category: research-planning
  the-thing.source: https://github.com/mattpocock/skills
---
# Research

Investigate the question against primary sources: official documentation, source code, specifications, papers or first-party APIs. Follow claims to the source that owns them, record versions/dates where relevant, and distinguish facts, estimates and unverified items. Delegated background research uses a fresh-context agent; the same evidence and note policy applies to its output.

## Default note policy

Update Markdown by default, using the existing related note in place. First inspect the project's established note location and the current topic. Preserve useful earlier findings, source links and unresolved questions; reconcile corrections in the relevant section instead of appending duplicate notes. Historical archives remain immutable under the user's archive rules.

When the topic branches enough to merit a separate note, ask whether to create that note before creating it. Offer a title/location and briefly state why it is a separate branch; continue independent research while waiting, keeping the new branch findings in the response rather than writing an unrelated note. If there is no suitable existing note, ask which existing note to use or whether to create the first one. An explicit instruction to create a named note already authorizes that creation and needs no repeated confirmation.

Report the note actually updated and any pending file-creation choice. Do not create a temporary, alternate or worker-owned Markdown note to bypass the user's choice. Research agents should return findings to the parent when the approved destination is unavailable.

## Relation to planning

Use this skill for independent investigation. When findings must become an implementation plan, read `../case-based-planning/SKILL.md` and reuse the verified evidence, then distinguish direct reuse, references, customization and feasibility. Do not make this handoff a reason to create another note; apply the same in-place note policy.
