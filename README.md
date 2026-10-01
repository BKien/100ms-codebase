# 100ms research codebase

This research product prepares source generation experiments from the researcher-provided 100ms Markdown specification and Figma design. The active inputs contain 18 frozen use cases, 15 endpoint contracts, OCL utilities, shared UML vocabulary and assumptions.

- [Project profile](PROJECT_PROFILE.json)
- [Connected sources and retrieval receipt](docs/00-context/sources/CONNECTED-SOURCES.md)
- [Migration execution report](docs/00-context/100MS-SETUP-REPORT.md)
- [Figma mapping and full page inventory](docs/00-context/FIGMA-LINK-REVIEW.md)
- [Research workflow](docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md)

The neutral baseline uses React 18/TypeScript/Vite/Tailwind and NestJS 11/TypeORM tooling. It contains no 100ms UC implementations. Source restoration uses `.codex/skills/restore-source-baseline/assets/source-baseline.zip` and the SHA-256 pinned in the project profile.

Current setup is incomplete: the researcher deferred database preparation, and Figma capture reached the Education plan MCP quota. The checksum-valid partial dataset is not a complete immutable input for generation. Archived Financial resources are cold evidence outside the active input inventory.

## Local scaffold

The current frontend/backend run at http://localhost:18080 and http://localhost:13000/api/health. The local `.env` is ignored and contains placeholders for deferred credentials; replace them before preparing the database or credential-dependent application behavior.

```powershell
docker compose --env-file finalsource/.env -f finalsource/compose.yaml up -d --build --no-deps backend frontend
python tools/validate_100ms_preparation.py
python .codex/skills/resolve-figma-design-dataset/scripts/resolve.py --validate-all --dataset-version 100ms-2026-10-01-001
```

The `database-setup` profile remains unused. Do not start its services until the schema/persistence policy and migrations have been reviewed. Experiment generation still requires all four prepared research JSON inputs and the fifth database input; no preflight check has been disabled.
