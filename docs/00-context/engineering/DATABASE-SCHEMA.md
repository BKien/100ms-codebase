# Researcher-managed database baseline

The database is the fifth prepared input alongside the four research JSON inputs. Keep NestJS, TypeORM and MySQL 8.4. Design the initial schema as completely as possible from known requirements. TypeORM migrations create application tables and retain the history of necessary changes; do not create an empty migration for every UC. The researcher may evolve the schema between runs. From a run's first START through finalization its database baseline is immutable. Retain accumulated application data between cumulative UCs.

## Configuration contract

Experiment Configurations require exactly:

```json
"database_baseline": {
  "migration_head": "InitialSchema1790000000000",
  "dbml_sha256": "sha256:<64 lowercase hex characters>",
  "schema_fingerprint_sha256": "sha256:<64 lowercase hex characters>"
}
```

`migration_head` is the exact TypeORM migration class name, including its 13-digit timestamp. DBML always lives at `docs/00-context/engineering/schema.dbml`. Use the configuration's existing Confirmed status; no database status, manifest or extra confirmation gate. Never rewrite pins in frozen configuration, run evidence or activation receipts. A baseline change requires a new configuration identity and run.

The DBML hash covers exact bytes, including line endings. The runtime fingerprint covers normalized MySQL metadata. These independently verify the prepared inputs; matching both does not prove DBML and MySQL were semantically equivalent when prepared. The researcher reviews that correspondence before capture. Never derive replacement expected pins from an unverified database during preflight.

## Schema files and history

- `finalsource/be/src/database/migrations/<13-digit-timestamp>-<Name>.ts`: one exported `Name<timestamp>` class implementing `MigrationInterface`, with `up` and `down`. Keep timestamps unique and increasing. Do not override the instance name with a different value.
- `finalsource/be/src/database/migration-data-source.ts`: setup-only CLI connection; migrations use the `typeorm_migrations` table.
- TypeORM entities: backend mappings to existing tables. Correcting a mapping does not authorize changing the database.
- `docs/00-context/engineering/schema.dbml`: researcher-maintained, consolidated application schema at the selected migration head. Document keys, defaults, lengths, nullability and FK actions accurately.

Commit reviewed migration files and DBML with their UC/reason. Applied migrations are append-only: create a new migration instead of editing an applied file. TypeORM's table stores names/timestamps, not file checksums or a failed-migration journal. Git preserves reviewed file history; the runtime fingerprint detects structural drift. Check the complete ordered applied history against prepared files, not just the last name. Use the repository revision for the selected UC: no future pending migrations during generation.

## Researcher setup in Docker

Prepare `finalsource/.env` from the existing example. On a fresh volume, the MySQL image creates an empty database using `MYSQL_DATABASE`. A one-shot Compose `migration` service waits for MySQL health and runs `migration:run`; backend waits for migration success. Application startup keeps `synchronize: false` and `migrationsRun: false`. No separate SQL initializer is used.

Outside measured runs, from the repository root:

```text
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up -d --build
docker compose --env-file finalsource/.env -f finalsource/compose.yaml ps --all
```

To apply a new researcher-reviewed migration between runs, rebuild the migration image and explicitly recreate its one-shot service so a previously completed container is not mistaken for a new execution:

```text
docker compose --env-file finalsource/.env -f finalsource/compose.yaml build migration
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up -d database
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up --no-deps --force-recreate --exit-code-from migration migration
```

Wait for database health before the last command. Inspect the exit code, then capture pins and start the application. No concurrent DDL, migration execution or active UC is allowed during setup. A nonzero migration exit blocks application startup. MySQL DDL can commit partially: inspect and resolve a failed migration outside generation; never claim automatic rollback or mark it applied manually. An existing database with application tables but no migration history is not automatically adopted. Back it up and use an explicitly authorized fresh database or a researcher-reviewed adoption procedure; never reset it silently.

Available npm commands are `migration:create`, `migration:generate`, `migration:run`, `migration:revert` and `migration:show`. CLI execution uses compiled `dist` files in the Docker image. Create/generate commands need an explicit output path; rebuild before running new migrations. A generated migration compares all loaded entities with the database, so review every statement and discard unrelated changes. Manual migration creation is supported. Reverting can delete data and needs explicit researcher authorization; never use it to make an audit pass.

To save a newly created migration on the host, run from `finalsource/` with a writable source-directory mount (researcher setup only):

```text
docker compose run --rm --no-deps -v ./be/src/database/migrations:/app/src/database/migrations migration npm run migration:create -- src/database/migrations/UC02Change
```

Replace the example name with the actual change. To generate from reviewed entity changes, first rebuild the migration image, then use the same mount and `migration:generate` command with the same output-path argument against the prepared running database. Review the generated SQL before execution. Changes written only inside a disposable container would otherwise be lost.

