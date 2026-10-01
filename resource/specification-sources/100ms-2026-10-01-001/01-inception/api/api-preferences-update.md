---
artifact_type: api-contract
status: Draft
api_id: API-PREFERENCES-UPDATE
related_uc_ids: ["UC-12", "UC-13", "UC-14", "UC-15"]
---

# API-PREFERENCES-UPDATE: Update Session Preferences

## General Information

### API ID

`API-PREFERENCES-UPDATE`

### API Name

Update Session Preferences

### Related Use Case IDs

- `UC-12`
- `UC-13`
- `UC-14`
- `UC-15`

### Method

`PATCH`

### Path

`/api/v1/sessions/{sessionId}/participants/{participantId}/preferences`

### Description

Returns the media and view preference representation.

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

### participantId

Type: string
Required: Yes
Nullable: No
Description: UUID identifier.
Example: `11111111-1111-4111-8111-111111111111`

## Query Parameter(s)

None.

## Request Body

### microphoneDeviceId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: microphoneDeviceId value.

### cameraDeviceId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: cameraDeviceId value.

### speakerDeviceId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: speakerDeviceId value.

### virtualBackgroundId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: virtualBackgroundId value.

### layout

Type: string
Required: No
Nullable: No
Allowed values: `EQUAL_PROMINENCE`, `SIDEBAR`, `PRESENTER`
Validation: Must be a JSON string. String values must belong to the declared enum.
Description: layout value.

### focusedParticipantId

Type: string
Required: No
Nullable: Yes
Validation: Must be null or a JSON string.
Description: focusedParticipantId value.

### sidePanel

Type: string
Required: No
Nullable: Yes
Allowed values: `CHAT`, `PARTICIPANTS`, `SETTINGS`
Validation: Must be null or a JSON string. String values must belong to the declared enum.
Description: sidePanel value.

### pictureInPicture

Type: boolean
Required: No
Nullable: No
Validation: Must be a JSON boolean.
Description: pictureInPicture value.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

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
