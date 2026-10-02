# Prepared 100ms database infrastructure

Researcher-authorized setup on 2026-10-02 creates the complete 16-table MySQL 8.4 baseline through Initial100msSchema1790916544190. The application opens the prepared database and its health endpoint checks SELECT 1. There are no UC business implementations or seeds. Application synchronization and automatic migrations remain disabled; the setup-only CLI uses typeorm_migrations.

The repository-priority adaptation uses mysql84-tables-v1 without triggers/routines. Read docs/00-context/engineering/100MS-DATABASE-ADAPTATION.md and the active schema.dbml from the repository root. Aggregate guards, immutable membership identity, full-key idempotency equality and SERIALIZABLE session locking belong to later UC application implementation. The generated digest lookup index is deliberately non-unique.

Whole-stack Compose runs setup migration before backend. Within a pinned experiment run, rebuild only backend/frontend with --no-deps. Applied migrations are append-only. No reset, revert, DDL or migration execution is authorized during a run. The source baseline ZIP includes this infrastructure and never resets database data.
