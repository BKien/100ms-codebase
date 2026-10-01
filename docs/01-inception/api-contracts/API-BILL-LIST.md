---
artifact_type: api-contract
status: Frozen
api_id: API-BILL-LIST
related_uc_id: UC-12
---

# API-BILL-LIST: List Upcoming Bills

## General Information

### API ID

API-BILL-LIST

### API Name

List Upcoming Bills

### Related Use Case IDs

UC-12

### Method

GET

### Path

/api/v1/bills

### Description

Return the authenticated user's bills whose due date is today or later.

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
Trigger: Bills are retrieved.
Description: Upcoming bills ordered by due date.
Example: []


### data[].billId

Type: integer; Required: Yes; Nullable: No
Trigger: Bills are retrieved.
Description: Bill identifier.
Example: 7


### data[].userId

Type: integer; Required: Yes; Nullable: No
Trigger: Bills are retrieved.
Description: Owner user identifier.
Example: 1


### data[].itemDescription

Type: string; Required: Yes; Nullable: No
Trigger: Bills are retrieved.
Description: Bill description.
Example: Netflix


### data[].logoUrl

Type: string; Required: Yes; Nullable: Yes
Trigger: Bills are retrieved.
Description: Optional logo URL.
Example: https://example.com/netflix.png


### data[].dueDate

Type: string; Format: date; Required: Yes; Nullable: No
Trigger: Bills are retrieved.
Description: Due date.
Example: 2025-11-15


### data[].lastChargeDate

Type: string; Format: date; Required: Yes; Nullable: Yes
Trigger: Bills are retrieved.
Description: Most recent charge date.
Example: 2025-10-15


### data[].amount

Type: number; Required: Yes; Nullable: No
Trigger: Bills are retrieved.
Description: Bill amount.
Example: 260000

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
Trigger: Bill retrieval fails.
Description: Error description returned by the global HTTP exception filter.
Example: Failed to fetch bills
Note: The error envelope also contains success=false and may contain an error field.
