---
artifact_type: api-contract
status: Frozen
api_id: API-SESSION-STATE
related_uc_ids: ["UC-02", "UC-03", "UC-04", "UC-05", "UC-06", "UC-07", "UC-08", "UC-10", "UC-11", "UC-12", "UC-13", "UC-14", "UC-15", "UC-16", "UC-17", "UC-18"]
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\api\\api-session-state.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/api/api-session-state.md
source_sha256: sha256:a904d785bdff34cd3615abe6b2d58c3887e9d784a967f944d9b7db138e7c73c4
source_range: "Markdown: complete document"
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# API-SESSION-STATE: Read Session State

## General Information

### API ID

`API-SESSION-STATE`

### API Name

Read Session State

### Related Use Case IDs

- `UC-02`
- `UC-03`
- `UC-04`
- `UC-05`
- `UC-06`
- `UC-07`
- `UC-08`
- `UC-10`
- `UC-11`
- `UC-12`
- `UC-13`
- `UC-14`
- `UC-15`
- `UC-16`
- `UC-17`
- `UC-18`

### Method

`GET`

### Path

`/api/v1/sessions/{sessionId}/state`

### Description

Returns the current session and caller representations, stage requests, and a page of reaction events.

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

### reactionCursor

Type: string
Required: No
Nullable: No
Validation: Must be a JSON string.
Description: URI-encoded opaque reaction continuation token.

## Request Body

None.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.session

Type: object (SessionSummary)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

### data.selfParticipant

Type: object (Participant)
Required: Yes
Nullable: No
Description: Representation defined in the common contract.

### data.stream

Type: object (Stream)
Required: Yes
Nullable: Yes
Description: Representation defined in the common contract.

### data.recording

Type: object (Recording)
Required: Yes
Nullable: Yes
Description: Representation defined in the common contract.

### data.share

Type: object (Share)
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

### data.stageRequests

Type: array (StageRequest)
Required: Yes
Nullable: No
Description: Array of representations defined in the common contract.
Example: `[]`

### data.reactions

Type: array (Reaction)
Required: Yes
Nullable: No
Description: Array of representations defined in the common contract.
Example: `[]`

### data.nextReactionCursor

Type: string
Required: Yes
Nullable: No
Description: Opaque continuation token, including for an empty event page.

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

This endpoint inherits [Common Contract](common-contract.md). The client can repeat this request to refresh its representation. Chat and participant collections have separate list endpoints.
