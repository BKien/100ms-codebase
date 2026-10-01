# TypeScript and Vite 8 rules

## TypeScript

- Preserve `strict` behavior. Model nullable/optional states explicitly and narrow `unknown` before use.
- Do not use `any`, boxed primitives (`String`, `Number`, `Boolean`, `Object`), non-null assertions or unsafe casts without a documented boundary reason.
- Define domain/API types near the API layer; keep component props specific and readonly where practical.
- Use discriminated unions for multi-state flows and exhaustive switches for business-sensitive variants.
- Prefer inference for local obvious values; annotate exported contracts, function boundaries and ambiguous return types.
- Avoid TypeScript `enum` when the codebase uses string unions; follow the existing convention consistently.

## Vite

- Use `import.meta.env`; type custom client variables in `vite-env.d.ts`.
- Treat every `VITE_*` value as public because it is bundled into client code. Apply the [shared operational constitution](../../../../AGENTS.md#shared-operational-constitution) to client configuration.
- Parse env strings explicitly into validated booleans/numbers/URLs. Do not rely on truthiness of string values.
- Keep `.env.*.local` ignored. Provide placeholders only in `.env.example` when requested.
- Use static ESM imports and project aliases already configured. Do not add Vite plugins without an explicit need and dependency approval.

Official basis: TypeScript strictness and type guidance, Vite environment behavior:

- https://www.typescriptlang.org/docs/handbook/2/basic-types.html
- https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html
- https://vite.dev/guide/env-and-mode
