---
name: build-react-frontend
description: Build or review React 18, TypeScript, Vite and Tailwind frontend code from the approved prompt using frozen Figma evidence.
---

# Build React Frontend

Apply the [shared operational constitution](../../../AGENTS.md#shared-operational-constitution).

Read [the approved prompt](../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md), project context, connected sources and `docs/00-context/engineering/TECHNICAL-STACK-RULES.md`. Inspect `finalsource/fe/package.json` and its lockfile, then extend the existing app under `finalsource/fe`.

Cover all applicable Basic/Main, Alternative and Exception Flows. See [shared contract](../../../docs/00-context/workflow/WORKFLOW-CONTRACT.md).

Load only the references required by the active change areas:

- React components or hooks: [references/react-rules.md](references/react-rules.md)
- TypeScript, Vite configuration or client environment: [references/typescript-vite.md](references/typescript-vite.md)
- Routes, API client, Context or Zustand: [references/routing-data-state.md](references/routing-data-state.md)
- Tailwind or Recharts: [references/tailwind-charts.md](references/tailwind-charts.md)

- For Figma-backed work, require a checksum-valid frozen dataset and map every visible node/state. Use Figma only to create or refresh a missing dataset through the repository resolver.
- Reuse the HTTP client, router, shell and established state patterns. Implement typed loading, empty, success, validation and error states. Apply accessible labels, keyboard/focus behavior and responsive Tailwind.
- Do not invent navigation, API calls or business behavior; stop for material business/API/schema/ownership ambiguity.
- Run only permitted non-test lint/typecheck/build and visual/runtime observations.
