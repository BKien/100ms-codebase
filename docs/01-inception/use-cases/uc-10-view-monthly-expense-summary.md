---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "View Monthly Expense Summary"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A219:B237"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-10: View Monthly Expense Summary

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

View Monthly Expense Summary

### Description

As an authenticated user, I want to view current-year expense totals grouped by month.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user opens the Expenses page.

### Pre-Condition(s)

PRE-1: The user is authenticated.

### Post-Condition(s)

POST-1: If eligible expense data exists, the system displays the user's monthly expense summary for the current calendar year.
POST-2: The monthly summary represents all twelve calendar months, with months containing no eligible expense transactions represented by zero.

### Basic Flow

1. The user opens /expenses.
2. ExpenseSummaryChart sends GET /api/v1/expenses/summary.
3. JwtAuthGuard supplies userId.
4. ExpensesService loads account IDs owned by the user.
5. If accounts exist, the service aggregates only Expense transactions between the first and last day of the current year, grouped by SQL month and ordered ascending.
6. The backend returns data entries containing month abbreviations and totalExpense.
7. The frontend expands the response to Jan-Dec by inserting zero for missing months and renders the comparison bar chart.

### Alternative Flow

AF-1: No owned accounts or no expense rows
4a. The service returns an empty array.
7a. The frontend displays its no-expense-data message rather than the chart.

### Exception Flow

EF-1: Retrieval or aggregation failure
5a. The backend returns HTTP 500.
5b. The frontend displays the returned error value or its general loading error.

### Related UI

ExpensesPage; ExpenseSummaryChart; route /expenses

### Related API IDs

API-EXPENSE-SUMMARY

### Notes

Scope clarification: The expense summary aggregates the current calendar year only; the API does not accept a year parameter.

## UML Model

~~~plantuml
@startuml

class AuthenticatedRequest <<DTO>> {
  userId: Integer [1]
  email: String [1]
}

class Account <<Entity>> {
  accountId: Integer [1]
  userId: Integer [1]
}

class Transaction <<Entity>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  amount: Decimal [1]
  status: TransactionStatus [1]
}

