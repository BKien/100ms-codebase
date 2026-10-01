---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "Send an Emoji Reaction"
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\uc\\uc-10-send-an-emoji-reaction.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/uc/uc-10-send-an-emoji-reaction.md
source_sha256: sha256:196e541fd4a78959fd2c784ded2def2eed2a2bdb84b1cdfa2d8f32ede678cbd8
source_range: "Markdown: complete document"
uml_projection_contract: br-local-uml-v1
uml_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# UC-10: Send an Emoji Reaction

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

Send an Emoji Reaction

### Description

As a participant, I want to send an emoji reaction so that I can respond without interrupting the session.

### Actor(s)

Participant; Collaboration Service.

### Priority

P2.

### Trigger

The participant opens the reaction controls and chooses an emoji.

### Pre-Condition(s)

PRE-1: The participant is viewing a joined-session interface.

### Post-Condition(s)

POST-1: The client renders the reaction event returned by the system.

### Basic Flow

1. The participant opens the emoji reaction controls.
2. The client presents the available reaction choices.
3. The participant chooses a reaction.
4. The client submits the reaction.
5. The system returns the created event.
6. The client renders the reaction in the session.

### Alternative Flow

AF-1:

1. The participant closes the reaction controls without selecting an item.
2. The client restores the session controls.

### Exception Flow

EF-1:

1. The reaction cannot be created.
2. The client displays the returned failure notice without closing the session.

### Related UI

- Video Conferencing Desktop Features `6007:55138`.
- Component evidence: Modal/Emoji Reactions.

### Related API IDs

`API-REACTION-CREATE`.
`API-SESSION-STATE`.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

## UML Model

Local projection of exactly the vocabulary needed by the Business Rules below, including signature and helper types. Enum domains are retained in full to preserve their value semantics.

```plantuml
@startuml
hide empty members
enum SessionStatus {
  LOBBY
  LIVE
  ENDED
}
enum ParticipantStatus {
  JOINED
  LEFT
}
enum ReactionCode {
  LIKE
  CLAP
  HEART
  CELEBRATE
  HAND
  SURPRISE
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
  status: SessionStatus
  version: Integer
}
class Participant {
  id: String
  sessionId: String
  principalId: String
  status: ParticipantStatus
}
class StageRequest <<extent>> {
  {static} allInstances(): Set(StageRequest)
}
class ReactionEvent {
  id: String
  sessionId: String
  participantId: String
  reaction: ReactionCode
  createdAt: DateTime
  sequence: Integer
}
class ReactionCommand {
  sessionId: String
  participantId: String
  reaction: ReactionCode
  idempotencyKey: String
}
class CollaborationService {
  sendReaction(command: ReactionCommand, session: Session): ReactionEvent
}
note "allInstances() is the standard OCL classifier extent.\nAn extent-only classifier has no structural properties in this UC projection." as ExtentSemantics
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
-- BR-UC-10-01
-- Source: Assumption
-- Assumption: A-19
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
pre BR_UC_10_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.participantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.participantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~ocl
-- BR-UC-10-02
-- Source: Assumption
-- Assumption: A-19
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
pre BR_UC_10_02_TargetSession:
  command.sessionId = session.id and session.status <> SessionStatus::ENDED
~~~

~~~ocl
-- BR-UC-10-03
-- Source: Assumption
-- Assumption: A-20
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
pre BR_UC_10_03_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~ocl
-- BR-UC-10-04
-- Source: Assumption
-- Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_UC_10_04_CreatedIdentity:
  result.oclIsNew() and result.id <> null and result.sessionId = command.sessionId and result.participantId = command.participantId
~~~

~~~ocl
-- BR-UC-10-05
-- Source: Assumption
-- Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_UC_10_05_ReactionValue:
  result.reaction = command.reaction and result.createdAt <> null and result.sequence = session.version@pre + 1
~~~

~~~ocl
-- BR-UC-10-06
-- Source: Assumption
-- Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_UC_10_06_ParticipationUnaffected:
  Participant.allInstances() = Participant.allInstances()@pre
~~~

~~~ocl
-- BR-UC-10-07
-- Source: Assumption
-- Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_UC_10_07_NoImplicitStageRequest:
  StageRequest.allInstances() = StageRequest.allInstances()@pre
~~~
