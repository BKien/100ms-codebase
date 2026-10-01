---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "View Bank Accounts"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A83:B105"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-05: View Bank Accounts

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

View Bank Accounts

### Description

As an authenticated user, I want to view the bank accounts linked to my user identifier.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user opens the Accounts page.

### Pre-Condition(s)

PRE-1: The user is authenticated.

### Post-Condition(s)

POST-1: The frontend displays accounts owned by the authenticated user.
POST-2: Accounts are returned in ascending accountId order.
POST-3: If no accounts exist, the page displays an empty state and an Add Account action.

### Basic Flow

1. The user opens /accounts.
2. The frontend sends GET /api/v1/accounts.
3. JwtAuthGuard authenticates the request and supplies userId.
4. AccountService queries accounts where account.userId equals userId, selects the list fields, and orders by accountId ascending.
5. The backend queries and returns only the last four digits of the account number (account_number_last_4) for each account.
6. The backend returns success, message, and a data object containing user_id and accounts.
7. The frontend displays account cards containing bank name, account type, the last four account digits prefixed with exactly four asterisks (e.g., **** 5667) regardless of the original account number length, and balance.

### Alternative Flow

AF-1: No linked accounts
4a. The query returns an empty array.
6a. The frontend displays its no-account message and an action that navigates to /accounts/add.

### Exception Flow

EF-1: Unauthorized request
3a. HTTP 401 is handled by the Axios interceptor, which clears local authentication data and redirects to /login.

EF-2: Retrieval failure
4a. The page displays the returned error message or a general loading error.

### Related UI

AccountListPage; AccountCard; route /accounts

### Related API IDs

API-ACCOUNT-LIST

### Notes

Not specified

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

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}
note right of AccountType
  Credit_Card maps to database literal 'Credit Card'.
end note

class AccountDto <<DTO>> {
  id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class AccountListDataDto <<DTO>> {
  user_id: Integer [1]
  accounts: AccountDto [0..*]
}

class AccountListResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: AccountListDataDto [1]
}

class AccountService <<Service>> {
  findAllByUserId(user_id: Integer): AccountListResponseDto
}

User "1" -- "0..*" Account : owns

AccountService ..> AccountListResponseDto
AccountListResponseDto --> AccountListDataDto
AccountListDataDto "1" -- "0..*" AccountDto : contains
AccountDto ..> Account : maps from

@enduml
~~~

## Business Rules

~~~text
BR-ACC-01: Account ownership scope
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

pre BR_ACC_01_UserDefined:
  not user_id.oclIsUndefined()

post BR_ACC_01_OwnedAccountsOnly:
  result.success implies
    result.data.accounts->forAll(dto |
      Account.allInstances()->exists(a |
        a.account_id = dto.id and
        a.user_id = user_id
      )
    )

BR-ACC-02: Ordering
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

post BR_ACC_02_OrderedByAccountIdAsc:
  result.success implies
    result.data.accounts->size() <= 1 or
    Sequence{1..result.data.accounts->size()-1}->forAll(i |
      result.data.accounts->at(i).id < result.data.accounts->at(i + 1).id
    )

BR-ACC-03: Response rows map to persisted Accounts
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

post BR_ACC_03_ResponseBackedByAccount:
  result.success implies
    result.data.accounts->forAll(dto |
      Account.allInstances()->exists(a |
        a.account_id = dto.id and
        a.bank_name = dto.bank_name and
        a.account_type = dto.account_type and
        a.branch_name = dto.branch_name and
        a.account_number_last_4 = dto.account_number_last_4 and
        a.balance = dto.balance
      )
    )

BR-ACC-04: Account number exposure restriction
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto
post BR_ACC_04_NoFullAccountNumber:
  result.success implies
    result.data.accounts->forAll(dto |
      dto.account_number_full.oclIsUndefined()
    )

Technical constraints:
- The backend shall only query the necessary columns to optimize performance.
- The backend shall not return the full account number (account_number_full) in the list response to prevent exposing sensitive data over the network.
- The backend shall return only the stored account_number_last_4.
- The frontend shall mask the account number by prefixing these 4 digits with exactly four asterisks (e.g., ""**** 1234""), regardless of the original account number's length."

BR-ACC-05: Empty account result
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto
post BR_ACC_05_EmptyResultConsistency:
  not Account.allInstances()->exists(a | a.user_id = user_id)
  implies
    result.success and
    result.data.accounts->isEmpty()

BR-ACC-06: Viewing accounts is read-only
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

post BR_ACC_06_AccountIdentityUnchanged:
  Account.allInstances()->collect(a | a.account_id)->asSet() =
  Account.allInstances()@pre->collect(a | a.account_id)->asSet()

post BR_ACC_06_AccountDataUnchanged:
  Account.allInstances()->forAll(a |
    Account.allInstances()@pre->exists(old |
      old.account_id = a.account_id and
      old.user_id = a.user_id and
      old.bank_name = a.bank_name and
      old.account_type = a.account_type and
      old.branch_name = a.branch_name and
      old.account_number_full = a.account_number_full and
      old.account_number_last_4 = a.account_number_last_4 and
      old.balance = a.balance
    )
  )

Technical constraint:
- Listing accounts shall not create, update, or delete any Account or Transaction records.
~~~

