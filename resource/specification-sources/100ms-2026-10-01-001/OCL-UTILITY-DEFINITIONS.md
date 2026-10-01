---
artifact_type: ocl-utility-definitions
status: Frozen
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A2:B2"
retrieved_at: 2026-09-28T15:29:00Z
---

# OCL Utility Definitions

> The spreadsheet row supplies the `trim` definition and this document format. Project-specific definitions come from `01-inception/uc/shared-domain-model.md` and the local BRs. They are not an exact projection of the financial-management spreadsheet row.

```text
String.trim(): String
- Removes leading and trailing whitespace; internal whitespace is unchanged.

DateTime::now(): DateTime
- Returns the transaction-clock instant.

DateTime::addHours(value: DateTime, hours: Integer): DateTime
- Returns the instant after the specified number of elapsed hours.

DateTime::isAfter(value: DateTime, other: DateTime): Boolean
- True when value is later than other as an instant.

DomainState::snapshot(sessionId: String): String
- Canonically serializes the session and all session-owned domain rows.
- Excludes the command journal and immutable response storage; equality checks detect domain effects on replay or rejection.

DeviceCatalog::isAvailable(participantId: String, deviceId: String): Boolean
- Reports whether the named client device is available to the participant.
- This is a client device-discovery check, not a persisted server-device guarantee.

Paging::latestRecording(sessionId: String): Recording
- Returns the record with the latest (createdAt, id) key, including terminal records, or null if none exists.

Paging::validCursor(sessionId: String, cursor: String, collection: String): Boolean
- Validates cursor decoding, signature, collection, and session binding.
- An absent cursor starts before the first row.

Paging::participants(sessionId: String, pageSize: Integer, cursor: String): ParticipantPage
- Returns a live keyset page ordered by immutable (joinedAt, id) ascending.
- The cursor encodes session, collection, and last key; nextCursor is null when the scan is exhausted.

Paging::messages(sessionId: String, pageSize: Integer, cursor: String): MessagePage
- Returns messages ordered by sequence ascending, using a session-bound cursor.

Paging::reactions(sessionId: String, cursor: String): Sequence(ReactionEvent)
- Returns the next reaction-event page in ascending sequence.

Paging::nextReactionCursor(sessionId: String, cursor: String): String
- Returns the cursor for the next reaction read, retaining a high-water mark even when a page is empty.
```

The paging cursors are authenticated opaque values. Domain permissions and page limits remain in the BRs. Service operations such as `SessionJoinService::join` and `ClientPreferenceService::selectDevices` are BR contexts rather than utility helpers.

## Utility Classes

```text
class String <<Primitive>> {
  +trim(): String
}

class DateTime <<Primitive>> {
  +now(): DateTime
  +addHours(value: DateTime, hours: Integer): DateTime
  +isAfter(value: DateTime, other: DateTime): Boolean
}

class DomainState <<Utility>> {
  +snapshot(sessionId: String): String
}

class DeviceCatalog <<Utility>> {
  +isAvailable(participantId: String, deviceId: String): Boolean
}

class Paging <<Utility>> {
  +latestRecording(sessionId: String): Recording
  +validCursor(sessionId: String, cursor: String, collection: String): Boolean
  +participants(sessionId: String, pageSize: Integer, cursor: String): ParticipantPage
  +messages(sessionId: String, pageSize: Integer, cursor: String): MessagePage
  +reactions(sessionId: String, cursor: String): Sequence(ReactionEvent)
  +nextReactionCursor(sessionId: String, cursor: String): String
}

```
