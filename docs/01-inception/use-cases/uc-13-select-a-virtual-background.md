---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-13
uc_name: "Select a Virtual Background"
source_type: local-markdown
source_path: "D:\\figma_spec\\100ms Video Conferencing and Live Streaming\\01-inception\\uc\\uc-13-select-a-virtual-background.md"
source_snapshot_path: resource/specification-sources/100ms-2026-10-01-001/01-inception/uc/uc-13-select-a-virtual-background.md
source_sha256: sha256:369a69b8ed11b07e804acc652d0f608a69b8cddb9c6da102a63caf1b54ce1669
source_range: "Markdown: complete document"
uml_projection_contract: br-local-uml-v1
uml_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json
retrieved_at: 2026-10-01T09:29:46.379459Z
---

# UC-13: Select a Virtual Background

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

Select a Virtual Background

### Description

As a participant, I want to select a virtual background so that my preview uses the chosen appearance.

### Actor(s)

Participant; Preference Service.

### Priority

P2.

### Trigger

The participant opens virtual-background choices.

### Pre-Condition(s)

PRE-1: The client displays a camera preview.

### Post-Condition(s)

POST-1: The client displays the returned background preference in the preview.

### Basic Flow

1. The participant opens virtual-background choices.
2. The client presents the available background previews.
3. The participant selects a background.
4. The client applies the selection locally in preview, or submits the preference update from the joined session.
5. The client receives the local result or the returned media preference.
6. The client renders the selected background in the preview.

### Alternative Flow

AF-1:

1. The participant selects the no-background choice.
2. The client removes the background treatment from the preview.

### Exception Flow

EF-1:

1. The preference cannot be applied.
2. The client displays the returned failure state and retains the previous preview.

### Related UI

- Virtual Background `6026:1184329`.

### Related API IDs

`API-PREFERENCES-UPDATE`.
`API-SESSION-JOIN`.
`API-BACKGROUND-LIST`.
`API-SESSION-STATE`.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

UC-12 through UC-14 and the personal-pin rules in UC-15 constrain one atomic PreferenceService.update operation. Field-presence guards determine which values change. Client-local preview operations do not call this server operation.

## UML Model

Local projection of exactly the vocabulary needed by the Business Rules below, including signature and helper types. Enum domains are retained in full to preserve their value semantics.

```plantuml
@startuml
hide empty members
class String {
  trim(): String
}
class RequestContext {
  {static} authenticated: Boolean
}
class MediaPreference {
  virtualBackgroundId: String
}
class ViewPreference <<opaque>> {
}
note right of ViewPreference: Used only as a type; no structural member is accessed by these BRs.
class VirtualBackground {
  id: String
  assetReference: String
  active: Boolean
}
class PreviewDraft {
  microphoneDeviceId: String
  cameraDeviceId: String
  speakerDeviceId: String
  virtualBackgroundId: String
}
class PreferencePatch {
  hasVirtualBackgroundId: Boolean
  virtualBackgroundId: String
}
class PreferencesResult <<opaque>> {
}
note right of PreferencesResult: Used only as a type; no structural member is accessed by these BRs.
class PreferenceService {
  update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
  listBackgrounds(): Set(VirtualBackground)
}
class ClientPreferenceService {
  selectBackground(draft: PreviewDraft, backgroundId: String): PreviewDraft
}
note right of String
Removes leading and trailing whitespace; internal whitespace is unchanged.
end note
note right of RequestContext
Request-local trusted adapter data; not a process-global singleton.
Principal and session are decoded from the authenticated session access token.
end note
@enduml
```

## Business Rules

~~~ocl
-- BR-UC-13-01
-- Source: Assumption
-- Assumption: A-13
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_UC_13_01_AvailableBackground:
  command.hasVirtualBackgroundId implies (command.virtualBackgroundId = null or
    VirtualBackground.allInstances()->exists(b | b.id = command.virtualBackgroundId and b.active))
~~~

~~~ocl
-- BR-UC-13-02
-- Source: Assumption
-- Assumption: A-13
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_UC_13_02_BackgroundPatch:
  media.virtualBackgroundId = if command.hasVirtualBackgroundId then command.virtualBackgroundId else media.virtualBackgroundId@pre endif
~~~

~~~ocl
-- BR-UC-13-03
-- Source: Assumption
-- Assumption: A-13
context ClientPreferenceService::selectBackground(draft: PreviewDraft, backgroundId: String): PreviewDraft
pre BR_UC_13_03_LocalBackground:
  backgroundId = null or VirtualBackground.allInstances()->exists(b | b.id = backgroundId and b.active)
~~~

~~~ocl
-- BR-UC-13-04
-- Source: Assumption
-- Assumption: A-13
context ClientPreferenceService::selectBackground(draft: PreviewDraft, backgroundId: String): PreviewDraft
post BR_UC_13_04_LocalBackgroundDraft:
  result = draft and draft.virtualBackgroundId = backgroundId and
  draft.microphoneDeviceId = draft.microphoneDeviceId@pre and draft.cameraDeviceId = draft.cameraDeviceId@pre and draft.speakerDeviceId = draft.speakerDeviceId@pre
~~~

~~~ocl
-- BR-UC-13-05
-- Source: Assumption
-- Assumption: A-19
context PreferenceService::listBackgrounds(): Set(VirtualBackground)
pre BR_UC_13_05_CatalogReader:
  RequestContext::authenticated
~~~

~~~ocl
-- BR-UC-13-06
-- Source: Assumption
-- Assumption: A-13
context PreferenceService::listBackgrounds(): Set(VirtualBackground)
post BR_UC_13_06_CatalogResult:
  result = VirtualBackground.allInstances()->select(b | b.active)
~~~

~~~ocl
-- BR-UC-13-07
-- Source: Assumption
-- Assumption: A-13
context PreferenceService::listBackgrounds(): Set(VirtualBackground)
post BR_UC_13_07_CatalogIdentity:
  result->isUnique(id) and result->forAll(b | b.assetReference <> null and b.assetReference.trim().size() > 0)
~~~
