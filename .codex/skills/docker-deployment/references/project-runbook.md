# Business Vibe Coding Docker runbook

- Compose root: `finalsource/compose.yaml`
- Configuration: `finalsource/.env` created from the committed example after researcher authorization.
- Services: MySQL, one-shot TypeORM migration setup, NestJS backend and React/Nginx frontend.
- Use Compose v2 only; no native host fallback.
- The researcher supplies reviewed TypeORM migrations and the consolidated DBML. Follow `docs/00-context/engineering/DATABASE-SCHEMA.md` for setup, migration history checks and capturing the three pins, and the [shared operational constitution](../../../../AGENTS.md#shared-operational-constitution) for mutation boundaries. Verify existing pins with the helper.

Researcher setup outside active runs:

```text
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up -d --build
```

After adding a reviewed migration between runs, build the migration image, start/check database health, and recreate the one-shot service:

```text
docker compose --env-file finalsource/.env -f finalsource/compose.yaml build migration
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up -d database
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up --no-deps --force-recreate --exit-code-from migration migration
```

The last command requires a healthy database. A failed migration blocks startup; MySQL DDL may have committed partially. Do not automatically revert, retry destructive DDL, fake history or reset data. Preserve logs and report the failure for researcher resolution.

For an existing pinned run, verify the database baseline and then rebuild applications without invoking migrations:

```text
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up -d --build --no-deps backend frontend
```

Database must already be healthy. Verify backend/frontend health separately after this command.

Review with `docker --version`, `docker compose version`, daemon status and Compose configuration. In authorized run mode, build from current source, start the stack, then verify containers, healthchecks, frontend reachability, backend health, and the bounded UC checkpoints required by the active prompt.

Common URLs use the configured ports: frontend root, backend `/api/health`, Swagger `/docs`, and OpenAPI `/docs-json`. Persist sanitized evidence under the shared operational constitution.
