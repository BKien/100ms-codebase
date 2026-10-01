# React 18 coding rules

## Architecture and naming

- Keep source under `finalsource/fe/src` using `pages/`, `components/`, `api/`, `hooks/`, `context/`, `router/`, `utils/` and `assets/`.
- Name React components/types with PascalCase, hooks with `use` + PascalCase, functions/variables with camelCase, constants with descriptive camelCase or project-established uppercase style.
- Use one clear responsibility per component. Extract reusable presentation, not arbitrary one-line wrappers.
- Keep HTTP calls out of components; components call typed functions in `src/api`.

## Rules of React

- Keep render pure and idempotent. Never perform network calls, navigation, state writes or mutable global writes during render.
- Treat props/state/hook arguments and values already passed to JSX as immutable snapshots.
- Call hooks only at the top level of React components or custom hooks; never inside branches, loops, callbacks or ordinary functions.
- Use components through JSX; never call component functions directly.
- Use an effect only to synchronize with an external system. Derive values during render and handle user actions in event handlers.
- Declare complete hook dependency arrays. Do not silence `react-hooks/exhaustive-deps`; restructure unstable values or callbacks.
- Prefer controlled form inputs when [the approved prompt](../../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md) requires field-level state/errors. Prevent duplicate submissions explicitly.

## State and UI behavior

- Keep local/transient state local. Promote state to Context/Zustand only when multiple distant consumers need it.
- Model async UI explicitly: idle, loading, success/empty, safe error. Ignore stale responses and updates after unmount.
- Preserve semantic HTML, label/control association, keyboard operation, focus feedback and meaningful alternative text.
- Render untrusted strings as text. Raw HTML requires an approved sanitizer and explicit technical rationale.

Official basis: React Rules of React and Hooks guidance: https://react.dev/reference/rules
