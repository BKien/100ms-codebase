# Two-phase Business Vibe Coding method

## Phase 1 — Generate Business Coding Prompt

Inputs: frozen UC/UML, ordered checksum-pinned API contracts, applicable frozen Figma sources, existing project context, prepared artifacts and [the configured template](../../../templates/construction/coding-prompt.template.md) under the workflow input boundaries.

1. Verify provenance and checksum of the UC projection and the configured Frozen identity/path/SHA-256 of every referenced API contract.
2. Resolve the configured coding-prompt template and its permitted generation inputs.
3. Validate the existing BR/flow baselines and Canonical Run JSON prepared by the researcher's chosen tool before invocation. Missing or invalid inputs stop generation; no creation skill is mandatory and preflight never creates them.
4. The AI analyzes the validated inputs and authors the complete Draft prompt following the configured coding-prompt template.
5. The prompt-close command approves and pins the prompt, without another gate.

## Phase 2 — Generate Source Code

Inputs: [approved prompt](../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md), existing codebase, configuration-pinned DBML and existing MySQL schema, and project rules. Database preflight verifies migration history and file/runtime pins. Schema is immutable within a run: no proposal/approval, migrations or DDL; allow only compatible mappings and authorized business DML. Researcher setup may add migrations between runs; a changed baseline requires a new configuration/run.

1. Validate the pinned configuration and approved prompt for exactly one run; activation is optional. Then capture model/time metadata.
2. Generate only the source needed for the UC.
3. Preserve first-pass evidence, stop, and close source telemetry in the subsequent command turn. The audit command then assesses every frozen BR/flow.
4. On the subsequent repair command, create bounded sub-prompts for evidenced defects, apply corrections and automatically verify final BR/flow/runtime evidence.
5. Complete permitted lint/typecheck/build and Docker runtime observations; do not create or run tests.
6. Freeze the final source hash and finalize the run record.

This is a two-phase research workflow, not an enterprise AI-DLC process.
