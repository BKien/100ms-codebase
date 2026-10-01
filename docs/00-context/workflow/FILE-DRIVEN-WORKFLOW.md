# File-driven workflow

The researcher invokes the following commands in separate turns. Each command authorizes its own operation; never add a confirmation question, gate approval turn, activation requirement or automatic repair after audit/follow-up. End each response with the next command. The method still has exactly two phases: prompt generation and source generation, including audit/repair.

Reference: [researcher command sequence](https://docs.google.com/document/d/1R9Z4LQ_FEbEop_TmGMTyCPnM3HdNau9JvLBV4uB8ZMg/edit?tab=t.0).

## Prepare four JSON files and the database input before generation

1. `docs/04-experiments/configurations/CFG-<UC-ID>-<MODEL>-<VARIANT>.json`: complete, Confirmed configuration, including the ordered frozen API ID/path/SHA-256 entries for the UC.
2. `docs/02-construction/implementation/<UC-ID>/business-rule-baseline.json`: the complete ordered BR ID inventory and checksum-pinned frozen UC.
3. `docs/02-construction/implementation/<UC-ID>/flow-baseline.json`: the complete ordered Main/Basic, Alternative and Exception Flow ID inventory and checksum-pinned frozen UC.
4. `docs/04-experiments/<UC-ID>/canonical-run-<UC-ID>-<MODEL>-<VARIANT>.json`: Draft Canonical Run JSON with pinned configuration and baseline identities.

5. Database input: `docs/00-context/engineering/schema.dbml` and MySQL tables prepared by researcher-managed TypeORM migrations. Configuration pins migration head, DBML hash and runtime fingerprint. Follow [database policy](../engineering/DATABASE-SCHEMA.md).

The researcher chooses the preparation tool. Validate the four JSON files, database pins and frozen UC/API/Figma dependencies read-only; API validation checks the configured order against the UC and each pinned file's path, Frozen identity and SHA-256. Never initialize, repair or fill missing inputs during generation. Resolve one exact UC/run, never the newest file. Root `.env` is optional; initialized Docker MySQL and `finalsource/.env` are required for the database preflight. `run-activation.json` is an optional run receipt, not an additional prepared input; validate it when present. Requested model, replicate and run order come from the pinned configuration.

For these file names, `run_id` is `<UC-ID>-<MODEL>-<VARIANT>`: `MODEL` is the configuration's path-safe `requested_label`, and `VARIANT` is its `prompt_variant`. The configuration ID is `CFG-<run_id>`.

For optional deterministic preparation, run `experiment-input-helpers/calculate_input_values.py` with one frozen UC path, each frozen API contract path in the UC's `Related API IDs` order, and one explicit Figma dataset version. Repeat `--api-contract` for a multi-API UC; use `--require-empty` only at initial pipeline setup. The helper prints paths, identities and checksums—including the three database baseline pins—without writing files. After manually completing and reviewing the configuration, run `experiment-input-helpers/calculate_configuration_checksum.py --configuration <configuration-path>` and copy the printed checksum into the Draft Canonical Run JSON. Generation still performs its existing read-only configuration/API/Figma/database preflight.

## Command sequence

| Turn | Researcher command | Completion and next step |
|---|---|---|
| 1 | `$gen-coding-prompt docs/01-inception/use-cases/<UC-file>.md` | Validate prepared inputs; generate the Draft from [the configured coding-prompt template](../../../templates/construction/coding-prompt.template.md); preserve actual START/END. Next: Turn 2. |
| 2 | `$measure-uc-workflow close-phase prompt_generation` | This invocation approves the Draft, pins approved bytes/checksum, closes prompt telemetry and creates/validates activation in the same turn. Next: Turn 3, without another approval or activation turn. |
| 3 | `$gen-source-code docs/02-construction/coding-prompts/<UC-ID>-business-coding-prompt.md` | Generate first-pass source only; preserve source/hash/model/timing evidence; stop before audit/build/repair. Next: Turn 4. |
| 4 | `$measure-uc-workflow close-phase source_generation` | Close source telemetry and record completion. Next: Turn 5. |
| 5 | `$audit-generation-metrics` (includes `$audit-flow-accuracy`) | Run permitted checks and bounded Docker observations; persist every frozen BR/flow result and first-pass evidence. Do not ask to approve audit results. If all pass, record repair unnecessary and go to Turn 7. If defects exist, go to Turn 6. If results are unknown, save partial results and request missing verdicts or bounded LLM measurement. |
| 6 | `$bug-fixing-sub-prompt` | This invocation records repair authorization and starts bounded corrections immediately. Automatically verify BR/flow/runtime on final source and freeze terminal hash/status before returning. Next: Turn 7. |
| 7 | `$measure-uc-workflow finalize-workflow` | In one excluded measurement turn, close Repair (or persist a validated skipped bucket), compute and validate all phase/workflow metrics, record both internal transitions and finalize canonical telemetry. Failure before commit leaves the workflow unfinalized. No separate Repair-close, final-audit or Final Metrics confirmation. Next: optional Turn 8. |
| 8 | `$export-experiment-excel <UC-ID> "<LINK_OR_FILEPATH>" "<TAB_NAME>"` | Separate reporting operation, excluded from workflow tokens/time. Current export produces a new filled `.xlsx` copy from the supplied workbook/link. |

For unknown flow results, accept attributed researcher verdicts directly into canonical JSON, acknowledge the save and wait for `$bug-fixing-sub-prompt` when defects remain. LLM follow-up measurement also saves and waits for that command. Remaining unknown flows block new repair authorization; unknown evidence alone is not a defect. Never erase accepted verdicts because source changed or a later observation is inconclusive. Use `accepted-audit-results-v1` and preserve each selected result's actual stage/source. See the [follow-up contract](gates/FLOW-FOLLOWUP-AUTO-REPAIR.md).

## Evidence

The `gates` JSON field records internal command steps. `record_command.py` records commands with actual turn IDs, timestamps and evidence hashes. Measure records its step after telemetry succeeds. Audit records its step after evidence is persisted. Repair authorization is recorded within Turn 6. Do not rewrite frozen configurations, baselines, assessments, activations or gate receipts.

Preserve frozen BR/flow evaluation for the current run. Resolve frozen Figma evidence through the dataset skill and review mapping. Optional UI scoring never blocks any command. See [workflow boundaries](WORKFLOW-CONTRACT.md).

Capture only actual Prompt + first-pass Source + Repair execution intervals. Under `generation_execution_with_repair_audit_v2`, Repair includes its integrated BR/flow/runtime verification and final evidence/hash/status persistence before END. Standalone audit/runtime/follow-up observation contributes no generation execution seconds; close/report/export turns are excluded from workflow tokens. Each work turn has one semantic token label, matching any captured core execution; a repair's child audit remains `repair`. Keep phase-ledger/selection evidence and never fabricate missing counters/endpoints.

Preserve cumulative source provenance; do not reset between cumulative UCs. API envelopes and required application controls remain. Database structure is immutable within each run. Researcher setup may add migrations between runs when required. Read pinned DBML; perform authorized business DML only. No in-run DDL, migration or schema sync. A missing/conflicting schema element blocks work; close any open interval and preserve partial evidence. Changed baseline requires researcher setup and a new configuration/run. Within runs, Docker rebuilds use `--no-deps backend frontend` and never execute the migration service. Docker Compose v2 is the only runtime; missing daemon is BLOCKED. Never create or run tests/test cases or store secrets in evidence.

Prompt telemetry close (Turn 2) automatically creates a missing `run-activation.json` from the pinned configuration and [approved prompt](../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md), or validates an existing receipt without replacing it. The receipt records the actual prompt-close turn/time, before source generation. No standalone activation turn is required.
