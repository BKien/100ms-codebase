---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-15
uc_name: "Adjust a Financial Goal"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A314:B331"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-15: Adjust a Financial Goal

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

Adjust a Financial Goal

### Description

As an authenticated goal owner, I want to change an existing goal's target amount.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user selects Edit on a displayed Saving or Expense_Limit goal.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: The selected goal exists and belongs to the authenticated user.

### Post-Condition(s)

POST-1: On success, only targetAmount is changed.
POST-2: The modal closes, a success toast appears, and GoalsPage refreshes.
POST-3: On failure, the previous target amount remains stored.

### Basic Flow

1. The user selects Edit for a displayed goal.
2. AdjustGoalModal opens with the current target amount.
3. The user enters a new target amount and selects Save.
4. The frontend requires a numeric amount greater than zero.
5. The frontend sends PUT /api/v1/goals/:goalId with target_amount.
6. ValidationPipe validates UpdateGoalDto.
7. GoalService finds the goal, verifies that goal.userId equals the authenticated userId, and overwrites only targetAmount.
8. The backend returns the goal ID and updated target amount.
9. The frontend displays a success toast, closes the modal, and refreshes goals.

### Alternative Flow

AF-1: Cancel
3a. The user closes or cancels the modal and no update request is sent.

### Exception Flow

EF-1: Invalid target amount
4a. The frontend displays an input error, or the backend returns HTTP 400.

EF-2: Goal not found
7a. The backend returns HTTP 404.

EF-3: Goal belongs to another user
7a. The backend returns HTTP 403.

EF-4: Storage failure
7a. The backend returns HTTP 500 and the modal displays its save failure message.

### Related UI

GoalsPage; AdjustGoalModal

### Related API IDs

API-GOAL-UPDATE

### Notes

Not specified

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

class Goal <<Entity>> {
  goalId: Integer [1]
  userId: Integer [1]
  goalType: GoalType [1]
  categoryId: Integer [0..1]
  startDate: Date [1]
  endDate: Date [1]
  targetAmount: Decimal [1]
}

class UpdateGoalDto <<DTO>> {
  target_amount: Decimal [1]
}

class UpdatedGoalDto <<DTO>> {
  goal_id: Integer [1]
  target_amount: Decimal [1]
}

class UpdateGoalResponseDto <<DTO>> {
  message: String [1]
  updated_goal: UpdatedGoalDto [1]
}

class GoalController <<Controller>> {
  updateGoal(
    request: AuthenticatedRequest,
    goalId: Integer,
    dto: UpdateGoalDto
  ): UpdateGoalResponseDto
}

class GoalService <<Service>> {
  updateGoal(
    userId: Integer,
    goalId: Integer,
    dto: UpdateGoalDto
  ): Goal
}

User "1" -- "0..*" Goal : owns

GoalController ..> AuthenticatedRequest
GoalController ..> UpdateGoalDto
GoalController ..> UpdateGoalResponseDto
GoalController ..> GoalService

GoalService ..> Goal
GoalService ..> UpdateGoalDto

UpdateGoalResponseDto --> UpdatedGoalDto
UpdatedGoalDto ..> Goal : maps from

@enduml
~~~

## Business Rules

~~~text
BR-GOAL-12: Positive updated target amount

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

pre BR_GOAL_12_TargetDefined:
  not dto.target_amount.oclIsUndefined()

pre BR_GOAL_12_TargetPositive:
  dto.target_amount > 0


BR-GOAL-13: Existing goal required

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

pre BR_GOAL_13_GoalExists:
  Goal.allInstances()->exists(g |
    g.goalId = goalId
  )

Technical constraint:
- If no Goal exists with goalId, the backend shall return HTTP 404 Not Found with message "Goal does not exist."


BR-GOAL-14: Authenticated goal ownership

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

pre BR_GOAL_14_OwnedByAuthenticatedUser:
  Goal.allInstances()->exists(g |
    g.goalId = goalId and
    g.userId = userId
  )

Technical constraints:
- userId shall be obtained from the validated JWT.
- If the goal belongs to another user, the backend shall return HTTP 403 Forbidden with message "You do not have permission to edit this goal."


BR-GOAL-15: Target-only goal update

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

post BR_GOAL_15_NoGoalCreatedOrDeleted:
  Goal.allInstances()->size() =
    Goal.allInstances()@pre->size()

post BR_GOAL_15_OnlyTargetAmountChanged:
  let original : Goal =
    Goal.allInstances()@pre->any(g |
      g.goalId = goalId
    )
  in
  let updated : Goal =
    Goal.allInstances()->any(g |
      g.goalId = goalId
    )
  in
    updated.targetAmount = dto.target_amount and
    updated.userId = original.userId and
    updated.goalType = original.goalType and
    updated.startDate = original.startDate and
    updated.endDate = original.endDate and
    updated.categoryId.oclIsUndefined() =
      original.categoryId.oclIsUndefined() and
    (
      not original.categoryId.oclIsUndefined()
      implies updated.categoryId = original.categoryId
    )


BR-GOAL-16: Successful update response

context GoalController::updateGoal(
  request : AuthenticatedRequest,
  goalId : Integer,
  dto : UpdateGoalDto
) : UpdateGoalResponseDto

post BR_GOAL_16_Response:
  result.message = 'Goal updated successfully' and
  result.updated_goal.goal_id = goalId and
  result.updated_goal.target_amount = dto.target_amount and
  Goal.allInstances()->exists(g |
    g.goalId = goalId and
    g.userId = request.userId and
    g.targetAmount = dto.target_amount
  )


BR-GOAL-17: Update failure handling

Technical constraints:
- An invalid or non-positive target_amount shall result in HTTP 400 Bad Request.
- A failed or rejected update shall not persist a changed targetAmount.
- If the goal does not exist, the backend shall return HTTP 404 Not Found.
- If the goal belongs to another user, the backend shall return HTTP 403 Forbidden.
- An unexpected repository/database failure while saving shall result in HTTP 500 Internal Server Error with message "Unable to save changes at this time. Please try again later."
- The controller parses goalId with parseInt(goalId, 10) and does not explicitly reject NaN before calling the service.
~~~

