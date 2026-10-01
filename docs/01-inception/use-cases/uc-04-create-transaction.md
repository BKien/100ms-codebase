---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "Create a Transaction"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A64:B82"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-04: Create a Transaction

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

Create a Transaction

### Description

As an authenticated user, I want to create a revenue or expense transaction for one of my accounts.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user selects Add Transaction from the Transactions page.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: The user has at least one active bank account eligible for transactions.

### Post-Condition(s)

POST-1: On success, the transaction is recorded, the associated account balance is adjusted consistently, and the user receives a success confirmation.
POST-2: On failure, no transaction is created and account balances remain unchanged.

### Basic Flow

1. The user navigates to the transaction creation screen (/transactions/add).
2. The form loads the user's available accounts and available transaction categories.
3. The user fills in the transaction details (description, amount, type, account, date, counterparty/shop, payment method, and optional category).
4. The user submits the transaction form.
5. The frontend performs preliminary validation on the entered transaction details.
6. The frontend sends the creation request (POST /api/v1/transactions) to the backend API.
7. The backend authenticates the request and validates all transaction inputs against business and ownership rules.
8. Upon successful validation, the backend records the transaction and updates the associated account balance atomically.
9. The backend returns a success response with the created transaction details.
10. The frontend displays a success notification, clears form fields, and navigates back to the transactions list.

### Alternative Flow

AF-1: Revenue transaction
3a. The user selects a Revenue transaction type.
8a. The system processes the transaction and increases the account balance accordingly without applying minimum balance constraints.

AF-2: Transaction without category
3b. The user leaves the optional category unselected.
8b. The system records the transaction without assigning a category classification.

AF-3: Category list unavailable
2a. If category options cannot be loaded, the frontend notifies the user while allowing transaction creation to continue since classification is optional.

AF-4: Form cancellation
4a. The user cancels the operation and the frontend returns to the transaction list without submitting.

### Exception Flow

EF-1: Account data unavailable
2b. If the user's accounts cannot be retrieved, the frontend informs the user and disables submission until an account is available.

EF-2: Client-side validation failure
5a. If required fields fail preliminary validation, the frontend displays field errors and prevents submission.

EF-3: Unauthorized request
7a. If authentication is missing or expired, the backend rejects the request and the user is redirected to login.

EF-4: Business validation failure
7b. If the transaction violates business constraints (such as unauthorized account selection or insufficient balance), the backend rejects the request and the frontend displays the returned error.

EF-5: Processing failure
8c. If an error occurs during persistence, the system rolls back all changes to preserve data consistency and displays an error message.

### Related UI

AddTransactionPage; AddTransactionForm; route /transactions/add

### Related API IDs

API-TRANSACTION-CREATE; API-ACCOUNT-LIST; API-CATEGORY-LIST

### Notes

Specification alignment: Transaction ownership follows Users → Accounts → Transactions. category_id is optional/nullable; shopName and paymentMethod are required and must be non-empty. BR-TXN-08..15 belong to UC-04 and are intentionally distinct from UC-03 rules BR-TXN-01..07.

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

class CreateTransactionDto <<DTO>> {
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  itemDescription: String [1]
  category_id: Integer [0..1]
  shopName: String [1]
  amount: Decimal [1]
  paymentMethod: String [1]
  status: TransactionStatus [0..1]
}

class CreateTransactionDataDto <<DTO>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  itemDescription: String [1]
  shopName: String [1]
  amount: Decimal [1]
  paymentMethod: String [1]
  status: TransactionStatus [1]
  receiptId: Integer [0..1]
  category_id: Integer [0..1]
}

class CreateTransactionResponseDto <<DTO>> {
  message: String [1]
  data: CreateTransactionDataDto [1]
}

