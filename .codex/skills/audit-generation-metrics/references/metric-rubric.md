# Metric rubric

## Business Rule results

The frozen ordered BR list is the denominator. Each BR receives one terminal status:

- `met`: inspectable implementation evidence satisfies the complete rule.
- `unmet`: an applicable part is missing or contradictory.
- `not_evaluable`: permitted evidence cannot support a defensible decision; state the exact limitation.

Prompt prose alone is not evidence. Cite source/configuration/build/bounded-runtime locations. Initial and final snapshots must contain exactly the baseline BR IDs in order and their totals must match.

## Supporting metrics

- First-pass audit and automatic verification within authorized repair run `audit-flow-accuracy` against the frozen Basic/Main, Alternative and Exception Flow denominator. Each flow has equal weight; steps only determine whether their parent flow can complete. No separate final-audit gate is required.
- Figma/UI accuracy is researcher-managed. Audit never calculates, validates or overwrites it.
- Complexity records actors, main steps, alternate/exception flows, entities, integrations, Business Rules and UI states.
- Time comes from automatic timezone-qualified ISO/epoch pairs; tokens come only from telemetry.
- Explicit close/finalize commands invoke the measurement engine, which owns canonical `metrics`; Audit preserves it while validating BR/flow evidence.
- Export input, cached input, output, reasoning output and total per prompt/source/repair and full workflow, plus captured seconds, selected turn count and observable tool-call count. Cached/reasoning are subsets, never added again. Do not publish fresh input, usage-update count, estimated call counts, money cost or a three-phase subtotal. Missing telemetry is null with a reason.
- Workflow seconds = Prompt execution + first-pass Source execution + all Repair executions at the shared START/END boundaries. Configuration, approval, dataset resolution, separate audit/runtime/finalization and Measure/report work are excluded from time. Capture endpoints live; aggregate after completion. Never substitute UI duration, whole-chat elapsed time or missing endpoints.
- Record generation, audit and each repair model independently. Start model variants from the same [approved prompt](../../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md) and source baseline.
- The first-pass audit response and the repair response print BR and flow summaries. Researcher-managed UI and manual Excel fields remain untouched.
