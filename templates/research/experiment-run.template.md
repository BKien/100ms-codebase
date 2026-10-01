# Experiment run <RUN-ID>

- Configuration: `<CONFIG-ID>@sha256:<checksum>`
- UC: `<UC-ID> - <name>`
- Replicate/order: `<index>/<order>`
- Model: `<effective model/snapshot/effort>`
- Final source: `sha256:<checksum>`

## Timing and tokens

| Scope | Input | Cached input | Output | Reasoning output | Total tokens | Seconds | Turns | Tool calls |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Coding Prompt | | | | | | | | |
| Source Generation | | | | | | | | |
| Repair | | | | | | | | |
| Workflow | | | | | | | | |

Explicit close/finalize commands supply canonical `metrics` through the telemetry engine without additional gate confirmations. Cached input is part of input; reasoning is part of output. Measurement/report/export turns and researcher waiting are excluded. Phase closure happens only after the work response completes.

## Business Rule assessment

| BR ID | Initial | Final | Evidence |
|---|---|---|---|
| `<BR-ID>` | `met/unmet/not_evaluable` | `met/unmet/not_evaluable` | `<locations>` |

## Flow accuracy

- Status: `scored | repair_required | partial | not_evaluable`
- Correct/incorrect/not evaluable: `<counts>`
- Flow error/accuracy: `<percent or N/A>`
- Evaluated coverage and bounds: `<values>`
- Evaluated-only accuracy/error: `<percent or N/A; denominator = correct + incorrect>`
- Result basis/researcher result count: `<rubric_evidence | includes_researcher_results>/<count>`
- Pending flows, missing targets, reasons and attempts: `<stored details>`
- Follow-up choices: researcher supplies results for LLM entry; or LLM continues measurement. Neither permits source changes.

## Researcher-managed Figma/UI accuracy

- Status: `researcher_managed | measured`
- Accuracy: `<manual percent or N/A>`
- Evidence: `<researcher-supplied reference>`

## Repairs

| Repair | Evidence-backed defect | Affected BRs | Result |
|---|---|---|---|

This Markdown is a rendered view. The canonical JSON remains authoritative.
