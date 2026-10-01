# Coverage Report

## Candidate Use-Case Matrix

| Candidate ID | Actor goal | Figma node IDs | Desktop/mobile evidence | Status | Gap |
| --- | --- | --- | --- | --- | --- |
| C-01 | Review join preview and permissions | `6007:51245`, `6066:89727`, `6066:89005` | Both | Supported | Browser permission mechanics are outside Figma |
| C-02 | Join a session | `6007:51245`, `6066:89727`, `6012:44409`, `6066:89005` | Both | Supported | None |
| C-03 | Start a live stream | `6007:51245`, `6007:51075`, `6007:86770`, `6012:90506` | Both | Supported | Provider transport is outside Figma |
| C-04 | Stop a live stream | `6007:86770`, `6012:90506` | Both | Supported | Provider transport is outside Figma |
| C-05 | Watch a live stream | `6007:51397`, `6012:44409` | Both | Supported | Playback delivery is outside Figma |
| C-06 | Request stage access | `6007:51397`, `6007:86770`, `6012:90506` | Both | Supported | Admission policy is not shown |
| C-07 | Respond to a stage request | `6007:86770`, `6012:90506` | Both | Supported | Admission policy is not shown |
| C-08 | View session participants | `6007:86770`, `6007:55138`, `6012:90506`, `6012:52233` | Both | Supported | None |
| C-09 | Send a chat message | `6007:86770`, `6007:55138`, `6012:90506`, `6012:52233` | Both | Supported | Message retention is not shown |
| C-10 | Send an emoji reaction | `6007:55138`, Modal/Emoji Reactions | Desktop plus component | Supported | Reaction catalog is not shown as product data |
| C-11 | Share a screen or PDF | `6007:86770`, `6007:55138`, `6007:77656`, `6012:52233` | Both | Supported | Content storage is outside Figma |
| C-12 | Configure audio and video devices | `6007:51132`, `6066:89727`, `6066:89005` | Both | Supported | Device discovery is outside Figma |
| C-13 | Select a virtual background | `6026:1184329` | Desktop | Supported | Background catalog source is not shown |
| C-14 | Change session layout | `6007:96234`, `6012:102740`, `6007:77656`, `6012:78022` | Both | Supported | None |
| C-15 | Pin a tile for myself or spotlight a tile for everyone | `6007:55138`, `6012:78022`, `6073:15912` | Both plus component | Supported | Spotlight authorization is not shown |
| C-16 | Control session recording | `6007:55138`, `6012:90506`, `6012:52233` | Both | Supported | Recording retention is not shown |
| C-17 | Leave a session | `6007:86770`, `6007:55138`, `6012:90506`, `6012:52233` | Both | Supported | Rejoin policy is not shown |
| C-18 | End a session for everyone | `6007:86770`, `6007:55138`, `6012:90506`, `6012:52233` | Both | Supported | Host policy is not shown |
| C-19 | Schedule a future session | None | None | Missing | No scheduling interface is present |
| C-20 | Create or manage an account | None | None | Missing | No authentication flow is present |
| C-21 | Moderate or ban a participant | Participant and action panels only | Both | Partial | No complete moderation outcome is shown |
| C-22 | Download a recording | Recording controls only | Both | Partial | No recording library or download outcome is shown |

## Non-Use-Case Evidence

Foundation pages, component pages, generic tile-state galleries, progress indicators, and toasts support the specified flows but do not represent independent actor goals.

## Contract Completion — 2026-09-22

The 18 supported use cases remain unchanged in scope. Supporting session-state, chat-history and background-catalog read contracts complete their observable interactions. Internal role, identity, lifecycle, retry and concurrency decisions are explicitly recorded in ASSUMPTIONS.md. No new product screen is claimed by this revision. The tile-menu component distinguishes personal pinning from session-wide spotlighting; host transfer and stream restart after STOP are not added as supported flows.
