---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-16
uc_name: "View Savings Summary"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A332:B351"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-16: View Savings Summary

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-16

### Use Case Name

View Savings Summary

### Description

As an authenticated user, I want to compare monthly net savings for a selected year with the previous year.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user opens the Goals page or changes the year selector in Saving Summary.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: The frontend initializes selectedYear to the current year.

### Post-Condition(s)

POST-1: The API returns exactly 12 monthly rows for the selected year and 12 for the preceding year.
POST-2: Each amount equals monthly Revenue minus monthly Expense across the user's accounts.
POST-3: The frontend displays a two-line chart when either yearly series contains a non-zero value.

### Basic Flow

1. GoalsPage renders SavingsSummaryChart.
2. The component initializes selectedYear to the current year and sends GET /api/v1/savings/summary?year=selectedYear.
3. The controller parses year with parseInt; missing, NaN, less than 1900, or greater than 2100 resolves to the current year.
4. SavingsService loads account IDs owned by userId.
5. For each month 01-12 in the selected year, the service sums Revenue, sums Expense, and calculates amount = Revenue - Expense.
6. The service repeats the calculation for selectedYear - 1.
7. Monthly amounts are rounded to two decimals and returned in ordered 12-row arrays.
8. The frontend maps month numbers to Jan-Dec and displays this year and last year as two lines.

### Alternative Flow

AF-1: Select another year
2a. The user selects one of the current year and previous ten years.
2b. The component requests the selected year again.

AF-2: No owned accounts
4a. The service returns zero-valued 12-month arrays for both years.

AF-3: Both returned series contain only zero
8a. The frontend displays its no-transaction-data message instead of the chart.

### Exception Flow

EF-1: Unauthorized request
2a. HTTP 401 is handled by the Axios interceptor.

EF-2: Calculation failure
5a. The backend returns HTTP 500 and the chart displays its general load error.

### Related UI

GoalsPage; SavingsSummaryChart; year selector

### Related API IDs

API-SAVINGS-SUMMARY

### Notes

Parsing clarification: The year is resolved from its leading base-10 numeric prefix; for example, “2025abc” resolves to 2025. The current year is used only when the resolved value is missing, non-numeric, below 1900, or above 2100.

## UML Model

~~~plantuml
@startuml

enum TransactionType {
  REVENUE
  EXPENSE
}

enum SavingsSeries {
  THIS_YEAR
  LAST_YEAR
}

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class User <<Entity>> {
  userId: Integer [1]
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
}

class SavingsSummaryQueryDto <<DTO>> {
  year: String [0..1]
}

class MonthlySavingsDto <<DTO>> {
  month: String [1]
  amount: Decimal [1]
}

class SavingsSummaryDataDto <<DTO>> {
  this_year: MonthlySavingsDto [12]
  last_year: MonthlySavingsDto [12]
}

class SavingsSummaryResponseDto <<DTO>> {
  user_id: Integer [1]
  year: Integer [1]
  summary: SavingsSummaryDataDto [1]
}

class SavingsController <<Controller>> {
  getSavingsSummary(
    request: AuthenticatedRequest,
    year: String
  ): SavingsSummaryResponseDto

  resolveYear(year: String): Integer
}

class SavingsService <<Service>> {
  getSavingsSummary(
    userId: Integer,
    year: Integer
  ): SavingsSummaryResponseDto

  calculateMonthlySavings(
    userId: Integer,
    year: Integer
  ): MonthlySavingsDto [12]
}

class SavingsTooltip <<UIModel>> {
  visible: Boolean [1]
  month: String [0..1]
  amount: Decimal [0..1]
}