enum TransactionType {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

class ExpenseSummaryItem <<DTO>> {
  month: String [1]
  totalExpense: Number [1]
}

class ExpenseSummaryResponseDto <<DTO>> {
  data: ExpenseSummaryItem [0..*]
}

class JwtAuthGuard <<Guard>> {
  validate(token: BearerJWT): AuthenticatedRequest
}

class ExpensesController <<Controller>> {
  getExpenseSummary(request: AuthenticatedRequest): ExpenseSummaryResponseDto
}

class ExpensesService <<Service>> {
  getExpenseSummary(userId: Integer): Sequence(ExpenseSummaryItem)
}

Account "1" -- "0..*" Transaction : contains
ExpensesController ..> JwtAuthGuard : protected by
ExpensesController ..> ExpensesService
ExpensesController ..> ExpenseSummaryResponseDto : returns { data }
ExpensesService ..> Account : finds owned accounts
ExpensesService ..> Transaction : aggregates
ExpenseSummaryResponseDto --> ExpenseSummaryItem

note right of ExpensesService
  Uses the server's current calendar year.
  Returns only months having qualifying rows;
  a missing month is not returned by the API.
end note

@enduml
~~~

## Business Rules

~~~text
BR-EXP-01: Authenticated ownership scope

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

pre BR_EXP_01_AuthenticatedIdentity:
  not userId.oclIsUndefined()

post BR_EXP_01_OwnedAccountsOnly:
  let ownedAccountIds : Set(Integer) =
    Account.allInstances()
      ->select(a | a.userId = userId)
      ->collect(a | a.accountId)
      ->asSet()
  in
    result->forAll(item |
      Transaction.allInstances()->exists(t |
        ownedAccountIds->includes(t.accountId) and
        t.type = TransactionType::Expense and
        yearOf(t.transactionDate) = currentYear() and
        monthOf(t.transactionDate) = monthNumber(item.month)
      )
    )

Technical constraints:
- JwtAuthGuard must validate a Bearer JWT before the controller reads request.user.userId.
- Only Accounts whose userId equals the authenticated userId are in scope; another user's transactions must never contribute.

BR-EXP-02: Current-year Expense inclusion and amount calculation

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_02_ExpenseSum:
  let ownedAccountIds : Set(Integer) =
    Account.allInstances()
      ->select(a | a.userId = userId)
      ->collect(a | a.accountId)
      ->asSet()
  in
    result->forAll(item |
      item.totalExpense =
        Transaction.allInstances()
          ->select(t |
            ownedAccountIds->includes(t.accountId) and
            t.type = TransactionType::Expense and
            yearOf(t.transactionDate) = currentYear() and
            monthOf(t.transactionDate) = monthNumber(item.month)
          )
          ->collect(t | t.amount)
          ->sum()
    )

Technical constraints:
- currentYear() is calculated by the backend from new Date().getFullYear().
- The SQL boundary is inclusive: 1 January 00:00:00 through 31 December 23:59:59 of that server-side year.
- No predicate is applied to Transactions.status; every matching Expense transaction is included regardless of Complete, Pending, or Failed status.

BR-EXP-03: Sparse monthly aggregation and ordering

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_03_MonthlyAggregation:
  result->isUnique(item | item.month) and
  result->forAll(item |
    monthNumber(item.month) >= 1 and
    monthNumber(item.month) <= 12
  ) and
  result->forAll(first |
    result->forAll(second |
      result->indexOf(first) < result->indexOf(second)
        implies monthNumber(first.month) < monthNumber(second.month)
    )
  )

Technical constraints:
- The database groups by MONTH(transaction_date) and orders ascending.
- month is mapped to Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, or Dec.
- totalExpense is SUM(amount), converted to a JavaScript number.
- The API returns only months with at least one qualifying row; it does not create zero-value items.

BR-EXP-04: Client-side full-year display

context ExpenseSummaryChart::renderChart(
  summaryData : Sequence(ExpenseSummaryItem)
) : Sequence(ExpenseSummaryItem)

pre BR_EXP_04_HasSummaryData:
  summaryData->notEmpty()

post BR_EXP_04_CompleteYearDisplay:
  result->size() = 12 and
  result->isUnique(item | item.month) and
  result->forAll(item |
    monthNumber(item.month) >= 1 and
    monthNumber(item.month) <= 12
  ) and
  result->forAll(item |
    summaryData->exists(source |
      source.month = item.month and
      source.totalExpense = item.totalExpense
    ) or
    (summaryData->forAll(source | source.month <> item.month) and
      item.totalExpense = 0)
  )

BR-EXP-05: Empty result and no-data UI

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_05_EmptyWhenNoQualifyingData:
  let ownedAccountIds : Set(Integer) =
    Account.allInstances()
      ->select(a | a.userId = userId)
      ->collect(a | a.accountId)
      ->asSet()
  in
    (ownedAccountIds->isEmpty() or
      Transaction.allInstances()->forAll(t |
        not (ownedAccountIds->includes(t.accountId) and
             t.type = TransactionType::Expense and
             yearOf(t.transactionDate) = currentYear())
      ))
    implies result->isEmpty()

Technical constraints:
- When summaryData is empty, ExpenseSummaryChart displays its no-expense-data message and does not render the twelve-bar chart.

BR-EXP-06: Read-only operation and response envelope

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_06_NoPersistentChanges:
  Account.allInstances() = Account.allInstances()@pre and
  Transaction.allInstances() = Transaction.allInstances()@pre

Technical constraints:
- GET /api/v1/expenses/summary performs no create, update, or delete operation.
- On HTTP 200, ExpensesController returns exactly { data: summary }; this endpoint does not return success or message fields.
~~~

