# Skill mechanics in The Thing

Canonical SKILL.md frontmatter uses only Agent Skills specification fields. Keep name/description meaningful; optional fields are license, compatibility, metadata and allowed-tools. Metadata is a string-to-string map.

Default to normal task-based discovery. Preserve existing explicit-only skills: record `the-thing.invocation: explicit` under metadata and retain the prose invocation rule. Codex host policy lives in `agents/openai.yaml` as `policy.allow_implicit_invocation: false`. Original extensions are retained in `agents/legacy-frontmatter.yaml`; that file is archival configuration, not a cross-host enforcement mechanism. A host that does not read the policy needs its own adapter to enforce explicit-only loading.

Keep optional references one hop from SKILL.md; tool-specific calls need documented requirements and a truthful fallback. Add classification under `metadata.the-thing.category`, not by nesting installed skill folders. Keep drawing/modeling and document/report skill identities distinct.

The upstream invocation explanation is preserved at `references/upstream-skill-mechanics.md` for provenance; its top-level extension syntax is not the canonical format in this repository.
