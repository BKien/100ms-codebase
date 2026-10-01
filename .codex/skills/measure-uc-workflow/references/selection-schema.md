# Explicit post-turn selection

Use one task/session per UC/run. All commands are run from the Business repository. Resolve a real canonical run path and explicit rollout path, not the latest file. The canonical JSON must exist with `uc_id` and `run_id` before opening prompt metrics; use the configured run identity. This Draft bookkeeping does not activate source generation.

Prepare a private temporary selection JSON (absolute rollout paths must not be copied into public results):

```json
{
  "uc_id": "UC-01",
  "run_id": "UC-01-R1",
  "session_path": "C:/private/rollout.jsonl",
  "turns": [
    {"turn_id": "setup-turn-id", "phase": "uc_setup", "reason": "Setup specific to UC-01 before prompt phase"},
    {"turn_id": "prompt-turn-id", "phase": "prompt_generation", "reason": "Generate UC-01 Draft"},
    {"turn_id": "approval-turn-id", "phase": "configuration_and_approval", "reason": "Only approved the existing Draft; no prompt generation or revision"}
  ],
  "excluded_turns": [],
  "workflow_evidence": {
    "start": {"turn_id": "setup-turn-id", "required_terms": ["UC-01"]},
    "terminal": {"turn_id": "approval-turn-id", "required_terms": ["approve"]}
  }
}
```

Each later selection retains previously selected rows/reasons and adds new work. Every completed turn in the session before the current measurement turn must be selected or explicitly excluded, including turns before the selected workflow start. Inspect these earlier turns so UC-specific configuration/setup is not silently omitted. Intermediate Measure turns must be excluded with reason `measurement/report turn`. The current measurement turn is supplied separately by `--measurement-turn-id` and automatically excluded. Start/terminal text markers must match the actual user messages; start must identify the UC. Do not save message contents in results.

Core token labels: `prompt_generation`, `source_generation`, `repair`. Auxiliary workflow-only token labels: `configuration_and_approval`, `dataset_resolution`, `audit`, `runtime_verification`, `finalization`, `uc_setup`. Assign by the turn's actual primary work, not the currently open timing bucket or the skill named in the request.

| Actual primary work | Token label |
|---|---|
| Generate/revise the coding prompt | `prompt_generation` |
| Implement first-pass source | `source_generation` |
| Execute a source correction and its integrated BR/flow/runtime verification | `repair` |
| Only prepare/confirm configuration, activate a run, approve an artifact or resolve an approval gate | `configuration_and_approval` |
| Only resolve Figma/dataset inputs, including a missing-dataset blocker | `dataset_resolution` |
| Assess implementation, observe runtime, finalize evidence, or prepare UC-specific environment | `audit`, `runtime_verification`, `finalization`, or `uc_setup` |

All selected labels contribute to workflow tokens. Only a matching core label contributes to that core's tokens. A failed generation/repair attempt still counts under its actual work; failure alone never moves it to auxiliary or excludes it. A request to generate code that only receives an approval blocker is auxiliary. Under `generation_execution_with_repair_audit_v2`, a turn with core execution segments must use that same core token label, even when END is missing. An integrated repair audit therefore stays `repair`, never auxiliary `audit`. If approval and generation happen in one turn with core capture, retain the whole turn under that captured core label. Without core capture, classify from full work evidence; genuine generation with missing timing must retain its core label and an unavailable-time reason. Never split tokens between activities or classify solely by keywords. Explain ambiguous/mixed classifications in `reason`; surface unresolved uncertainty to the researcher before committing. Common setup before the UC and other UC work are excluded with reasons.

The script checks labels, sums and label agreement with any captured core execution; it cannot prove semantic intent without that evidence. Auxiliary-only labels are allowed between core phase open/close boundaries. Core labels must remain inside their own generation window so a later turn cannot silently change a closed phase. No new workflow steps are required.

Optional selected-turn fields: `repair_id` references a real canonical repair record; `timing_unavailable_reason` is mandatory if a generation execution endpoint is absent (auxiliary-only work needs no generation capture). Never fill missing endpoints with rollout or current timestamps. On `finalize-workflow`, `repair_skip_reason` records the actual explicit or automatic no-defect decision if no repair was performed. An unstarted phase has unavailable values; a recorded skipped repair is explicitly distinguished from missing evidence.

Boundary checks use explicit start/completion events. Aborted turns with terminal events remain chargeable; interrupted turns without an end are not finalized. The extractor refuses incomplete/missing token evidence rather than guessing. Missing explicit rollout boundaries block measurement.

`turns[].wall_clock_seconds` is the elapsed time between that selected turn's rollout `started_at` and `ended_at`: `round((epoch(ended_at) - epoch(started_at)) / 1000, 3)` where `epoch()` returns milliseconds. Reject missing, invalid, timezone-less or reversed endpoints. Retain the same completed/aborted-turn eligibility as tokens. `metrics.phases.<phase>.values.wall_clock_seconds` and `metrics.token_phase_breakdown.<label>.wall_clock_seconds` sum exactly the turns with that semantic token label. `metrics.workflow.wall_clock_seconds` sums every selected turn once, including auxiliary work. It covers selected work to date while the workflow is open and becomes final at finalize-workflow. Excluded turns and gaps between turns contribute nothing. Approval waits inside selected turns remain included. Closed-phase values and legitimate skipped-Repair zero values follow the existing lifecycle. No separate time selection or wait-time field is used. The `duration_seconds` and missing-endpoint rules below refer only to Duration seconds; missing Duration seconds do not erase valid rollout wall-clock evidence.

Schema 3 output's `metrics.phases.<phase>.values` contains tokens, duration_seconds, workflow_turn_count, tool_call_count and nullable model_call_count. Tokens/counts cover whole turns by `turns[].phase`; seconds cover only actual core execution segments under `timing_phase`. Under the execution protocol these labels must agree when core segments exist. Auxiliary-only work without core segments has zero counted execution seconds and `timing_exclusion_reason`, not a claim of zero elapsed time. `metrics.token_phase_breakdown` retains all selected labels and their five counters/counts. `metrics.repair_timing` retains every canonical repair's segment IDs, seconds and missing-evidence reason, including integrated verification and final evidence persistence. Workflow tokens cover all selected work; workflow time = Prompt + first-pass Source + all Repair executions, null while any phase is pending or missing time. Closed evidence is immutable. No three-phase token subtotal is emitted.
