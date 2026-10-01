# Domain Context

## Product Boundary

This package specifies the observable collaboration experience represented by the 100ms UI kit. It covers live streaming and video conferencing but does not specify account creation, billing, room scheduling, media-provider internals, moderation enforcement, or video encoding.

## Canonical Terms

- **Session**: A real-time room that participants join. Its kind is either `LIVE_STREAM` or `VIDEO_CONFERENCE`.
- **Host**: The participant responsible for session-wide controls.
- **Broadcaster**: A non-host publishing participant; this is also the default non-host role in video conferences.
- **Viewer**: A participant consuming a live stream without being on stage.
- **Stage Participant**: A viewer admitted to the live stage.
- **Participant**: A person represented inside a session, regardless of role.
- **Stage Request**: A viewer request to become a stage participant, together with the host decision.
- **Content Share**: A screen or PDF presentation made visible in the session.
- **Recording**: A persisted record of a recording-control lifecycle; it does not contain raw media bytes.
- **Media Preference**: A participant's selected input/output devices and virtual-background choice.
- **View Preference**: A participant's layout, focus, side-panel, or picture-in-picture choice.
- **Spotlight**: The participant tile selected for shared prominence across the session; it is distinct from a caller's personal pin.
- **Departure**: A participant leaves while the session remains available to others.
- **Termination**: The host ends the session for all participants.

## Domain Distinctions

- Joining creates participation; it does not create or schedule a session.
- A live stream is the broadcast state associated with a session, not the session itself.
- Leaving affects one participant; ending affects the session.
- A stage request is neither a participant role nor the admission decision.
- Media preferences are per participant; recording and content sharing are session-scoped.
- Pinning is per participant; spotlighting is session-scoped and visible to everyone.

## Integration Vocabulary

- **Principal**: A stable registered or guest identity represented by a session access token, distinct from a participation record created by joining.
- **Preview Draft**: Client-local selections awaiting transfer by a join request.
- **Session Revision**: The monotonic version of application state returned by session-state reads.
- **Resource Version**: The version of a stream, recording, share, stage request or participant.
- **Mutation Gateway**: The application command boundary; its OCL contract is declared in UC-02.
- **Media/Content Adapter**: The integration boundary for media tracks, playback, source selection and PDF assets.
- **Provisioning Adapter**: The external boundary that supplies an existing session, designated host identity and session credentials.
- **Provider Completion**: An authenticated integration result for a requested stream or recording start.

## Contract Dispatch

Wire action START/STOP maps to LiveStreamService.start/stop, not to a single operation with conflicting constraints. Stage CREATE/CANCEL maps to StageService.submitRequest; ACCEPT/REJECT maps to StageService.decide. Departure LEAVE/END maps to SessionService.leave/end. The preference PATCH maps to PreferenceService.update for UC-12 through UC-14 and personal pinning in UC-15. Shared spotlight updates map to SpotlightService.update. Media and view rows are obtained from the caller's participant record; spotlight is obtained from session state. Domain policy remains in the identified UC OCL blocks and assumption register.

## Supporting Reads

Session state, chat history and background-catalog reads support the existing actor goals. They are contract completions, not additional Figma-derived use cases. The source manifest and original UI evidence boundary remain unchanged. Response data uses the common API representations, mapping domain entity id to its named public identifier and returning resulting session/resource versions.
