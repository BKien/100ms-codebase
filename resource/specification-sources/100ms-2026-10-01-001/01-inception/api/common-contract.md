# Common API Contract

## Transport

Base path: `/api/v1`. JSON requests and responses use `application/json`. Identifiers use canonical UUID text. Timestamps use ISO 8601 UTC date-time syntax. Every endpoint explicitly inherits this contract, including envelopes, reusable representations, and errors. Nested requiredness applies when its containing object is present and non-null.

## Authentication Header

### `Authorization`

- Type: string
- Required: Yes
- Nullable: No
- Description: HTTP Authorization header: Bearer followed by a session access token. Both registered and guest tokens use this scheme.
- Example: `Bearer <session-access-token>`


## Success Envelope

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: success value.
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Description: message value.
- Example: `Request completed.`

### `data`

- Type: object
- Required: Yes
- Nullable: No
- Description: Endpoint-specific data object.


The success value is `true`. Endpoint success sections define the children of `data`; all three envelope fields are required and non-null.

## Error Envelope

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: success value.
- Example: `false`

### `code`

- Type: string
- Required: Yes
- Nullable: No
- Description: code value.
- Example: `OPERATION_CONFLICT`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Description: message value.
- Example: `The operation could not be completed.`

### `requestId`

- Type: string
- Required: No
- Nullable: No
- Description: requestId value.
- Example: `trace-reference`


The error success value is `false`. Error responses contain no `data` member. Each endpoint declares its public HTTP outcomes; each uses this error envelope. Error messages are public summaries.

## Request Field Presence

An optional property may be omitted. A nullable property may contain JSON `null`. Presence and null are distinct wire representations. Object schemas list their fields below; unknown request properties produce `INVALID_REQUEST`.

## Reusable Representations

The following named object definitions are referenced by endpoint field types. Their fields use JSON camelCase. The entity identifier appears as the corresponding resource-specific field, for example Participant.participantId and Recording.recordingId.

## Participant

### `participantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `displayName`

- Type: string
- Required: Yes
- Nullable: No
- Description: displayName value.
- Example: `Alex Morgan`

### `role`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `HOST`, `BROADCASTER`, `VIEWER`, `STAGE_PARTICIPANT`
- Description: role value.
- Example: `HOST`

### `status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `JOINED`, `LEFT`
- Description: status value.
- Example: `JOINED`

### `microphoneEnabled`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: microphoneEnabled value.
- Example: `false`

### `cameraEnabled`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: cameraEnabled value.
- Example: `false`

### `version`

- Type: integer
- Required: Yes
- Nullable: No
- Description: version value.
- Example: `1`

### `joinedAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `leftAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## SessionSummary

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `kind`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `LIVE_STREAM`, `VIDEO_CONFERENCE`
- Description: kind value.
- Example: `LIVE_STREAM`

### `status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `LOBBY`, `LIVE`, `ENDED`
- Description: status value.
- Example: `LOBBY`

### `version`

- Type: integer
- Required: Yes
- Nullable: No
- Description: version value.
- Example: `1`

### `hostParticipantId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `spotlightedParticipantId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UUID identifier of the tile spotlighted for everyone, or null when no shared spotlight is active.
- Example: `11111111-1111-4111-8111-111111111111`

### `endedAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## Stream

### `streamId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `READY`, `STARTING`, `LIVE`, `ENDED`
- Description: status value.
- Example: `READY`

### `version`

- Type: integer
- Required: Yes
- Nullable: No
- Description: version value.
- Example: `1`

### `startedAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `endedAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## StageRequest

### `requestId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `participantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `PENDING`, `ACCEPTED`, `REJECTED`, `CANCELLED`
- Description: status value.
- Example: `PENDING`

### `version`

- Type: integer
- Required: Yes
- Nullable: No
- Description: version value.
- Example: `1`

### `decidedByParticipantId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `createdAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `decidedAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## Share

### `shareId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `ownerParticipantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `kind`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `SCREEN`, `PDF`
- Description: kind value.
- Example: `SCREEN`

### `status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `ACTIVE`, `STOPPED`
- Description: status value.
- Example: `ACTIVE`

### `sourceReference`

- Type: string
- Required: Yes
- Nullable: No
- Description: sourceReference value.
- Example: `source-opaque-reference`

### `version`

- Type: integer
- Required: Yes
- Nullable: No
- Description: version value.
- Example: `1`

### `startedAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `stoppedAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## Recording

### `createdAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC creation timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `recordingId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `startedByParticipantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `IDLE`, `STARTING`, `RECORDING`, `STOPPED`, `FAILED`
- Description: status value.
- Example: `IDLE`

### `version`

- Type: integer
- Required: Yes
- Nullable: No
- Description: version value.
- Example: `1`

### `startedAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `stoppedAt`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## Message

### `messageId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `senderParticipantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `body`

- Type: string
- Required: Yes
- Nullable: No
- Description: body value.
- Example: `Hello everyone!`

### `sentAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `sequence`

- Type: integer
- Required: Yes
- Nullable: No
- Description: sequence value.
- Example: `1`

## Reaction

### `reactionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `participantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `reaction`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `LIKE`, `CLAP`, `HEART`, `CELEBRATE`, `HAND`, `SURPRISE`
- Description: reaction value.
- Example: `LIKE`

### `createdAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

### `sequence`

- Type: integer
- Required: Yes
- Nullable: No
- Description: sequence value.
- Example: `1`

## MediaPreference

### `participantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `microphoneDeviceId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: microphoneDeviceId value.
- Example: `device-reference`

### `cameraDeviceId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: cameraDeviceId value.
- Example: `device-reference`

### `speakerDeviceId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: speakerDeviceId value.
- Example: `device-reference`

### `virtualBackgroundId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `updatedAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## ViewPreference

### `participantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `layout`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `EQUAL_PROMINENCE`, `SIDEBAR`, `PRESENTER`
- Description: layout value.
- Example: `EQUAL_PROMINENCE`

### `focusedParticipantId`

- Type: string
- Required: Yes
- Nullable: Yes
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sidePanel`

- Type: string
- Required: Yes
- Nullable: Yes
- Allowed values: `CHAT`, `PARTICIPANTS`, `SETTINGS`
- Description: sidePanel value.
- Example: `CHAT`

### `pictureInPicture`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: pictureInPicture value.
- Example: `false`

### `updatedAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`

## Background

### `backgroundId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `name`

- Type: string
- Required: Yes
- Nullable: No
- Description: name value.
- Example: `Office`

### `assetReference`

- Type: string
- Required: Yes
- Nullable: No
- Description: assetReference value.
- Example: `background-asset-reference`

## Departure

### `departureId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `sessionId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `participantId`

- Type: string
- Required: Yes
- Nullable: No
- Description: UUID identifier.
- Example: `11111111-1111-4111-8111-111111111111`

### `kind`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `LEAVE`, `END`
- Description: kind value.
- Example: `LEAVE`

### `createdAt`

- Type: string
- Required: Yes
- Nullable: No
- Description: UTC timestamp in ISO 8601 date-time syntax.
- Example: `2026-09-22T09:00:00Z`
