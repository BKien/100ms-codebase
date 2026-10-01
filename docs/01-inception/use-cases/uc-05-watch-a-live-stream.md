---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "Watch a Live Stream"
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\uc\\uc-05-watch-a-live-stream.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/uc/uc-05-watch-a-live-stream.md
source_sha256: sha256:fdf2cc6ce6e9affab20e61c434d316c7b7177b50adb43603edae06ce9c666730
source_range: "Markdown: complete document"
uml_projection_contract: br-local-uml-v1
uml_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# UC-05: Watch a Live Stream

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

Watch a Live Stream

### Description

As a viewer, I want to open the live session so that I can watch the broadcast and access viewer controls.

### Actor(s)

Viewer; Live Stream Service.

### Priority

P0.

### Trigger

The viewer opens the live-session interface.

### Pre-Condition(s)

PRE-1: The client has a live-session destination to display.

### Post-Condition(s)

POST-1: The client displays live playback and the viewer controls returned by the system.

### Basic Flow

1. The viewer opens the live session.
2. The client requests the current session representation.
3. The system returns the viewer-facing stream state.
4. The client renders playback and viewer controls.

### Alternative Flow

AF-1:

1. The viewer opens the session menu.
2. The client displays the viewer actions shown by the design.

### Exception Flow

EF-1:

1. The live-session representation cannot be returned.
2. The client displays the visible loading or unavailable state.

### Related UI

- Live Streaming Viewer `6007:51397`.
- Live Streaming Mobile Preview `6012:44409`.

### Related API IDs

`API-LIVE-STREAM-VIEW`.
`API-SESSION-STATE`.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

## UML Model

Local projection of exactly the vocabulary needed by the Business Rules below, including signature and helper types. Enum domains are retained in full to preserve their value semantics.

```plantuml
@startuml
hide empty members
enum SessionKind {
  LIVE_STREAM
  VIDEO_CONFERENCE
}
enum SessionStatus {
  LOBBY
  LIVE
  ENDED
}
enum ParticipantRole {
  HOST
  BROADCASTER
  VIEWER
  STAGE_PARTICIPANT
}
enum ParticipantStatus {
  JOINED
  LEFT
}
enum StreamStatus {
  READY
  STARTING
  LIVE
  ENDED
}
class String <<datatype>> {
}
note right of String: Used only as a type; no structural member is accessed by these BRs.
class RequestContext {
  {static} principalId: String
  {static} participantId: String
  {static} sessionId: String
  {static} authenticated: Boolean
}
class Session {
  id: String
  kind: SessionKind
  status: SessionStatus
  version: Integer
}
class Participant {
  id: String
  sessionId: String
  principalId: String
  role: ParticipantRole
  status: ParticipantStatus
}
class LiveStream {
  sessionId: String
  status: StreamStatus
  version: Integer
}
class ViewerSession {
  sessionId: String
  participantId: String
  role: ParticipantRole
  streamStatus: StreamStatus
  streamVersion: Integer
  sessionVersion: Integer
  canPlayMedia: Boolean
  canPublishMedia: Boolean
  initialAudioMuted: Boolean
}
class LiveStreamService {
  view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
}
note right of RequestContext
Request-local trusted adapter data; not a process-global singleton.
Principal and session are decoded from the authenticated session access token.
participantId resolves the principal's membership.
end note
@enduml
```

## Business Rules

~~~ocl
-- BR-UC-05-01
-- Source: Assumption
-- Assumption: A-19
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
pre BR_UC_05_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = sessionId and
  participantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = participantId and
    p.principalId = RequestContext::principalId and p.sessionId = sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~ocl
-- BR-UC-05-02
-- Source: Assumption
-- Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
pre BR_UC_05_02_ViewerTarget:
  session.id = sessionId and stream.sessionId = sessionId and session.kind = SessionKind::LIVE_STREAM and
  session.status <> SessionStatus::ENDED and Participant.allInstances()->exists(p | p.id = participantId and
    (p.role = ParticipantRole::VIEWER or p.role = ParticipantRole::STAGE_PARTICIPANT))
~~~

~~~ocl
-- BR-UC-05-03
-- Source: Assumption
-- Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_UC_05_03_ViewerRepresentation:
  result.sessionId = session.id and result.participantId = participantId and
  result.role = Participant.allInstances()->any(p | p.id = participantId).role
~~~

~~~ocl
-- BR-UC-05-04
-- Source: Assumption
-- Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_UC_05_04_StreamSnapshot:
  result.streamStatus = stream.status and result.streamVersion = stream.version and result.sessionVersion = session.version
~~~

~~~ocl
-- BR-UC-05-05
-- Source: Assumption
-- Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_UC_05_05_PlaybackAvailability:
  result.canPlayMedia = (stream.status = StreamStatus::LIVE)
~~~

~~~ocl
-- BR-UC-05-06
-- Source: Assumption
-- Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_UC_05_06_PublishingAvailability:
  result.canPublishMedia = (stream.status = StreamStatus::LIVE and result.role = ParticipantRole::STAGE_PARTICIPANT)
~~~

~~~ocl
-- BR-UC-05-07
-- Source: Assumption
-- Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_UC_05_07_MutedPlaybackStart:
  result.initialAudioMuted
~~~
