# Assumptions

These explicit assumptions complete the existing supported Figma scope. They are implementation decisions, not additional claims about the design or the 100ms provider. Rule blocks cite the stable IDs below.

## A-01 — Preview and names

Display names are trimmed and contain 1–50 characters after trimming; preview and join use the same rule. Permissions, hardware and requested track state govern local preview. Viewer preview starts muted. These are assumptions, not asserted hidden Figma facts.

Rule references: `BR-UC-01-01`, `BR-UC-01-02`, `BR-UC-01-03`, `BR-UC-01-04`, `BR-UC-01-05`, `BR-UC-01-06`, `BR-UC-01-07`, `BR-UC-02-04`.

## A-02 — Join and session lifecycle

Provisioning supplies a designated host principal before join. Host identity takes precedence over role defaults. The host joins as HOST; other live-stream participants join as VIEWER and conference participants as BROADCASTER. Host join opens LOBBY to LIVE. Non-hosts can wait in LOBBY. Duplicate joined membership for a principal is rejected. Capacities are 100 conference members, 1,000 stream members and 10 on-stage members, including the host.

Rule references: `BR-UC-02-05`, `BR-UC-02-06`, `BR-UC-02-07`, `BR-UC-02-08`, `BR-UC-02-09`, `BR-UC-02-10`, `BR-UC-02-11`.

## A-03 — Stream start and completion

Only the joined host starts a READY stream in a LIVE session. START produces STARTING; a trusted provider completion produces LIVE or resets to READY on failure. A completion is conditional on its resource version, so a stale completion cannot undo STOP/END.

Rule references: `BR-UC-03-04`, `BR-UC-03-05`, `BR-UC-03-06`, `BR-UC-03-07`, `BR-UC-03-08`, `BR-UC-03-09`.

## A-04 — Stream stop and restart

Only the joined host stops STARTING/LIVE. STOP produces ENDED but preserves the session status. A stopped stream cannot restart in that session. A new provisioned session is required. The stop operation also applies the cascade rules.

Rule references: `BR-UC-04-04`, `BR-UC-04-05`, `BR-UC-04-06`, `BR-UC-04-07`.

## A-05 — Viewer representation

Viewer playback uses LIVE stream state; viewer publishing is disabled. Stage participants may publish while the stream is live. Autoplay starts muted.

Rule references: `BR-UC-05-02`, `BR-UC-05-03`, `BR-UC-05-04`, `BR-UC-05-05`, `BR-UC-05-06`, `BR-UC-05-07`.

## A-06 — Stage requests

Joined viewers create one pending request while the stream is live. CREATE has no request/version target. A viewer cancels only its own pending request with the observed request version.

Rule references: `BR-UC-06-04`, `BR-UC-06-05`, `BR-UC-06-06`, `BR-UC-06-07`, `BR-UC-06-08`.

## A-07 — Stage decisions

Only the joined host decides a pending request belonging to the same live stream session. ACCEPT changes the viewer role to STAGE_PARTICIPANT; REJECT preserves it. ACCEPT enforces the 10-person stage limit. Version comparison makes decisions atomic.

Rule references: `BR-UC-07-04`, `BR-UC-07-05`, `BR-UC-07-06`, `BR-UC-07-07`, `BR-UC-07-08`.

## A-08 — Participant reads

Joined members read their session roster. Page size defaults to 50 and must be 1–50. The roster uses stable ascending joinedAt/id keyset order, without inferred host-first ranking. Cursors are scoped to the session and collection.

Rule references: `BR-UC-08-02`, `BR-UC-08-03`, `BR-UC-08-07`.

## A-09 — Chat

Joined members send nonempty trimmed messages of at most 1,000 characters. The stored normalized body is returned. Server timestamps and session revision sequences identify messages. Chat is rendered as plain text; trimming is not an HTML sanitizer.

Rule references: `BR-UC-09-04`, `BR-UC-09-05`, `BR-UC-09-06`.

## A-10 — Reactions

Canonical values are LIKE, CLAP, HEART, CELEBRATE, HAND and SURPRISE. Clients map these to the six emoji appearances. Reaction HAND is visual feedback, not an implicit stage request.

