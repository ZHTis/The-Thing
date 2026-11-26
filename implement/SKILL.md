---
name: implement
description: Implement a piece of work based on a spec or set of tickets.
license: MIT
metadata:
  the-thing.legacy.disable-model-invocation: 'true'
  the-thing.invocation: explicit
  the-thing.category: coding-architecture
  the-thing.source: https://github.com/mattpocock/skills
---
> Invocation: use this workflow when the user explicitly requests it. This is an instruction-level rule; host enforcement is tool-specific.
Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, call the Skill tool with "code-review" to review the work.

After the relevant checks and review pass, automatically commit only the changes for the actual implement task. Inspect the branch and diff first; preserve unrelated staged and unstaged changes. Invoking implement authorizes this local commit under the user's standing preference, but not a push, merge of unrelated work or issue publication. If checks fail or the result is incomplete, report the gap instead of creating a misleading completion commit.

This exception applies when the user actually activates the implement workflow. Merely mentioning implement while discussing skill preferences, or invoking another skill such as implement-spec, is not that activation. Outside an actual implement workflow, the user decides whether to commit. Push still requires separate explicit authorization.

## Host adaptation

`Skill` tool calls in this workflow mean loading the named skill's `SKILL.md` and following it. If the host has no such tool, locate the installed skill directory and read the file directly. A tool name in prose does not grant missing capabilities or permissions; report a missing required capability rather than claiming that step ran.
