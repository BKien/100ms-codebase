# NestJS 11 architecture and coding rules

## Structure and naming

- Keep source under `finalsource/be/src`. Organize business capabilities under `modules/<feature>/` with module, controller, service, DTOs and entity only when the feature owns persistence.
- Use PascalCase for classes/types, camelCase for methods/variables, kebab-case for folders, and suffixes `.controller.ts`, `.service.ts`, `.module.ts`, `.entity.ts`, `.dto.ts`.
- Use explicit imports and constructor injection. Avoid circular dependencies; do not reach into another module's internal files when it can export a provider.

## Layer responsibilities

- Controller: bind HTTP method/path, receive decorated parameters/DTOs, call a service and return the project response envelope. Keep business/persistence logic out.
- Service/provider: own business rules, authorization/ownership decisions, orchestration and transaction boundaries.
- Repository/TypeORM: own persistence expressions. Do not expose entities directly as public response contracts when fields differ.
- DTO class: define runtime-validatable inbound structure. Do not use erased TypeScript interfaces for ValidationPipe inputs.
- Module: import/export only required capabilities. Keep providers singleton/stateless unless a documented scope is required.

## Error and async conventions

- Use `async`/`await` and explicit `Promise<T>` on exported service/controller methods when helpful. Never leave floating promises.
- Throw Nest HTTP exceptions or domain errors mapped by the global filter. Do not construct ad-hoc status responses or mix standard handling with raw `@Res()` without a specific need.
- Return the established `{ success, message, data }` envelope and safe error format. Never leak stack/SQL/internal messages.

Official basis:

- https://docs.nestjs.com/controllers
- https://docs.nestjs.com/providers
- https://docs.nestjs.com/modules