Rule references: `BR-UC-10-04`, `BR-UC-10-05`, `BR-UC-10-06`, `BR-UC-10-07`.

## A-11 — Sharing

Only one share is active in a session. A live-stream viewer cannot start sharing. START requires a selected SCREEN/PDF kind and a source reference supplied by the media/content adapter, and has no expected share version. The owner or joined host stops the current share with its observed version.

Rule references: `BR-UC-11-04`, `BR-UC-11-05`, `BR-UC-11-06`.

## A-12 — Preview drafts and media preferences

Before join, device choices are local draft state. Join transfers them and creates the participant preference rows. Device availability is checked by the client adapter. Server PATCH stores opaque references. All server preference operations are self-only; omitted fields are preserved and explicit null clears nullable fields.

Rule references: `BR-UC-02-13`, `BR-UC-12-03`, `BR-UC-12-04`, `BR-UC-12-05`, `BR-UC-12-06`, `BR-UC-12-07`, `BR-UC-12-08`, `BR-UC-12-09`, `BR-UC-12-10`, `BR-UC-12-11`, `BR-UC-12-12`, `BR-UC-12-13`.

## A-13 — Virtual backgrounds

The catalog lists enabled background assets. The no-background choice is null. A local preview selection becomes a draft until join; joined selections use the same preference PATCH.

Rule references: `BR-UC-02-12`, `BR-UC-13-01`, `BR-UC-13-02`, `BR-UC-13-03`, `BR-UC-13-04`, `BR-UC-13-06`, `BR-UC-13-07`.

## A-14 — Layout and panels

Layout and pictureInPicture cannot be null. PiP clears the side panel; otherwise the panel is null, CHAT, PARTICIPANTS or SETTINGS. PRESENTER can be selected only with an active content share. Updates are personal.

Rule references: `BR-UC-14-01`, `BR-UC-14-02`, `BR-UC-14-03`, `BR-UC-14-04`, `BR-UC-14-05`, `BR-UC-14-06`, `BR-UC-14-07`.

## A-15 — Pin and spotlight

Pin is a personal view preference, matching `Pin Tile for Myself` in the Figma tile menu. Spotlight is session-scoped, matching `Spotlight Tile for Everyone`; the session state exposes one nullable spotlight target to every client. Pin and spotlight targets must be joined in the same session. The design shows spotlight to publishing participants, so HOST, BROADCASTER and STAGE_PARTICIPANT may set or clear it; VIEWER may not. Personal pins remain unchanged when the shared spotlight changes.

Rule references: `BR-UC-15-01`, `BR-UC-15-02`, `BR-UC-15-03`, `BR-UC-15-06`, `BR-UC-15-07`, `BR-UC-15-08`, `BR-UC-15-09`, `BR-UC-15-10`.

## A-16 — Recording

Only the joined host controls recording. START in a LIVE session creates a STARTING record with a creation timestamp at version 1 with no expected recording version. One STARTING/RECORDING instance is permitted. Provider completion changes it to RECORDING or FAILED. STOP compares the current recording version. Provider references remain internal.

Rule references: `BR-UC-16-04`, `BR-UC-16-05`, `BR-UC-16-06`, `BR-UC-16-07`, `BR-UC-16-08`.

## A-17 — Leave

A non-host leaves independently and the session status is preserved. The host uses End for everyone; host transfer is not introduced. Leave disables media, stops owned content and cancels pending requests. Rejoin creates a new participant ID for the same principal.

Rule references: `BR-UC-17-04`, `BR-UC-17-05`, `BR-UC-17-06`, `BR-UC-17-07`.

## A-18 — End for everyone

The joined host ends a non-ended session with its observed session version. The session becomes ENDED, joined participants become LEFT, media is disabled, and the stream, recording, share and pending-request cascades run atomically.

Rule references: `BR-UC-18-04`, `BR-UC-18-05`, `BR-UC-18-06`, `BR-UC-18-07`, `BR-UC-18-08`.

## A-19 — Trust and identity

