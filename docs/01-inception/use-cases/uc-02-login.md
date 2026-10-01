---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-02
uc_name: "Log In"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A26:B44"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-02: Log In

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-02

### Use Case Name

Log In

### Description

As a registered visitor, I want to log in with my email address and password so that the application creates an authenticated session.

### Actor(s)

Visitor

### Priority

Not Specified

### Trigger

The visitor opens the login page or selects the Login link.

### Pre-Condition(s)

PRE-1: The login route (/login) is accessible to the visitor.
PRE-2: The backend and database services are operational.

### Post-Condition(s)

POST-1: On success, an authenticated user session is established and the user is redirected to the home page.
POST-2: On failure, no authenticated session is created, the visitor remains on the login page, and an error notification is displayed.

### Basic Flow

1. The visitor opens the login page (/login).
2. The frontend displays the login form (LoginForm).
3. The visitor enters credentials: email and password.
4. The visitor submits the login form.
5. The frontend performs preliminary validation on the credentials.
6. The frontend sends the authentication request (POST /api/auth/login) to the backend API.
7. The backend verifies the submitted credentials against registered accounts according to established security and authentication rules.
8. Upon successful authentication, the backend issues an authenticated session.
9. The backend returns a successful response with session credentials and user profile information.
10. The frontend establishes the authenticated session and redirects the user to the home page (/).

### Alternative Flow

AF-1: Client-side validation failure
5a. If credentials fail preliminary validation, the frontend displays field-level error messages and halts submission without calling the API.

### Exception Flow

EF-1: Authentication failure / Invalid credentials
7a. If credentials do not match an active registered account or fail security verification, the backend rejects the request and the frontend displays an authentication failure notification.

EF-2: Service or network failure
6a. If the request encounters a network error or server malfunction, the frontend displays a general failure message and remains on the login page.

### Related UI

Login page; LoginForm; route /login; AuthContext

### Related API IDs

API-AUTH-LOGIN

### Notes

Scope clarification: Authentication data is persisted in localStorage regardless of the “Keep me signed in” selection. Password recovery and Google login are outside scope.

## UML Model

~~~plantuml
@startuml

class LoginDto <<DTO>> {
  email: String [0..1]
  password: String [0..1]
}

class User <<Entity>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
  passwordHash: String [1]
}

class LoginUserDto <<DTO>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
}

class LoginDataDto <<DTO>> {
  accessToken: String [1]
  user: LoginUserDto [1]
}

class LoginResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: LoginDataDto [0..1]
}

class PasswordHasher <<Service>> {
  matches(password: String, hash: String): Boolean {query}
}

class AuthService <<Service>> {
  login(dto: LoginDto): LoginResponseDto
  isLoginInputValid(dto: LoginDto): Boolean {query}
}

AuthService ..> LoginDto
AuthService ..> LoginResponseDto
AuthService ..> PasswordHasher

LoginResponseDto --> LoginDataDto
LoginDataDto --> LoginUserDto
LoginUserDto ..> User : maps from

@enduml
~~~

## Business Rules

~~~text
BR-LOG-01 - Valid login email

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

pre BR_LOG_01_Defined:
  not dto.email.oclIsUndefined()

pre BR_LOG_01_NotEmpty:
  trim(dto.email).size() > 0

pre BR_LOG_01_ValidFormat:
  let normalizedEmail : String =
    lower(trim(dto.email))
  in
    isEmail(normalizedEmail)

BR-LOG-02 - Non-empty login password

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

pre BR_LOG_02_Defined:
  not dto.password.oclIsUndefined()

pre BR_LOG_02_NotEmpty:
  dto.password.size() > 0

BR-LOG-03 - Existing login account

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_03_SuccessRequiresExistingUser:
  result.success implies
    User.allInstances()->exists(
      user |
        lower(trim(user.email)) =
        lower(trim(dto.email))
    )

BR-LOG-04 - Credential verification

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_04_SuccessRequiresValidCredentials:
  result.success implies
    User.allInstances()->exists(
      user |
        lower(trim(user.email)) =
          lower(trim(dto.email))
        and
        self.passwordHasher.matches(
          dto.password,
          user.passwordHash
        )
    )

BR-LOG-05 - Invalid credential handling

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_05_InvalidCredentialsRejected:
  let credentialsValid : Boolean =
    User.allInstances()->exists(
      user |
        lower(trim(user.email)) =
          lower(trim(dto.email))
        and
        self.passwordHasher.matches(
          dto.password,
          user.passwordHash
        )
    )
  in
    result.success = credentialsValid

Technical constraints:

If credentialsValid = false, the backend shall return HTTP 401 Unauthorized.
The same authentication error shall be returned when the email does not exist or when the password is incorrect.

BR-LOG-06 - Successful login

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_06_SuccessResponse:
  result.success implies
    not result.data.oclIsUndefined() and
    not result.data.accessToken.oclIsUndefined() and
    result.data.accessToken.size() > 0 and
    not result.data.user.oclIsUndefined()

post BR_LOG_06_CorrectAuthenticatedUser:
  result.success implies
    User.allInstances()->exists(
      user |
        user.id = result.data.user.id and
        lower(trim(user.email)) =
          lower(trim(dto.email)) and
        result.data.user.fullName = user.fullName and
        result.data.user.email = user.email
    )

Technical constraints:

The backend shall issue a signed JWT access token after successful authentication.
Neither the submitted plaintext password nor the stored password hash shall be included in the API response.
After receiving a successful response, the client shall establish the authenticated session using the returned access token and user information.
~~~

