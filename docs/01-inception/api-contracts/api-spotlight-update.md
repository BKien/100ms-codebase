---
artifact_type: api-contract
status: Frozen
api_id: API-SPOTLIGHT-UPDATE
related_uc_id: UC-15
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\api\\api-spotlight-update.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/api/api-spotlight-update.md
source_sha256: sha256:857e2aa9d2e00f29d81206040509f9bcc48c429b421e003cd8d6b3e3d883f16d
source_range: "Markdown: complete document"
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# API-SPOTLIGHT-UPDATE: Update Session Spotlight

## General Information

### API ID

`API-SPOTLIGHT-UPDATE`

### API Name

Update Session Spotlight

### Related Use Case IDs

- `UC-15`

### Method

`PATCH`

### Path

`/api/v1/sessions/{sessionId}/spotlight`

### Description

Returns the session representation after setting or clearing the tile spotlighted for everyone.

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
Example: `command-15-01`

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

### targetParticipantId

Type: string
Required: Yes
Nullable: Yes
Validation: Must be null or a JSON string.
Description: Participant identifier to spotlight, or null to clear the shared spotlight.

### expectedVersion

Type: integer
Required: Yes
Nullable: No
Validation: Must be a JSON integer.
Description: Session version observed by the client.
Example: `1`

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.session

Type: object (SessionSummary)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

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

This endpoint inherits [Common Contract](common-contract.md). Personal pinning remains part of API-PREFERENCES-UPDATE.
