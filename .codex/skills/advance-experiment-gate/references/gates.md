# Internal command step records

The human-facing sequence is [FILE-DRIVEN-WORKFLOW.md](../../../../docs/00-context/workflow/FILE-DRIVEN-WORKFLOW.md). No additional confirmations are required. Canonical `gates` records internal command steps.

| Command | Internal receipt | Next command |
|---|---|---|
| close prompt | prompt, plus [approved prompt](../../../../docs/02-construction/coding-prompts/%3CUC-ID%3E-business-coding-prompt.md) checksum | generate source |
| close source | source | audit |
| audit | first_pass_audit; all-passing repair_decision skipped | repair or finalize workflow |
| repair | repair_decision authorized within same work turn | finalize workflow after automatic verification |
| finalize workflow (internal first step when Repair is open) | repair | internal finalization in the same turn |
| finalize workflow (internal final step) | final_metrics | optional export |

Use `record_command.py` and actual turn IDs; no fabricated confirmation times. Audit and all-passing skip can be recorded within the same audit turn. Closing telemetry never executes later generation/audit/repair work. Preserve recorded receipts and their hashes/times; validate optional activation when present. Initial/final BR/flow evidence, frozen rubric and source provenance remain required; UI scoring is optional.