Both registered and anonymous users receive an externally provisioned bearer session access token with a stable principal ID and session scope. The token remains usable across the documented endpoints; join does not exchange it. Command actor IDs come from trusted membership resolution. Provider callbacks use separate authentication. UUID text is used consistently at wire and database boundaries. Raw tokens are not persisted.

Rule references: `BR-UC-02-01`, `BR-UC-02-02`, `BR-UC-03-01`, `BR-UC-03-02`, `BR-UC-04-01`, `BR-UC-04-02`, `BR-UC-05-01`, `BR-UC-06-01`, `BR-UC-06-02`, `BR-UC-07-01`, `BR-UC-07-02`, `BR-UC-08-01`, `BR-UC-09-01`, `BR-UC-09-02`, `BR-UC-09-07`, `BR-UC-10-01`, `BR-UC-10-02`, `BR-UC-11-01`, `BR-UC-11-02`, `BR-UC-12-01`, `BR-UC-13-05`, `BR-UC-15-04`, `BR-UC-16-01`, `BR-UC-16-02`, `BR-UC-17-01`, `BR-UC-17-02`, `BR-UC-18-01`, `BR-UC-18-02`.

## A-20 — Mutation execution and retry

Every public server mutation, including join and preferences, uses MutationGateway. A serializable transaction locks the session row before lookup and dispatch. Deduplication key scope is principal/session/operation/key and uses a canonical payload hash. Same-key same-payload replay returns the immutable original HTTP response without dispatch. A changed payload is a conflict. Successful receipts are retained for 24 hours; an expired record is atomically replaced on a fresh command; infrastructure failures roll back. Fresh successful commands and provider completions advance session.version once. Replays do not rerun domain preconditions, including after leave/end. All effects, result serialization and the receipt commit atomically; no raw bearer/provider token is stored.

Rule references: `BR-UC-02-03`, `BR-UC-02-14`, `BR-UC-02-15`, `BR-UC-02-16`, `BR-UC-02-17`, `BR-UC-03-03`, `BR-UC-04-03`, `BR-UC-06-03`, `BR-UC-07-03`, `BR-UC-09-03`, `BR-UC-10-03`, `BR-UC-11-03`, `BR-UC-12-02`, `BR-UC-15-05`, `BR-UC-16-03`, `BR-UC-17-03`, `BR-UC-18-03`.

## A-21 — Cascades

Stream stop demotes former stage participants, disables their publication, stops shares and recordings, and cancels pending stage requests. Leave applies owned-share and own-request cleanup. End applies all cleanup and closes even a READY stream. Cleanup uses pre-state membership and advances each changed resource version.

Rule references: `BR-UC-04-08`, `BR-UC-04-09`, `BR-UC-04-10`, `BR-UC-04-11`, `BR-UC-17-08`, `BR-UC-17-09`, `BR-UC-17-10`, `BR-UC-18-09`, `BR-UC-18-10`, `BR-UC-18-11`.

## A-22 — Persistence and concurrent constraints

Conditional unique expression indexes enforce one joined membership per principal/session, one joined host, one pending request per viewer, one active share and one active recording. Historical terminal rows remain repeatable. Session-row serialization enforces aggregate capacities and orders state changes with callbacks. Composite foreign keys bind actors/resources to the same session.

Rule references: `BR-UC-02-18`, `BR-UC-02-19`, `BR-UC-06-09`, `BR-UC-11-07`, `BR-UC-16-09`.

## A-23 — Read and adapter boundaries

Session-state polling supplies session/resource versions, self media/view preferences, host-visible stage requests (or only the caller requests), and reaction events. A departed member may retrieve final state only after the session has ended. Chat has a separate ascending-sequence read API. Message/reaction cursors retain a high-water mark for polling; reaction pages contain at most 50 events. Session-state reads use a consistent database snapshot. Media bytes, PDF upload/source registration, session provisioning and credential issuance belong to named external adapters; their internals are outside this product package.

Rule references: `BR-UC-08-04`, `BR-UC-08-05`, `BR-UC-08-06`, `BR-UC-09-08`, `BR-UC-09-09`.
