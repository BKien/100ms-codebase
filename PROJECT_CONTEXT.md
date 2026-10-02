# PROJECT_CONTEXT

## Canonical terminology

- **Research product:** this repository, its two-phase generation workflow, artifacts, source and experiment evidence.
- **Researcher:** the human who supplies sources, confirms experiment configuration, approves prompts and resolves ambiguity.
- **Codex/AI:** the agent that projects sources, generates prompts/source and records evidence. It never approves its own output.
- **Application user:** an actor represented in a use case.
- **Reviewer:** an independent reader of the method and evidence.

Configuration confirmation is supplied by the researcher's externally prepared JSON with `status: Confirmed`, not an additional chat approval. Prompt generation requires the configuration, BR baseline, flow baseline and Draft Canonical Run JSON already on disk, validates them read-only and persists only the Draft prompt and live measurement evidence in the work turn; the next researcher command is prompt telemetry closure, which also approves the Draft; no additional confirmation gate is required. Any integrity issue blocks generation rather than being inferred or auto-corrected.

## Research objective

This project studies automated source-code generation from use-case specifications enriched with explicit Business Rules. Rules are expressed as OCL invariants, preconditions or postconditions when representable; remaining constraints stay in authoritative natural language.

The configured method extends the two-phase method described by Dang Thi Thanh Truc:

[The configured coding-prompt template](templates/construction/coding-prompt.template.md) defines all prompt structure and section responsibilities.

The method has two phases:
- **Phase 1 - Generate Business Coding Prompt:** produce and approve the designated prompt artifact (`*-business-coding-prompt.md`).
- **Phase 2 - Generate Source Code:** implement [the approved prompt](docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md) starting from clean baseline, record first-pass evidence, assess every frozen BR, perform bounded repairs, and run Docker runtime observations.

The [workflow contract](docs/00-context/workflow/WORKFLOW-CONTRACT.md) defines functional-flow coverage, gates, evaluation and provenance controls. Cumulative UCs extend the recorded predecessor within the configured pipeline; new experimental conditions use their documented baseline.

## Authoritative sources

### Functional and business specification

The active project's source identity is defined once in `PROJECT_PROFILE.json`. The 100ms project uses researcher-provided local Markdown, retained byte-exact in a repository source snapshot. Each frozen projection records its original path, snapshot path, raw-byte SHA-256 and retrieval time. Google Sheets URL/tab/range fields apply only to projects whose configured source is a spreadsheet.

Files matching `docs/01-inception/use-cases/uc-*.md` are the complete frozen UC inventory for the active project. Each projection supplies functional fields, UML PlantUML, Business Rules, related UI/API IDs, notes and exact source provenance. `docs/01-inception/use-cases/OCL-UTILITY-DEFINITIONS.md` is the frozen project-level OCL utility projection when applicable; it is not a UC.

### API contracts

`PROJECT_PROFILE.json` identifies the authoritative API source. Files under `docs/01-inception/api-contracts/` are its frozen API specification inputs. For each UC, the Confirmed configuration records the complete ordered API ID/path/SHA-256 inventory resolved from the frozen UC's `Related API IDs`. Configuration validation checks each API's Frozen identity and bytes; Prompt and Source preflight also require the configured order to match the frozen UC before START.

### Method reference

`resource/TrucDTT_21020414-4889_baoveee.pdf` and the researcher-supplied thesis PDF describe the original two-phase method.

## Business-rule baseline

Follow the researcher command sequence in [FILE-DRIVEN-WORKFLOW.md](docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md). Every command authorizes its operation without extra gate confirmations. Prompt close approves the Draft; repair invocation authorizes the correction. Four research JSON inputs plus a researcher-provided database baseline are required for generation; activation is optional. Internal `gates` fields remain bookkeeping only.

The evaluation baseline identifies all BRs supplied for the active UC. There is no rule-selection mode. Before invoking prompt generation, preparation by the researcher's chosen tool records:

- frozen UC path and SHA-256;
- configured source document/section (or spreadsheet range when applicable);
- exact ordered BR IDs;
- baseline status and freeze time.