class TransactionService <<Service>> {
  create(user_id: Integer, dto: CreateTransactionDto): CreateTransactionResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains
Category "0..1" -- "0..*" Transaction : classifies

TransactionService ..> CreateTransactionDto
TransactionService ..> CreateTransactionResponseDto
CreateTransactionResponseDto --> CreateTransactionDataDto
CreateTransactionDataDto ..> Transaction : maps from

@enduml
~~~

## Business Rules

~~~text
BR-TXN-08: Required transaction data
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_08_RequiredFields:
  not dto.accountId.oclIsUndefined() and
  not dto.transactionDate.oclIsUndefined() and
  not dto.type.oclIsUndefined() and
  not dto.itemDescription.oclIsUndefined() and
  trim(dto.itemDescription).size() > 0 and
  not dto.shopName.oclIsUndefined() and
  trim(dto.shopName).size() > 0 and
  not dto.paymentMethod.oclIsUndefined() and
  trim(dto.paymentMethod).size() > 0 and
  not dto.amount.oclIsUndefined() and
  dto.amount >= 0.01

BR-TXN-09: Allowed transaction type and status
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_09_AllowedType:
  dto.type = TransactionType::Revenue or
  dto.type = TransactionType::Expense

pre BR_TXN_09_AllowedStatus:
  dto.status.oclIsUndefined() or
  Set{TransactionStatus::Complete,
      TransactionStatus::Pending,
      TransactionStatus::Failed}->includes(dto.status)

post BR_TXN_09_DefaultStatus:
  (dto.status.oclIsUndefined() implies
    result.data.status = TransactionStatus::Complete) and
  (not dto.status.oclIsUndefined() implies
    result.data.status = dto.status)

BR-TXN-10: Optional category must be valid when supplied
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_10_CategoryOptionalAndValid:
  dto.category_id.oclIsUndefined() or
  Category.allInstances()->exists(c |
    c.category_id = dto.category_id
  )

post BR_TXN_10_CategoryStored:
  (dto.category_id.oclIsUndefined() implies
    result.data.category_id.oclIsUndefined()) and
  (not dto.category_id.oclIsUndefined() implies
    result.data.category_id = dto.category_id)

BR-TXN-11: Account ownership
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_11_AccountOwnedByUser:
  Account.allInstances()->exists(a |
    a.account_id = dto.accountId and
    a.user_id = user_id
  )

BR-TXN-12: Sufficient balance for Expense
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_12_SufficientExpenseBalance:
  dto.type = TransactionType::Expense implies
    Account.allInstances()->exists(a |
      a.account_id = dto.accountId and
      a.user_id = user_id and
      a.balance >= dto.amount
    )

BR-TXN-13: Account balance adjustment
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

post BR_TXN_13_BalanceAdjusted:
  Account.allInstances()->exists(a |
    a.account_id = dto.accountId and
    ((dto.type = TransactionType::Revenue and
      a.balance = a.balance@pre + dto.amount) or
     (dto.type = TransactionType::Expense and
      a.balance = a.balance@pre - dto.amount))
  )

BR-TXN-14: Created transaction maps to the request and database
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

post BR_TXN_14_OneNewTransaction:
  Transaction.allInstances()->size() =
    Transaction.allInstances()@pre->size() + 1

post BR_TXN_14_PersistedTransaction:
  Transaction.allInstances()->exists(t |
    t.transaction_id = result.data.transactionId and
    t.account_id = dto.accountId and
    t.transaction_date = dto.transactionDate and
    t.type = dto.type and
    t.item_description = trim(dto.itemDescription) and
    t.shop_name = trim(dto.shopName) and
    t.amount = dto.amount and
    t.payment_method = trim(dto.paymentMethod) and
    t.status = result.data.status and
    ((dto.category_id.oclIsUndefined() and
      t.category_id.oclIsUndefined()) or
     (not dto.category_id.oclIsUndefined() and
      t.category_id = dto.category_id))
  )

BR-TXN-15: Atomic transaction creation
Technical constraints:
- The Transactions insert and Accounts.balance update shall execute in one database transaction.
- If any validation, persistence, or balance-update step fails before commit, the operation shall roll back and leave both Transactions and Accounts unchanged by this request.
- shopName maps to Transactions.shop_name and paymentMethod maps to Transactions.payment_method; both are mandatory and shall not be null or empty.
- category_id maps to Transactions.category_id and remains optional/nullable.
~~~

