---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-01
uc_name: "Register an Account"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A5:B25"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-01: Register an Account

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-01

### Use Case Name

Register an Account

### Description

As a visitor, I want to register with my full name, email address, password, and password confirmation so that the application creates an authenticated user session.

### Actor(s)

Visitor

### Priority

Not Specified

### Trigger

The visitor opens the registration page or selects the Create an account link.

### Pre-Condition(s)

PRE-1: The registration route (/register) is accessible to the visitor.
PRE-2: The backend and database services are operational.

### Post-Condition(s)

POST-1: On success, a new user account is created and persisted, an authenticated session is established, and the user is redirected to the home page.
POST-2: On failure, no user account or authenticated session is created, and an appropriate error message is displayed.

### Basic Flow

1. The visitor opens the registration page (/register).
2. The frontend displays the registration form (SignUpForm).
3. The visitor enters registration details: fullName, email, password, and confirmPassword.
4. The visitor submits the registration form.
5. The frontend performs preliminary validation on the submitted form fields.
6. The frontend sends the registration request (POST /api/auth/register) to the backend API.
7. The backend validates and processes the registration data according to established business rules.
8. Upon successful validation, the backend persists the new user account securely and generates an authenticated session.
9. The backend returns a successful response containing the authentication token and created user profile data.
10. The frontend establishes the authenticated user session and redirects the user to the home page (/).

### Alternative Flow

AF-1: Client-side validation failure
5a. If any submitted field fails preliminary validation, the frontend displays field-level error messages and halts form submission without calling the API.

AF-2: Registration conflict / Duplicate account
7a. If registration data conflicts with existing account policies (e.g., email already registered), the backend rejects the request and the frontend displays the returned error message.

### Exception Flow

EF-1: Registration request failure
6a. If the registration request encounters an unexpected network or server error, the frontend displays a failure notification and remains on the registration form.

### Related UI

Register page; SignUpForm; route /register; AuthContext

### Related API IDs

API-AUTH-REGISTER

### Notes

Scope clarification: This use case covers email/password registration only. Google sign-up is outside scope.

## UML Model

~~~plantuml
@startuml

class RegisterDto <<DTO>> {
  fullName: String [0..1]
  email: String [0..1]
  password: String [0..1]
  confirmPassword: String [0..1]
}

class User <<Entity>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
  passwordHash: String [1]
}

class RegisteredUserDto <<DTO>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
}

class RegisterDataDto <<DTO>> {
  accessToken: String [1]
  user: RegisteredUserDto [1]
}

class RegisterResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: RegisterDataDto [0..1]
}

class AuthResponse <<DTO>> {
  success: Boolean
  user: User [0..1]
  accessToken: String [0..1]
}

class PasswordHasher <<Service>> {
  hash(password: String, rounds: Integer): String
  matches(password: String, hash: String): Boolean {query}
  cost(hash: String): Integer {query}
}

class AuthService <<Service>> {
  register(dto: RegisterDto): RegisterResponseDto
  isRegistrationInputValid(dto: RegisterDto): Boolean {query}
}

AuthService ..> RegisterDto
AuthService ..> RegisterResponseDto
AuthService ..> PasswordHasher

RegisterResponseDto --> RegisterDataDto
RegisterDataDto --> RegisteredUserDto
RegisteredUserDto ..> User : maps from

@enduml
~~~

## Business Rules

~~~text
BR-REG-01: Valid registration full name:
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_01_Defined:
  not dto.fullName.oclIsUndefined()

pre BR_REG_01_Length:
  let normalizedName : String = trim(nfc(dto.fullName))
  in
    normalizedName.size() >= 4 and
    normalizedName.size() <= 25

pre BR_REG_01_Pattern:
  let normalizedName : String = trim(nfc(dto.fullName))
  in
    matches(
      normalizedName,
      '^[\p{L}]+(?: [\p{L}]+)*$'
    )

post BR_REG_01_Normalized:
  let normalizedName : String = trim(nfc(dto.fullName))
  in
    result.success implies
      not result.data.oclIsUndefined() and
      not result.data.user.oclIsUndefined() and
      result.data.user.fullName = normalizedName

BR-REG-02: Valid registration email:
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_02_Defined:
  not dto.email.oclIsUndefined()

pre BR_REG_02_NotEmpty:
  trim(dto.email).size() > 0

pre BR_REG_02_MaxLength:
  let normalizedEmail : String = lower(trim(dto.email))
  in
    normalizedEmail.size() <= 255

pre BR_REG_02_ValidFormat:
  let normalizedEmail : String = lower(trim(dto.email))
  in
    isEmail(normalizedEmail)

