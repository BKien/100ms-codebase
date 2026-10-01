# Business vibe coding agent contract

Work only inside this repository unless the researcher expands scope. On setup or review requests, read `CODEX_SETUP_GUIDE.md`. Before planning or editing, read `PROJECT_PROFILE.json`, `PROJECT_CONTEXT.md` and `docs/00-context/sources/CONNECTED-SOURCES.md`. For each feature, follow `docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md` and `docs/00-context/workflow/gates/EXPERIMENT-CONFIGURATION-GATE.md`.

Use the canonical terminology from `PROJECT_CONTEXT.md`: this repository is a research product, the human operator/approver is the researcher, and actors inside use cases are application users.

## Authoritative inputs

`PROJECT_PROFILE.json` identifies the active project's authoritative UC, API and Figma sources. Files under `docs/01-inception/use-cases/uc-*.md` are frozen, read-only projections of the configured UC source. They contain the functional specification, UML model, OCL business rules, natural-language constraints, UI/API mappings and source provenance. The frozen OCL utility projection, when supplied by the project, is `docs/01-inception/use-cases/OCL-UTILITY-DEFINITIONS.md`.

API contracts under `docs/01-inception/api-contracts/` are frozen, read-only specification inputs. Each configured UC pins the complete ordered API ID/path/SHA-256 inventory resolved from its frozen `Related API IDs`. Prompt and Source preflight reject a missing, changed, reordered or identity-mismatched API contract before START. Do not edit an API contract within a configured run.

Never edit a frozen UC to repair a source issue. Report the exact source location and stop for the researcher when ambiguity changes behavior, rule meaning, API, schema or evaluation. Refreshing the frozen UC set requires an explicit researcher request and a new source retrieval record.

When a UC contains a Figma reference, resolve it through `resolve-figma-design-dataset`. Use `docs/00-context/FIGMA-LINK-REVIEW.md` as the sole mapping authority when creating or refreshing a dataset.

## Two-phase method

The research method has exactly two phases:

1. **Phase 1 - Generate the business coding prompt.** Read one frozen UC, its UML model and applicable API/Figma sources under the existing input boundaries in `docs/00-context/workflow/WORKFLOW-CONTRACT.md`. Source locations are recorded in `docs/00-context/sources/CONNECTED-SOURCES.md`. Validate the prepared inputs and create [the configured prompt](docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md) as a Draft from its template. [The configured coding-prompt template](templates/construction/coding-prompt.template.md) defines all prompt structure and section responsibilities.
2. **Phase 2 - Generate source code.** After the prompt-close command approves the Draft, implement the approved prompt in `finalsource/fe` and/or `finalsource/be`. Record first-pass evidence, assess every frozen BR from the baseline, create bounded bug-fixing sub-prompts for evidenced errors, rebuild/run with Docker Compose and freeze the final source hash.

Do not use a separate dimension to change Business Rule acceptance. The current run evaluates against the frozen BR baseline; flow accuracy is a supplementary frozen measurement. The researcher may inspect UI by eye or skip scoring. Missing/null `ui_accuracy` or UI scores never block BR/flow audit, telemetry, export or completion.

Before Phase 1, resolve every BR and every explicit Basic/Main, Alternative and Exception Flow associated with the UC. Persist `business-rule-baseline.json` and `flow-baseline.json`; do not select, omit or add rules/flows after implementation is visible.

Before Phase 2 source mutation, validate the pinned configuration, approved prompt and closed prompt telemetry. `run-activation.json` is optional and validated when present; no activation file or turn is required.

## Command and measurement boundaries

Follow the command sequence in `docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md`: generate prompt; close prompt; generate source; close source; audit BR/flows; repair when needed; finalize (which closes/skips Repair and finalizes telemetry atomically); optionally export. Each researcher command authorizes that step without an additional confirmation gate. Closing prompt also approves and pins the Draft. Invoking `$bug-fixing-sub-prompt` authorizes and begins evidenced repair in the same turn. Initial audit and follow-up measurement never automatically start repair.

