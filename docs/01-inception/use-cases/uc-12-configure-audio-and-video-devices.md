---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-12
uc_name: "Configure Audio and Video Devices"
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\uc\\uc-12-configure-audio-and-video-devices.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/uc/uc-12-configure-audio-and-video-devices.md
source_sha256: sha256:c4d57472414e077ca1d44c44fee751eed13ba2b5ee1e127c2d4a314ec4740bf7
source_range: "Markdown: complete document"
uml_projection_contract: br-local-uml-v1
uml_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# UC-12: Configure Audio and Video Devices

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

Configure Audio and Video Devices

### Description

As a participant, I want to select my microphone, camera, and audio output so that the session uses my preferred devices.

### Actor(s)

Participant; Preference Service.

### Priority

P1.

### Trigger

The participant opens device settings.

### Pre-Condition(s)

PRE-1: The client displays a preview or joined-session interface.

### Post-Condition(s)

POST-1: The client displays and applies the returned device preferences.

### Basic Flow

1. The participant opens device settings.
2. The client presents the available microphone, camera, and audio-output choices.
3. The participant selects the desired values and confirms.
4. The client applies the selection locally in preview, or submits the preference update from the joined session.
5. The client receives the local result or the returned device preferences.
6. The client applies the returned settings to the preview or session.

### Alternative Flow

AF-1:

1. The participant closes settings without confirming.
2. The client restores the previous preview or session state.

### Exception Flow

EF-1:

1. The selected preference cannot be applied.
2. The client displays the returned failure state and keeps the previous visible selection.

### Related UI

- Settings `6007:51132`.
- Video Conferencing Desktop Preview `6066:89727`.
- Video Conferencing Mobile Preview `6066:89005`.

### Related API IDs

`API-PREFERENCES-UPDATE`.
`API-SESSION-JOIN`.
`API-SESSION-STATE`.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

UC-12 through UC-14 and the personal-pin rules in UC-15 constrain one atomic PreferenceService.update operation. Field-presence guards determine which values change. Client-local preview operations do not call this server operation.

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
}
class Participant {
  id: String
  sessionId: String
  principalId: String
  status: ParticipantStatus
}
class MediaPreference {
  participantId: String
  microphoneDeviceId: String
  cameraDeviceId: String
  speakerDeviceId: String
  virtualBackgroundId: String
  updatedAt: DateTime
}
class ViewPreference {
  participantId: String
  updatedAt: DateTime
}
class DeviceCatalog {
  {static} isAvailable(participantId: String, deviceId: String): Boolean
}
class PreviewDraft {
  participantKey: String
  microphoneDeviceId: String
  cameraDeviceId: String
  speakerDeviceId: String
  virtualBackgroundId: String
}
class PreferencePatch {
  sessionId: String
  participantId: String
  idempotencyKey: String
  hasMicrophoneDeviceId: Boolean
  microphoneDeviceId: String
  hasCameraDeviceId: Boolean
  cameraDeviceId: String
  hasSpeakerDeviceId: Boolean
  speakerDeviceId: String
}
class PreferencesResult {
  media: MediaPreference
  view: ViewPreference
}
class PreferenceService {
  update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
}
class ClientPreferenceService {
  selectDevices(draft: PreviewDraft, microphone: String, camera: String, speaker: String): PreviewDraft
}
note right of String
Removes leading and trailing whitespace; internal whitespace is unchanged.
end note
note right of DeviceCatalog
Reports whether the named client device is available to the participant.
This is a client device-discovery check, not a persisted server-device guarantee.
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
-- BR-UC-12-01
-- Source: Assumption
-- Assumption: A-19
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_12_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.participantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.participantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~ocl
-- BR-UC-12-02
-- Source: Assumption
-- Assumption: A-20
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_12_02_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~ocl
-- BR-UC-12-03
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_12_03_PreferenceTarget:
  media.participantId = command.participantId and view.participantId = command.participantId and
  Session.allInstances()->exists(s | s.id = command.sessionId and s.status <> SessionStatus::ENDED)
~~~

~~~ocl
-- BR-UC-12-04
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_12_04_PreferenceIdentity:
  result.media = media and result.view = view and media.updatedAt <> null and view.updatedAt <> null
~~~

~~~ocl
-- BR-UC-12-05
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_12_05_microphoneDeviceIdSyntax:
  command.hasMicrophoneDeviceId implies (command.microphoneDeviceId = null or command.microphoneDeviceId.trim().size() > 0)
~~~

~~~ocl
-- BR-UC-12-06
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_12_06_microphoneDeviceIdPatch:
  media.microphoneDeviceId = if command.hasMicrophoneDeviceId then command.microphoneDeviceId else media.microphoneDeviceId@pre endif
~~~

~~~ocl
-- BR-UC-12-07
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_12_07_cameraDeviceIdSyntax:
  command.hasCameraDeviceId implies (command.cameraDeviceId = null or command.cameraDeviceId.trim().size() > 0)
~~~

~~~ocl
-- BR-UC-12-08
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_12_08_cameraDeviceIdPatch:
  media.cameraDeviceId = if command.hasCameraDeviceId then command.cameraDeviceId else media.cameraDeviceId@pre endif
~~~

~~~ocl
-- BR-UC-12-09
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_12_09_speakerDeviceIdSyntax:
  command.hasSpeakerDeviceId implies (command.speakerDeviceId = null or command.speakerDeviceId.trim().size() > 0)
~~~

~~~ocl
-- BR-UC-12-10
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_12_10_speakerDeviceIdPatch:
  media.speakerDeviceId = if command.hasSpeakerDeviceId then command.speakerDeviceId else media.speakerDeviceId@pre endif
~~~

~~~ocl
-- BR-UC-12-11
-- Source: Assumption
-- Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_12_11_OtherMediaUnchanged:
  MediaPreference.allInstances() = MediaPreference.allInstances()@pre and
  MediaPreference.allInstances()@pre->select(m | m.participantId <> command.participantId)->forAll(m |
    m.microphoneDeviceId = m.microphoneDeviceId@pre and m.cameraDeviceId = m.cameraDeviceId@pre and
    m.speakerDeviceId = m.speakerDeviceId@pre and m.virtualBackgroundId = m.virtualBackgroundId@pre and m.updatedAt = m.updatedAt@pre)
~~~

~~~ocl
-- BR-UC-12-12
-- Source: Assumption
-- Assumption: A-12
context ClientPreferenceService::selectDevices(draft: PreviewDraft, microphone: String, camera: String, speaker: String): PreviewDraft
pre BR_UC_12_12_LocalDeviceAvailability:
  (microphone = null or DeviceCatalog::isAvailable(draft.participantKey, microphone)) and
  (camera = null or DeviceCatalog::isAvailable(draft.participantKey, camera)) and
  (speaker = null or DeviceCatalog::isAvailable(draft.participantKey, speaker))
~~~

~~~ocl
-- BR-UC-12-13
-- Source: Assumption
-- Assumption: A-12
context ClientPreferenceService::selectDevices(draft: PreviewDraft, microphone: String, camera: String, speaker: String): PreviewDraft
post BR_UC_12_13_LocalDeviceDraft:
  result = draft and draft.microphoneDeviceId = microphone and draft.cameraDeviceId = camera and
  draft.speakerDeviceId = speaker and draft.virtualBackgroundId = draft.virtualBackgroundId@pre
~~~
