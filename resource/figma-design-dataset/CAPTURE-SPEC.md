# Offline Figma capture specification — UC scope

A node may be marked `complete` only when the dataset contains enough data for code generation and audit runs to avoid calling Figma MCP again:

1. `design-context.md`: preserve all returned reference code/instructions for each primary UC frame. Supplemental states may use a read-only native Plugin API snapshot (`native-design.json`) containing the complete descendant tree, actual layout, paints, typography/text runs, geometry and component properties. Identify this evidence as native design data, never generated reference code. Replace temporary asset URLs with local paths.
2. `metadata.json`: dataset version, file key, node ID, frame name, node type, natural dimensions, capture time, framework/language parameters, Code Connect status and capture schema version.
3. `screenshot.png`: a context image of the correct node at a resolution sufficient to read details.
4. `export.png`: an entire-node render from `download_assets`, when already available. A native whole-node screenshot at natural scale is sufficient; do not call a second endpoint to obtain the same render. Metadata records the actual method and scale.
5. `assets/`: every asset referenced by required design context or the native subtree, including actual image paints and vector geometry/SVGs. If the connector cannot export a vector, exact native paths, paints and transforms (or complete boolean operation/child geometry) plus the whole-node render are valid geometry evidence; record the unavailable SVG export explicitly. Retain returned truncation flags. A complete native subtree/asset enumeration can resolve truncated download inventories; record that proof. Failed inventory assets proven unused by both context and native subtree may be excluded with an explicit reason. Never omit a referenced asset.
6. `asset-map.json`: map URLs/identifiers in the design context to local files, MIME types, byte sizes and SHA-256.
7. `checksums.sha256`: checksums of every data file in the version.

## Capture boundary and quota

The researcher selected UC-sufficient capture on 2026-10-02, then explicitly restricted it to **desktop only**. `FIGMA-LINK-REVIEW.md` is still the sole mapping authority. A versioned coverage matrix pins required desktop states for all 18 UCs and distinguishes captured design from behavior specified only by the UC. Do not capture mobile. Frozen UC mobile references stay unchanged; desktop completeness does not assert mobile readiness. Shared frames/assets are captured once.

The historical full-file inventory is discovery evidence, not a mandatory download queue. Documentation, changelogs, unrelated foundations/components and redundant peer-count variants are optional. Capture only referenced components and representative layout states. Reuse saved primary context and assets, then batch native reads/rendering by page for missing states. Do not repeatedly retry a quota-limited endpoint or claim a measured quota saving without usage counters.

## Must not be considered complete

- Only screenshot/export is present.
- Design context or metadata is missing.
- A required asset is truncated or missing without complete native subtree/asset evidence.
- Context still depends on temporary URLs.
- Checksums are missing or incorrect.
- Node IDs are guessed rather than verified through the plugin.

The dataset is an immutable versioned snapshot. Changes on Figma must be retrieved through a new capture run and create a new version; generation and audit use the same version to ensure reproducibility.