Require four prepared research JSON inputs (Confirmed configuration with the configured UC's frozen API pins, frozen BR baseline, frozen flow baseline and Draft Canonical Run JSON) plus the fifth database input: configured DBML and the existing MySQL schema. Validate them read-only using the existing preflight; no extra user turn. Never initialize or repair missing inputs during prompt/source generation, require root `.env`, or ask for configuration reconfirmation. Keep existing `gates` fields/receipts only as internal command bookkeeping; preserve recorded evidence.

Save partial flow results immediately. Offer researcher-supplied verdicts or bounded LLM measurement. Save either path with attribution, acknowledge the update and wait for the subsequent repair command if defects remain. Remaining unknown accepted flow verdicts block new repair authorization; pending evidence is not a defect. Use `accepted-audit-results-v1`, retaining conclusive results across repairs and later inconclusive audits. Do not fabricate runtime proof for researcher verdicts or reset accepted results to null.

If all BRs and flows pass on unchanged source, record repair unnecessary during audit, skip Turn 6 and let `finalize-workflow` persist the skipped Repair bucket and final workflow in Turn 7. Authorized repair automatically verifies BR/flow/runtime and freezes final source hash/status before returning; the same finalize command closes its telemetry. No separate audit-result approval, Repair Decision confirmation, Repair-close command, final-audit or Final Metrics confirmation is required.

Prompt/source/repair remain telemetry buckets within two phases. Close telemetry only in the subsequent requested close turn; do no source/audit/repair work in a measurement turn. Assign one semantic token label per work turn; observations must match any captured core execution, including repair's integrated audit under label `repair`. Counted time sums only Prompt + Source + Repair execution intervals; Repair includes integrated BR/flow/runtime verification and final evidence/hash/status persistence before END. Use `generation_execution_with_repair_audit_v2`. Standalone audit remains workflow-only tokens, outside counted execution time. Export remains separate after finalization, excluded from workflow tokens/time; it copies validated skipped-Repair zero values and preserves canonical evidence, formulas/manual/protected content and saves a new workbook copy.

## Business-rule contract

Baseline preparation and validation preserve the complete ordered Rule ID inventory and pin the frozen UC that contains the exact OCL and natural-language text.

Every frozen BR receives exactly one evidence-based result: `met`, `unmet` or `not_evaluable`. Evidence may come from inspectable source, configuration, non-test build/lint checks and bounded Docker runtime observation. Prompt text alone is never evidence.

## Shared operational constitution

These rules apply to every skill.

Execute a top-level workflow step only when the researcher explicitly invokes that step in the current turn. The invocation authorizes the active skill and only the subordinate skills that its contract explicitly requires to complete that same step. It does not authorize opening or preloading a later step's `SKILL.md`, references or scripts, or executing or preparing that later top-level step, even when its name and short description are already visible in the installed skill catalog or documented workflow.

During a run-scoped workflow step, read only the active skill, its explicitly required references, the current application codebase and the exact active-run artifacts resolved from the pinned configuration and Canonical Run. Do not browse experiment or implementation directories to discover alternatives. An explicitly requested reporting, export, baseline-restoration or repository-review operation may inspect the additional artifacts its active contract requires, but that exception does not authorize later-step execution or use of prior results as generation, audit or repair context.

During generation, audit or repair for an active run, do not open, inspect, summarize, compare or use configurations, Canonical Runs, audit results, repair records, reports or other experiment artifacts belonging to another UC, run, model or variant. If such an artifact is encountered incidentally, disregard it and do not use it as generation, evaluation or repair context.

`finalsource` is the permitted cumulative application codebase and is not treated as a prior experiment-result artifact. Deterministic validators may read the exact active-run files supplied by the active skill and may inspect artifact identities and checksums solely for deterministic selection and integrity validation. They must not expose unrelated artifact contents to the AI context.

Any path containing `<UC-ID>` or its URL-encoded form `%3CUC-ID%3E` is a generic path pattern, not a literal file. During execution, substitute the actual active use-case ID before opening, validating or writing the referenced artifact; never treat the placeholder itself as an existing file.

During source generation, generate source only and modify only files required by the active use case. Do not introduce unapproved public API, ownership, dependency or destructive-data changes.

When a material ambiguity, contradiction, missing decision or other blocker becomes apparent, do not invent or change requirements, behavior, API, data structures, ownership, security or evaluation semantics. Report the exact evidence and wait for researcher resolution, unless the active skill contract defines a specific evidence-preserving outcome for that condition.

In particular, during business coding-prompt generation or first-pass source generation, if a material contradiction involving the active frozen UC, its configured API contracts, the configured DBML or the existing database schema becomes apparent, stop and report the exact conflicting evidence. Do not modify the affected inputs or infer a resolution. Skill-specific preflight checks, evidence requirements and stopping conditions remain mandatory.

Apply the project-wide API normalization downstream: successful payloads use `{ success: true, message, data }`; errors use `{ success: false, statusCode, message, timestamp, path }`. Preserve source status, business fields and message semantics.

Keep JWT, password hashing, validation, ownership, secret handling, safe errors, transactionality and concurrency behavior when the UC, BR, API contract or required technical baseline calls for them. They are ordinary application controls, not a separate research intervention.

Database follows `docs/00-context/engineering/DATABASE-SCHEMA.md`. The researcher prepares a complete initial schema and may add reviewed TypeORM migrations between runs when necessary; retain cumulative data. Configuration pins exactly `migration_head`, `dbml_sha256` and `schema_fingerprint_sha256` using its existing status. Read `docs/00-context/engineering/schema.dbml` and map code to existing tables. Schema and migration inputs are immutable within each run. AI may perform authorized business DML but never DDL, migration execution/edits, DBML edits or schema sync. Missing structure blocks work; preserve actual END/partial evidence, then researcher setup and a new configuration/run are required if the baseline changes. Prompt/Source verify pins/history before START; Audit/Repair recheck drift. Within a run, rebuild only backend/frontend with `--no-deps` so Docker cannot invoke the setup migration service. Measure/activation/export perform no live DB check.

Docker Compose v2 is mandatory for FE/BE/MySQL execution. A missing daemon is `BLOCKED`; do not fall back to native host Node.js/MySQL.

Generation preflight reads the existing database only. Never start, reset or bootstrap database inputs, replace expected pins, or dump SQL/metadata into generation context. Use the existing validators to report missing or mismatched inputs.

Do not create or run tests or test cases. Permitted checks are source inspection, deterministic validators, typecheck, lint, build, Docker health/reachability and bounded manual runtime observation.

Never store credentials, access tokens, passwords, full account numbers or sensitive payloads in source, logs, prompts or reports.

Keep secrets out of client bundles, `.env.example`, public API documentation and persisted tool output. Never commit `.env` or raw sensitive logs. Use sanitized evidence. Destructive database resets, volume/image cleanup and destructive migrations require an explicit researcher request outside an active run. Preserve cumulative data and frozen evidence.

Prompt telemetry close (Turn 2) automatically creates a missing `run-activation.json` from the pinned configuration and approved prompt, or validates an existing receipt without replacing it. The receipt records the actual prompt-close turn/time, before source generation. No standalone activation turn is required.
