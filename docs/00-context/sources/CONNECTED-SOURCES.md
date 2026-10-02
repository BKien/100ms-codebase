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
- Selected dataset: **100ms-2026-10-02-001**, desktop only, explicitly authorized on 2026-10-02. [Frozen manifest](../../../resource/figma-design-dataset/100ms-2026-10-02-001/manifest.json); manifest pin sha256:ead5b6aa248f3c132950dc533b5b3392052cfdcfec6efc029c3fb01e6845c298. All 74 required nodes across 8 pages and 18 UC mappings are complete. Use resolver primary and supplementary snapshot directories and [coverage](../../../resource/figma-design-dataset/100ms-2026-10-02-001/uc-design-coverage.json). Frozen mobile references remain outside this design scope.
- UC Figma references are provenance-only. Do not use archived Finebank evidence or auto-select a newest version.
- Never retain temporary asset URLs or credentials in frozen artifacts. Sparse context and truncated assets require further capture, never guessed completion.

## API and generation boundaries

Desktop validation receipt: [100ms-desktop-dataset-validation.json](100ms-desktop-dataset-validation.json), with 1,929 checksum files and all 18 required UC inventories validated against the exact selected version.

For each UC, pin every frozen Related API ID in its original order with repository path and raw-byte SHA-256. Resolve the common contract and assumption/utility dependencies from the configured receipt; UML is resolved solely from the active UC's local block. Do not select substitutes by filename similarity. UC-01 has no server API according to its frozen source.

## Local UML refresh

Contract: `br-local-uml-v1`. Every active UC has exactly one PlantUML block containing the vocabulary used by its own BRs and the type dependencies needed to interpret those rules. Unused class members and service operations are omitted. Full enum domains preserve the meaning of typed values and comparisons. Extent-only classifiers explicitly expose the standard OCL `allInstances()` operation; opaque signature types declare that these BRs access no structural members.

The original Markdown snapshot remains byte-exact. Previous UC projections and the retired shared model are archived under `resource/specification-transformations/100ms-local-uml/before/` and are historical evidence only. The refresh receipt pins source and projection hashes and records member-to-BR references. Functional sections, BR IDs and OCL, API contracts and schema inputs are unchanged. Existing configuration/baseline UC checksums must be prepared against the refreshed files before a new run; old pins are never rewritten automatically.

The configured prompt structure remains [coding-prompt.template.md](../../../templates/construction/coding-prompt.template.md). Preparation is separate from generation. No experiment configuration/model/run assignment is invented in this setup.

## Prepared database

Researcher authorized setup on 2026-10-02 with repository database requirements taking priority. Active [DBML](../engineering/schema.dbml), [adaptation](../engineering/100MS-DATABASE-ADAPTATION.md), [source receipt](100ms-database-adaptation.json) and [prepared baseline pins](100ms-database-baseline.json) are now available. MySQL 8.4 with unchanged mysql84-tables-v1, 16 application tables, no routines/triggers, one applied TypeORM migration; the source snapshot and frozen UC/API remain unchanged. Aggregate guards and full-key idempotency semantics are later application responsibilities. Preflight remains mandatory; no experiment configuration/run was created.

Current capture policy: retain primary reference code and complete native subtrees with verified local assets. The historical 604-target inventory is discovery only; unused and previously captured mobile nodes are historical evidence excluded from desktop resolution. [Database proposal](../engineering/100MS-DATABASE-RESOLUTION-PROPOSAL.md) is retained as historical analysis; the subsequent [repository-priority adaptation](../engineering/100MS-DATABASE-ADAPTATION.md) and explicit researcher setup request now govern the prepared database.

Database setup instructions: [Google Docs retrieval](100ms-database-setup-guide.json). Runtime: [setup operation](../../03-audit/docker-deployment/operations/20261002-100ms-database-setup.json). Current [clean source baseline](100ms-source-baseline.json) includes the applied migration and DB connection infrastructure; the previous ZIP/receipt are preserved under resource/source-baselines/100ms-pre-database-2026-10-02-001/.
