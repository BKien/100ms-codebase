---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "Create a Financial Goal"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A295:B313"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-14: Create a Financial Goal

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Create a Financial Goal

### Description

As an authenticated user, I want to create a Saving or Expense_Limit goal.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user selects Create Goal on the Goals page.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: Categories can be loaded when an Expense_Limit goal is selected.

### Post-Condition(s)

POST-1: On success, a Goal row is stored for userId from the JWT.
POST-2: Saving goals store categoryId as null.
POST-3: The modal closes, a success toast appears, and the Goals page refreshes.

### Basic Flow

1. The user opens the Create Goal modal.
2. The modal loads GET /api/categories.
3. The form defaults goal_type to Saving and clears all values each time it opens.
4. The user selects Saving or Expense_Limit, enters target_amount, start_date, and end_date, and selects a category when Expense_Limit is used.
5. The user selects Save.
6. The frontend requires target_amount > 0, non-empty dates, end_date later than start_date, and categoryId for Expense_Limit.
7. The frontend sends POST /api/v1/goals; for Saving it sends category_id=null.
8. ValidationPipe validates CreateGoalDto.
9. GoalService rechecks positive target, valid dates, end date ordering, and an existing category for Expense_Limit.
10. GoalService stores the goal under userId.
11. The frontend displays a success toast, closes the modal, and refreshes the goal list.

### Alternative Flow

AF-1: Create Saving goal
4a. The user keeps Saving selected.
7a. The request contains category_id=null.

AF-2: Create Expense_Limit goal
4a. The user selects Expense_Limit and chooses a category loaded from the category API.

AF-3: Cancel
5a. The user closes or cancels the modal and no create request is sent.

### Exception Flow

EF-1: Client-side validation failure
6a. The modal displays field errors and does not send the request.

EF-2: Invalid backend data or category
8a. The backend returns HTTP 400 and the modal displays the returned message.

EF-3: Storage failure
10a. The backend returns HTTP 500 and the modal displays its create-goal failure message.

### Related UI

GoalsPage; CreateGoalModal

### Related API IDs

API-GOAL-CREATE; API-CATEGORY-LIST

### Notes

Multiplicity clarification: Multiple Saving goals and duplicate Expense_Limit goals are allowed; goal creation does not enforce uniqueness by type or category.

## UML Model

~~~plantuml
@startuml

enum GoalType {
  SAVING
  EXPENSE_LIMIT
}

note right of GoalType
  SAVING maps to "Saving".
  EXPENSE_LIMIT maps to "Expense_Limit".
end note

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class User <<Entity>> {
  userId: Integer [1]
}

class Category <<Entity>> {
  categoryId: Integer [1]
  categoryName: String [1]
}

class Goal <<Entity>> {
  goalId: Integer [1]
  userId: Integer [1]
  goalType: GoalType [1]
  categoryId: Integer [0..1]
  startDate: Date [1]
  endDate: Date [1]
  targetAmount: Decimal [1]
}

class CreateGoalDto <<DTO>> {
  goal_type: GoalType [1]
  category_id: Integer [0..1]
  start_date: String [1]
  end_date: String [1]
  target_amount: Decimal [1]
}

class CreateGoalResponseDto <<DTO>> {
  message: String [1]
  goal_id: Integer [1]
}

class GoalController <<Controller>> {
  createGoal(
    request: AuthenticatedRequest,
    dto: CreateGoalDto
  ): CreateGoalResponseDto
}

class GoalService <<Service>> {
  createGoal(
    userId: Integer,
    dto: CreateGoalDto
  ): Goal

  isValidDate(value: String): Boolean {query}
  toDate(value: String): Date {query}
}

User "1" -- "0..*" Goal : owns
Category "0..1" -- "0..*" Goal : categorizes

GoalController ..> AuthenticatedRequest
GoalController ..> CreateGoalDto
GoalController ..> CreateGoalResponseDto
GoalController ..> GoalService

GoalService ..> Goal
GoalService ..> Category
GoalService ..> CreateGoalDto

@enduml
~~~

## Business Rules

~~~text
BR-GOAL-04: Valid goal type

context GoalService::createGoal(
  userId : Integer,
  dto : CreateGoalDto
) : Goal

