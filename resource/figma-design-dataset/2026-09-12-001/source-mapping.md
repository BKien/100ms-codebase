# Figma Link Review for 16 Use Cases

## Purpose and usage

This file is the authoritative downstream mapping used to capture the frozen offline Figma dataset. Do not edit the 16 immutable files under `docs/01-inception/use-cases/`.

The current frozen UC projections contain no Figma URL occurrences. Every URL below is therefore an external mapping confirmed by the researcher and verified through the Figma connector. Capture tools must use only the `Replacement URL` column; URLs or file keys found in immutable UC provenance are not capture authority.

On 2026-08-29, connector inspection of the approved `Design` canvas (`66:4728`) and grouped account frames corrected the stale UC names, paths, and numbering previously recorded in this file. The connector also verified dedicated frames in the researcher-supplied `VibeTesting - Copy` file for UC-004, UC-006, UC-007, UC-008, and UC-015.

## Summary list

| UC | Use case | Source UC | File key | Node ID | Occurrence count | Replacement URL | Connector verification |
|---|---|---|---|---|---:|---|---|
| UC-001 | Register an Account | `docs/01-inception/use-cases/uc-01-register-account.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `137:8071` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=137-8071` | Frame `102. Signup`, 1440×1024. |
| UC-002 | Log In | `docs/01-inception/use-cases/uc-02-login.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `137:7477` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=137-7477` | Frame `101. Login`, 1440×1024. |
| UC-003 | View Transaction History | `docs/01-inception/use-cases/uc-03-view-transaction-history.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `611:3062` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=611-3062&t=QICD7ICt3PMX2eoP-0` | Frame `107. Transactions`, 1440×1024. |
| UC-004 | Create a Transaction | `docs/01-inception/use-cases/uc-04-create-transaction.md` | `zu3rZ336n1et2pWUGGIxlO` | `4740:1106` | 0 (external mapping) | `https://www.figma.com/design/zu3rZ336n1et2pWUGGIxlO/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting---Copy-?node-id=4740-1106&m=dev` | Frame `107.1 Add Transactions`, 1440×1024. |
| UC-005 | View Bank Accounts | `docs/01-inception/use-cases/uc-05-view-bank-accounts.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `66:5320` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=66-5320&t=n38xugZ25sDOw2pb-0` | Group `105. View Bank Accounts`; includes the base list and account-creation states. |
| UC-006 | Add a Bank Account | `docs/01-inception/use-cases/uc-06-add-bank-account.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `2925:1677` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=2925-1677&t=n38xugZ25sDOw2pb-0` | Dedicated frame `UC-06 • Add Bank Account`, 1440×900. |
| UC-007 | View Bank Account Details | `docs/01-inception/use-cases/uc-07-view-bank-account-details.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `416:7878` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=416-7878&t=7da6JXZAow3SksyU-0` | Dedicated frame `UC-07 • Bank Account Details`, 1440×900. |
| UC-008 | Edit a Bank Account | `docs/01-inception/use-cases/uc-08-edit-bank-account.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `2929:1679` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=2929-1679&t=7da6JXZAow3SksyU-0` | Dedicated frame `UC-08 • Edit Bank Account`, 1440×900; covers the primary UC and its UC-08.1 UI variant. |
| UC-009 | Delete a Bank Account | `docs/01-inception/use-cases/uc-09-delete-bank-account.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `2929:1680` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=2929-1680&t=7da6JXZAow3SksyU-0` | Primary frame `106.4 Remove and Confirm Account Deletion`, 1440×1024. Success state `2798:2468` is supplementary evidence. |
| UC-010 | View Monthly Expense Summary | `docs/01-inception/use-cases/uc-10-view-monthly-expense-summary.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `66:5698` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=66-5698&t=QICD7ICt3PMX2eoP-0` | Shared frame `109. Expenses` with UC-011, 1440×1024. |
| UC-011 | View Expenses by Category | `docs/01-inception/use-cases/uc-11-view-expenses-by-category.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `66:5698` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=66-5698&t=QICD7ICt3PMX2eoP-0` | Shared frame `109. Expenses` with UC-010, 1440×1024. |
| UC-012 | View Upcoming Bills | `docs/01-inception/use-cases/uc-12-view-upcoming-bills.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `66:5609` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=66-5609&t=QICD7ICt3PMX2eoP-0` | Frame `108. Bills`, 1440×1024. |
| UC-013 | View Financial Goals | `docs/01-inception/use-cases/uc-13-view-financial-goals.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `66:5829` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=66-5829&t=QICD7ICt3PMX2eoP-0` | Shared frame `110. Goals` with UC-016, 1440×1024. |
| UC-014 | Create a Financial Goal | `docs/01-inception/use-cases/uc-14-create-financial-goal.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `416:6052` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=416-6052&t=QICD7ICt3PMX2eoP-0` | Frame `110.1. Goals`, 1440×1024. |
| UC-015 | Adjust a Financial Goal | `docs/01-inception/use-cases/uc-15-adjust-financial-goal.md` | `zu3rZ336n1et2pWUGGIxlO` | `4795:6` | 0 (external mapping) | `https://www.figma.com/design/zu3rZ336n1et2pWUGGIxlO/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting---Copy-?node-id=4795-6&m=dev` | Dedicated frame `UC-15 • Adjust Financial Goal`, 1440×900. |
| UC-016 | View Savings Summary | `docs/01-inception/use-cases/uc-16-view-savings-summary.md` | `BTSOvEnU2X3CNrNvSxX9Ry` | `66:5829` | 0 (external mapping) | `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=66-5829&t=QICD7ICt3PMX2eoP-0` | Shared frame `110. Goals` with UC-013, 1440×1024. |

## Supplementary capture

UC-009 additionally uses the following verified success-state frame. It supplements the primary replacement mapping and does not create a seventeenth use case:

- File key: `BTSOvEnU2X3CNrNvSxX9Ry`
- Node ID: `2798:2468`
- Frame: `106.5 Account Removed Successfully`
- URL: `https://www.figma.com/design/BTSOvEnU2X3CNrNvSxX9Ry/Finebank---Financial-Management-Dashboard-UI-Kits--Community---VibeTesting-?node-id=2798-2468`

## Dataset capture conditions

- All 16 current frozen UC files have one exact, connector-verified primary mapping.
- UC-010/UC-011 and UC-013/UC-016 deliberately share nodes.
- UC-009 has one primary node and one explicitly related success-state node.
- Capture must deduplicate by exact file key plus node ID.
- A node is complete only when every artifact in `resource/figma-design-dataset/CAPTURE-SPEC.md` exists and all checksums pass.
- Do not store cookies, OAuth tokens, credentials, or short-lived Figma asset URLs.
