---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "Add a Bank Account"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A106:B130"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-06: Add a Bank Account

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

Add a Bank Account

### Description

As an authenticated user, I want to add a bank account with its current balance.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user selects an Add Account action.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: The Add Account route /accounts/add is accessible.

### Post-Condition(s)

POST-1: On success, an account row is stored with userId from the JWT and account_number_last_4 derived from account_number_full.
POST-2: The frontend shows a success toast and navigates to /accounts after 1.5 seconds.
POST-3: On failure, the account is not added by the request.

### Basic Flow

1. The user opens /accounts/add.
2. The frontend displays AddAccountForm with accountType defaulted to Checking.
3. The user enters bank_name, account_type, optional branch_name, account_number_full, and balance.
4. The user selects Add Account.
5. The frontend requires bank_name and account_number_full and requires balance to be numeric and non-negative.
6. The frontend sends POST /api/v1/accounts.
7. The backend ValidationPipe validates CreateAccountDto.
8. AccountService checks for another account owned by the same user with the same account_number_full.
9. AccountService derives the final four characters, creates the account using userId from the JWT, and stores it.
10. The frontend shows a success toast and navigates to /accounts after 1.5 seconds.

### Alternative Flow

AF-1: Optional branch omitted
3a. The user leaves branch_name empty.
6a. The frontend omits branch_name and the backend stores it as undefined/null.

AF-2: Cancel
4a. The user selects Cancel and returns to /accounts without submitting.

### Exception Flow

EF-1: Client-side validation failure
5a. The form displays field errors and does not call the API.

EF-2: Duplicate account number for the same user
8a. The backend returns HTTP 409 and the frontend displays the duplicate-account message.

EF-3: Backend validation failure
7a. The frontend maps returned validation messages to fields when possible.

EF-4: Storage failure
9a. The backend returns HTTP 500 and the frontend displays its create-account failure message.

### Related UI

AddAccountPage; AddAccountForm; route /accounts/add

### Related API IDs

API-ACCOUNT-CREATE

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

class CreateAccountDto <<DTO>> {
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  balance: Decimal [1]
}

class AccountResponseDto <<DTO>> {
  id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class AccountService <<Service>> {
  create(userId: Integer, dto: CreateAccountDto): AccountResponseDto
}

User "1" -- "0..*" Account : owns
AccountService ..> AccountResponseDto
AccountService ..> CreateAccountDto
CreateAccountDto ..> Account : mapped to
AccountResponseDto ..> Account : mapped from

@enduml
~~~

## Business Rules

~~~text
BR-ACC-07: Allowed account type
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_07_ValidType:
  Set{'Checking', 'Credit Card', 'Savings', 'Investment', 'Loan'}->includes(dto.account_type)

BR-ACC-08: Required account text fields
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_08_RequiredText:
  not dto.bank_name.oclIsUndefined() and dto.bank_name.trim().size() > 0 and
  not dto.account_number_full.oclIsUndefined() and dto.account_number_full.trim().size() > 0

BR-ACC-09: Numeric non-negative account balance
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_09_IsNumeric:
  dto.balance.oclIsTypeOf(Real) or dto.balance.oclIsTypeOf(Integer)

pre BR_ACC_09_NonNegativeBalance:
  not dto.balance.oclIsUndefined() and dto.balance >= 0
Technical constraint:
- The balance must be a valid numeric type (not a string), and must be greater than or equal to zero.

BR-ACC-10: Unique account number per owner
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_10_UniqueAccount:
  not Account.allInstances()->exists(a | 
    a.user_id = userId and 
    a.account_number_full = dto.account_number_full
  )

BR-ACC-11: Derive final four account characters
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

post BR_ACC_11_DeriveLast4:
  let newAcc = Account.allInstances()->any(a | a.account_id = result.id) in
  newAcc.account_number_last_4 = dto.account_number_full.substring(dto.account_number_full.size() - 3, dto.account_number_full.size())

Technical constraint:
- The backend derives account_number_last_4 by taking the exact last 4 characters of the submitted account_number_full (e.g., via .slice(-4)).

BR-ACC-12: Account creation persistence mapping
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

post BR_ACC_12_StorageMapping:
  Account.allInstances()->exists(a |
    a.account_id = result.id and
    a.user_id = userId and
    a.bank_name = dto.bank_name and
    a.account_type = dto.account_type and
    a.branch_name = dto.branch_name and
    a.account_number_full = dto.account_number_full and
    a.balance = dto.balance
  )

post BR_ACC_12_ResponseMapping:
  result.id = Account.allInstances()->any(a | a.account_number_full = dto.account_number_full).account_id

BR-ACC-13: Account number format and length
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_13_NumericCharactersOnly:
  not dto.account_number_full.oclIsUndefined() and 
  matches(dto.account_number_full, '^[0-9]+$')
pre BR_ACC_13_LengthConstraints:
  dto.account_number_full.size() >= 8 and dto.account_number_full.size() <= 34

Technical constraint:
- account_number_full must contain only numeric digits.
- The length must be between 8 and 34 characters (to safely derive the last 4 digits and reflect real-world bank account numbers).

BR-ACC-14: Optional branch name
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_14_BranchNameOptional:
  dto.branch_name.oclIsUndefined() or dto.branch_name.oclIsTypeOf(String)

Technical constraint:
- The branch_name field is optional. If omitted, it shall be processed and stored as null or undefined.
~~~

