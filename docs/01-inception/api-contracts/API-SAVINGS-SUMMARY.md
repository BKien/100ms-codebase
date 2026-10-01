---
artifact_type: api-contract
status: Frozen
api_id: API-SAVINGS-SUMMARY
related_uc_id: UC-16
---

# API-SAVINGS-SUMMARY: Get Savings Summary

## General Information

### API ID

API-SAVINGS-SUMMARY

### API Name

Get Savings Summary

### Related Use Case IDs

UC-16

### Method

GET

### Path

/api/v1/savings/summary

### Description

Return monthly net savings for a selected year and the preceding year.

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

## Query Parameter(s)

### query.year

Type: integer; Format: YYYY; Required: No; Nullable: No
Default: Current year
Validation: The controller applies parseInt(year, 10). Missing, NaN, <1900, or >2100 values use the current year. A leading numeric prefix is accepted by parseInt.
Trigger: Savings summary request.
Description: Optional target year resolved by the controller.
Example: 2025

## Request Body

None

## Success Response — HTTP 200

### user_id

Type: integer; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Authenticated user identifier.
Example: 1


### year

Type: integer; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Resolved target year.
Example: 2025


### summary.this_year

Type: array<object>; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Twelve monthly savings values for the selected year.
Example: []


### summary.this_year[].month

Type: string; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Two-digit month number.
Example: 01


### summary.this_year[].amount

Type: number; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Revenue minus expense for the month.
Example: 1500000


### summary.last_year

Type: array<object>; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Twelve monthly savings values for the previous year.
Example: []


### summary.last_year[].month

Type: string; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Two-digit month number.
Example: 01


### summary.last_year[].amount

Type: number; Required: Yes; Nullable: No
Trigger: The summary is calculated; missing data produces zero-valued months.
Description: Revenue minus expense for the month.
Example: 1200000

## Error Response — HTTP 401

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The JWT is missing, invalid, or expired.
Description: Error description returned by the global HTTP exception filter.
Example: Unable to authenticate the user. Please log in again.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: Savings calculation fails.
Description: Error description returned by the global HTTP exception filter.
Example: An internal server error occurred while processing the savings summary.
Note: The error envelope also contains success=false and may contain an error field.
