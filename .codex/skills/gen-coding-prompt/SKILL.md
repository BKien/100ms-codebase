---
name: gen-coding-prompt
description: Generate the configured coding prompt from validated, pre-existing experiment inputs and one frozen UC; never initialize configuration/baselines/trackers.
---

# Generate Business Coding Prompt

Apply the [shared operational constitution](../../../AGENTS.md#shared-operational-constitution).

Accept one readable `docs/01-inception/use-cases/uc-*.md` path. Optional `--configuration <config.json>`, `--run-id <RUN-ID>`, `--run-json <canonical.json>` and `--variant <configured-variant>` disambiguate existing inputs; explicit values must match their recorded identities. Resolve only a unique matching Canonical Run JSON. Never select the newest file.

Read [configuration input contract](../../../docs/00-context/workflow/gates/EXPERIMENT-CONFIGURATION-GATE.md), [workflow contract](../../../docs/00-context/workflow/WORKFLOW-CONTRACT.md) and [execution timing protocol](../measure-uc-workflow/references/phase-ledger-schema.md).

## Read-only preflight

Before START, require four prepared research JSON inputs (Confirmed configuration, frozen BR baseline, frozen flow baseline and Draft Canonical Run JSON) plus the fifth input: the researcher-provided database baseline. Configuration pins `database_baseline.migration_head`, `dbml_sha256` and `schema_fingerprint_sha256`, with no separate database status. Canonical draft state is `run_status: draft`, with `coding_prompt: null`, `metrics: null` before first measurement, and initial gates at `prompt` with empty history. Resume only an open prompt phase with valid existing evidence.

The researcher may prepare these files manually, with another model, external Python or optional repository helpers. Validate their contents, identities and checksums; never require a particular creator, skill invocation, creation command or fabricated creation receipt. Configuration has no confirmation gate or summary for approval. Root `.env` is not required.

Resolve an available Python executable and run this read-only command, supplying explicit selection arguments when available:

```text
<python-executable> .codex/skills/gen-coding-prompt/scripts/preflight_configuration.py --uc-id <UC-ID> --run-json <canonical.json> --use-case <use-case.md>
```

Both baselines and the Canonical Run JSON are mandatory on every invocation, with all required fields. Missing, malformed, ambiguous or conflicting inputs stop the turn immediately with the exact file/field/checksum error. Do not create, fill, normalize, repair, replace or initialize any of the four inputs during preflight or prompt generation. Do not invoke baseline generation or activation creation to fill a gap.

Referenced provenance, frozen UC, checksum-pinned API/Figma and template dependencies must also exist and validate under their existing contracts; they are not silently generated as a workaround. If a checksum-normalization receipt is required by the existing UC contract, it must already exist.

## Generate the Draft

The same preflight imports `database_baseline.py` internally to verify the ordered TypeORM migration history, DBML bytes and live MySQL metadata against the configured pins. Follow [database policy](../../../docs/00-context/engineering/DATABASE-SCHEMA.md). Require an initialized running Compose database and `finalsource/.env`; root `.env` remains unnecessary. Missing/mismatched input blocks before START. After PASS, read DBML once as technical input and use its exact structure wherever [the configured template](../../../templates/construction/coding-prompt.template.md) or applicable input contract requires it. Follow the database policy's missing-schema procedure: close an open interval before waiting, preserve partial evidence, and require a new configuration/run if researcher setup changes the baseline.

1. Read `PROJECT_CONTEXT.md`, source/workflow rules and the configured template: `templates/construction/coding-prompt.template.md`.
2. Verify frozen UC provenance and the exact source path returned by preflight. Read only the ordered API contract paths returned from the pinned configuration after preflight has matched their IDs to the frozen UC and verified their Frozen identity and SHA-256. Resolve frozen Figma evidence through `resolve-figma-design-dataset` in read-only resolution mode. Missing or changed dataset/API evidence stops generation; no capture, refresh or helper-file setup occurs here.
3. Use the read-only preflight result for prepared-input integrity. Preserve those inputs unchanged. Verify complete Main/Alternative/Exception Flow coverage against the frozen UC.
4. Once all input checks pass, immediately capture live prompt START. Analyze the provided functional UC/UML/API/Figma inputs and configured DBML; map every frozen-UC flow and terminal outcome to the applicable sections defined by the configured coding-prompt template. Preserve source provenance and apply the standard response envelope without changing domain status, fields or message semantics.
5. The AI must reason over the validated provided inputs and author the complete coding prompt itself, following `templates/construction/coding-prompt.template.md`. Fill `prompt_variant` metadata from the pinned configuration, treating its value as an opaque identity rather than an instruction about prompt content. The configured template defines the prompt's sections, content and instructions, subject to the shared operational constitution and input contracts. Read-only preflight, timing and post-generation validation tools remain required; they do not generate prompt content.
6. Persist the Draft at `docs/02-construction/coding-prompts/<UC-ID>-business-coding-prompt.md`, including `source_api_contracts` as the semicolon-separated ordered configured API paths. Immediately capture END, then run `scripts/validate_prompt_contract.py --configuration <config.json> --uc-id <UC-ID> --run-id <RUN-ID> --prompt <prompt.md> --allow-draft`. Recheck configuration with preflight `--expected-checksum <original checksum>`; review semantic flow coverage and provenance. Any unresolved anomaly prevents reporting success.
7. Present the Draft and next command `$measure-uc-workflow close-phase prompt_generation`. That command approves/pins the Draft and closes telemetry without another confirmation. Do not start source here.

The existing timing helper appends actual timestamps to its runtime journal after successful input validation. This is measurement evidence, not initialization of the four configuration inputs. Preflight must not mutate the Canonical Run JSON; later approval/audit/measurement operations may update its results normally. Whole-turn token telemetry still includes reads, validation and timestamp calls; never invent a token deduction or promise zero measurement overhead.
