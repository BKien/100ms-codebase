# Connected sources — 100ms

The researcher selected the local Markdown package as the authoritative functional/API source and authorized replacing the copy-file Figma provenance with the standard file.

- Source identity: `PROJECT_PROFILE.json` → `authoritative_sources`.
- Original package: `D:/figma_spec/100ms Video Conferencing and Live Streaming` (read-only).
- Byte-exact snapshot: `resource/specification-sources/100ms-2026-10-01-001/`.
- Original source retrieval paths, checksums and actual retrieval time: [100ms-source-retrieval.json](100ms-source-retrieval.json).
- Active UC projection receipt: [100ms-local-uml-retrieval.json](100ms-local-uml-retrieval.json). This researcher-authorized refresh derives each local UML from that UC's unchanged BRs using the checksum-verified existing snapshot; it does not claim a new external retrieval.
- Frozen UC inventory: every `docs/01-inception/use-cases/uc-*.md`, 18 files.
- Frozen OCL utility semantics: `docs/01-inception/use-cases/OCL-UTILITY-DEFINITIONS.md`. UML classifiers, accessed members, required operation signatures and helpers are declared locally in each UC; there is no active shared UML model.
- Frozen assumptions/domain scope: `docs/01-inception/ASSUMPTIONS.md`, `CONTEXT.md`.
- Frozen API inventory: 15 `api-*.md` in `docs/01-inception/api-contracts/`, plus `common-contract.md`. Source README count of 14 is historical and does not remove any endpoint.

Read only configured source inputs. Never invent spreadsheet IDs, tabs or ranges for this local package. Source snapshots remain byte-exact; downstream projections record allowed structural/provenance changes separately. Changes to Frozen behavior require researcher source revision and a new retrieval record.

## Figma

- Standard file: `lCvn1rB7IdRchqAuEatJJp`.
- All 69 pages were enumerated with figma-use and inspected one page per call; [page inventory](100ms-figma-page-inventory.json) includes roots, node types, dimensions and empty pages.
- The provided `4732:52930` is a PAGE. Profile URLs use verified root frames only.
- [FIGMA-LINK-REVIEW.md](../FIGMA-LINK-REVIEW.md) is the sole capture authority, including approved supplementary/descendant targets.
- Selected dataset version for this authorized setup: `100ms-2026-10-01-001`. Completeness and checksum validation must pass before configuration pins are used.
- UC Figma references are provenance-only. Do not use archived Finebank evidence or auto-select a newest version.
- Never retain temporary asset URLs or credentials in frozen artifacts. Sparse context and truncated assets require further capture, never guessed completion.

## API and generation boundaries

For each UC, pin every frozen Related API ID in its original order with repository path and raw-byte SHA-256. Resolve the common contract and assumption/utility dependencies from the configured receipt; UML is resolved solely from the active UC's local block. Do not select substitutes by filename similarity. UC-01 has no server API according to its frozen source.

## Local UML refresh

Contract: `br-local-uml-v1`. Every active UC has exactly one PlantUML block containing the vocabulary used by its own BRs and the type dependencies needed to interpret those rules. Unused class members and service operations are omitted. Full enum domains preserve the meaning of typed values and comparisons. Extent-only classifiers explicitly expose the standard OCL `allInstances()` operation; opaque signature types declare that these BRs access no structural members.

The original Markdown snapshot remains byte-exact. Previous UC projections and the retired shared model are archived under `resource/specification-transformations/100ms-local-uml/before/` and are historical evidence only. The refresh receipt pins source and projection hashes and records member-to-BR references. Functional sections, BR IDs and OCL, API contracts and schema inputs are unchanged. Existing configuration/baseline UC checksums must be prepared against the refreshed files before a new run; old pins are never rewritten automatically.

The configured prompt structure remains [coding-prompt.template.md](../../../templates/construction/coding-prompt.template.md). Preparation is separate from generation. No experiment configuration/model/run assignment is invented in this setup.

## Deferred database

Researcher instruction: temporarily skip database preparation. DBML and persistence.sql remain only as source evidence in the snapshot; the old Financial DBML is archived. No active schema, migration history or database fingerprint has been created. Resolve the procedure/trigger policy before preparing the fifth input. Existing database preflight is not bypassed.
