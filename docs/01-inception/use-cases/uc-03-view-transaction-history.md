---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-03
uc_name: "View Transaction History"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A45:B63"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-03: View Transaction History

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-03

### Use Case Name

View Transaction History

### Description

As an authenticated user, I want to view, filter, and paginate transactions belonging to my accounts.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user opens the Transactions page.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: The protected route (/transactions) is accessible to the authenticated user.

### Post-Condition(s)

POST-1: The page displays transaction history within the user's authorized ownership scope matching the selected filter and pagination parameters.
POST-2: If no transactions exist for the selected criteria, an empty-state message is displayed.
POST-3: System state and data remain unchanged (read-only query operation).

### Basic Flow

1. The user navigates to the Transactions page (/transactions).
2. The page initializes default query parameters (filter and pagination settings).
3. The frontend requests the initial transaction list (GET /api/v1/transactions) with default parameters.
4. The backend authenticates the user and verifies authorization.
5. The backend queries transaction records owned by the user, applying business rules for filtering, ordering, and pagination.
6. The backend returns the transaction list along with total count and pagination metadata.
7. The frontend renders the transaction history items and pagination controls.

### Alternative Flow

AF-1: Filter by transaction type
2a. The user selects a specific transaction category or type filter.
2b. The page resets pagination and requests transaction data according to the selected filter criteria.

AF-2: Pagination / Load more
7a. If additional transaction pages are available, the user requests to load more records.
7b. The frontend requests the subsequent page of transactions and appends them to the current list.

AF-3: Empty transaction history
5a. If no transactions match the query criteria, the backend returns an empty dataset.
7c. The frontend displays the appropriate empty-state message.

### Exception Flow

EF-1: Unauthorized request
4a. If user authentication is missing or invalid, the backend rejects the request and the frontend redirects the user to the login page.

EF-2: Invalid query parameters
5b. If filter or pagination parameters fail validation, the backend rejects the request and the frontend displays a validation error.

EF-3: Service failure
5c. If transaction retrieval encounters a server or database error, the frontend displays an error notification.

### Related UI

TransactionsPage; route /transactions

### Related API IDs

