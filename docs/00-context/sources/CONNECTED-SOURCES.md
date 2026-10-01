# Connected sources

## Canonical functional and Business Rule source

- Source type, URL and tab: `PROJECT_PROFILE.json` -> `authoritative_sources.use_case_specification`
- Authorized ranges and retrieval timestamps: recorded in each frozen UC projection
- Frozen UC inventory: every file matching `docs/01-inception/use-cases/uc-*.md`
- Frozen OCL utilities, when applicable: `docs/01-inception/use-cases/OCL-UTILITY-DEFINITIONS.md`

Use the connected Google Drive/Sheets interface. Never scrape, reconstruct or guess cell contents. Store source identity, tab, exact range and retrieval time in derived artifacts. Read only the source/tab/range authorized by the active project profile and parent prompt. Stop when access fails or when duplicate/conflicting rows make a business requirement ambiguous.

## Prompt template

- [The configured coding-prompt template](../../../templates/construction/coding-prompt.template.md) defines all prompt structure and section responsibilities.

## Figma and API sources

Use them only where the frozen UC references them. `PROJECT_PROFILE.json` identifies the authoritative API source and Figma root file(s). API contracts are explicitly defined as markdown files in `docs/01-inception/api-contracts/`. Detailed per-UC Figma mappings come only from `docs/00-context/FIGMA-LINK-REVIEW.md`; a frozen dataset is required before use.

- Treat API contracts as frozen, read-only inputs. For each UC, copy every ID from its frozen `Related API IDs` into the Confirmed configuration in source order, together with the exact repository path and raw-byte SHA-256. Do not scan for substitutes or select an API by filename similarity.
- Configuration validation requires every pinned API file to exist under `docs/01-inception/api-contracts/` with `artifact_type: api-contract`, `status: Frozen`, the configured `api_id` and the configured checksum. Prompt and Source preflight additionally require the configured ordered IDs to equal the frozen UC references.

- When creating or refreshing a dataset, read every file key, node ID and URL only from `docs/00-context/FIGMA-LINK-REVIEW.md`. The links inside immutable UC files are provenance-only and may be inaccessible; do not call Figma with them.
- Use `resolve-figma-design-dataset` whenever a prompt or UC contains a Figma URL, file key, frame name, node ID or selection ID.
- If no dataset exists, that is not permission to fall back to UC links. Start capture from the review mapping or stop if that mapping is incomplete.
- Select one immutable Figma dataset version explicitly before configuration. Copy that exact version and manifest checksum into the configuration; never scan directories or follow a moving newest/default dataset.
- Use the checksum-valid frozen snapshot as reproducible generation input. The researcher may inspect UI manually. UI scoring is never an automatic audit or experiment prerequisite; missing UI results do not block the workflow.
- Use the installed Figma plugin only to create a new dataset version or complete entries explicitly marked pending. Never overwrite a dataset version already used by an experiment.
- Stop when the resolver reports `pending-rate-limit`, a checksum mismatch, a missing target or ambiguity. Do not substitute a different frame or infer hidden screens.
