---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "Change Session Layout"
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\uc\\uc-14-change-session-layout.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/uc/uc-14-change-session-layout.md
source_sha256: sha256:403457daaf0adf6366ea8f38e9d9e3315dd958801096fc1d52405caa7aaa6f47
source_range: "Markdown: complete document"
uml_projection_contract: br-local-uml-v1
uml_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# UC-14: Change Session Layout

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Change Session Layout

### Description

As a participant, I want to change my session layout or picture-in-picture view so that I can focus on the content that matters to me.

### Actor(s)

Participant; Preference Service.

### Priority

P2.

### Trigger

The participant chooses a layout or picture-in-picture control.

### Pre-Condition(s)

PRE-1: The client displays a joined-session interface.

### Post-Condition(s)

POST-1: The client renders the returned view preference.

### Basic Flow

1. The participant opens the view controls.
2. The client presents the layouts shown by the design.
3. The participant selects a layout.
4. The client submits the preference update.
5. The system returns the updated view preference.
6. The client renders the selected layout.

### Alternative Flow

AF-1:

1. The participant enables picture-in-picture.
2. The client renders the returned picture-in-picture view.

AF-2:

1. The participant opens or closes a side panel.
2. The client adjusts the returned session layout.

### Exception Flow

EF-1:

1. The preference update cannot be completed.
2. The client displays the returned failure state and retains the previous layout.

### Related UI

- Live Streaming Desktop Layouts `6007:96234`.
- Live Streaming Mobile Layouts `6012:102740`.
- Video Conferencing Desktop Layouts `6007:77656`.
- Video Conferencing Mobile Layouts `6012:78022`.

### Related API IDs

`API-PREFERENCES-UPDATE`.
`API-SESSION-STATE`.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

UC-12 through UC-14 and the personal-pin rules in UC-15 constrain one atomic PreferenceService.update operation. Field-presence guards determine which values change. Client-local preview operations do not call this server operation.

## UML Model

Local projection of exactly the vocabulary needed by the Business Rules below, including signature and helper types. Enum domains are retained in full to preserve their value semantics.

```plantuml
@startuml
hide empty members
enum ShareStatus {
  ACTIVE
  STOPPED
}
enum LayoutMode {
  EQUAL_PROMINENCE
  SIDEBAR
  PRESENTER
}
class String <<datatype>> {
}
note right of String: Used only as a type; no structural member is accessed by these BRs.
class ContentShare {
  sessionId: String
  status: ShareStatus
}
class MediaPreference <<opaque>> {
}
note right of MediaPreference: Used only as a type; no structural member is accessed by these BRs.
class ViewPreference {
  layout: LayoutMode
  sidePanel: String
  pictureInPicture: Boolean
}
class PreferencePatch {
  sessionId: String
  hasLayout: Boolean
  layout: LayoutMode
  hasSidePanel: Boolean
  sidePanel: String
  hasPictureInPicture: Boolean
  pictureInPicture: Boolean
}
class PreferencesResult <<opaque>> {
}
note right of PreferencesResult: Used only as a type; no structural member is accessed by these BRs.
class PreferenceService {
  update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
}
@enduml
```

## Business Rules

~~~ocl
-- BR-UC-14-01
-- Source: Assumption
-- Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_14_01_NonNullLayoutAndPiP:
  (command.hasLayout implies command.layout <> null) and (command.hasPictureInPicture implies command.pictureInPicture <> null)
~~~

~~~ocl
-- BR-UC-14-02
-- Source: Assumption
-- Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_14_02_PresenterLayout:
  (command.hasLayout and command.layout = LayoutMode::PRESENTER) implies
  ContentShare.allInstances()->exists(s | s.sessionId = command.sessionId and s.status = ShareStatus::ACTIVE)
~~~

~~~ocl
-- BR-UC-14-03
-- Source: Assumption
-- Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_14_03_PanelValues:
  command.hasSidePanel implies (command.sidePanel = null or command.sidePanel = 'CHAT' or command.sidePanel = 'PARTICIPANTS' or command.sidePanel = 'SETTINGS')
~~~

~~~ocl
-- BR-UC-14-04
-- Source: Assumption
-- Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_14_04_LayoutPatch:
  view.layout = if command.hasLayout then command.layout else view.layout@pre endif
~~~

~~~ocl
-- BR-UC-14-05
-- Source: Assumption
-- Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_14_05_PiPPatch:
  view.pictureInPicture = if command.hasPictureInPicture then command.pictureInPicture else view.pictureInPicture@pre endif
~~~

~~~ocl
-- BR-UC-14-06
-- Source: Assumption
-- Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_14_06_PiPClearsPanel:
  view.pictureInPicture implies view.sidePanel = null
~~~

~~~ocl
-- BR-UC-14-07
-- Source: Assumption
-- Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_14_07_PanelPatch:
  not view.pictureInPicture implies
    view.sidePanel = if command.hasSidePanel then command.sidePanel else view.sidePanel@pre endif
~~~