API-TRANSACTION-LIST

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
  branch_name: String [1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class Category <<Entity>> {
  category_id: Integer [1]
  category_name: String [1]
}

class Transaction <<Entity>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  transaction_date: Date [1]
  type: TransactionType [1]
  item_description: String [1]
  shop_name: String [1]
  amount: Decimal [1]
  payment_method: String [1]
  status: TransactionStatus [1]
  receipt_id: Integer [1]
  category_id: Integer [0..1]
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

enum TransactionType {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

enum TransactionFilterType {
  All
  Revenue
  Expense
}

class TransactionListQueryDto <<DTO>> {
  type: TransactionFilterType [1]
  limit: Integer [0..1]
  offset: Integer [0..1]
}

class TransactionDto <<DTO>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  transaction_date: Date [1]
  type: TransactionType [1]
  item_description: String [1]
  shop_name: String [1]
  amount: Decimal [1]
  payment_method: String [1]
  status: TransactionStatus [1]
}

class TransactionListResponseDto <<DTO>> {
  data: TransactionDto [*]
  total: Integer [1]
  hasMore: Boolean [1]
}

class TransactionService <<Service>> {
  findAllByUserId(user_id: Integer, type: TransactionFilterType, limit: Integer, offset: Integer): TransactionListResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains
Category "0..1" -- "0..*" Transaction : classifies

TransactionService ..> TransactionListQueryDto
TransactionService ..> TransactionListResponseDto
TransactionListResponseDto --> TransactionDto
TransactionDto ..> Transaction : maps from

@enduml
~~~

## Business Rules

~~~text
BR-TXN-01: Transaction ownership scope
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

pre BR_TXN_01_UserExists:
  User.allInstances()->exists(u |
    u.user_id = user_id
  )

post BR_TXN_01_OwnedAccountsOnly:
  result.data->forAll(t |
    Account.allInstances()->exists(a |
      a.account_id = t.account_id and
      a.user_id = user_id
    )
  )

BR-TXN-02: Allowed transaction filter and stored transaction type
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

pre BR_TXN_02_AllowedFilter:
  Set{TransactionFilterType::All,
      TransactionFilterType::Revenue,
      TransactionFilterType::Expense}->includes(type)

post BR_TXN_02_FilterApplied:
  (type = TransactionFilterType::Revenue implies
    result.data->forAll(t |
      t.type = TransactionType::Revenue
    )) and
  (type = TransactionFilterType::Expense implies
    result.data->forAll(t |
      t.type = TransactionType::Expense
    ))

context Transaction
inv BR_TXN_02_StoredType:
  type = TransactionType::Revenue or
  type = TransactionType::Expense

Technical constraint:
- All is a query/UI filter only. It shall never be stored in Transactions.type.

BR-TXN-03: Pagination and ordering
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

pre BR_TXN_03_LimitPositive:
  limit > 0

pre BR_TXN_03_OffsetNonNegative:
  offset >= 0

post BR_TXN_03_PageSize:
  result.data->size() <= limit

post BR_TXN_03_HasMore:
  result.hasMore =
    (offset + result.data->size() < result.total)

post BR_TXN_03_DescendingTransactionDate:
  result.data->size() <= 1 or
  Sequence{1..result.data->size()-1}->forAll(i |
    result.data->at(i).transaction_date >=
    result.data->at(i + 1).transaction_date
  )

Technical constraints:
- If limit is omitted, the endpoint shall use limit = 10.
- If offset is omitted, the endpoint shall use offset = 0.

BR-TXN-04: Database relationship integrity
context Account
inv BR_TXN_04_AccountOwnerExists:
  User.allInstances()->exists(u |
    u.user_id = self.user_id
  )

context Transaction
inv BR_TXN_04_TransactionAccountExists:
  Account.allInstances()->exists(a |
    a.account_id = self.account_id
  )

inv BR_TXN_04_OptionalCategoryValid:
  self.category_id.oclIsUndefined() or
  Category.allInstances()->exists(c |
    c.category_id = self.category_id
  )

BR-TXN-05: Empty transaction result
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

post BR_TXN_05_EmptyResultConsistency:
  result.total = 0 implies
    result.data->isEmpty() and
    result.hasMore = false

BR-TXN-06: Response rows map to persisted Transactions
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

post BR_TXN_06_ResponseBackedByTransaction:
  result.data->forAll(dto |
    Transaction.allInstances()->exists(t |
      t.transaction_id = dto.transaction_id and
      t.account_id = dto.account_id and
      t.transaction_date = dto.transaction_date and
      t.type = dto.type and
      t.item_description = dto.item_description and
      t.shop_name = dto.shop_name and
      t.amount = dto.amount and
      t.payment_method = dto.payment_method and
      t.status = dto.status
    )
  )

BR-TXN-07: Viewing transaction history is read-only
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

post BR_TXN_07_TransactionIdentityUnchanged:
  Transaction.allInstances()->collect(t | t.transaction_id)->asSet() =
  Transaction.allInstances()@pre->collect(t | t.transaction_id)->asSet()

post BR_TXN_07_TransactionDataUnchanged:
  Transaction.allInstances()->forAll(t |
    Transaction.allInstances()@pre->exists(old |
      old.transaction_id = t.transaction_id and
      old.account_id = t.account_id and
      old.transaction_date = t.transaction_date and
      old.type = t.type and
      old.item_description = t.item_description and
      old.shop_name = t.shop_name and
      old.amount = t.amount and
      old.payment_method = t.payment_method and
      old.status = t.status and
      old.receipt_id = t.receipt_id and
      old.category_id = t.category_id
    )
  )

post BR_TXN_07_AccountIdentityUnchanged:
  Account.allInstances()->collect(a | a.account_id)->asSet() =
  Account.allInstances()@pre->collect(a | a.account_id)->asSet()

Technical constraint:
- Listing transaction history shall not create, update, or delete Transactions or Accounts records.
~~~

