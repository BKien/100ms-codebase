# TypeORM 0.3 and MySQL rules

## Entity and repository

- Register every entity through the existing Nest/TypeORM configuration and give every entity a primary column.
- Map nullability, uniqueness, precision/scale, length, relation ownership and `onDelete` exactly from the configured DBML. Do not invent or broaden cascades.
- Inject the entity repository using established Nest patterns. Use repository/find options or QueryBuilder parameters, never SQL string interpolation.
- Map DTO fields explicitly. Do not pass untrusted request objects directly into `save`/`update`.
- Scope owned-resource queries by both resource identifier and authenticated owner identifier where possible.
- Select only required columns and constrain pagination, sort columns and relation loading.

## Transactions and concurrency

- Use a transaction when one business operation performs multiple dependent writes or state changes.
- Inside a TypeORM transaction use only the provided transactional entity manager/repositories, never the global manager/repository.
- Choose isolation, locking and idempotency only from explicit UC/Business Rule requirements. Handle duplicate/deadlock outcomes without exposing database errors.
- Use `synchronize: false` and application `migrationsRun: false` under the [shared operational constitution](../../../../AGENTS.md#shared-operational-constitution). Entity edits map existing tables.

## MySQL

- Preserve supplied database types and numeric precision; report incompatible requirements.
- Use existing constraints and required application enforcement. Missing necessary structure is an input blocker.
- Use existing indexes.
- Keep timestamps/timezone semantics explicit and consistent with the API contract.

Official basis:

- https://typeorm.io/docs/entity/entities/
- https://typeorm.io/docs/relations/relations/
- https://typeorm.io/docs/transactions/
- https://typeorm.io/docs/working-with-entity-manager/repository-api/
- https://dev.mysql.com/doc/refman/8.4/en/optimization-indexes.html
- https://dev.mysql.com/doc/refman/8.4/en/innodb-storage-engine.html