class SavingsSummaryChart <<UIComponent>> {
  isChartVisible: Boolean [1]
  hoverPoint(
    series: SavingsSeries,
    month: String
  ): SavingsTooltip
  leavePoint(): void
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains

SavingsSummaryChart ..> SavingsSummaryResponseDto
SavingsSummaryChart ..> SavingsTooltip
SavingsSummaryChart ..> SavingsSeries

SavingsController ..> AuthenticatedRequest
SavingsController ..> SavingsSummaryQueryDto
SavingsController ..> SavingsService
SavingsController ..> SavingsSummaryResponseDto

SavingsService ..> Account
SavingsService ..> Transaction
SavingsService ..> SavingsSummaryResponseDto

SavingsSummaryResponseDto --> SavingsSummaryDataDto
SavingsSummaryDataDto --> MonthlySavingsDto

@enduml
~~~

## Business Rules

~~~text
BR-SAV-01: Authenticated user data scope

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_01_UserIdentity:
  result.user_id = userId

post BR_SAV_01_OwnedAccountsOnly:
  Transaction.allInstances()
    ->select(t |
      Account.allInstances()->exists(a |
        a.accountId = t.accountId and
        a.userId = userId
      )
    )
    ->includesAll(
      Transaction.allInstances()
        ->select(t |
          Account.allInstances()->exists(a |
            a.accountId = t.accountId and
            a.userId = userId
          )
        )
    )

Technical constraints:
- userId shall be obtained from the validated JWT.
- Transactions from accounts owned by other users shall not contribute to the savings summary.


BR-SAV-02: Savings summary year resolution

context SavingsController::getSavingsSummary(
  request : AuthenticatedRequest,
  year : String
) : SavingsSummaryResponseDto

post BR_SAV_02_ValidYearUsed:
  let parsedYear : Integer = parseInt(year, 10)
  in
    (
      not isNaN(parsedYear) and
      parsedYear >= 1900 and
      parsedYear <= 2100
    )
    implies
      result.year = parsedYear

post BR_SAV_02_InvalidYearDefaultsToCurrentYear:
  let parsedYear : Integer = parseInt(year, 10)
  in
    (
      year.oclIsUndefined() or
      isNaN(parsedYear) or
      parsedYear < 1900 or
      parsedYear > 2100
    )
    implies
      result.year = currentYear()

Technical constraint:
- The implementation uses JavaScript parseInt(year, 10).
- Therefore, a value such as "2025abc" resolves to 2025 rather than defaulting to the current year.

BR-SAV-03: Complete monthly summary

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_03_TwelveMonthsThisYear:
  result.summary.this_year->size() = 12

post BR_SAV_03_TwelveMonthsLastYear:
  result.summary.last_year->size() = 12

post BR_SAV_03_ThisYearMonthOrder:
  Sequence{1..12}->forAll(i |
    result.summary.this_year->at(i).month =
      padTwoDigits(i)
  )

post BR_SAV_03_LastYearMonthOrder:
  Sequence{1..12}->forAll(i |
    result.summary.last_year->at(i).month =
      padTwoDigits(i)
  )

Technical constraint:
- Month values shall be returned as two-digit strings from "01" through "12" in ascending order.


BR-SAV-04: Monthly net savings calculation

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_04_ThisYearAmounts:
  result.summary.this_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let monthlyTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          yearOf(t.transactionDate) = year and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
    let revenue : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::REVENUE
        )
        ->collect(t | t.amount)
        ->sum()
    in
    let expense : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::EXPENSE
        )
        ->collect(t | t.amount)
        ->sum()
    in
      dto.amount = roundToTwoDecimals(
        revenue - expense
      )
  )

Technical constraint:
- Monthly savings equals total Revenue minus total Expense across all accounts owned by the authenticated user.

BR-SAV-05: Previous-year comparison

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_05_LastYearAmounts:
  result.summary.last_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let monthlyTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          yearOf(t.transactionDate) = year - 1 and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
    let revenue : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::REVENUE
        )
        ->collect(t | t.amount)
        ->sum()
    in
    let expense : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::EXPENSE
        )
        ->collect(t | t.amount)
        ->sum()
    in
      dto.amount = roundToTwoDecimals(
        revenue - expense
      )
  )

