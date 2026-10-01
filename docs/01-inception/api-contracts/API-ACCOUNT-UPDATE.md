---
artifact_type: api-contract
status: Frozen
api_id: API-ACCOUNT-UPDATE
related_uc_ids: [UC-08, UC-08.1]
---

# API-ACCOUNT-UPDATE: Update Bank Account

## General Information

### API ID

API-ACCOUNT-UPDATE

### API Name

Update Bank Account

### Related Use Case IDs

UC-08, UC-08.1

### Method

PUT

### Path

/api/v1/accounts/:id

### Description

Update an account owned by the authenticated user.

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


### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No
Default: application/json
Allowed values: application/json
Validation: Request body must be JSON.
Trigger: Every request containing a JSON body.
Description: Declares the request body format.
Example: application/json

## Path Parameter(s)

### path.id

Type: integer; Required: Yes; Nullable: No
Validation: Must parse as an integer account identifier.
Trigger: Account update request.
Description: Account identifier.
Example: 3

## Request Body

### bank_name

Type: string; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Account update request.
Description: Updated bank name.
Example: Vietcombank


### account_type

Type: string; Required: Yes; Nullable: No
Allowed values: Checking; Credit Card; Savings; Investment; Loan
Validation: Must be an allowed account type.
Trigger: Account update request.
Description: Updated account type.
Example: Checking


### branch_name

Type: string; Required: No; Nullable: Yes
Validation: If supplied, must be a string.
Trigger: Account update request.
Description: Updated branch name.
Example: Hanoi Branch


### account_number_full

Type: string; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Account update request.
Description: Updated full account number.
Example: 9704221234567890123


### balance

Type: number; Format: decimal; Required: Yes; Nullable: No
Validation: Must be greater than or equal to 0.
Trigger: Account update request.
Description: Updated balance.
Example: 4500000

## Success Response — HTTP 200

### message

Type: string; Required: Yes; Nullable: No
Trigger: The account is updated.
Description: Update success message.
Example: Account updated successfully


### account.account_id

Type: integer; Required: Yes; Nullable: No
Trigger: The account is updated.
Description: Updated account identifier.
Example: 3


### account.user_id

Type: integer; Required: Yes; Nullable: No
Trigger: The account is updated.
Description: Owner identifier.
Example: 1


### account.bank_name

Type: string; Required: Yes; Nullable: No
Trigger: The account is updated.
Description: Updated bank name.
Example: Vietcombank


### account.account_type

Type: string; Required: Yes; Nullable: No
Allowed values: Checking; Credit Card; Savings; Investment; Loan
Trigger: The account is updated.
Description: Updated account type.
Example: Checking


### account.branch_name

Type: string; Required: Yes; Nullable: Yes
Trigger: The account is updated.
Description: Updated branch name.
Example: Hanoi Branch


### account.account_number_full

Type: string; Required: Yes; Nullable: No
Trigger: The account is updated.
Description: Updated full account number.
Example: 9704221234567890123


### account.account_number_last_4

Type: string; Required: Yes; Nullable: No
Trigger: The account is updated.
Description: Updated final four digits.
Example: 0123


### account.balance

Type: number; Required: Yes; Nullable: No
Trigger: The account is updated.
Description: Updated balance.
Example: 4500000

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The path ID or request body is invalid.
Description: Error description returned by the global HTTP exception filter.
Example: Balance must not be less than 0
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
Example: You do not have permission to edit this account information.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 404

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The account does not exist.
Description: Error description returned by the global HTTP exception filter.
Example: This account could not be found.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The updated account cannot be stored.
Description: Error description returned by the global HTTP exception filter.
Example: An error occurred while saving the data. Please try again later.
Note: The error envelope also contains success=false and may contain an error field.
