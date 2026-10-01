---
name: render-experiment-report
description: Render a researcher-readable Markdown view from finalized canonical Business Rule experiment-run JSON without changing evidence.
---

# Render Experiment Report

Resolve exactly one finalized canonical run JSON and run:

```text
python3 .codex/skills/render-experiment-report/scripts/render_report.py <run.json> [--output <report.md>]
```

The renderer validates lifecycle fields and completed per-BR results, records input path/checksum, and maps canonical fields to the report template. Markdown is disposable; never reconcile edits back into JSON. Do not load unrelated source/prompts/runtime history unless interpretation is separately requested.

Render the three measured bucket breakdowns and full workflow from canonical `metrics`. Mark unclosed values N/A until workflow metrics are finalized. Rendering has no authority to recompute telemetry or change BR/flow results.

Render stored `flow_accuracy.current_summary` when present, otherwise the current immutable assessment, without recomputation. For `accepted-audit-results-v1`, label results as accepted experiment audit results and show each result's actual stage/source, retained earlier-source count and latest assessment limitations/counts. An inconclusive later audit does not erase accepted results. Show evaluated-only rates, coverage, whole-baseline rates, pending targets, known failures and researcher/LLM provenance. Terminal blocked/stopped/repair-declined runs can be rendered honestly; partial flow data must not hide telemetry. Optional UI data may be missing/null and never blocks reporting. Excel output remains separate.
