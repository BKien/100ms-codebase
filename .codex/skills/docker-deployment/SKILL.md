---
name: docker-deployment
description: Review whether a research environment can install and run Docker, initialize local FE/BE/MySQL configuration, run Compose when explicitly authorized, diagnose deployment failures, and persist sanitized environment history. Use for setup review, Docker installation, project startup, health checks, deployment troubleshooting, or resuming a failed deployment; do not use to generate features.
---

# Guide Docker Deployment

Apply the [shared operational constitution](../../../AGENTS.md#shared-operational-constitution).

Read the shared timing protocol. Standalone deployment/setup/runtime contributes no generation execution seconds. End core segments before waiting; final token calculation belongs to a later confirmed telemetry gate, not a researcher-invoked skill.

Always read `AGENTS.md`, the artifact/context policy, `finalsource/compose.yaml`, affected Dockerfiles/env examples and only the selected mode section of `references/project-runbook.md`. Read `CODEX_SETUP_GUIDE.md` only for fresh setup/install/initialize. Read `PROJECT_CONTEXT.md` only when a research invariant cannot be resolved from `AGENTS.md`. Read `environment-current.json` when present; otherwise treat current state as unknown and create it from its template when persisting the first result. For troubleshooting, query `incidents/index.json` when present and read only a matching incident. Read only the current state and the incident records needed for the requested operation.

## Select the mode

- `review`: run read-only environment/repository checks and report `PASS`, `WARN` or `BLOCKED`. Do not install, configure, build or start anything.
- `initialize`: after researcher authorization, create missing local FE/BE/MySQL configuration from committed examples, validate presence/format without exposing values, and provide the researcher with exact next steps.
- `run`: after researcher authorization and valid configuration, build/start Compose, inspect service health and verify UI/API evidence.
- `troubleshoot`: inspect sanitized evidence, match prior incident fingerprints, make only deployment/config/source fixes explicitly authorized by the request, rerun the smallest relevant check and record the outcome.

If the request is ambiguous, begin with `review`. Ask before the first package installation, GUI launch, `.env` creation, image build, container start, or material configuration/source edit.

## Review the machine

1. Identify OS, architecture, available memory/disk and virtualization/container constraints using read-only commands from `references/environment-checks.md`.
2. Check Git root/status, Docker CLI, Compose v2 and daemon separately. Missing Compose v2 or an unavailable daemon is always `BLOCKED`; native Node.js/MySQL is not a supported fallback.
3. Determine the supported installation path. Guide the researcher to the official installer/package for the target OS; do not download or install software without explicit approval. Do not silently fall back to native Node/MySQL.
4. Check the project Compose structure and whether `finalsource/.env` is absent, ignored and untracked. Never print its values.
5. Replace `environment-current.json` with the latest sanitized snapshot and append one small operation JSON under `operations/`. Do not copy raw successful output.

## Initialize safely

1. Require authorization before creating `finalsource/.env` from `finalsource/.env.example`.
2. Require the researcher to replace `MYSQL_PASSWORD` and `JWT_SECRET`; never invent, display or log their values. Validate only presence, placeholder rejection and JWT minimum length.
3. Confirm `finalsource/.env` is ignored and not tracked. Stop if a secret-bearing file is tracked.
4. Validate Compose interpolation with the env file. Do not start containers in initialize mode unless the researcher also requested `run`.
5. Explain that the mandatory Docker runtime uses only `finalsource/.env`. Do not create or use per-app env files or native Node.js/MySQL commands as a fallback; they must not override Compose networking.
## Run and verify

Follow [database policy](../../../docs/00-context/engineering/DATABASE-SCHEMA.md). The researcher prepares a complete initial schema with TypeORM migrations and maintains `docs/00-context/engineering/schema.dbml`. Between runs, reviewed migrations may add necessary structure while retaining data. In researcher-authorized setup, whole-stack Compose creates an empty database on a fresh volume, runs the one-shot migration service and starts backend only after success. For later migrations, rebuild/recreate that service as documented in the runbook; do not assume a previously exited container applied new files. During preparation use `experiment-input-helpers/calculate_input_values.py` with the active UC/API/Figma arguments and `--require-empty` (omit emptiness between UCs) to print migration head, DBML hash and fingerprint with the other objective input values. For a pinned run use `database_baseline.py --configuration <path>` to verify them. Within Prompt/Source/Audit/Repair, build/start backend/frontend using `--no-deps`. Missing schema blocks the run and requires researcher setup/new configuration before restart. Use application `synchronize: false` and `migrationsRun: false`. Metadata access uses container-root internally; application operations use the backend account. Claim DML-only privileges only when verified.

1. Use the explicit root command from `references/project-runbook.md`; never depend on the current directory implicitly.
2. Build/start only after authorization under the shared operational constitution.
3. Inspect `docker compose ps`, database/backend/frontend health and bounded logs. Redact credentials, tokens, account data and sensitive payloads before reporting or persisting evidence.
4. Verify three distinct outcomes: containers running, healthchecks passing, and the UI/API reachable. Do not infer one from another.
5. Record a compact operation JSON. On failure, update `incidents/index.json` and one fingerprint-addressed incident JSON using `references/history-contract.md`.

## Troubleshoot one failure at a time

1. Search `incidents/index.json` before collecting new evidence; read only a matching incident record.
2. Capture the smallest bounded evidence: affected service status, last relevant log lines, Compose config, port ownership or build output. Do not copy complete logs into the repository.
3. Classify the layer: host/Docker, Compose/env, database, backend build/start/health, frontend build/Nginx/health, proxy/network, port or browser.
4. State the root-cause hypothesis and evidence. Apply the smallest authorized correction; do not change application behavior merely to make a container healthy.
5. Rerun only the failed stage, then verify downstream health. Record resolved, unresolved or blocked with a reusable fingerprint.

## Boundaries

- Do not edit immutable `docs/01-inception/use-cases/uc-*.md` files.
- Do not claim Business Rule compliance from successful deployment alone; per-rule conclusions require the audit workflow.
- Keep canonical current state and indexed incident evidence in `docs/03-audit/docker-deployment/`.
- Persist only command identifier, exit code, timestamp, tool version, source hash and a bounded relevant error excerpt; never persist successful raw transcripts or complete build logs.
