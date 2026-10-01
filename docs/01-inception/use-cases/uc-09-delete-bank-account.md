---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-09
uc_name: "Delete a Bank Account"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A200:B218"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-09: Delete a Bank Account

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Delete a Bank Account

### Description

As an authenticated account owner, I want to permanently delete an account and its related transactions.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user selects Delete from an account card or account detail page.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: The account exists and is owned by the authenticated user.

### Post-Condition(s)

POST-1: On confirmed success, all Transaction rows with the accountId and the Account row are deleted in one database transaction.
POST-2: On confirmed success, the system displays a success dialog, waits 1500ms, and then refreshes the account list or navigates to /accounts.
POST-3: On cancellation or rollback, no deletion is committed.

### Basic Flow

1. The user selects Delete for an account.
2. Delete Account Modal displays the bank name, final four account digits, and a warning that all related transactions will be deleted.
3. The user selects Confirm Delete.
4. The frontend sends DELETE /api/v1/accounts/:id.
5. The controller validates that id parses to an integer.
6. AccountService starts a database transaction, loads the account, and verifies ownership.
7. AccountService deletes related Transaction rows.
8. AccountService deletes the Account row and commits the transaction.
9. The frontend closes the modal, displays a success dialog, waits 1500ms, and then refreshes the list or navigates to /accounts.

### Alternative Flow

AF-1: Cancel deletion
3a. The user selects Cancel or closes the modal.
3b. No API request is sent and no data changes.

### Exception Flow

EF-1: Invalid account ID
5a. The controller returns HTTP 400.

EF-2: Missing or non-owned account
6a. The service rolls back and returns HTTP 404 using the same message for both cases.

EF-3: Database deletion failure
7a. The service rolls back the transaction and returns HTTP 500.

### Related UI

AccountListPage; AccountDetailPage; DeleteAccountModal

### Related API IDs

API-ACCOUNT-DELETE

### Notes

Security rationale: An account that does not exist and an account not owned by the authenticated user are both reported as HTTP 404, rather than 403, to avoid disclosing the existence of another user's account.

## UML Model

~~~plantuml
@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [1]
  profile_picture_url: String [1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class Transaction <<Entity>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  transaction_date: Date [1]
  type: TransactionType [1]
  item_description: String [1]
  shop_name: String [0..1]
  amount: Decimal [1]
  payment_method: String [0..1]
  status: TransactionStatus [1]
  receipt_id: String [0..1]
  category_id: Integer [0..1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

enum TransactionType {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

class DeleteAccountResponseDto <<DTO>> {
  message: String [1]
  deleted_account_id: Integer [1]
}

class AccountService <<Service>> {
  delete(accountId: Integer, userId: Integer): DeleteAccountResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains
AccountService ..> DeleteAccountResponseDto
AccountService ..> Account : deletes
AccountService ..> Transaction : deletes cascade

@enduml
~~~

## Business Rules

~~~text
BR-ACC-27: Account deletion ownership validation
context AccountService::delete(accountId : Integer, userId : Integer) : DeleteAccountResponseDto
pre BR_ACC_27_MustOwnAccount:
  Account.allInstances()->exists(a | a.account_id = accountId and a.user_id = userId)
Technical constraint:
- If the account does not exist or does not belong to the user, the backend intentionally throws a 404 NotFoundException to prevent data 
enumeration.

BR-ACC-28: Account deletion data integrity (Cascading)
context AccountService::delete(accountId : Integer, userId : Integer) : DeleteAccountResponseDto
post BR_ACC_28_AtomicDeletion:
  not Account.allInstances()->exists(a | a.account_id = accountId) and
  not Transaction.allInstances()->exists(t | t.account_id = accountId)
Technical constraint:
- The backend MUST execute the deletion of all related Transaction rows and the Account row within a single atomic database transaction (using QueryRunner). If any step fails, the entire transaction rolls back.
~~~

