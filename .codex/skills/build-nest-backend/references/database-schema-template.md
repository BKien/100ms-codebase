# Existing database mapping reference

Follow `docs/00-context/engineering/DATABASE-SCHEMA.md`. The configured DBML is the researcher-provided structure. Preserve its exact names and definitions.

Map required TypeScript properties to existing table/column names, types, null/default behavior, keys and FK actions. Implement compatible behavior in application code. Keep ownership, sensitive-field selection and API exposure explicit.

Use `synchronize: false` and application `migrationsRun: false` under the [shared operational constitution](../../../../AGENTS.md#shared-operational-constitution). Report incompatible requirements with the exact table/column/constraint involved.
