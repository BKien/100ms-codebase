# Technical-stack skill routing

Persistence follows [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md): read the configured DBML and map existing structure. Keep `synchronize: false` and application `migrationsRun: false`. Researcher setup alone may execute TypeORM migrations between runs; generation/audit/repair cannot edit or execute them.

`$gen-source-code` reads this routing table and invokes the applicable stack skill; researchers do not need to invoke each stack skill manually. Each stack skill loads only the references required by the active change areas.

| Change area | Skill | References loaded conditionally |
|---|---|---|
| React component/hook | `$build-react-frontend` | `react-rules.md` |
| TypeScript/Vite config or client env | `$build-react-frontend` | `typescript-vite.md` |
| Routes, API client, Context/Zustand | `$build-react-frontend` | `routing-data-state.md` |
| Tailwind/Recharts | `$build-react-frontend` | `tailwind-charts.md` |
| Nest module/controller/service | `$build-nest-backend` | `nest-rules.md` |
| DTO/validation/backend typing | `$build-nest-backend` | `typescript-validation.md` |
| Entity/repository/MySQL/transaction | `$build-nest-backend` | `typeorm-mysql.md` |
| JWT/Passport/bcrypt/config/Swagger | `$build-nest-backend` | `auth-config-openapi.md` |

Version rule: use the versions declared in the target `package.json` and lockfile. Do not introduce a separate security requirement or evaluation dimension.

The current FE baseline uses the Vite and React Router versions pinned by its manifest and lockfile. Preserve those exact resolved versions unless an approved requirement authorizes a dependency change.

Lint/type/build rule: do not create or run tests/test cases, but run permitted ESLint, TypeScript compilation and production build commands. Do not suppress diagnostics to obtain a green result.
