---
name: claude-handoff
description: Hand the current conversation off to a fresh background agent that picks up the work immediately.
compatibility: Claude Code CLI with background-agent support; otherwise produce a handoff document and report that
  launch is unavailable.
license: MIT
metadata:
  the-thing.legacy.argument-hint: What will the next session be used for?
  the-thing.legacy.disable-model-invocation: 'true'
  the-thing.invocation: explicit
  the-thing.category: handoff-retrospective
  the-thing.source: https://github.com/mattpocock/skills
---
> Invocation: use this workflow when the user explicitly requests it. This is an instruction-level rule; host enforcement is tool-specific.
Write a handoff summary of the current conversation so a fresh agent can continue the work. Save it to the temporary directory of the user's OS, then launch a background agent seeded with it as its prompt: `claude --bg --name "<descriptive name>" -- "$(cat <summary file>)"`. Passing the file keeps the shell from running backticks or expanding `$` in the summary. It starts in the current working directory and returns immediately; the user manages it with `claude agents`.

Always pass `-n`/`--name` with a descriptive name (e.g. `--name "Fix login bug"`); it sets the display name shown in the job list, session picker, and terminal title.

Include a "suggested skills" section in the summary, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information, since the summary becomes the agent's prompt.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the summary accordingly.

## Host adaptation

`Skill` tool calls in this workflow mean loading the named skill's `SKILL.md` and following it. If the host has no such tool, locate the installed skill directory and read the file directly. A tool name in prose does not grant missing capabilities or permissions; report a missing required capability rather than claiming that step ran.
