---
name: audit-flow-accuracy
description: Audit frozen use-case flows and update canonical experiment results directly from researcher verdicts or LLM re-audits, retaining accepted results across repair. Preserve evidence; never change application source, generate tests or authorize repairs.
---

# Audit Flow Accuracy

Read [FILE-DRIVEN-WORKFLOW.md](../../../docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md). Audit flows automatically within directly requested BR audit and requested repair verification; never request a separate Audit Gate. For partial results/follow-ups read [follow-up measurement](references/follow-up-measurement.md).

Save either attributed researcher verdicts or validated bounded LLM observations directly in canonical JSON. Acknowledge and wait for a subsequent `$bug-fixing-sub-prompt` when defects remain; neither follow-up path automatically starts repair. Remaining unknown accepted flows block new repair authorization. The scorer never edits source, authorizes repair, closes telemetry or changes gates. All-passing unchanged-source bookkeeping belongs to the coordinator. Activation is optional; rubric comes from the pinned configuration.

The final reported flow result is the latest conclusive accepted verdict per flow across the experiment (`accepted-audit-results-v1`). Both researcher replies and validated LLM re-audits update canonical JSON in the same turn, without another save confirmation. Repair, changed source hashes and later `not_evaluable` attempts do not erase accepted results. A newer conclusive result can replace an older verdict. Retain actual stage/source provenance per result and show later audit limitations separately. See the follow-up contract for schema 2, stdin input and corrections to already scored flows.

Before assessing, read the frozen UC, canonical run, [per-flow audit procedure](references/per-flow-audit.md) and [assessment schema](references/assessment-schema.md). Resolve and validate the checksum-pinned configuration directly, including every frozen API path/identity/SHA-256; optional activation is validated when present. Configurations use `completion-critical-flow-runtime-v2`: `correct` requires observed completion through the integrated runtime. Require `docs/02-construction/implementation/<UC-ID>/flow-baseline.json`, frozen from the same UC checksum before generation. Read `ordered_flow_ids` as the complete ordered audit inventory, assess every listed flow exactly once and use its length as the frozen denominator. Resolve every listed flow's steps, branch and terminal outcome from the checksum-pinned frozen UC. Never add, omit, reorder or reconstruct the denominator after seeing implementation results.

## Baseline

1. `ordered_flow_ids` includes every explicit Basic/Main Flow and each named Alternative and Exception Flow in source order. Include explicit nested UI-variant flows; an “identical to” reference does not duplicate a flow.
2. Do not count triggers, conditions, postconditions, Business Rules, steps, UI states or API operations as additional flows.
3. Freeze the UC path/checksum and complete ordered flow IDs. Validate them with `scripts/validate_flow_baseline.py`. Initial and final audit must use this exact baseline.
4. During assessment, read each listed flow from the frozen UC, preserve every step in the assessment, and mark `completion_critical: true` only when failure prevents the branch-specific terminal outcome or a mandatory completion state. Record why and stop for researcher resolution when material ambiguity remains.

## Audit (runtime-v2)

1. Follow the per-flow procedure from specified entry through the actual branch to its frozen terminal outcome. Use the UI for UI-entry flows. Keep each attempt's actions and sanitized evidence under its own observation ID, bound to UC/run/stage/baseline/source revision. Trace source separately; do not infer runtime completion from implementation, API success, build or health alone.
2. A flow is `incorrect` when a completion-critical step is `unmet` or its terminal outcome is `unmet`. Retain noncritical deviations without failing the flow.
3. A flow is `not_evaluable` when no blocking failure is proven but a critical step, terminal outcome or connected runtime chain lacks evidence. Otherwise it is `correct`. For v2, critical/outcome `met` requires appropriate runtime evidence; the scorer rejects unsupported claims instead of silently downgrading them. Unreached steps are `not_evaluable`, not automatically `unmet`.
4. Treat an Exception Flow as correct when its specified failure handling completes; the primary business action need not succeed.
5. For v2, bounded Docker Compose v2 runtime observation is mandatory for `correct`. Set scope/time bounds before observation, retain failed attempts, and stop on sufficient evidence, blocker or the bound. Missing daemon is runtime `BLOCKED`; unverifiable deployment or inaccessible branches leave affected behavior `not_evaluable`. Do not modify source, add mocks, force infrastructure failures outside authorization, create or run tests/test cases.
6. Run `scripts/score_flow_accuracy.py --run-json <run.json> --assessment <input.json> --dry-run`, then repeat without `--dry-run` to persist. Store checksummed, sanitized runtime artifacts and immutable source snapshots/excerpts in the run evidence directory. Preserve `initial`; before the repair work response ends, observe every flow on repaired final source with the same rubric. If no repair occurred and source is unchanged, the existing initial assessment may serve as terminal evidence without a new assessment. Preserve its stage, ID and timestamps; never copy it into a fabricated final observation.


## Formula

Let `T = main + alternative + exception` and `W = incorrect`.

- Error percentage: `W / T * 100`.
- Accuracy percentage: `(T - W) / T * 100`.

Each flow has equal weight. If an accepted result remains `not_evaluable`, whole-baseline error and accuracy remain null. Persist evaluated-only rates, coverage, bounds and pending details in canonical `flow_accuracy.current_summary`; do not create current or follow-up JSON mirrors in `flow-accuracy`. Immutable assessment/evidence files remain. Evaluated rates use correct + incorrect; never change the frozen denominator or present researcher verdicts as LLM runtime observations.

Run automatically inside directly requested first-pass BR audit and final verification within requested repair. Return ordinary scoring control to the caller. After saved follow-up, return to the command coordinator to report pending measurement, wait for a repair request or record all-passing skip. No additional confirmations, automatic repair or final-audit turn. Preserve recorded evidence, runtime rubric and optional UI independence.
