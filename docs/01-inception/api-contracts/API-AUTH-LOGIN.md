---
artifact_type: api-contract
status: Frozen
api_id: API-AUTH-LOGIN
related_uc_id: UC-02
---

# API-AUTH-LOGIN: User Login

## General Information

### API ID

API-AUTH-LOGIN

### API Name

User Login

### Related Use Case IDs

UC-02

### Method

POST

### Path

/api/auth/login

### Description

Authenticate a registered user and issue a JWT access token.

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

### email

Type: string; Format: email; Required: Yes; Nullable: No
Validation: Must be a valid email address and must not be empty.
Trigger: Login request.
Description: Registered email address.
Example: user@example.com


### password

Type: string; Format: password; Required: Yes; Nullable: No
Validation: Must be a non-empty string.
Trigger: Login request.
Description: User password.
Example: P@ssw0rd!

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No
Trigger: Credentials are valid.
Description: Indicates whether authentication succeeded.
Example: true


### message

Type: string; Required: Yes; Nullable: No
Trigger: Credentials are valid.
Description: Human-readable success message.
Example: Successful Login


### data.accessToken

Type: string; Required: Yes; Nullable: No
Trigger: Credentials are valid.
Description: JWT access token.
Example: eyJhbGciOiJIUzI1NiIs...


### data.user.id

Type: integer; Required: Yes; Nullable: No
Trigger: Credentials are valid.
Description: Authenticated user identifier.
Example: 1


### data.user.fullName

Type: string; Required: Yes; Nullable: No
Trigger: Credentials are valid.
Description: Authenticated user's full name.
Example: John Doe


### data.user.email

Type: string; Required: Yes; Nullable: No
Trigger: Credentials are valid.
Description: Authenticated user's email address.
Example: user@example.com

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: Email is invalid, a required field is empty, or an undeclared field is supplied.
Description: Error description returned by the global HTTP exception filter.
Example: ["Invalid email"]
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 401

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: The email is not registered or the password is incorrect.
Description: Error description returned by the global HTTP exception filter.
Example: Email or password is incorrect.
Note: The error envelope also contains success=false and may contain an error field.

## Error Response — HTTP 500

### message

Type: string | string[]; Required: Yes; Nullable: No
Trigger: An unexpected authentication or database error occurs.
Description: Error description returned by the global HTTP exception filter.
Example: Internal Server Error
Note: The error envelope also contains success=false and may contain an error field.
