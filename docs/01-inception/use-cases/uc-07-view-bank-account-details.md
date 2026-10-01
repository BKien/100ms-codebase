---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-07
uc_name: "View Bank Account Details"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A131:B152"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-07: View Bank Account Details

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

View Bank Account Details

### Description

As an authenticated account owner, I want to view one account and its five most recent transactions.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user selects an account card.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: The path contains an account identifier.

### Post-Condition(s)

POST-1: On success, the page displays account information and at most five recent transactions.
POST-2: Expense amounts in recent_transactions are returned as negative values.
POST-3: Unauthorized account data is not returned.

### Basic Flow

1. The user selects an account card and opens /accounts/:id.
2. AccountDetailPage requests GET /api/v1/accounts/:id.
3. The controller validates authentication and parses id as an integer.
4. AccountService loads the account by accountId.
5. AccountService verifies account.userId equals the authenticated userId.
6. AccountService loads at most five transactions for the account, ordered by transactionDate descending.
7. AccountService maps transaction dates to YYYY-MM-DD and makes Expense amounts negative.
8. The frontend displays bank name, type, branch, full account number, balance, and recent transactions.

### Alternative Flow

AF-1: No recent transactions
6a. The query returns an empty array.
8a. The account information remains visible with an empty recent-transactions section.

### Exception Flow

EF-1: Invalid account ID
3a. The controller returns HTTP 400.

EF-2: Account not found
4a. The backend returns HTTP 404.

EF-3: Account belongs to another user
5a. The backend returns HTTP 403.

EF-4: Retrieval failure
6a. The backend returns HTTP 500 and the frontend displays its error state.

### Related UI

AccountDetailPage; route /accounts/:id

### Related API IDs

API-ACCOUNT-DETAIL

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
  phone_number: String [0..1]
  profile_picture_url: String [0..1]
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

class Transaction <<Entity>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  category_id: Integer [0..1]
  transaction_date: Date [1]
  type: TransactionTypeEnum [1]
  item_description: String [1]
  shop_name: String [0..1]
  amount: Decimal [1]
  payment_method: String [0..1]
  status: TransactionStatus [1]
  receipt_id: String [0..1]
}

enum TransactionTypeEnum {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

class TransactionDto <<DTO>> {
  date: String [1]
  amount: Decimal [1]
  description: String [1]
  status: TransactionStatus [1]
  receipt_id: String [0..1]
  type: TransactionTypeEnum [1]
}

class AccountDetailResponseDto <<DTO>> {
  id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  balance: Decimal [1]
  recent_transactions: TransactionDto [0..5]
}

class AccountService <<Service>> {
  findOneWithTransactions(accountId: Integer, userId: Integer): AccountDetailResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : has
AccountService ..> AccountDetailResponseDto
AccountDetailResponseDto *-- "0..5" TransactionDto : contains
AccountDetailResponseDto ..> Account : maps from
TransactionDto ..> Transaction : maps from

@enduml
~~~

## Business Rules

~~~text
BR-ACC-15: Account existence and ownership
context AccountService::findOneWithTransactions(
  accountId : Integer,
  userId : Integer
) : AccountDetailResponseDto
pre BR_ACC_15_AccountMustBeOwned:
  Account.allInstances()->exists(a | 
    a.account_id = accountId and 
    a.user_id = userId
  )

BR-ACC-16: Five most recent account transactions
context AccountService::findOneWithTransactions(
  accountId : Integer,
  userId : Integer
) : AccountDetailResponseDto
post BR_ACC_16_MaxFiveRecentTransactions:
  result.recent_transactions->size() <= 5
post BR_ACC_16_OrderedByDateDescending:
  result.recent_transactions->size() <= 1 or
  Sequence{1..result.recent_transactions->size()-1}->forAll(i |
    result.recent_transactions->at(i).date >= result.recent_transactions->at(i + 1).date
  )
Technical constraint:
- The backend shall return at most five transactions ordered by transaction_date descending.

BR-ACC-17: Response rows map to persisted data with signed amounts
context AccountService::findOneWithTransactions(
  accountId : Integer,
  userId : Integer
) : AccountDetailResponseDto
post BR_ACC_17_ResponseBackedByAccount:
  Account.allInstances()->exists(a |
    a.account_id = result.id and
    a.user_id = userId and
    a.bank_name = result.bank_name and
    a.account_type = result.account_type and
    (a.branch_name.oclIsUndefined() implies result.branch_name.oclIsUndefined()) and
    (not a.branch_name.oclIsUndefined() implies a.branch_name = result.branch_name) and
    a.account_number_full = result.account_number_full and
    a.balance = result.balance
  )
post BR_ACC_17_ResponseBackedByTransaction:
  result.recent_transactions->forAll(tDto |
    Transaction.allInstances()->exists(t |
      t.account_id = accountId and
      t.item_description = tDto.description and
      ((t.type = TransactionTypeEnum::Expense and tDto.amount = -(t.amount)) or
       (t.type = TransactionTypeEnum::Revenue and tDto.amount = t.amount)) and
      t.status = tDto.status and
      (t.receipt_id.oclIsUndefined() implies tDto.receipt_id.oclIsUndefined()) and
      (not t.receipt_id.oclIsUndefined() implies t.receipt_id = tDto.receipt_id) and
      t.type = tDto.type and
      tDto.date = toIsoDate(t.transaction_date)
    )
  )
Technical constraint:
- In the account-detail mapping, Expense amounts are negated (returned as negative) and Revenue amounts remain positive.
- Unused persisted fields in Transaction (e.g., shop_name, payment_method, category_id) are intentionally excluded from the returned TransactionDto.

post BR_ACC_18_AccountIdentityUnchanged:
  Account.allInstances()->collect(a | a.account_id)->asSet() =
  Account.allInstances()@pre->collect(a | a.account_id)->asSet()
post BR_ACC_18_AccountDataUnchanged:
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
post BR_ACC_18_TransactionIdentityUnchanged:
  Transaction.allInstances()->collect(t | t.transaction_id)->asSet() =
  Transaction.allInstances()@pre->collect(t | t.transaction_id)->asSet()
post BR_ACC_18_TransactionDataUnchanged:
  Transaction.allInstances()->forAll(t |
    Transaction.allInstances()@pre->exists(old |
      old.transaction_id = t.transaction_id and
      old.account_id = t.account_id and
      old.category_id = t.category_id and
      old.transaction_date = t.transaction_date and
      old.type = t.type and
      old.item_description = t.item_description and
      old.shop_name = t.shop_name and
      old.amount = t.amount and
      old.payment_method = t.payment_method and
      old.status = t.status and
      old.receipt_id = t.receipt_id
    )
  )
Technical constraint:
- Viewing account details shall not create, update, or delete any Account or Transaction records.
~~~

