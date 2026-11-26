---
name: to-spec
description: Draft a specification from the existing discussion when the user requests one; publish to an issue
  tracker only under explicit publication authorization.
license: MIT
metadata:
  the-thing.legacy.disable-model-invocation: 'true'
  the-thing.invocation: explicit
  the-thing.category: plans-progress
  the-thing.source: https://github.com/mattpocock/skills
---
> Invocation: use this workflow when the user explicitly requests it. This is an instruction-level rule; host enforcement is tool-specific.
This skill synthesizes an existing discussion into a specification draft. A request for a plan alone stays in case-based-planning; it does not activate specification, ticketing or implementation phases.

Drafting, saving a local document, publishing to a tracker and executing code are distinct scopes. Default to the draft and stop there. Explicit authorization to publish a specification permits publishing that approved content to the specified destination; it does not authorize code implementation, PR creation or release. Honor existing scoped authorization without requesting it again.

Draft from the available context even without a configured tracker. Tracker and label setup is needed only when publication is actually requested; then use the established configuration or resolve the missing destination.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Include proposed seams and unresolved decisions in the draft. Ask a focused question only when its answer materially changes the specification; do not require approval just to produce a reviewable draft.

3. Write the draft using the template below. Use an existing approved document location or present it in the response; writing a new local artifact follows the user's requested destination. Do not advance to to-tickets or implement-spec unless that phase is requested.

4. Only when publishing is explicitly authorized, publish the reviewed scope to the configured tracker and apply the established labels. Approval of wording or technical decisions alone is not authorization to publish. If publication was already explicitly requested, complete that authorized action without asking for a second identical approval.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of user stories covering the requested scope. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover necessary user-visible behavior and relevant edge cases without expanding the feature or imposing a length quota.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
