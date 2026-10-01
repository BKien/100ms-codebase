---
artifact_type: api-contract
status: Frozen
api_id: API-TRANSACTION-CREATE
related_uc_id: UC-04
---

# API-TRANSACTION-CREATE: Create Transaction

## General Information

### API ID

API-TRANSACTION-CREATE

### API Name

Create Transaction

### Related Use Case IDs

UC-04

### Method

POST

### Path

/api/v1/transactions

### Description

Create a revenue or expense transaction and update the account balance atomically.

### Authentication

Bearer JWT

### Authorization

Owner of the referenced account

## Request Header(s)

### headers.Authorization

Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
Validation: Must contain a valid, unexpired JWT access token.
Trigger: Every protected request.
Description: Authenticates the current user.
Example: Bearer eyJhbGciOiJIUzI1NiIs...
Note: Added by the frontend Axios interceptor.


### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No
Default: application/json
Allowed values: application/json
Validation: Request body must be JSON.
Trigger: Every request containing a JSON body.
Description: Declares the request body format.
Example: application/json

## Request Body

### accountId

Type: integer; Required: Yes; Nullable: No
Validation: Must reference Accounts.account_id owned by the authenticated Users.user_id.
Trigger: Transaction creation request.
Description: Account identifier.
Example: 3


### transactionDate

Type: string; Format: date; Required: Yes; Nullable: No
Validation: Must be a valid ISO date string.
Trigger: Transaction creation request.
Description: Maps to Transactions.transaction_date.
Example: 2025-11-01


### type

Type: string; Required: Yes; Nullable: No
Allowed values: Revenue; Expense
Validation: Must be Revenue or Expense.
Trigger: Transaction creation request.
Description: Maps to Transactions.type.
Example: Expense


### itemDescription

Type: string; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Transaction creation request.
Description: Maps to Transactions.item_description.
Example: Movie Ticket


### category_id

Type: integer; Required: No; Nullable: Yes
Validation: When supplied, must reference an existing Categories.category_id.
Trigger: Transaction creation request.
Description: Optional transaction category; maps to Transactions.category_id.
Example: 3
Note: The request is valid when category_id is omitted/null.


### shopName

Type: string; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Transaction creation request.
Description: Maps to Transactions.shop_name.
Example: Cinema


### amount

Type: number; Format: decimal; Required: Yes; Nullable: No
Validation: Must be at least 0.01. For Expense, must not exceed the selected account balance.
Trigger: Transaction creation request.
Description: Maps to Transactions.amount.
Example: 150000


### paymentMethod

Type: string; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Transaction creation request.
Description: Maps to Transactions.payment_method.
Example: Credit Card


### status

Type: string; Required: No; Nullable: No
Default: Complete
Allowed values: Complete; Pending; Failed
Validation: When supplied, must be an allowed status.
Trigger: Transaction creation request.
Description: Maps to Transactions.status.
Example: Complete

## Success Response — HTTP 201

### message

Type: string; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Creation success message.
Example: Transaction created successfully


### data.transactionId

Type: integer; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Created transaction identifier.
Example: 8


### data.accountId

Type: integer; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Related account identifier.
Example: 3


### data.transactionDate

Type: string; Format: date-time; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Stored transaction date.


### data.type

Type: string; Required: Yes; Nullable: No
Allowed values: Revenue; Expense
Trigger: The transaction and account balance are committed.
Description: Stored transaction type.
Example: Expense


### data.itemDescription

Type: string; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Stored description.
Example: Movie Ticket


### data.shopName

Type: string; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Stored merchant name from Transactions.shop_name.
Example: Cinema


### data.amount

Type: number; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Stored amount.
Example: 150000


### data.paymentMethod

Type: string; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Stored payment method from Transactions.payment_method.
Example: Credit Card


### data.status

Type: string; Required: Yes; Nullable: No
Allowed values: Complete; Pending; Failed
Trigger: The transaction and account balance are committed.
Description: Stored status.
Example: Complete


### data.receiptId

Type: string; Required: Yes; Nullable: Yes
Trigger: The transaction and account balance are committed.
Description: Receipt identifier.
Example: null


### data.createdAt

Type: string; Format: date-time; Required: Yes; Nullable: No
Trigger: The transaction and account balance are committed.
Description: Response-time timestamp generated with new Date(); it is not read from a persisted Transaction entity column.


### data.category_id

Type: integer; Required: Yes; Nullable: Yes
Trigger: The transaction and account balance are committed.
Description: Stored optional category identifier.
Example: 3

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: Required input is missing/invalid; shopName or paymentMethod is empty/missing; a supplied category_id does not exist; accountId is not owned by the authenticated user; type/status is invalid; or an Expense exceeds the account balance.
Description: Error description returned by the global HTTP exception filter.
Example: Invalid or missing transaction data
Note: Omitting category_id by itself is not an error because Transactions.category_id is nullable. The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 401

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The JWT is missing, invalid, or expired.
Description: Error description returned by the global HTTP exception filter.
Example: Unauthorized
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The database transaction fails.
Description: Error description returned by the global HTTP exception filter.
Example: Error when creating transaction. Try it again later.
Note: The error envelope also contains success=false and may contain an error field.