This receipt prevents the evaluation inventory from changing after source generation; it is not an approval, selection or semantic restatement of rules. Resolve each listed Rule ID from the checksum-pinned frozen UC.

Before invoking generation, preparation also freezes the ordered IDs of every explicit Basic/Main, Alternative and Exception Flow. Resolve each listed flow from the checksum-pinned frozen UC. A flow is incorrect only when a completion-critical step fails or its specified terminal outcome is not achieved. Flow scoring never changes the BR denominator or BR result.

Configurations freeze `flow_audit_rubric: completion-critical-flow-runtime-v2` before generation. This rubric requires connected integrated-runtime observation for flow `correct`, with evidence linked to UC/run/stage/baseline/source revision. Source findings remain separate; unavailable critical/outcome or connected-runtime proof means `not_evaluable` unless a blocking failure is evidenced. Initial and final use the same rubric. Authorized repair automatically observes every flow on final source before repair closure. When repair is skipped and source is unchanged, the original first-pass assessment remains terminal evidence, preserving its original stage/ID/time; no duplicate assessment is required. Weights, formulas, BR criteria and generation-only timing remain unchanged; the researcher command sequence supplies authorization without extra confirmations.

Flow accuracy retains evaluated-only accuracy/error, coverage, failures and pending targets. Offer researcher verdicts or bounded LLM measurement; persist attributed follow-ups without changing source/telemetry. After saving either path, wait for `$bug-fixing-sub-prompt` if defects remain. Unknown accepted flow verdicts block new repair. All-passing unchanged-source audit records repair unnecessary. Never automatically reopen terminal runs. See the [follow-up contract](docs/00-context/workflow/gates/FLOW-FOLLOWUP-AUTO-REPAIR.md).

The reported experiment flow result follows `accepted-audit-results-v1`: use the latest conclusive accepted verdict per flow across audit stages. Both researcher results and LLM re-audits update canonical JSON directly; repair/source changes or later inconclusive observations do not erase accepted results. Per-flow source/stage provenance and latest-source limitations remain visible. This reporting policy does not change frozen evidence rubrics, BR acceptance, telemetry or gates. Show the selection policy in comparisons.

## Database input

The fifth input is the researcher-prepared MySQL database and `docs/00-context/engineering/schema.dbml`. Configurations pin exactly `migration_head`, `dbml_sha256` and `schema_fingerprint_sha256` inside `database_baseline`; no separate status or manifest. See [database policy](docs/00-context/engineering/DATABASE-SCHEMA.md). Researcher setup builds a complete initial schema with TypeORM migrations and adds migrations between runs only when needed. Each run locks its schema/history/DBML; AI maps existing tables and may perform authorized business DML only. Prompt/Source preflight checks migration history and both hashes before START. Subsequent UCs retain data; changed baselines require new configuration/run identities. Docker setup applies migrations; application rebuilds within a run use `--no-deps backend frontend`.

## System baseline

- Frontend: React 18, TypeScript, Vite, Tailwind, React Router, Axios, Context/Zustand, Recharts.
- Backend: NestJS 11, TypeScript, TypeORM/MySQL, class-validator, Passport JWT, bcrypt and Swagger.
- Runtime: Docker Compose v2 with frontend, backend and MySQL.
- Clean source baseline: `.codex/skills/restore-source-baseline/assets/source-baseline.zip`, with its project-specific asset checksum pinned by `PROJECT_PROFILE.json` as `clean_source_baseline_sha256`.
- API prefix: `/api`.
- Success envelope: `{ success: true, message, data }`.
- Error envelope: `{ success: false, statusCode, message, timestamp, path }`.
- Project-specific domain behavior is supplied only by the active frozen UC/API/Figma/database inputs, not by this shared context file.

