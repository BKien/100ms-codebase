# Review Resolution — 2026-09-22

The user authorized corrections to the findings in [the historical review](REVIEW-2026-09-22.md). This revision updates the package in place. It preserves the 18 supported actor goals and the original Figma source boundary; it does not claim a new Figma audit or a tested application implementation.

## Resolution map

| Finding | Correction | Main evidence |
| --- | --- | --- |
| R01 | One exclusive host/default-role branch uses a pre-provisioned designated host principal. | [UC-02](01-inception/uc/uc-02-join-a-session.md) |
| R02 | Separate leave/end and start/stop domain operations replace incompatible shared preconditions. | [UC-17](01-inception/uc/uc-17-leave-a-session.md), [UC-18](01-inception/uc/uc-18-end-a-session-for-everyone.md), [CONTEXT](CONTEXT.md) |
| R03 | Explicit join, stream, stage, sharing, recording and end effects; authenticated asynchronous start completions; host join opens the session. | [UC-02](01-inception/uc/uc-02-join-a-session.md), [UC-03](01-inception/uc/uc-03-start-a-live-stream.md), [UC-07](01-inception/uc/uc-07-respond-to-a-stage-request.md), [UC-16](01-inception/uc/uc-16-control-session-recording.md) |
| R04 | Property-level pre-state access, pre-state cascade selection, version increments and field-by-field preference frame conditions. | [UC-04](01-inception/uc/uc-04-stop-a-live-stream.md), [UC-12](01-inception/uc/uc-12-configure-audio-and-video-devices.md), [UC-15](01-inception/uc/uc-15-pin-or-spotlight-a-participant.md) |
| R05 | Trusted principal/session context, authenticated actor binding, self-only preferences and session-bound stage targets. | [Shared model](01-inception/uc/shared-domain-model.md), [UC-07](01-inception/uc/uc-07-respond-to-a-stage-request.md), [schema](schema.dbml) |
| R06 | Focus and side-panel fields, full media/view responses, and a unified atomic preference operation. | [Preferences API](01-inception/api/api-preferences-update.md) |
| R07 | Local preview draft operations and transfer of draft preferences during join. | [UC-12](01-inception/uc/uc-12-configure-audio-and-video-devices.md), [UC-13](01-inception/uc/uc-13-select-a-virtual-background.md), [Join API](01-inception/api/api-session-join.md) |
| R08 | Initial versions through join/state reads, returned resource versions, and distinct create/update version requirements. | [State API](01-inception/api/api-session-state.md), [Recording API](01-inception/api/api-recording-control.md), [UC-11](01-inception/uc/uc-11-share-presentation-content.md) |
| R09 | A stable-principal command gateway defines replay, conflicting payloads, expiry, atomic receipts and rollback. Preferences also carries a command key. | [UC-02](01-inception/uc/uc-02-join-a-session.md), [schema](schema.dbml) |
| R10 | Conditional unique expression indexes preserve repeatable history; composite foreign keys enforce session scope; serializable InnoDB transactions and MySQL triggers enforce capacities. | [schema](schema.dbml), [persistence supplement](persistence.sql) |
| R11 | Page-size input/default, stable keyset semantics and a response continuation cursor. | [Participant API](01-inception/api/api-participant-list.md), [UC-08](01-inception/uc/uc-08-view-session-participants.md) |
| R12 | Supporting state polling, chat-history and background-catalog APIs; complete reusable result representations. Terminal recording results remain visible in state reads. | [API index](01-inception/api/README.md), [Common contract](01-inception/api/common-contract.md) |
| R13 | One ReactionCode enum uses LIKE/CLAP/HEART/CELEBRATE/HAND/SURPRISE across OCL, API and storage. | [UC-10](01-inception/uc/uc-10-send-an-emoji-reaction.md), [Reaction API](01-inception/api/api-reaction-create.md) |
| R14 | Presence flags distinguish omission from explicit null; layout/PiP are non-null; merged preferences are constrained field by field. | [UC-12](01-inception/uc/uc-12-configure-audio-and-video-devices.md), [UC-14](01-inception/uc/uc-14-change-session-layout.md) |
| R15 | Preview, join and participant storage share the trimmed 1–50-character name policy, explicitly attributed to an assumption. | [UC-01](01-inception/uc/uc-01-review-join-preview-and-permissions.md), [UC-02](01-inception/uc/uc-02-join-a-session.md), [ASSUMPTIONS](ASSUMPTIONS.md) |
| R16 | UUID wire/storage mapping, persisted effective media state, explicit source-reference requirements and adapter boundaries. | [Shared model](01-inception/uc/shared-domain-model.md), [schema](schema.dbml), [UC-11](01-inception/uc/uc-11-share-presentation-content.md) |
| R17 | Explicit common envelope inheritance, complete named representations, and public authentication/access/domain-rejection outcomes. | [Common contract](01-inception/api/common-contract.md), [API index](01-inception/api/README.md) |
| R18 | Removed the join error policy leak; registered assumptions A-01 through A-23 and linked every rule; fixed PowerShell UTF-8 handling and checked UC/API references in both directions. | [ASSUMPTIONS](ASSUMPTIONS.md), [repository validator](../skills/figma-to-ocl-specs/scripts/validate_specs.ps1), [targeted validator](scripts/validate_contract.py) |

## Explicit product choices

- Preview settings remain local until join; persisted preferences belong to the joined participant.
- Guest and registered participants use the same bearer session-access boundary and stable principal identity.
- The host ends the session instead of leaving it without a controller. Host transfer is outside this package.
- Pin and spotlight affect only the caller's view.
- A stream stopped with STOP does not restart within the same session. Failed START completion may return it to READY.
- Session-state polling, rather than an unspecified event channel, supplies application state to other clients. Media delivery remains an external adapter boundary.

These decisions are assumptions in the package and can be revised through their stable assumption IDs. They are not presented as facts independently verified in Figma.

## Validation and limits

- Package and repository structural validators pass, including both-direction UC/API traceability.
- DBML targets and compiles to MySQL 8.0 SQL.
- The persistence supplement is expressed with MySQL procedures, triggers, checks, and InnoDB locking semantics.
- The MySQL verification helper applies the generated schema and persistence supplement to a disposable schema and performs a transactional smoke probe. Full constraint and concurrency scenarios require a configured MySQL 8.0 test service.
- Targeted package checks cover declared OCL operation contexts/properties/enums, assumption IDs, known pre-state mistakes, key lifecycle effects, required API fields, persistence guards and relative links.
- No full OCL parser/model checker, application implementation test, original-Figma comparison, or concurrent multi-connection stress test was run. Database runtime probes require the configured disposable MySQL service and do not replace complete service-orchestration tests.
- The unrelated Travel Booking package is unchanged; its repository validation was run to check compatibility of the shared validator changes.

## Reference notes

Pre-state and object-identity corrections follow [OMG OCL 2.4](https://www.omg.org/spec/OCL/2.4/PDF). Expression indexes and checks use [DBML's documented syntax](https://dbml.dbdiagram.io/docs/). Database verification now targets a disposable MySQL 8.0 schema.
