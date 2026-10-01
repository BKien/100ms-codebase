---
artifact_type: api-contract
status: Frozen
api_id: API-LIVE-STREAM-VIEW
related_uc_id: UC-05
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\api\\api-live-stream-view.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/api/api-live-stream-view.md
source_sha256: sha256:7c96606daebf644dd7fbc82030d6fb0bbd0b7cfd3aa5045d47c40e107675f1b7
source_range: "Markdown: complete document"
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# API-LIVE-STREAM-VIEW: View a Live Stream

## General Information

### API ID

`API-LIVE-STREAM-VIEW`

### API Name

View a Live Stream

### Related Use Case IDs

- `UC-05`

### Method

`GET`

### Path

`/api/v1/sessions/{sessionId}/live-stream/view`

### Description

Returns the viewer-facing stream representation.

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

### Accept

Type: string
Required: Yes
Nullable: No
Allowed values: `application/json`
Description: HTTP media-type header.
Example: `application/json`

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

None.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.sessionId

Type: string
Required: Yes
Nullable: No
Description: UUID identifier.
Example: `11111111-1111-4111-8111-111111111111`

### data.participantId

Type: string
Required: Yes
Nullable: No
Description: UUID identifier.
Example: `11111111-1111-4111-8111-111111111111`

### data.viewerRole

Type: string
Required: Yes
Nullable: No
Allowed values: `VIEWER`, `STAGE_PARTICIPANT`
Description: viewerRole value.
Example: `VIEWER`

### data.streamStatus

Type: string
Required: Yes
Nullable: No
Allowed values: `READY`, `STARTING`, `LIVE`, `ENDED`
Description: streamStatus value.
Example: `READY`

### data.streamVersion

Type: integer
Required: Yes
Nullable: No
Description: streamVersion value.
Example: `1`

### data.sessionVersion

Type: integer
Required: Yes
Nullable: No
Description: sessionVersion value.
Example: `1`

### data.canPlayMedia

Type: boolean
Required: Yes
Nullable: No
Description: canPlayMedia value.
Example: `false`

### data.canPublishMedia

Type: boolean
Required: Yes
Nullable: No
Description: canPublishMedia value.
Example: `false`

### data.initialAudioMuted

Type: boolean
Required: Yes
Nullable: No
Description: initialAudioMuted value.
Example: `false`

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

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
Trigger: A required service is temporarily unavailable.
Description: Uses the common error envelope.
- Example message: `The request could not be completed.`

## Notes

This endpoint inherits [Common Contract](common-contract.md). Media playback is delivered through the media adapter.