Technical constraint:
- this_year represents the resolved target year.
- last_year represents exactly resolvedYear - 1.


BR-SAV-06: Missing transaction data

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_06_ZeroForMissingThisYearData:
  result.summary.this_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let matchingTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          Account.allInstances()->exists(a |
            a.accountId = t.accountId and
            a.userId = userId
          ) and
          yearOf(t.transactionDate) = year and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
      matchingTransactions->isEmpty()
      implies
        dto.amount = 0
  )

post BR_SAV_06_ZeroForMissingLastYearData:
  result.summary.last_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let matchingTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          Account.allInstances()->exists(a |
            a.accountId = t.accountId and
            a.userId = userId
          ) and
          yearOf(t.transactionDate) = year - 1 and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
      matchingTransactions->isEmpty()
      implies
        dto.amount = 0
  )

Technical constraint:
- If the user owns no accounts, both returned series shall still contain 12 entries with amount = 0.

BR-SAV-07: Savings amount rounding

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_07_ThisYearRounded:
  result.summary.this_year->forAll(dto |
    dto.amount =
      roundToTwoDecimals(dto.amount)
  )

post BR_SAV_07_LastYearRounded:
  result.summary.last_year->forAll(dto |
    dto.amount =
      roundToTwoDecimals(dto.amount)
  )

Technical constraint:
- Every calculated monthly amount shall be rounded to two decimal places before being returned.


BR-SAV-08: Response consistency and read-only behavior

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_08_ResponseConsistency:
  result.user_id = userId and
  result.year = year and
  not result.summary.oclIsUndefined() and
  result.summary.this_year->size() = 12 and
  result.summary.last_year->size() = 12

post BR_SAV_08_AccountIdentityUnchanged:
  Account.allInstances()
    ->collect(a | a.accountId)
    ->asSet()
  =
  Account.allInstances()@pre
    ->collect(a | a.accountId)
    ->asSet()

post BR_SAV_08_TransactionIdentityUnchanged:
  Transaction.allInstances()
    ->collect(t | t.transactionId)
    ->asSet()
  =
  Transaction.allInstances()@pre
    ->collect(t | t.transactionId)
    ->asSet()

Technical constraints:
- Retrieving the savings summary shall not create, update, or delete Account or Transaction records.
- If the savings calculation fails unexpectedly, the backend shall return HTTP 500 Internal Server Error.

BR-SAV-09: Savings chart point value tooltip

context SavingsSummaryChart::hoverPoint(
  series : SavingsSeries,
  month : String
) : SavingsTooltip

pre BR_SAV_09_ChartDisplayed:
  self.isChartVisible = true

pre BR_SAV_09_PointExists:
  (
    series = SavingsSeries::THIS_YEAR
    implies
      self.summary.this_year->exists(p |
        p.month = month
      )
  )
  and
  (
    series = SavingsSeries::LAST_YEAR
    implies
      self.summary.last_year->exists(p |
        p.month = month
      )
  )

post BR_SAV_09_TooltipVisible:
  result.visible = true

post BR_SAV_09_CorrectThisYearValue:
  series = SavingsSeries::THIS_YEAR
  implies
    self.summary.this_year->exists(p |
      p.month = month and
      result.month = p.month and
      result.amount = p.amount
    )

post BR_SAV_09_CorrectLastYearValue:
  series = SavingsSeries::LAST_YEAR
  implies
    self.summary.last_year->exists(p |
      p.month = month and
      result.month = p.month and
      result.amount = p.amount
    )

context SavingsSummaryChart::leavePoint()

post BR_SAV_09_TooltipHidden:
  self.tooltip.visible = false

Technical constraints:
- Each rendered data point in both yearly series shall be hoverable.
- The tooltip amount shall exactly match the amount of the hovered monthly data point.
- Moving the pointer away from the data point shall hide the tooltip.
~~~

