# Storybook arcade production — v1

Start with [ART_BIBLE.md](ART_BIBLE.md), then [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md). [animations.json](animations.json) defines the first 64-frame Hulk package. [sources.json](sources.json) pins the current game/account references.

This review branch versions documentation and specifications only. It changes no application source, dependencies, Firebase rules, account records, score logic or deployment workflow. Do not merge it as though it were the new playable renderer.

The accompanying downloadable **Jamesy Art Production Kit v1** contains the illustrated 22-page PDF, editable Markdown, four labeled reference images, five written hero briefs, three world briefs, design tokens, 153-entry asset register, approval checklist, prompts, atlas packer, asset validator and local browser review studio. The larger kit is not represented as already committed by this document-only branch.

## Status

- Direction: accepted by the owner in conversation.
- Written production baseline: v1 available for review.
- New costume art, production sprites and world layers: not approved by this document.
- Renderer: existing game remains unchanged.
- Accounts: existing v1.3 email/nickname flow preserved; Sean remains the sole initial Master; no sample roster or scores.

## First batch

Five-costume lineup candidate → Hulk five-pose proof → eight-frame rear run → Emerald composition → isolated playable slice. Fix identity, transparency or anchor defects before generating the full roster.

## Toolkit checks completed locally

11 Python unit tests passed for the atlas/registry tools. Seven local Chromium review-tool checks passed using temporary synthetic fixtures; file navigation was unavailable in that environment, so the authored HTML was loaded directly. All 22 PDF pages were rendered and visually inspected. These checks do not approve new character art, validate a rebuilt game or replace physical iPhone testing.
