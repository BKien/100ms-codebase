---
artifact_type: bug-fixing-sub-prompt
uc_id: <UC-ID>
run_id: <RUN-ID>
repair_index: <N>
affected_br_ids: [<BR-ID>]
---

# Repair <N> — <bounded defect>

## Evidence

`<exact source/build/runtime evidence>`

## Required correction

Apply the smallest change that corrects this defect while preserving the [approved configured prompt](../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md) and unrelated behavior.

## Scope

- Allowed files: `<paths>`
- Affected BRs: `<BR IDs>`
- Permitted non-test verification: `<lint/typecheck/build/runtime observation>`
- Prohibited: new features, speculative refactors, any database schema/DBML/migration-file change or migration, public-API/ownership decisions without researcher approval, and all test creation/execution.

## Completion

Record changed files, verification evidence, time/tokens and reassessment of affected BRs. Do not overwrite first-pass evidence.
