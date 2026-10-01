---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "Stop a Live Stream"
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\uc\\uc-04-stop-a-live-stream.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/uc/uc-04-stop-a-live-stream.md
source_sha256: sha256:0a7bb9f148af3e6e22cceb338e908b6eab282219a5ac1e5a65041c8f3e984ae7
source_range: "Markdown: complete document"
uml_projection_contract: br-local-uml-v1
uml_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# UC-04: Stop a Live Stream

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

Stop a Live Stream

### Description

As a host, I want to stop a live stream so that the broadcast ends for viewers.

### Actor(s)

Host; Live Stream Service.

### Priority

P0.

### Trigger

The host chooses the visible end-stream action.

### Pre-Condition(s)

PRE-1: The client displays a running live session.

### Post-Condition(s)

POST-1: The host interface displays the returned ended state.
POST-2: The viewer interface displays the returned post-stream outcome.

### Basic Flow

1. The host opens the end-stream action.
2. The client presents the confirmation shown by the design.
3. The host confirms the action.
4. The client submits the stop request.
5. The system returns the ended stream representation.
6. The client displays the post-stream state.

### Alternative Flow

AF-1:

1. The host cancels the confirmation.
2. The client closes the dialog and restores the live session interface.

### Exception Flow

EF-1:

1. The system cannot complete the stop request.
2. The client displays the returned failure state and preserves the current session view.

### Related UI

- Live Streaming Desktop Features `6007:86770`.
- Live Streaming Mobile Features `6012:90506`.

### Related API IDs

`API-LIVE-STREAM-CONTROL`.
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
enum StreamAction {
  START
  STOP
}
enum StageRequestStatus {
  PENDING
  ACCEPTED
  REJECTED
  CANCELLED
}
enum ShareStatus {
  ACTIVE
  STOPPED
}
enum RecordingStatus {
  IDLE
  STARTING
  RECORDING
  STOPPED
  FAILED
}
class String {
  trim(): String
}
class DateTime <<datatype>> {
}
note right of DateTime: Used only as a type; no structural member is accessed by these BRs.
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
}
class Participant {
  id: String
  sessionId: String
  principalId: String
  role: ParticipantRole
  status: ParticipantStatus
  microphoneEnabled: Boolean
  cameraEnabled: Boolean
}
class LiveStream {
  sessionId: String
  status: StreamStatus
  version: Integer
  endedAt: DateTime
}
class StageRequest {
  sessionId: String
  status: StageRequestStatus
  decidedAt: DateTime
  version: Integer
}
class ContentShare {
  sessionId: String
  status: ShareStatus
  version: Integer
  stoppedAt: DateTime
}
class Recording {
  sessionId: String
  status: RecordingStatus
  version: Integer
  stoppedAt: DateTime
}
class StreamControlCommand {
  sessionId: String
  actorParticipantId: String
  action: StreamAction
  expectedVersion: Integer
  idempotencyKey: String
}
class LiveStreamService {
  stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
}
note right of String
Removes leading and trailing whitespace; internal whitespace is unchanged.
end note
note right of RequestContext
Request-local trusted adapter data; not a process-global singleton.
Principal and session are decoded from the authenticated session access token.
participantId resolves the principal's membership.
end note
@enduml
```

## Business Rules

~~~ocl
-- BR-UC-04-01
-- Source: Assumption
-- Assumption: A-19
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
pre BR_UC_04_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.actorParticipantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.actorParticipantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED and p.role = ParticipantRole::HOST)
~~~

~~~ocl
-- BR-UC-04-02
-- Source: Assumption
-- Assumption: A-19
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
pre BR_UC_04_02_TargetSession:
  command.sessionId = session.id and session.status <> SessionStatus::ENDED
~~~

~~~ocl
-- BR-UC-04-03
-- Source: Assumption
-- Assumption: A-20
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
pre BR_UC_04_03_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~ocl
-- BR-UC-04-04
-- Source: Assumption
-- Assumption: A-04
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
pre BR_UC_04_04_StreamTargetAndVersion:
  command.action = StreamAction::STOP and session.kind = SessionKind::LIVE_STREAM and
  session.status = SessionStatus::LIVE and stream.sessionId = session.id and command.expectedVersion = stream.version
~~~

~~~ocl
-- BR-UC-04-05
-- Source: Assumption
-- Assumption: A-04
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
post BR_UC_04_05_SameStreamVersion:
  result = stream and stream.version = stream.version@pre + 1
~~~

~~~ocl
-- BR-UC-04-06
-- Source: Assumption
-- Assumption: A-04
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
pre BR_UC_04_06_RunningOnly:
  stream.status = StreamStatus::LIVE or stream.status = StreamStatus::STARTING
~~~

~~~ocl
-- BR-UC-04-07
-- Source: Assumption
-- Assumption: A-04
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
post BR_UC_04_07_EndedStream:
  stream.status = StreamStatus::ENDED and stream.endedAt <> null and session.status = session.status@pre
~~~

~~~ocl
-- BR-UC-04-08
-- Source: Assumption
-- Assumption: A-21
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
post BR_UC_04_08_DemoteFormerStageParticipants:
  Participant.allInstances()@pre->select(p | p.sessionId = command.sessionId and p.role@pre = ParticipantRole::STAGE_PARTICIPANT)->forAll(p |
    p.role = ParticipantRole::VIEWER and not p.microphoneEnabled and not p.cameraEnabled)
~~~

~~~ocl
-- BR-UC-04-09
-- Source: Assumption
-- Assumption: A-21
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
post BR_UC_04_09_StopContentShares:
  ContentShare.allInstances()@pre->select(cs | cs.sessionId = command.sessionId and cs.status@pre = ShareStatus::ACTIVE)->forAll(cs |
    cs.status = ShareStatus::STOPPED and cs.stoppedAt <> null and cs.version = cs.version@pre + 1)
~~~

~~~ocl
-- BR-UC-04-10
-- Source: Assumption
-- Assumption: A-21
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
post BR_UC_04_10_CancelPendingRequests:
  StageRequest.allInstances()@pre->select(r | r.sessionId = command.sessionId and r.status@pre = StageRequestStatus::PENDING)->forAll(r |
    r.status = StageRequestStatus::CANCELLED and r.decidedAt <> null and r.version = r.version@pre + 1)
~~~

~~~ocl
-- BR-UC-04-11
-- Source: Assumption
-- Assumption: A-21
context LiveStreamService::stop(command: StreamControlCommand, stream: LiveStream, session: Session): LiveStream
post BR_UC_04_11_StopRecordings:
  Recording.allInstances()@pre->select(r | r.sessionId = command.sessionId and
    (r.status@pre = RecordingStatus::STARTING or r.status@pre = RecordingStatus::RECORDING))->forAll(r |
    r.status = RecordingStatus::STOPPED and r.stoppedAt <> null and r.version = r.version@pre + 1)
~~~
