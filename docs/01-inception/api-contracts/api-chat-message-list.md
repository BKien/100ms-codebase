---
artifact_type: api-contract
status: Frozen
api_id: API-CHAT-MESSAGE-LIST
related_uc_id: UC-09
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\api\\api-chat-message-list.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/api/api-chat-message-list.md
source_sha256: sha256:7c0a9b2f5b707ff0a4a392cc68a43ac19acefaa6f146048f2ddb0d5bd72422ad
source_range: "Markdown: complete document"
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# API-CHAT-MESSAGE-LIST: Read Session Chat

## General Information

### API ID

`API-CHAT-MESSAGE-LIST`

### API Name

Read Session Chat

### Related Use Case IDs

- `UC-09`

### Method

`GET`

### Path

`/api/v1/sessions/{sessionId}/chat/messages`

### Description

Returns a page of chat messages and a continuation token.

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

### cursor

Type: string
Required: No
Nullable: No
Validation: Must be a JSON string.
Description: URI-encoded opaque continuation token.
Example: `cursor-reference`

### pageSize

Type: integer
Required: No
Nullable: No
Default: 50
Validation: Must be a JSON integer.
Description: pageSize value.
Example: `50`

## Request Body

None.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.items

Type: array (Message)
Required: Yes
Nullable: No
Description: Array of representations defined in the common contract.
Example: `[]`

### data.nextCursor

Type: string
Required: Yes
Nullable: No
Description: Opaque continuation token, including for an empty page.

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

This endpoint inherits [Common Contract](common-contract.md).
