---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
license: MIT
metadata:
  the-thing.legacy.argument-hint: What will the next session be used for?
  the-thing.legacy.disable-model-invocation: 'true'
  the-thing.invocation: explicit
  the-thing.category: handoff-retrospective
  the-thing.source: https://github.com/mattpocock/skills
---
> Invocation: use this workflow when the user explicitly requests it. This is an instruction-level rule; host enforcement is tool-specific.
Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Host adaptation

`Skill` tool calls in this workflow mean loading the named skill's `SKILL.md` and following it. If the host has no such tool, locate the installed skill directory and read the file directly. A tool name in prose does not grant missing capabilities or permissions; report a missing required capability rather than claiming that step ran.
