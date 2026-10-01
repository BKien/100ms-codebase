# Research sources and authority

1. The UC and API sources identified in `PROJECT_PROFILE.json` are authoritative for their respective project inputs. Frozen projections retain exact source ranges and retrieval provenance.
2. [The configured coding-prompt template](../../../templates/construction/coding-prompt.template.md) is authoritative for the prompt's structure, sections and instructions.
3. The reference thesis is authoritative for retaining the original two phases: prompt generation, then source generation with bounded self-correction.
4. Existing source/database/Figma/API artifacts provide implementation context.

When sources conflict, record the exact discrepancy and ask the researcher. Do not silently normalize business meaning. The project-wide API response envelope may be applied mechanically because it changes transport shape, not domain semantics.

## Local materials and boundaries

- `resource/TrucDTT_21020414-4889_baoveee.pdf`: two-phase pipeline from use case/design/API/templates to coding prompt, then code generation and self-correction.
- `resource/TechnicalReport.pdf`: supporting reference for use cases and coding-prompt design.
- `resource/VC-AWG-Demo_FinalCode-main`: architectural reference for React/Vite and NestJS/TypeORM.
