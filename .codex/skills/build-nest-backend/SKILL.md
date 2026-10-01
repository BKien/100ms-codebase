---
name: build-nest-backend
description: Build or review NestJS 11, TypeScript and TypeORM/MySQL backend code from the approved prompt against the researcher-pinned database.
---

# Build Nest Backend

Apply the [shared operational constitution](../../../AGENTS.md#shared-operational-constitution).

Read [the approved prompt](../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md), project context, existing application codebase and `docs/00-context/engineering/TECHNICAL-STACK-RULES.md`. Inspect `finalsource/be/package.json` and its lockfile, then extend existing modules under `finalsource/be`.

Implement all applicable Basic/Main, Alternative and Exception Flows. BR/flow audit and authorized repair subsequently use the complete frozen evaluation baseline. See [shared contract](../../../docs/00-context/workflow/WORKFLOW-CONTRACT.md).

Load only the references required by the active change areas:

- Nest module, controller or service: [references/nest-rules.md](references/nest-rules.md)
- DTO, validation or backend typing: [references/typescript-validation.md](references/typescript-validation.md)
- Entity, repository, MySQL or transaction: [references/typeorm-mysql.md](references/typeorm-mysql.md)
- Existing database/entity mapping: [references/database-schema-template.md](references/database-schema-template.md)
- JWT, Passport, bcrypt, configuration or OpenAPI: [references/auth-config-openapi.md](references/auth-config-openapi.md)

- Keep controllers thin; enforce business/ownership rules in services and persistence constraints where explicitly required.
- Use validated DTOs, injected repositories, standard response/error handling and existing authentication/configuration mechanisms.
- Read the configured checksum-valid DBML and [database contract](../../../docs/00-context/engineering/DATABASE-SCHEMA.md). Map entities to existing names/types/keys exactly. Use `synchronize: false` and application `migrationsRun: false`. Missing necessary structure blocks work under the database policy's restart procedure; no schema proposal or approval gate exists.
- Preserve application controls required by the UC/BR/API, including authentication, hashing, ownership, validation, secrets, safe errors and transactions.
- Do not invent endpoints, rules, dependencies, schema or policies.
- Run only permitted non-test lint/typecheck/build checks.
