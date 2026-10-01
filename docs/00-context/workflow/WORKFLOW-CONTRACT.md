# Workflow contract

The configured method uses [the configured prompt](../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md). [The configured coding-prompt template](../../../templates/construction/coding-prompt.template.md) defines all prompt structure and section responsibilities. Preserve all functional Basic/Main, Alternative and Exception Flows, required technical controls, frozen BR/flow evaluation baseline, audit rubric, gate sequence and telemetry rules.

## Input boundaries

The current run receives the researcher-prepared per-run database baseline through configuration `database_baseline`. The same configuration pins the complete ordered API contract ID/path/SHA-256 inventory for each UC. Prompt/Source preflight verifies that inventory against the frozen UC and verifies every API's Frozen identity and current bytes before START. DBML is technical input for prompt generation. Read the configured DBML; use existing structure and authorized business DML only. Prompt/Source preflight verifies migration history, DBML bytes and runtime fingerprint before START. In-run migrations and DDL are prohibited. Researcher setup may evolve schema between runs; matched UC comparisons use identical API pins, migration history and hashes. See [database policy](../engineering/DATABASE-SCHEMA.md). Database data persists across cumulative UCs.

| Operation | Configured method |
|---|---|
| Evaluation preparation | Freeze all BRs and flows before generation |
| Prompt generation | Functional/UML/UI/API sources, configured template and its permitted inputs |
| First-pass source | Approved prompt from the configured template and its permitted inputs |
| First-pass audit / automatic repair verification | Every frozen BR and flow, configured rubric |
| Authorized repair | One evidenced defect per bounded sub-prompt |

Map every frozen flow and terminal clause to the applicable sections defined by the configured template before approval. This is a traceability check, not a new flow denominator. Required JWT/hash/ownership/validation and other technical controls remain where the permitted functional/API/technical sources require them.

## Identity

Prompt metadata requires `prompt_variant` to match the pinned configuration; the canonical run and activation use that same value. Validate the exact heading structure, filename and approved prompt checksum.

`gen-coding-prompt/scripts/validate_prompt_contract.py` validates the configured UC/run, approved status (or `--allow-draft`), source UC, exact configured API metadata, filename, the prompt headings defined by the configured template, BR reference boundaries and optional activation checksum. It is read-only. It does not prove semantic flow coverage.

At `$measure-uc-workflow close-phase prompt_generation`, approve the Draft and pin canonical `coding_prompt: {path, sha256}` and configured variant. Keep a run-local approved snapshot if the common prompt path will be reused. Optional activation receipts remain immutable and are validated when present; no activation preparation or turn is mandatory.

## One command sequence

The current run follows [FILE-DRIVEN-WORKFLOW.md](FILE-DRIVEN-WORKFLOW.md): prompt -> close prompt -> source -> close source -> audit -> requested repair if needed -> finalize (atomically close/skip Repair and finalize workflow) -> optional export. Each command supplies authorization without extra gate confirmations. Audit includes all frozen BRs/flows. Follow-ups save attributed results and wait for a repair command when defects remain; unknown accepted flow verdicts block new repair. All-passing unchanged-source audit records repair unnecessary and skips correction.

`record_command.py` preserves the internal `gates` history, with actual command turn/time and evidence hashes; it does not ask for confirmation. Audit evidence remains pinned and immutable. Repair records authorization within its work turn; final verification is automatic there. `finalize-workflow` closes or skips Repair, validates all aggregates and records Repair-close plus Final receipts before one canonical commit. Missing UI scores never block a command.

## Cumulative source provenance

Allow cumulative UCs within the configured pipeline and source order. Before each source generation, record in the run's `source-input.json`: UC/run, configuration reference/checksum, prompt variant, model tuple, replicate, run order, input source SHA-256 and predecessor run/final hash (null at pipeline start), with references to the preserved source/hash evidence. Compare the observed input to that predecessor or the documented clean baseline before mutation.

Do not restore between cumulative UCs. A new pipeline/model/replicate condition uses its documented starting baseline; it cannot silently inherit another condition's generated source. An unresolved source identity is a preflight blocker, not permission to bypass comparison checks or reset files automatically. Restore only within the researcher's authorized scope. Preserve existing source and recorded evidence while resolving provenance.

Prompt/source/repair remain telemetry buckets in two phases. Audit, runtime, approval and finalization do not add generation execution seconds. No tests or test cases are created or run by this contract.

Prompt telemetry close (Turn 2) automatically creates a missing `run-activation.json` from the pinned configuration and approved prompt, or validates an existing receipt without replacing it. The receipt records the actual prompt-close turn/time, before source generation. No standalone activation turn is required.
