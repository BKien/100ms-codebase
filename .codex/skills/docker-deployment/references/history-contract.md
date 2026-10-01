# Persistent deployment history contract

Store only sanitized evidence under `docs/03-audit/docker-deployment/`.

## Current environment snapshot

Replace `environment-current.json` from `templates/operations/docker-environment-current.template.json` with the latest timestamp, tool versions, sanitized status and next action. Store one compact operation JSON under `operations/<timestamp>-<mode>.json` containing command identifiers, exit codes, source hash and only a bounded error excerpt.

## Incident index and record

- Query `incidents/index.json` first. If absent, initialize it from `templates/operations/docker-incident-index.template.json`.
- Store a detailed record at `incidents/<fingerprint>.json` only for a new or changed incident.
- Incident ID: `DEP-YYYYMMDD-NNN`.
- Timestamp and layer.
- Stable fingerprint: normalized service + stage + primary error; remove changing container IDs, paths, timestamps and secrets.
- Sanitized symptom/evidence.
- Root cause: confirmed, suspected or unknown.
- Actions attempted in order.
- Files changed and commands rerun.
- Outcome: resolved, unresolved or blocked.
- Reusable resolution and prevention note.

Append operation records chronologically. Update current state and index deterministically; never delete incident records. If evidence may contain a secret, summarize it instead of storing raw text.
