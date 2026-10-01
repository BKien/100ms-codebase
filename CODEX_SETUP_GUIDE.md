# Codex setup guide - Business vibe coding

Setup Review verifies that the research repository and mandatory runtime are available. It does not generate prompts/source, alter frozen UCs, start containers or create/run tests.

## Required read order

1. `AGENTS.md`
2. `PROJECT_PROFILE.json`
3. `PROJECT_CONTEXT.md`
4. `CODEX_SETUP_GUIDE.md`
5. `docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md`
6. `docs/00-context/sources/CONNECTED-SOURCES.md`

## Read-only setup checklist

Run:

```bash
pwd
git status --short
git rev-parse --show-toplevel
git log -1 --oneline
find .codex/skills -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort
find docs/01-inception/use-cases -maxdepth 1 -name 'uc-*.md' -print | sort
docker --version
docker compose version
docker info
```

Expected repository invariants:

- `PROJECT_PROFILE.json` identifies the active project's UC, API and Figma sources without embedding per-UC ranges or counts.
- `PROJECT_PROFILE.json` pins the active project's clean source baseline ZIP with `clean_source_baseline_sha256`; the restore skill contains no project-specific checksum.
- The complete active UC inventory is the set of frozen files matching `docs/01-inception/use-cases/uc-*.md`.
- Each UC contains functional specification, UML Model and Business Rules.
- `docs/01-inception/use-cases/OCL-UTILITY-DEFINITIONS.md` exists when the project's UC source supplies shared OCL utilities.
- Only the two-phase Business Rule workflow and its implementation/audit skills are installed.
- The two-phase commands are `$gen-coding-prompt` and `$gen-source-code`.
- Docker Compose v2 is available; native host Node.js/MySQL is unsupported.

## Local configuration

Read [FILE-DRIVEN-WORKFLOW.md](docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md) for the researcher command sequence. Prepare four research JSON files (Confirmed configuration with per-UC frozen API ID/path/SHA-256 entries, frozen BR/flow baselines and Draft Canonical Run JSON) and the fifth database input under [DATABASE-SCHEMA.md](docs/00-context/engineering/DATABASE-SCHEMA.md). Researcher setup initializes a complete schema through TypeORM migrations on a fresh database and adds migrations between runs only when needed; preserve data between UCs. Capture migration head, DBML hash and runtime fingerprint outside generation and store them in configuration. Generation preflight verifies API and database pins; it never creates schema or asks for schema approval. Generation validates them read-only without extra confirmation or initialization. Prompt close approves the Draft and pins its bytes; activation is optional. Root `.env` is optional preparation convenience. Runtime `finalsource/.env` remains ignored and is prepared only on a setup request, before database preflight; never print secrets.

## Runtime authorization

Do not build/start containers during Setup Review. After explicit researcher authorization:

```bash
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up --build -d
docker compose --env-file finalsource/.env -f finalsource/compose.yaml ps
```

The whole-stack command above is researcher setup outside active runs and executes the migration service. Within a pinned run, after database preflight, rebuild with `up -d --build --no-deps backend frontend`; never invoke setup migrations. Distinguish container state, health and UI/API reachability. Do not run `docker compose down -v` unless the researcher explicitly requests destructive database reset.

## Connected sources

The UC source identified in `PROJECT_PROFILE.json` is required when explicitly refreshing UC/business-rule inputs. Sources may be researcher-provided local Markdown with a byte-exact snapshot and retrieval receipt, or a configured connected spreadsheet. Do not fabricate spreadsheet metadata for local sources. Ordinary Phase 1 uses the frozen repository projection and recorded provenance.

Figma is required only to create/refresh an offline design dataset. Resolve targets through `docs/00-context/FIGMA-LINK-REVIEW.md`.

If connector access fails, mark the source `BLOCKED`; do not scrape or guess.

## Setup report

```markdown
# Setup Review

- Repository: PASS | WARN | BLOCKED
- Required context: PASS | WARN | BLOCKED
- Use-case/UML/BR inputs: PASS | WARN | BLOCKED
- Repo-local skills: PASS | WARN | BLOCKED
- Docker/Compose: PASS | WARN | BLOCKED
- Local configuration: PASS | WARN | BLOCKED
- Connected sources: PASS | NOT_APPLICABLE | BLOCKED
- Runtime: NOT_RUN | PASS | BLOCKED
- Git safety: PASS | WARN | BLOCKED

Overall: READY | READY_WITH_WARNINGS | NOT_READY
Next action: <one concrete action>
```

`READY` means the environment can execute the two-phase method; it does not mean generated source satisfies Business Rules.

## Supplementary researcher output

- `$export-experiment-excel <UC-ID> <LINK_OR_FILEPATH> <TAB_NAME>`: after workflow finalization, invoke separately with exactly three positional arguments (quote paths/tab names containing spaces). It dynamically maps every result heading against canonical JSON, including recorded BR/flow/repair and optional UI data, and saves a new filled copy plus provenance. Unavailable values become N/A; formulas and protected/manual content remain unchanged. No additional prose or clarification is required.

Figma/UI accuracy may be inspected manually. All UI fields may be missing/null without blocking validation or reports. Excel export remains reporting-only.

Prompt telemetry close (Turn 2) automatically creates a missing `run-activation.json` from the pinned configuration and [approved prompt](docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md), or validates an existing receipt without replacing it. The receipt records the actual prompt-close turn/time, before source generation. No standalone activation turn is required.
