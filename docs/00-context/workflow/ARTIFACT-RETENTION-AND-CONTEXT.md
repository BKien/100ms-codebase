# Artifact retention and context

Retain separately:

- immutable Sheet-derived UC/UML/BR projections;
- a source-checksum normalization receipt only when raw checkout bytes differ solely by line endings;
- frozen BR and flow baseline receipts;
- [approved configured prompt artifact](../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md);
- optional run activation, model/time/token metadata and immutable first-pass assessment;
- each repair sub-prompt and reassessment;
- final per-BR assessment and final-source checksum.

Never overwrite first-pass results with repaired results. Derived artifacts may reference source paths and hashes but must not append decisions to immutable UC files. Keep prompts and reports free of secrets and unrelated payloads.
