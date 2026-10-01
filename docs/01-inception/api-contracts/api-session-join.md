---
artifact_type: api-contract
status: Frozen
api_id: API-SESSION-JOIN
related_uc_ids: ["UC-02", "UC-12", "UC-13"]
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\api\\api-session-join.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/api/api-session-join.md
source_sha256: sha256:b20ee3abd23b7a9ce9a5a9ceed60075473ee3ea7937156b5c7b1774183ecd38b
source_range: "Markdown: complete document"
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# API-SESSION-JOIN: Join a Session

## General Information

### API ID

`API-SESSION-JOIN`

### API Name

Join a Session

### Related Use Case IDs

- `UC-02`
- `UC-12`
- `UC-13`

### Method

`POST`

### Path

`/api/v1/sessions/{sessionId}/participants`

### Description

Submits preview identity, media selections, and draft preferences.

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

### displayName

Type: string
Required: Yes
Nullable: No
Validation: Must be a JSON string.
Description: displayName value.
Example: `Alex Morgan`

### microphoneEnabled

Type: boolean
Required: Yes
Nullable: No
Validation: Must be a JSON boolean.
Description: microphoneEnabled value.
Example: `false`

### cameraEnabled

Type: boolean
Required: Yes
Nullable: No
Validation: Must be a JSON boolean.
Description: cameraEnabled value.
Example: `false`

### microphoneDeviceId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: microphoneDeviceId value.
Example: `device-reference`

### cameraDeviceId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: cameraDeviceId value.
Example: `device-reference`

### speakerDeviceId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: speakerDeviceId value.
Example: `device-reference`

### virtualBackgroundId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: UUID identifier.
Example: `11111111-1111-4111-8111-111111111111`

## Success Response — HTTP 201

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.participant

Type: object (Participant)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

### data.session

Type: object (SessionSummary)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

### data.stream

Type: object (Stream)
Required: Yes
Nullable: Yes
Description: Representation defined in the common contract.

### data.media

Type: object (MediaPreference)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

### data.view

Type: object (ViewPreference)
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

This endpoint inherits [Common Contract](common-contract.md).
