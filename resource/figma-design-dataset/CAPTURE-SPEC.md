# Complete offline Figma capture specification

A node may be marked `complete` only when the dataset contains enough data for code generation and audit runs to avoid calling Figma MCP again:

1. `design-context.md`: all reference code and semantic instructions returned by `get_design_context`; replace temporary asset URLs with local paths.
2. `metadata.json`: dataset version, file key, node ID, frame name, node type, natural dimensions, capture time, framework/language parameters, Code Connect status and capture schema version.
3. `screenshot.png`: a context image of the correct node at a resolution sufficient to read details.
4. `export.png`: render the entire node from `download_assets`.
5. `assets/`: all raw images and SVG assets returned by MCP; the manifest explicitly records every truncated flag.
6. `asset-map.json`: map URLs/identifiers in the design context to local files, MIME types, byte sizes and SHA-256.
7. `checksums.sha256`: checksums of every data file in the version.

## Must not be considered complete

- Only screenshot/export is present.
- Design context or metadata is missing.
- An asset is truncated but has not been recorded and handled.
- Context still depends on temporary URLs.
- Checksums are missing or incorrect.
- Node IDs are guessed rather than verified through the plugin.

The dataset is an immutable versioned snapshot. Changes on Figma must be retrieved through a new capture run and create a new version; generation and audit use the same version to ensure reproducibility.
