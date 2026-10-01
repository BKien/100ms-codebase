---
artifact_type: api-contract
status: Frozen
api_id: API-REACTION-CREATE
related_uc_id: UC-10
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\api\\api-reaction-create.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/api/api-reaction-create.md
source_sha256: sha256:cd7bbc2feb93dd709e0324999d1f58ed4f8b24f4c645805968ef820c30f7b0f6
source_range: "Markdown: complete document"
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# API-REACTION-CREATE: Send a Reaction

## General Information

### API ID

`API-REACTION-CREATE`

### API Name

Send a Reaction

### Related Use Case IDs

- `UC-10`

### Method

`POST`

### Path

`/api/v1/sessions/{sessionId}/reactions`

### Description

Returns the created reaction event.

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

### reaction

Type: string
Required: Yes
Nullable: No
Allowed values: `LIKE`, `CLAP`, `HEART`, `CELEBRATE`, `HAND`, `SURPRISE`
Validation: Must be a JSON string. String values must belong to the declared enum.
Description: reaction value.
Example: `LIKE`

## Success Response — HTTP 201

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.reaction

Type: object (Reaction)
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

This endpoint inherits [Common Contract](common-contract.md). Client display mapping: LIKE = thumbs up; CLAP = applause; HEART = heart; CELEBRATE = celebration; HAND = raised hand; SURPRISE = surprise.