## Capture and read-only validation

After reviewing DBML and the migrated database, obtain the three database pins as part of the combined researcher-side input calculation:

```text
<python-executable> experiment-input-helpers/calculate_input_values.py --use-case <frozen-uc.md> --api-contract <frozen-api.md> --figma-dataset-version <version> --require-empty
```

Repeat `--api-contract` in the UC's declared order when it references multiple APIs. This prints the three database configuration fields together with the other objective input values, without writing files or invoking an LLM. `--require-empty` checks application tables only; migration history must contain records. Omit this option between cumulative UCs. The helper never starts containers, runs migrations or resets data. Root `.env` is unused. Copy reviewed pins into a new configuration and pin that configuration in its Canonical Run JSON.

Prompt/Source call the existing `preflight_configuration.py`; it imports the helper internally before START. Offline validation checks the three fields, DBML checksum, named migration and disabled application sync/automatic migrations. Runtime validation reads the ordered `typeorm_migrations` history, rejects pending/missing/extra/reordered migrations, compares the configured head and fingerprints the live schema. It checks migration files/history again during inspection. Missing inputs, connection errors or drift block with a concise error and never trigger setup. Read DBML once after PASS, without dumping SQL or metadata into model context.

The START capture helper also revalidates preflight. Preserve existing token labels and timing boundaries: actual whole-turn overhead remains counted under the existing accounting rules; no estimates or token deductions. Measure, activation and export do not query MySQL.

Audit/Repair verify before observation/correction and after integrated verification:

```text
<python-executable> .codex/skills/gen-coding-prompt/scripts/database_baseline.py --configuration <pinned-configuration.json>
```

For application rebuilds within a pinned run, after successful preflight use:

```text
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up -d --build --no-deps backend frontend
```

Do not invoke whole-stack `up`, the `migration` service or migration npm commands inside Prompt/Source/Audit/Repair. `--no-deps` avoids starting the setup migration service; verify backend/frontend health separately afterward. The database must already be running. Never silently change the three pins to accept drift.

## Missing schema during a run

Report the exact missing/conflicting table, column, relationship or constraint with the requirement that needs it. Distinguish a schema gap from a wrong query/entity/service; fix compatible application code under its existing authorization. A genuine schema gap blocks work. AI must not create or run a migration, edit DBML or request permission to mutate the active run's database.

If a core interval is open, record its actual END before waiting, preserve partial source and evidence, and record the blocked outcome using the existing run-status contract. Do not fabricate successful completion. The researcher decides whether a migration is necessary, prepares/applies it outside the run, updates DBML and captures new pins. Use a new configuration/run identity after any pinned baseline change; never splice pre-change and post-change telemetry. Preserve the interrupted attempt and restore/review its source input before a new run so partial generated code is not silently inherited. If preflight blocked before START, no core interval is invented.

## Source and data boundaries

- AI may read DBML/migrations and map entities/queries to exact existing tables, keys and types. It must not edit migration files, CLI schema infrastructure, DBML or live schema during generation/audit/repair.
- Allow authorized business SELECT/INSERT/UPDATE/DELETE and transactions. Never seed, truncate, reset or erase data just to make an audit pass.
- Keep `synchronize: false` and application `migrationsRun: false`. Docker migration execution belongs only to researcher setup outside runs.
- A later UC may retain the same migration head if no schema change is needed. Matched runs for the same UC use matching migration history, DBML hash, schema fingerprint and the agreed starting-data protocol on independent runtime state.
- Reset a volume only on explicit researcher instruction. Source baseline restoration preserves database infrastructure and never resets MySQL.
- Fingerprinting is detection, not privilege enforcement. Do not claim DDL is technically impossible without checking account grants.

## Fingerprint protocol: mysql84-tables-v1

Keep the same normalized metadata algorithm for capture and verification. Container-root metadata access avoids incomplete application-account visibility; credentials never appear in output. Backend and migration Compose settings must target the inspected database, and the running backend is checked when present.

Include schema name/default charset/collation, case policy, base table options, columns/order/types/defaults/nullability/generated expressions/SRID, ordered indexes, PK/unique/FK/CHECK constraints, FK actions and partitions. The migration table's structure is included; its records are checked separately. Exclude business records, physical sizes, cardinality, timestamps, auto-increment counters, comments and MySQL patch version. Require MySQL 8.4. Views, triggers, routines and events remain unsupported and block validation. Equivalent database instances intentionally share a fingerprint. Emptiness is verified separately.

References: https://typeorm.io/docs/advanced-topics/migrations/ and https://dev.mysql.com/doc/refman/8.4/en/information-schema.html . The helper accepts the Compose v2-compatible CLI (major 2 or 5).
