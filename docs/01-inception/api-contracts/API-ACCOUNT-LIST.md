---
artifact_type: api-contract
status: Frozen
api_id: API-ACCOUNT-LIST
related_uc_id: UC-05
---

# API-ACCOUNT-LIST: List User Accounts

## General Information

### API ID

API-ACCOUNT-LIST

### API Name

List User Accounts

### Related Use Case IDs

UC-05

### Method

GET

### Path

/api/v1/accounts

### Description

Return all bank accounts owned by the authenticated user.

### Authentication

Bearer JWT

### Authorization

Authenticated user

## Request Header(s)

### headers.Authorization

Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
Validation: Must contain a valid, unexpired JWT access token.
Trigger: Every protected request.
Description: Authenticates the current user.
Example: Bearer eyJhbGciOiJIUzI1NiIs...
Note: Added by the frontend Axios interceptor.

## Request Body

None

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Indicates successful retrieval.
Example: true

### message

Type: string; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Human-readable success message.
Example: Account list retrieved successfully.

### data.user_id

Type: integer; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Authenticated user identifier.
Example: 1

### data.accounts

Type: array<object>; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Array of accounts. May be empty.
Example: []

### data.accounts[].id

Type: integer; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Account identifier.
Example: 3

### data.accounts[].bank_name

Type: string; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Bank or financial institution name.
Example: Vietcombank

### data.accounts[].account_type

Type: string; Required: Yes; Nullable: No
Allowed values: Checking; Credit Card; Savings; Investment; Loan
Trigger: The user is authenticated.
Description: Account type.
Example: Checking

### data.accounts[].branch_name

Type: string; Required: Yes; Nullable: Yes
Trigger: The user is authenticated.
Description: Branch name.
Example: Hanoi Branch

### data.accounts[].account_number_last_4

Type: string; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Last four digits of the account number.
Example: 0123

### data.accounts[].balance

Type: number; Required: Yes; Nullable: No
Trigger: The user is authenticated.
Description: Current account balance.
Example: 4500000

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
Trigger: Account retrieval fails.
Description: Error description returned by the global HTTP exception filter.
Example: system error occurred. Please try again later.
Note: The error envelope also contains success=false and may contain an error field.
