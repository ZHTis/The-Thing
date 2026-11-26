---
name: implement-spec
description: Execute an explicitly requested specification task graph with verification; planning alone does not
  activate execution, and commits, tracker publication and PR changes follow their separate authorization.
compatibility: Git, worktrees, subagents and the project's configured issue tracker; unavailable capabilities must
  be reported.
license: MIT
metadata:
  the-thing.legacy.disable-model-invocation: 'true'
  the-thing.invocation: explicit
  the-thing.category: coding-architecture
  the-thing.source: https://github.com/mattpocock/skills
---
# Implement Spec

Use this workflow only when the user actually requests implementing the specification. A plan, a spec draft or an approved technical design does not start execution. If the current request is planning only, return that draft and the proposed next step without creating branches, launching implementers or posting issues.

## Execution and publication boundaries

Read the spec, task graph and existing authorization. Implementation, local commits, external tracker changes, PR creation, push and merge-to-main are distinct scopes. This skill is implement-spec, not implement: it does not inherit the user's implement-only automatic-commit exception. If a particular task is explicitly run through implement, apply its scoped local-commit rule to that task only. Do not manufacture that activation to bypass a commit restriction or an approval rejection.

Tracker configuration is optional for local execution from an existing task list. Use the actual available tools; report missing required capabilities. Preserve the user's current worktree contents and inspect branch bases; never reset an existing worktree to force the expected base.

## Work the task graph

1. Read the complete spec and ticket dependencies, confirming acceptance criteria and scope from existing artifacts. Work only tickets whose prerequisites are satisfied.
2. Reuse a suitable checkout. For a large task that needs isolation, use suitable worktrees and an integration branch. Read required project facts directly or use an exploration agent when useful; preserve a pointer to findings rather than duplicating them across agents.
3. For independent ready tickets, use fresh-context implementer agents when the host supports them. Each produces scoped changes and test evidence. Use tdd where appropriate and preserve unrelated work. Without commit authorization, return/apply reviewed patches rather than creating commits just to enable branch merging.
4. Integrate each verified result in the authorized local workspace, resolving conflicting changes and rerunning relevant checks. Merge committed ticket branches only when their commits and the local integration operation are authorized; otherwise retain reviewable patches/files and identify the remaining commit step.
5. Recompute the ready frontier and continue until requested implementation is complete or an actual dependency blocks progress. Do not silently change feature scope to remove a blocker.
6. Review the full implementation with code-review and fix actionable findings, then report implementation, tests, outstanding issues and the branch or file locations. Distinguish completed code from unrun tests or unverified runtime behavior.
7. Perform external publication only when explicitly authorized for the specified destination: creating/pushing a PR, marking it ready, changing issue status or closing tickets are separate from producing local code. Approval of a draft or a test result alone is not publication authorization. Honor already-provided scoped authorization without asking again.
8. Clean up only task-owned worktrees no longer needed, preserving review artifacts and any uncommitted user work.

## Host adaptation

A Skill-tool call means loading the named skill's SKILL.md and following it; read the file directly if that tool is unavailable. Delegation and worktree capabilities remain actual requirements, not claims that text can substitute for tools. Small tasks may be implemented directly when parallel orchestration adds no benefit.