post BR_REG_02_Normalized:
  let normalizedEmail : String = lower(trim(dto.email))
  in
    result.success implies
      not result.data.oclIsUndefined() and
      not result.data.user.oclIsUndefined() and
      result.data.user.email = normalizedEmail

BR-REG-03: Unique registration email:
context User

inv BR_REG_03_UniqueNormalizedEmail:
  User.allInstances()->isUnique(
    user | lower(trim(user.email))
  )

context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_03_EmailNotRegistered:
  not User.allInstances()->exists(
    user |
      lower(trim(user.email)) =
      lower(trim(dto.email))
  )

BR-REG-04: Valid registration password
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_04_Defined:
  not dto.password.oclIsUndefined()

pre BR_REG_04_Length:
  dto.password.size() >= 8 and
  dto.password.size() <= 64

pre BR_REG_04_NoWhitespace:
  not matches(
    dto.password,
    '.*\s.*'
  )

pre BR_REG_04_ContainsLowercase:
  matches(
    dto.password,
    '.*[a-z].*'
  )

pre BR_REG_04_ContainsUppercase:
  matches(
    dto.password,
    '.*[A-Z].*'
  )

pre BR_REG_04_ContainsDigit:
  matches(
    dto.password,
    '.*[0-9].*'
  )

pre BR_REG_04_ContainsSpecialCharacter:
  matches(
    dto.password,
    '.*[!@#$%^&*(){}\-_+=\[\],./<>?\\|:;].*'
  )

BR-REG-05: Permitted password characters
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_05_AllowedCharacters:
  matches(
    dto.password,
    '^[A-Za-z0-9!@#$%^&*(){}_=+\[\],./<>?\\|:;\-]+$'
  )

BR-REG-06: Matching registration passwords
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_06_ConfirmPasswordDefined:
  not dto.confirmPassword.oclIsUndefined()

pre BR_REG_06_PasswordsMatch:
  dto.confirmPassword = dto.password

BR-REG-07: Confirm password handling
confirmPassword shall not be persisted or written to application logs.

BR-REG-08: Invalid registration handling
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

post BR_REG_08_InvalidRequestRejected:
  not self.isRegistrationInputValid(dto)
  implies
    result.success = false

post BR_REG_08_NoUserCreated:
  not self.isRegistrationInputValid(dto)
  implies
    User.allInstances()->size() =
    User.allInstances()@pre->size()

BR-REG-09: Bcrypt password storage
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

post BR_REG_09_PasswordHashed:
  result.success implies
    let createdUser : User =
      User.allInstances()->any(
        user |
          lower(trim(user.email)) =
          lower(trim(dto.email))
      )
    in
      not createdUser.oclIsUndefined() and
      createdUser.passwordHash <> dto.password and
      bcryptMatches(
        dto.password,
        createdUser.passwordHash
      ) and
      bcryptCost(createdUser.passwordHash) = 10
Technical constraints:
- The plaintext password shall not be persisted or logged.
- Neither the plaintext password nor passwordHash shall be included in the API response.
- The bcrypt hash shall be generated before the User record is persisted.

BR-REG-10: Concurrent registration conflict handling
context User

inv BR_REG_10_AtMostOneUserPerNormalizedEmail:
  User.allInstances()->forAll(user |
    User.allInstances()
      ->select(other |
        lower(trim(other.email)) =
        lower(trim(user.email))
      )
      ->size() = 1
  )
Technical constraints:
- User.email shall be protected by the database unique constraint defined in BR-REG-03.
- If multiple concurrent registration requests contain the same normalized email, exactly one User creation shall succeed.
- Each conflicting request shall be rejected with HTTP 409 Conflict.
- A rejected request shall not issue a JWT or establish an authenticated session.
- After all concurrent requests complete, exactly one User shall exist for the normalized email.

BR-REG-11: Successful registration
context AuthService::register(
  dto : RegisterDto
) : RegisterResponseDto

post BR_REG_11_SuccessResponse:
  result.success implies
    result.message.size() > 0 and
    not result.data.oclIsUndefined() and
    not result.data.user.oclIsUndefined() and
    not result.data.accessToken.oclIsUndefined() and
    result.data.accessToken.size() > 0

post BR_REG_11_UserCreated:
  result.success implies
    User.allInstances()->one(user |
      user.id = result.data.user.id and
      lower(trim(user.email)) =
        lower(trim(dto.email))
    )
Technical constraints:
- After the User has been successfully persisted, the backend shall issue a signed JWT access token identifying that User.
- The successful response shall contain the created user information and access token inside the data object.
- After receiving the successful response, the client shall establish an authenticated session using the returned token.
- The client shall redirect the authenticated user to the home page.
- A session shall not be established and navigation shall not occur when registration fails.
~~~

