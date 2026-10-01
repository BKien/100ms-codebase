---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-13
uc_name: "View Financial Goals"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A276:B294"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-13: View Financial Goals

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

View Financial Goals

### Description

As an authenticated user, I want to view a saving goal, active expense-limit goals, and their calculated current-month progress.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user opens the Goals page.

### Pre-Condition(s)

PRE-1: The user is authenticated.

### Post-Condition(s)

POST-1: The response contains one Saving goal or null and an array of Expense_Limit goals whose date ranges overlap the current month.
POST-2: Saving progress and expense-category progress are calculated from the user's current-month transactions.
POST-3: The page displays an empty goal state when both sections are absent.

### Basic Flow

1. The user opens /goals.
2. GoalsPage sends GET /api/v1/goals.
3. GoalService finds one Saving goal for userId.
4. The service finds all Expense_Limit goals for userId and filters those whose intervals overlap the current month.
5. If a Saving goal exists, the service sums current-month Revenue and Expense transactions across user-owned accounts and calculates target_achieved = revenue - expense.
6. For each active Expense_Limit goal, the service sums current-month Expense transactions for the goal's category across user-owned accounts.
7. The backend returns success, message, savingGoal, and expenseGoals.
8. The frontend displays goal amounts, dates, and progress percentages.

### Alternative Flow

AF-1: No goals
3a. savingGoal is null and expenseGoals is empty.
8a. The page displays its no-goals state and a Create Goal action.

AF-2: No owned accounts or no matching transactions
5a. Calculated progress values remain zero.

### Exception Flow

EF-1: Unauthorized request
2a. HTTP 401 redirects to /login.

EF-2: Retrieval or calculation failure
3a. The backend returns HTTP 500 and the page displays its retryable error component.

### Related UI

GoalsPage; saving and expense goal cards; route /goals

### Related API IDs

API-GOAL-LIST

### Notes

Assumption: The dashboard treats the Saving goal as singular. Uniqueness is not a persisted invariant; if multiple Saving goals exist, which one is selected is unspecified.

## UML Model

~~~plantuml
@startuml

enum GoalType {
  SAVING
  EXPENSE_LIMIT
}

enum TransactionType {
  REVENUE
  EXPENSE
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

class Account <<Entity>> {
  accountId: Integer [1]
  userId: Integer [1]
}

class Transaction <<Entity>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  categoryId: Integer [0..1]
  transactionDate: Date [1]
  type: TransactionType [1]
  amount: Decimal [1]
}

class Category <<Entity>> {
  categoryId: Integer [1]
  categoryName: String [1]
}

class SavingGoalDto <<DTO>> {
  goalId: Integer [1]
  goalType: GoalType [1]
  targetAmount: Decimal [1]
  targetAchieved: Decimal [1]
  startDate: String [1]
  endDate: String [1]
}

class ExpenseGoalDto <<DTO>> {
  goalId: Integer [1]
  category: String [1]
  targetAmount: Decimal [1]
  currentExpense: Decimal [1]
}

class GoalDataDto <<DTO>> {
  savingGoal: SavingGoalDto [0..1]
  expenseGoals: ExpenseGoalDto [*]
}

class GoalListResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: GoalDataDto [1]
}

class GoalService <<Service>> {
  getGoals(userId: Integer): GoalListResponseDto
  currentMonthStart(): Date {query}
  currentMonthEnd(): Date {query}
}

GoalService ..> GoalListResponseDto
GoalListResponseDto --> GoalDataDto
GoalDataDto --> SavingGoalDto
GoalDataDto --> ExpenseGoalDto
SavingGoalDto ..> Goal : maps from
ExpenseGoalDto ..> Goal : maps from
Goal --> Category : category [0..1]
Transaction --> Account
Transaction --> Category : category [0..1]

@enduml
~~~

## Business Rules

~~~text
BR-GOAL-01: Goals selected for display

context GoalService::getGoals(
  userId : Integer
) : GoalListResponseDto

post BR_GOAL_01_SavingGoalScope:
  let savingGoals : Set(Goal) =
    Goal.allInstances()
      ->select(g |
        g.userId = userId and
        g.goalType = GoalType::SAVING
      )
      ->asSet()
  in
    result.success implies
      (
        (savingGoals->isEmpty() and
          result.data.savingGoal.oclIsUndefined())
        or
        (not savingGoals->isEmpty() and
          not result.data.savingGoal.oclIsUndefined() and
          savingGoals->exists(g |
            g.goalId = result.data.savingGoal.goalId and
            g.targetAmount = result.data.savingGoal.targetAmount
          ))
      )

post BR_GOAL_01_ExpenseGoalsExact:
  let expected : Set(Goal) =
    Goal.allInstances()
      ->select(g |
        g.userId = userId and
        g.goalType = GoalType::EXPENSE_LIMIT and
        g.startDate <= self.currentMonthEnd() and
        g.endDate >= self.currentMonthStart()
      )
      ->asSet()
  in
    result.success implies
      result.data.expenseGoals->size() = expected->size() and
      result.data.expenseGoals->forAll(dto |
        expected->exists(g |
          g.goalId = dto.goalId and
          g.targetAmount = dto.targetAmount
        )
      )

Technical Constraint:
- The current implementation uses the repository's findOne method for Saving goals and does not enforce uniqueness. If multiple Saving goals exist, one matching goal is returned.

BR-GOAL-02: Saving goal achieved amount

context GoalService::getGoals(
  userId : Integer
) : GoalListResponseDto

post BR_GOAL_02_TargetAchieved:
  not result.data.savingGoal.oclIsUndefined()
  implies
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let monthTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          t.transactionDate >= self.currentMonthStart() and
          t.transactionDate <= self.currentMonthEnd()
        )
        ->asSet()
    in
    let totalRevenue : Decimal =
      monthTransactions
        ->select(t | t.type = TransactionType::REVENUE)
        ->collect(t | t.amount)
        ->sum()
    in
    let totalExpense : Decimal =
      monthTransactions
        ->select(t | t.type = TransactionType::EXPENSE)
        ->collect(t | t.amount)
        ->sum()
    in
      result.data.savingGoal.targetAchieved =
        totalRevenue - totalExpense

Technical Constraint:
- An empty SUM result is treated as 0, corresponding to COALESCE(SUM(...), 0) in the implementation.

BR-GOAL-03: Expense-limit current expense

context GoalService::getGoals(
  userId : Integer
) : GoalListResponseDto

post BR_GOAL_03_CurrentExpense:
  result.data.expenseGoals->forAll(dto |
    let goal : Goal =
      Goal.allInstances()->any(g | g.goalId = dto.goalId)
    in
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let currentExpense : Decimal =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          t.type = TransactionType::EXPENSE and
          t.categoryId = goal.categoryId and
          t.transactionDate >= self.currentMonthStart() and
          t.transactionDate <= self.currentMonthEnd()
        )
        ->collect(t | t.amount)
        ->sum()
    in
      dto.currentExpense = currentExpense and
      (
        (goal.categoryId.oclIsUndefined() and dto.category = 'Unknown')
        or
        Category.allInstances()->exists(c |
          c.categoryId = goal.categoryId and
          dto.category = c.categoryName
        )
      )
  )

Technical Constraint:
- If the user has no owned accounts or no matching Expense transactions, currentExpense is 0.
~~~

