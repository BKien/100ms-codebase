---
artifact_type: api-contract
status: Frozen
api_id: API-EXPENSE-SUMMARY
related_uc_id: UC-10
---

# API-EXPENSE-SUMMARY: Get Monthly Expense Summary

## General Information

### API ID

API-EXPENSE-SUMMARY

### API Name

Get Monthly Expense Summary

### Related Use Case IDs

UC-10

### Method

GET

### Path

/api/v1/expenses/summary

### Description

Aggregate the current year's expense transactions by month.

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

### data

Type: array<object>; Required: Yes; Nullable: No
Trigger: Expense data is aggregated.
Description: Monthly summary array; only months containing expenses are returned.
Example: []


### data[].month

Type: string; Required: Yes; Nullable: No
Trigger: Expense data is aggregated.
Description: English three-letter month abbreviation.
Example: Nov


### data[].totalExpense

Type: number; Required: Yes; Nullable: No
Trigger: Expense data is aggregated.
Description: Total expense amount for the month.
Example: 3500000

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
Trigger: Expense aggregation fails.
Description: Error description returned by the global HTTP exception filter.
Example: Unable to retrieve expense data.
Note: The error envelope also contains success=false and may contain an error field.