pre BR_GOAL_04_GoalTypeDefined:
  not dto.goal_type.oclIsUndefined()

pre BR_GOAL_04_AllowedGoalType:
  Set{
    GoalType::SAVING,
    GoalType::EXPENSE_LIMIT
  }->includes(dto.goal_type)


BR-GOAL-05: Positive target amount

context GoalService::createGoal(
  userId : Integer,
  dto : CreateGoalDto
) : Goal

pre BR_GOAL_05_TargetDefined:
  not dto.target_amount.oclIsUndefined()

pre BR_GOAL_05_TargetPositive:
  dto.target_amount > 0


BR-GOAL-06: Valid goal date interval

context GoalService::createGoal(
  userId : Integer,
  dto : CreateGoalDto
) : Goal

pre BR_GOAL_06_DatesDefined:
  not dto.start_date.oclIsUndefined() and
  not dto.end_date.oclIsUndefined()

pre BR_GOAL_06_ValidDates:
  self.isValidDate(dto.start_date) and
  self.isValidDate(dto.end_date)

pre BR_GOAL_06_EndAfterStart:
  self.toDate(dto.end_date) >
  self.toDate(dto.start_date)

Technical constraint:
- start_date and end_date shall use valid YYYY-MM-DD date strings.


BR-GOAL-07: Goal category rules

context GoalService::createGoal(
  userId : Integer,
  dto : CreateGoalDto
) : Goal

pre BR_GOAL_07_ExpenseCategoryRequired:
  dto.goal_type = GoalType::EXPENSE_LIMIT
  implies
    not dto.category_id.oclIsUndefined()

pre BR_GOAL_07_ExpenseCategoryExists:
  dto.goal_type = GoalType::EXPENSE_LIMIT
  implies
    Category.allInstances()->exists(c |
      c.categoryId = dto.category_id
    )

post BR_GOAL_07_CategoryPersisted:
  (
    dto.goal_type = GoalType::SAVING
    implies
      result.categoryId.oclIsUndefined()
  )
  and
  (
    dto.goal_type = GoalType::EXPENSE_LIMIT
    implies
      result.categoryId = dto.category_id
  )

Technical constraint:
- Any category_id supplied for a Saving goal is not persisted.
- Saving goals are stored with categoryId = null.

BR-GOAL-08: Authenticated goal ownership

context GoalService::createGoal(
  userId : Integer,
  dto : CreateGoalDto
) : Goal

post BR_GOAL_08_OwnedByAuthenticatedUser:
  result.userId = userId

Technical constraint:
- userId shall be obtained from the validated JWT.
- The client shall not determine the owner through the request body.


BR-GOAL-09: Created goal persistence

context GoalService::createGoal(
  userId : Integer,
  dto : CreateGoalDto
) : Goal

post BR_GOAL_09_ExactlyOneGoalCreated:
  Goal.allInstances()->size() =
    Goal.allInstances()@pre->size() + 1

post BR_GOAL_09_PersistedValues:
  Goal.allInstances()->one(g |
    g.goalId = result.goalId and
    g.userId = userId and
    g.goalType = dto.goal_type and
    g.startDate = self.toDate(dto.start_date) and
    g.endDate = self.toDate(dto.end_date) and
    g.targetAmount = dto.target_amount
  )


BR-GOAL-10: Successful creation response

context GoalController::createGoal(
  request : AuthenticatedRequest,
  dto : CreateGoalDto
) : CreateGoalResponseDto

post BR_GOAL_10_Response:
  result.message = 'Goal created successfully' and
  Goal.allInstances()->exists(g |
    g.goalId = result.goal_id and
    g.userId = request.userId
  )


BR-GOAL-11: Creation failure handling

Technical constraints:
- Invalid goal_type, target_amount, dates, date ordering, or Expense_Limit category shall result in HTTP 400 Bad Request.
- Validation failure shall not persist a Goal record.
- An unexpected repository/database failure shall result in HTTP 500 Internal Server Error with message:
  "Unable to create the goal at this time. Please try again later."
- The implementation does not enforce uniqueness for Saving goals or Expense_Limit goals. Existing goals of the same type or category do not prevent creation.
~~~