The [shared operational constitution](AGENTS.md#shared-operational-constitution) governs every skill, including testing, database mutations, secrets and destructive operations.

Implementation controls such as authentication, hashing, ownership, validation, secret handling, safe errors and transactions remain when required by BRs, APIs or the baseline. They are not treated as a separate experimental dimension.

## Repository map

```text
.codex/skills/                         two-phase workflow and implementation skills
docs/01-inception/use-cases/           frozen source-derived UC/UML/BR specifications
docs/02-construction/coding-prompts/   approved coding-prompt artifacts
docs/02-construction/implementation/   BR baseline, schema, run and repair records
docs/04-experiments/                   canonical run JSON and rendered views
templates/                             artifact contracts
finalsource/fe                         generated React source
finalsource/be                         generated NestJS source
```

## Definition of done

A run is complete only when:

- the approved prompt follows the configured coding-prompt template;
- initial generation telemetry is preserved before repair;
- first-pass generation ends before audit; the subsequent close command preserves telemetry, and the repair command supplies explicit authorization when needed;
- every BR has one `met`, `unmet` or `not_evaluable` assessment with evidence;
- every frozen flow has one `correct`, `incorrect` or `not_evaluable` assessment with evidence;
- every evidenced defect has a bounded repair record or an explicit researcher decision;
- permitted validators, lint/typecheck/build checks pass;
- Docker images are rebuilt from current source and required services are healthy/reachable;
- bounded runtime observation covers the UC trigger, main flow, success and exception behavior;
- the final `finalsource/` hash is frozen.

No test or test-case generation is part of this method.

Telemetry uses prompt/source/repair buckets within the two phases and follows [the command sequence](docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md). Close/report/export turns are excluded. Captures follow `generation_execution_with_repair_audit_v2`: Repair includes integrated BR/flow/runtime verification and final evidence persistence, and a turn's token label must match any captured core execution. Standalone audit remains workflow-only tokens and excluded from counted execution time. Audit and repair verification preserve frozen BR/flow evidence. The existing gate field records completed commands without asking the researcher for further approval.

Missing/null UI scores never block audit, measurements, reports, export or completion. After finalization, `$export-experiment-excel <UC-ID> <LINK_OR_FILEPATH> <TAB_NAME>` is a separate reporting operation that copies stored canonical values into a new workbook while preserving formulas/protected/manual content.

## 100ms setup state

Researcher-authorized database setup on 2026-10-02 supersedes the earlier deferral. MySQL 8.4, TypeORM Initial100msSchema1790916544190, active DBML and the three baseline pins are prepared. The unchanged mysql84-tables-v1 policy excludes procedures/triggers; aggregate capacity/identity guards and full-key idempotency comparison remain later application responsibilities under docs/00-context/engineering/100MS-DATABASE-ADAPTATION.md. Whole-stack Compose waits for migration success before starting backend; application synchronization/automatic migrations stay disabled. The clean baseline has DB infrastructure and a neutral frontend shell, without UC business implementations. Four prepared research JSON inputs remain required before generation, with existing preflight unchanged.

The specification package contains 18 UC files and 15 endpoint contracts (its original README count of 14 is stale). Each UC contains one local UML projection derived from its own unchanged BRs, with only accessed members, required operation signatures, helper definitions and their types. Enum value domains remain complete to preserve OCL semantics. No active UC imports a shared model. `ASSUMPTIONS.md`, OCL utilities and the common API contract remain frozen specification dependencies. The researcher-authorized UML refresh is recorded in `docs/00-context/sources/100ms-local-uml-retrieval.json`; the earlier receipt, source snapshot and previous UML projections remain historical evidence. API paths retain `/api/v1`; downstream errors preserve `code`/`requestId` where supplied while using the repository envelope.

Prompt telemetry close (Turn 2) automatically creates a missing `run-activation.json` from the pinned configuration and approved prompt, or validates an existing receipt without replacing it. The receipt records the actual prompt-close turn/time, before source generation. No standalone activation turn is required.

Desktop design setup completed on 2026-10-02 using explicitly selected frozen dataset 100ms-2026-10-02-001: 74 required nodes and 18 UC mappings; mobile excluded by researcher instruction. Resolve primary and supplementary directories plus the coverage matrix from this exact version. Database preparation is now complete; generation still requires the four prepared research JSON inputs and unchanged mandatory preflight.
