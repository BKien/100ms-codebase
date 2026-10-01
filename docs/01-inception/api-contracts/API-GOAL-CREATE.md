---
artifact_type: api-contract
status: Frozen
api_id: API-GOAL-CREATE
related_uc_id: UC-14
---

# API-GOAL-CREATE: Create Financial Goal

## General Information

### API ID

API-GOAL-CREATE

### API Name

Create Financial Goal

### Related Use Case IDs

UC-14

### Method

POST

### Path

/api/v1/goals

### Description

Create a saving or expense-limit goal for the authenticated user.

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


### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No
Default: application/json
Allowed values: application/json
Validation: Request body must be JSON.
Trigger: Every request containing a JSON body.
Description: Declares the request body format.
Example: application/json

## Request Body

### goal_type

Type: string; Required: Yes; Nullable: No
Allowed values: Saving; Expense_Limit
Validation: Must be Saving or Expense_Limit.
Trigger: Goal creation request.
Description: Goal type.
Example: Saving


### category_id

Type: integer; Required: Conditional; Nullable: Yes
Validation: Required and must reference an existing category when goal_type is Expense_Limit.
Trigger: Goal creation request.
Description: Category for an expense-limit goal.
Example: 3


### start_date

Type: string; Format: YYYY-MM-DD; Required: Yes; Nullable: No
Validation: Must be a valid date.
Trigger: Goal creation request.
Description: Goal start date.
Example: 2025-11-01


### end_date

Type: string; Format: YYYY-MM-DD; Required: Yes; Nullable: No
Validation: Must be a valid date later than start_date.
Trigger: Goal creation request.
Description: Goal end date.
Example: 2025-11-30


### target_amount

Type: number; Format: decimal; Required: Yes; Nullable: No
Validation: Must be greater than 0.
Trigger: Goal creation request.
Description: Target amount.
Example: 10000000

## Success Response — HTTP 201

### message

Type: string; Required: Yes; Nullable: No
Trigger: The goal is stored.
Description: Creation success message.
Example: Goal created successfully


### goal_id

Type: integer; Required: Yes; Nullable: No
Trigger: The goal is stored.
Description: Created goal identifier.
Example: 5

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: Input validation fails, end_date is not after start_date, or an expense-limit category is missing or invalid.
Description: Error description returned by the global HTTP exception filter.
Example: target_amount must be greater than 0.
Note: The error envelope also contains success=false and may contain an error field.

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
Trigger: The goal cannot be stored.
Description: Error description returned by the global HTTP exception filter.
Example: Unable to create the goal at this time. Please try again later.
Note: The error envelope also contains success=false and may contain an error field.
