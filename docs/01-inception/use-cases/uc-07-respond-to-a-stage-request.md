---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-07
uc_name: "Respond to a Stage Request"
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\uc\\uc-07-respond-to-a-stage-request.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/uc/uc-07-respond-to-a-stage-request.md
source_sha256: sha256:662ab50b65776c89369058cc6968c310be58b759caa88c40d73ae448422ac2b3
source_range: "Markdown: complete document"
uml_projection_contract: br-local-uml-v1
uml_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# UC-07: Respond to a Stage Request

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

Respond to a Stage Request

### Description

As a host, I want to accept or reject a viewer's stage request so that the viewer receives a clear participation outcome.

### Actor(s)

Host; Stage Service.

### Priority

P1.

### Trigger

The host opens a displayed stage request and chooses a response.

### Pre-Condition(s)

PRE-1: The host interface displays a stage-request item.

### Post-Condition(s)

POST-1: The host and viewer interfaces display the returned decision outcome.

### Basic Flow

1. The host opens the displayed request.
2. The client presents the available response actions.
3. The host chooses Accept.
4. The client submits the response.
5. The system returns the updated stage request and participant representation.
6. The host client renders the viewer on the stage.
7. The viewer client requests session state and renders its returned participation state.

### Alternative Flow

AF-1:

1. The host chooses Reject.
2. The client submits the response and displays the returned rejected outcome.

### Exception Flow

EF-1:

1. The stage service cannot complete the response.
2. The client displays the returned failure state and retains the request item.

### Related UI

- Live Streaming Desktop Features `6007:86770`.
- Live Streaming Mobile Features `6012:90506`.

### Related API IDs

`API-STAGE-REQUEST-CREATE`.
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
enum StageRequestStatus {
  PENDING
  ACCEPTED
  REJECTED
  CANCELLED
}
enum StageRequestAction {
  CREATE
  ACCEPT
  REJECT
  CANCEL
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
  participants: Set(Participant)
}
class Participant {
  id: String
  sessionId: String
  principalId: String
  role: ParticipantRole
  status: ParticipantStatus
  version: Integer
}
class LiveStream {
  sessionId: String
  status: StreamStatus
}
class StageRequest {
  id: String
  sessionId: String
  participantId: String
  status: StageRequestStatus
  decidedByParticipantId: String
  decidedAt: DateTime
  version: Integer
}
class StageCommand {
  sessionId: String
  actorParticipantId: String
  requestId: String
  action: StageRequestAction
  expectedVersion: Integer
  idempotencyKey: String
}
class StageService {
  decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
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
-- BR-UC-07-01
-- Source: Assumption
-- Assumption: A-19
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
pre BR_UC_07_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.actorParticipantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.actorParticipantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED and p.role = ParticipantRole::HOST)
~~~

~~~ocl
-- BR-UC-07-02
-- Source: Assumption
-- Assumption: A-19
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
pre BR_UC_07_02_TargetSession:
  command.sessionId = session.id and session.status <> SessionStatus::ENDED
~~~

~~~ocl
-- BR-UC-07-03
-- Source: Assumption
-- Assumption: A-20
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
pre BR_UC_07_03_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~ocl
-- BR-UC-07-04
-- Source: Assumption
-- Assumption: A-07
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
pre BR_UC_07_04_StreamBinding:
  stream.sessionId = session.id and session.kind = SessionKind::LIVE_STREAM and stream.status = StreamStatus::LIVE
~~~

~~~ocl
-- BR-UC-07-05
-- Source: Assumption
-- Assumption: A-07
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
pre BR_UC_07_05_PendingRequestTarget:
  (command.action = StageRequestAction::ACCEPT or command.action = StageRequestAction::REJECT) and
  request.id = command.requestId and request.sessionId = session.id and request.status = StageRequestStatus::PENDING and
  request.version = command.expectedVersion and Participant.allInstances()->exists(p | p.id = request.participantId and
    p.sessionId = session.id and p.status = ParticipantStatus::JOINED and p.role = ParticipantRole::VIEWER)
~~~

~~~ocl
-- BR-UC-07-06
-- Source: Assumption
-- Assumption: A-07
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
pre BR_UC_07_06_StageCapacity:
  command.action = StageRequestAction::ACCEPT implies session.participants->select(p |
    p.status = ParticipantStatus::JOINED and p.role <> ParticipantRole::VIEWER)->size() < 10
~~~

~~~ocl
-- BR-UC-07-07
-- Source: Assumption
-- Assumption: A-07
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
post BR_UC_07_07_Decision:
  result = request and request.version = request.version@pre + 1 and request.decidedAt <> null and
  request.decidedByParticipantId = command.actorParticipantId and
  request.status = if command.action = StageRequestAction::ACCEPT then StageRequestStatus::ACCEPTED else StageRequestStatus::REJECTED endif
~~~

~~~ocl
-- BR-UC-07-08
-- Source: Assumption
-- Assumption: A-07
context StageService::decide(command: StageCommand, session: Session, stream: LiveStream, request: StageRequest): StageRequest
post BR_UC_07_08_StageAdmission:
  let p : Participant = Participant.allInstances()->any(p | p.id = request.participantId) in
  if command.action = StageRequestAction::ACCEPT then p.role = ParticipantRole::STAGE_PARTICIPANT and p.version = p.version@pre + 1
  else p.role = p.role@pre and p.version = p.version@pre endif
~~~
