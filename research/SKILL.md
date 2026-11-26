---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads. Start it with a fresh context window.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.


## 与方案入口的分工

独立调研使用本技能；调研要形成实施方案时，再读取相邻 `../case-based-planning/SKILL.md`，复用已查证资料并完成直接复用、参考、定制和可行性判断。只在用户需要可保存的调研交付时写入文件，并遵循其指定格式与位置。
