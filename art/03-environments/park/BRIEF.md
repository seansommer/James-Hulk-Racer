# Emerald Skyway — minimal environment kit

Hulk-first slice: existing `park` / 0. Two other worlds wait for gameplay feedback. Use [Art Bible v1.3](../../../production/art-bible-v1/ART_BIBLE_v1.3.md), not the old all-art-before-testing order.

## Mood

A welcoming sunny city park. Pale blue sky, soft clouds, distant warm stone/blue-glass skyline, rounded green treetops, warm ivory paths/architecture and restrained violet accents. Dimensional storybook surfaces and soft upper-left daylight match Hulk and the object family.

## Required source layers

1. **Far backdrop:** wide sky/city/park distance. No hero, pickups, hazards, foreground road, half-pipe or HUD. It sits behind the moving track, not on it. Label a flattened scene honestly as a backdrop.
2. **Mid canopy layer:** separately authored transparent treetop silhouettes, sparse in the center. A crop of the full backdrop is not an independently painted layer.
3. **Near props:** isolated rounded tree and shrub clump at the gameplay camera. Transparent backgrounds, no baked floor or shadow. Place outside collision lanes.
4. **Gateway:** separate warm-ivory park arch with a genuinely open center and simple violet trim. No text. Decorative and non-colliding for the first test; uprights outside the route.

Reuse existing perspective half-pipe geometry/material during the first test. An elaborate ground texture, animated waterfall, second world or title illustration must not block assembly.

## Layer review

Check horizon/camera agreement, edge transparency, silhouette readability, overlap/depth order and central route visibility. Keep close props from hiding upcoming hazards. Avoid conflicting baked shadows and exaggerated parallax. A composition concept is a guide, not proof of an exported layer kit.

## Status at brief creation

Specified. Required source images and layer exports must be produced and verified separately. No environment image is counted as archived by this brief. The new world presentation is not yet integrated or deployed.
