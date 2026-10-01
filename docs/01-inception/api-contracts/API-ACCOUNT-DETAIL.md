---
artifact_type: api-contract
status: Frozen
api_id: API-ACCOUNT-DETAIL
related_uc_id: UC-07
---

# API-ACCOUNT-DETAIL: Get Account Details

## General Information

### API ID

API-ACCOUNT-DETAIL

### API Name

Get Account Details

### Related Use Case IDs

UC-07

### Method

GET

### Path

/api/v1/accounts/:id

### Description

Return one owned account and its five most recent transactions.

### Authentication

Bearer JWT

### Authorization

Account owner

## Request Header(s)

### headers.Authorization

Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
Validation: Must contain a valid, unexpired JWT access token.
Trigger: Every protected request.
Description: Authenticates the current user.
Example: Bearer eyJhbGciOiJIUzI1NiIs...
Note: Added by the frontend Axios interceptor.

## Path Parameter(s)

### path.id

Type: integer; Required: Yes; Nullable: No
Validation: Must parse as an integer account identifier.
Trigger: Account detail request.
Description: Account identifier.
Example: 3

## Request Body

None

## Success Response — HTTP 200

### id

Type: integer; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Account identifier.
Example: 3


### bank_name

Type: string; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Bank name.
Example: Vietcombank


### account_type

Type: string; Required: Yes; Nullable: No
Allowed values: Checking; Credit Card; Savings; Investment; Loan
Trigger: The account exists and is owned by the user.
Description: Account type.
Example: Checking


### branch_name

Type: string; Required: Yes; Nullable: Yes
Trigger: The account exists and is owned by the user.
Description: Branch name.
Example: Hanoi Branch


### account_number_full

Type: string; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Full account number.
Example: 9704221234567890123


### balance

Type: number; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Current balance.
Example: 4500000


### recent_transactions

Type: array<object>; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Up to five most recent transactions.
Example: []


### recent_transactions[].date

Type: string; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Transaction date.
Example: 2025-11-01


### recent_transactions[].amount

Type: number; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Signed amount; expenses are returned as negative values.
Example: -150000


### recent_transactions[].description

Type: string; Required: Yes; Nullable: No
Trigger: The account exists and is owned by the user.
Description: Transaction description.
Example: Movie Ticket


### recent_transactions[].status

Type: string; Required: Yes; Nullable: No
Allowed values: Complete; Pending; Failed
Trigger: The account exists and is owned by the user.
Description: Transaction status.
Example: Complete


### recent_transactions[].receipt_id

Type: string; Required: Yes; Nullable: Yes
Trigger: The account exists and is owned by the user.
Description: Receipt identifier.
Example: null


### recent_transactions[].type

Type: string; Required: Yes; Nullable: No
Allowed values: Revenue; Expense
Trigger: The account exists and is owned by the user.
Description: Transaction type.
Example: Expense

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The path parameter is not a valid integer.
Description: Error description returned by the global HTTP exception filter.
Example: Invalid account ID.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 401

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The JWT is missing, invalid, or expired.
Description: Error description returned by the global HTTP exception filter.
Example: Unable to authenticate the user. Please log in again.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 403

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The account belongs to another user.
Description: Error description returned by the global HTTP exception filter.
Example: You are not authorized to view this account information.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 404

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The account does not exist.
Description: Error description returned by the global HTTP exception filter.
Example: This account was not found.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: Account or transaction retrieval fails.
Description: Error description returned by the global HTTP exception filter.
Example: A system error occurred while retrieving the account details. Please try again later.
Note: The error envelope also contains success=false and may contain an error field.
