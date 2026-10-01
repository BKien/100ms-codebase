---
artifact_type: api-contract
status: Frozen
api_id: API-EXPENSE-BREAKDOWN
related_uc_id: UC-11
---

# API-EXPENSE-BREAKDOWN: Get Expense Breakdown by Category

## General Information

### API ID

API-EXPENSE-BREAKDOWN

### API Name

Get Expense Breakdown by Category

### Related Use Case IDs

UC-11

### Method

GET

### Path

/api/v1/expenses/breakdown

### Description

Return category totals, month-over-month changes, and transaction details for a selected month.

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

### query.month

Type: string; Format: YYYY-MM; Required: Yes; Nullable: No
Validation: Must match YYYY-MM and represent a month from 01 to 12.
Trigger: Expense breakdown request.
Description: Selected month.
Example: 2025-11

## Request Body

None

## Success Response — HTTP 200

### data

Type: array<object>; Required: Yes; Nullable: No
Trigger: Expense data exists for the selected month.
Description: Category breakdown sorted by total descending.
Example: []


### data[].category

Type: string; Required: Yes; Nullable: No
Trigger: Expense data exists for the selected month.
Description: Category name; uncategorized records use Uncategorized.
Example: Entertainment


### data[].total

Type: number; Required: Yes; Nullable: No
Trigger: Expense data exists for the selected month.
Description: Total expense amount in the category.
Example: 1500000


### data[].changePercent

Type: number; Required: Yes; Nullable: Yes
Trigger: Expense data exists for the selected month.
Description: Percentage change from the previous month.
Example: 25.5


### data[].subCategories

Type: array<object>; Required: Yes; Nullable: No
Trigger: Expense data exists for the selected month.
Description: Underlying expense transactions.
Example: []


### data[].subCategories[].item_description

Type: string; Required: Yes; Nullable: No
Trigger: Expense data exists for the selected month.
Description: Transaction description.
Example: Movie Ticket


### data[].subCategories[].amount

Type: number; Required: Yes; Nullable: No
Trigger: Expense data exists for the selected month.
Description: Transaction amount.
Example: 150000


### data[].subCategories[].date

Type: string; Format: date; Required: Yes; Nullable: No
Trigger: Expense data exists for the selected month.
Description: Transaction date.
Example: 2025-11-01

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: month is missing or does not match YYYY-MM.
Description: Error description returned by the global HTTP exception filter.
Example: Invalid month parameter. Please use the YYYY-MM format (for example: 2025-11)
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 401

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The JWT is missing, invalid, or expired.
Description: Error description returned by the global HTTP exception filter.
Example: Unauthorized
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 404

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The user has no account, the month is invalid, or no expense exists in the selected month.
Description: Error description returned by the global HTTP exception filter.
Example: No expense data for this month.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: Breakdown calculation fails.
Description: Error description returned by the global HTTP exception filter.
Example: Unable to retrieve expense breakdown data.
Note: The error envelope also contains success=false and may contain an error field.
