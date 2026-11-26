---
name: ppt-card-layout
description: Design one polished 16:9 presentation slide from supplied content using editable native tables, cards,
  timelines, and comparison layouts. Use for metric cards, research questions, project status, comparisons, timelines,
  risks, next steps, or a concise one-page PPT summary. Avoid for multi-slide narrative decks or inline HTML visualizations.
compatibility: A presentation-authoring runtime producing editable objects and rendered previews; a compatible Presentations
  workflow is required.
metadata:
  the-thing.category: documents-reports
---
# PPT Card Layout

Turn supplied content into one clear 16:9 presentation slide. Use the `Presentations` workflow for the deliverable. Apply `visualize` composition principles to choose the smallest useful structure; do not create a separate HTML visualization unless the user requests one.

## Workflow

1. Extract the slide title, atomic facts, labels, numbers, units, relationships, chronology, and caveats. Preserve the source meaning and never invent missing values.
2. Choose the layout by content shape, not by decoration. Read [layout catalog](references/layout-catalog.md) for the matching preset.
3. Compress prose into short labels and one-line explanations. Retain caveats that affect interpretation.
4. Build the slide with native editable presentation objects: text boxes, rounded rectangles, tables, simple lines, and connectors. Keep supplied logos and evidence images as their original files.
5. Render and inspect the slide. Fix overflow, overlap, weak hierarchy, inconsistent spacing, incorrect numbers, and lost editability before delivery.

## Automatic layout selection

- One dominant point plus 2-4 metrics: use a dominant statement with metric cards.
- Two parallel themes: use two columns.
- Three peer groups: use three columns.
- Four peer groups with similar content: use a four-card grid.
- Repeated fields across at least three items: use a native comparison table.
- Ordered stages or dated events: use a timeline.
- Risks paired with actions: use a two-column risk and next-step layout.
- More content than fits at readable size: consolidate related items or choose a table. Do not shrink body text below 17 pt to preserve every sentence.

## Visual system

- Use the user's template first. Without one, use a restrained scientific-report style: one CJK-capable sans-serif family, dark neutral text, light neutral surfaces, and one cool accent color.
- Keep a clear title zone, consistent outer margins, equal internal padding, and aligned baselines.
- Use 32 pt or larger for the slide title and at least 17 pt for body text. Use weight and spacing before adding colors.
- Use rounded cards only because this skill is explicitly for card layouts. Keep them flat, with no dashboard controls, ornamental badges, nested cards, or heavy shadows.
- Use one accent color for emphasis. Reserve warning colors for actual risks or exceptions.
- Keep each card focused on one idea. Prefer a label, a key value or statement, and at most one short supporting line.
- Use native tables for row-and-column evidence. Apply subtle horizontal dividers, readable headers, aligned numbers, explicit units, and calculated totals only when supported by the source.

## Deliverable rules

- If the user supplies an existing deck or template, edit that presentation and preserve its design language.
- Otherwise create a new one-slide 16:9 presentation. Do not add a cover.
- Keep all requested tables, cards, timelines, and diagrams editable.
- Cite external facts and images in speaker notes when required by the presentation workflow.
- Return the saved presentation, not screenshots of the slide.
