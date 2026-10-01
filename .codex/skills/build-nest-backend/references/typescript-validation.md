# Backend TypeScript and validation rules

## TypeScript

- Preserve strict typing. Avoid `any`, unsafe casts, non-null assertions and boxed primitive types.
- Type public service return values and external boundaries. Narrow caught errors from `unknown`.
- Use readonly DTO properties where mutation is unnecessary; use string unions/project enums consistently.
- Separate input DTO, persistence entity and safe response DTO when their field sets or trust levels differ.

## Nest ValidationPipe and class-validator

- Use DTO classes with focused decorators for type, length, enum, numeric range, date and nested constraints.
- Configure global validation with `transform: true`, `whitelist: true` and `forbidNonWhitelisted: true`; retain `forbidUnknownValues` unless an approved compatibility reason exists.
- Add `@Type` for nested/converted values where class-transformer requires it; do not assume query strings are numbers/booleans.
- Do not use `skipMissingProperties` for create DTOs. For updates, use explicit optional/mapped fields while retaining constraints.
- Avoid exposing rejected values or DTO targets in production validation errors when they contain sensitive data.
- Validation enforces shape; services still enforce business rules, object ownership and database-dependent uniqueness.

Official basis:

- https://www.typescriptlang.org/docs/handbook/2/basic-types.html
- https://docs.nestjs.com/techniques/validation
- https://github.com/typestack/class-validator

