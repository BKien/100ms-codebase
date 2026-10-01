# Authentication, configuration, hashing and OpenAPI rules

## Authentication and authorization

- Keep authentication in Passport/JWT guards/strategies and authorization/ownership in guards or services according to the existing architecture.
- Extract subject identity only from the verified JWT; never trust a client-provided owner/user ID.
- Validate JWT algorithm, expiry and approved issuer/audience policy. Load signing secrets from validated configuration; never use fallback secrets.
- Return generic authentication failures that do not reveal account existence.
- Hash passwords with the existing bcrypt package and an approved cost. Compare through bcrypt; never decrypt, truncate or pre-hash passwords insecurely.

## Configuration

- Use `@nestjs/config` and validate required environment variables at startup. Keep production defaults fail-closed.
- Configure least-privilege CORS and production-safe logging/error behavior under the [shared operational constitution](../../../../AGENTS.md#shared-operational-constitution).
- Do not enable debug output in production.

## Swagger/OpenAPI

- Keep route, DTO, status and auth documentation aligned with implementation using `@nestjs/swagger`.
- Document safe request/response DTOs and expected error statuses; never expose password/hash/internal entity fields in schemas/examples.
- Do not make an internal route public merely to make it visible in Swagger.

Official basis:

- https://docs.nestjs.com/security/authentication
- https://docs.nestjs.com/security/authorization
- https://docs.nestjs.com/security/encryption-and-hashing
- https://docs.nestjs.com/techniques/configuration
- https://docs.nestjs.com/openapi/introduction

