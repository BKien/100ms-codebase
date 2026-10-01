---
artifact_type: api-contract
status: Frozen
api_id: API-STAGE-REQUEST-CREATE
related_uc_ids: ["UC-06", "UC-07"]
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\api\\api-stage-request-create.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/api/api-stage-request-create.md
source_sha256: sha256:33d846e371c3604f8c90a54b67f1a91ba3dbd4194d1bc513d9de663f90e0219b
source_range: "Markdown: complete document"
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# API-STAGE-REQUEST-CREATE: Submit a Stage Request Action

## General Information

### API ID

`API-STAGE-REQUEST-CREATE`

### API Name

Submit a Stage Request Action

### Related Use Case IDs

- `UC-06`
- `UC-07`

### Method

`POST`

### Path

`/api/v1/sessions/{sessionId}/stage-request-commands`

### Description

Submits a stage request action and returns the request and its participant.

### Authentication

Bearer session access token, using the registered or guest form described in the common contract.

### Authorization

Required.

## Request Header(s)

### Authorization

Type: string
Required: Yes
Nullable: No
Description: Bearer session access token.
Example: `Bearer <session-access-token>`

### Content-Type

Type: string
Required: Yes
Nullable: No
Allowed values: `application/json`
Description: HTTP media-type header.
Example: `application/json`

### Idempotency-Key

Type: string
Required: Yes
Nullable: No
Description: Opaque HTTP command token.
Example: `command-22-01`

## Path Parameter(s)

### sessionId

Type: string
Required: Yes
Nullable: No
Description: UUID identifier.
Example: `11111111-1111-4111-8111-111111111111`

## Query Parameter(s)

None.

## Request Body

### action

Type: string
Required: Yes
Nullable: No
Allowed values: `CREATE`, `ACCEPT`, `REJECT`, `CANCEL`
Validation: Must be a JSON string. String values must belong to the declared enum.
Description: action value.
Example: `CREATE`

### requestId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: UUID identifier.
Example: `11111111-1111-4111-8111-111111111111`

### expectedVersion

Type: integer
Required: No
Nullable: Yes
Validation: Must be null or a JSON integer.
Description: expectedVersion value.
Example: `1`

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.request

Type: object (StageRequest)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

### data.participant

Type: object (Participant)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

### data.sessionVersion

Type: integer
Required: Yes
Nullable: No
Description: sessionVersion value.
Example: `1`

## Error Response — HTTP 400

- Code: `INVALID_REQUEST`
Trigger: The request cannot be decoded or does not match the declared wire schema.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Error Response — HTTP 401

- Code: `AUTHENTICATION_REJECTED`
Trigger: The authentication context is rejected.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Error Response — HTTP 403

- Code: `ACCESS_REJECTED`
Trigger: The operation is rejected for the supplied access context.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Error Response — HTTP 404

- Code: `RESOURCE_UNAVAILABLE`
Trigger: The requested resource is unavailable.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Error Response — HTTP 409

- Code: `OPERATION_CONFLICT`
Trigger: The operation conflicts with the current resource response.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Error Response — HTTP 422

- Code: `COMMAND_REJECTED`
Trigger: The submitted command is rejected.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
Trigger: A required service is temporarily unavailable.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Notes

This endpoint inherits [Common Contract](common-contract.md).
