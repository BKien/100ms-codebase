---
artifact_type: api-contract
status: Frozen
api_id: API-AUTH-REGISTER
related_uc_id: UC-01
---

# API-AUTH-REGISTER: User Registration

## General Information

### API ID

API-AUTH-REGISTER

### API Name

User Registration

### Related Use Case IDs

UC-01

### Method

POST

### Path

/api/auth/register

### Description

Create a new user account and issue a JWT token.

### Authentication

Public

### Authorization

None

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No
Default: application/json
Allowed values: application/json
Validation: Request body must be JSON.
Trigger: Every request containing a JSON body.
Description: Declares the request body format.
Example: application/json

## Request Body

### fullName

Type: string; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Registration request.
Description: User's full name.
Example: John Doe


### email

Type: string; Format: email; Required: Yes; Nullable: No
Validation: Must be a valid, non-empty email address.
Trigger: Registration request.
Description: Unique email address.
Example: user@example.com


### password

Type: string; Format: password; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Registration request.
Description: New password.
Example: P@ssw0rd!


### confirmPassword

Type: string; Format: password; Required: Yes; Nullable: No
Validation: Must be a non-empty string and equal password.
Trigger: Registration request.
Description: Password confirmation.
Example: P@ssw0rd!

## Success Response — HTTP 201

### success

Type: boolean; Required: Yes; Nullable: No
Trigger: The account is created successfully.
Description: Indicates that registration succeeded.
Example: true


### message

Type: string; Required: Yes; Nullable: No
Trigger: The account is created successfully.
Description: Human-readable registration success message.
Example: Registration successful


### data.accessToken

Type: string; Required: Yes; Nullable: No
Trigger: The account is created successfully.
Description: JWT access token issued for the created user.
Example: eyJhbGciOiJIUzI1NiIs...


### data.user.id

Type: integer; Required: Yes; Nullable: No
Trigger: The account is created successfully.
Description: Created user identifier.
Example: 1


### data.user.fullName

Type: string; Required: Yes; Nullable: No
Trigger: The account is created successfully.
Description: Normalized full name of the created user.
Example: John Doe


### data.user.email

Type: string; Required: Yes; Nullable: No
Trigger: The account is created successfully.
Description: Normalized email address of the created user.
Example: user@example.com

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: Input validation fails or password and confirmPassword do not match.
Description: Error description returned by the global HTTP exception filter.
Example: Bad Request / Passwords do not match.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 409

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The email address is already registered.
Description: Error description returned by the global HTTP exception filter.
Example: Conflict / This email is already registered.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The user record or token cannot be created.
Description: Error description returned by the global HTTP exception filter.
Example: Internal Server Error
Note: The error envelope also contains success=false and may contain an error field.
