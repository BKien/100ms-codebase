---
artifact_type: api-contract
status: Frozen
api_id: API-GOAL-UPDATE
related_uc_id: UC-15
---

# API-GOAL-UPDATE: Update Financial Goal

## General Information

### API ID

API-GOAL-UPDATE

### API Name

Update Financial Goal

### Related Use Case IDs

UC-15

### Method

PUT

### Path

/api/v1/goals/:goalId

### Description

Update the target amount of a goal owned by the authenticated user.

### Authentication

Bearer JWT

### Authorization

Goal owner

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

### path.goalId

Type: integer; Required: Yes; Nullable: No
Validation: The controller applies parseInt(goalId, 10) and does not explicitly reject NaN before calling the service.
Trigger: Every goal update request.
Description: Goal identifier as parsed by the controller.
Example: 5

## Request Body

### target_amount

Type: number; Format: decimal; Required: Yes; Nullable: No
Validation: Must be greater than 0.
Trigger: Goal update request.
Description: New target amount.
Example: 12000000

## Success Response — HTTP 200

### message

Type: string; Required: Yes; Nullable: No
Trigger: The goal is updated.
Description: Update success message.
Example: Goal updated successfully


### updated_goal.goal_id

Type: integer; Required: Yes; Nullable: No
Trigger: The goal is updated.
Description: Updated goal identifier.
Example: 5


### updated_goal.target_amount

Type: number; Required: Yes; Nullable: No
Trigger: The goal is updated.
Description: Updated target amount.
Example: 12000000

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: target_amount fails UpdateGoalDto validation.
Description: Validation errors for the request body.
Example: ["target_amount must be a positive number"]
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 401

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The JWT is missing, invalid, or expired.
Description: Error description returned by the global HTTP exception filter.
Example: Unauthorized
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 403

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The goal belongs to another user.
Description: Error description returned by the global HTTP exception filter.
Example: You do not have permission to edit this goal.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 404

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The goal does not exist.
Description: Error description returned by the global HTTP exception filter.
Example: The goal does not exist.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The goal update cannot be saved.
Description: Error description returned by the global HTTP exception filter.
Example: Unable to save changes at this time. Please try again later.
Note: The error envelope also contains success=false and may contain an error field.
