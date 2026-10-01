---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-11
uc_name: "View Expenses by Category"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A238:B256"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-11: View Expenses by Category

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-11

### Use Case Name

View Expenses by Category

### Description

As an authenticated user, I want to view one month's Expense transactions grouped by category and compared with the previous month.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user opens the Expenses page or changes the month input.

### Pre-Condition(s)

PRE-1: The user is authenticated.
PRE-2: selectedMonth is initialized to the current month in YYYY-MM form.

### Post-Condition(s)

POST-1: The page displays category totals, changePercent, and underlying transactions for the selected month.
POST-2: Category groups are sorted by total descending.
POST-3: If no data exists, the frontend displays its no-data message.

### Basic Flow

1. The user opens /expenses.
2. ExpensesPage initializes selectedMonth to the current YYYY-MM value.
3. ExpensesBreakdown sends GET /api/v1/expenses/breakdown?month=selectedMonth.
4. The controller requires month to match four digits, a hyphen, and two digits.
5. ExpensesService loads account IDs owned by the user and parses year and month number.
6. The service queries current-month and previous-month Expense transactions for those accounts.
7. Current-month rows are grouped by categoryId; previous-month totals are grouped by the same key.
8. The service labels categoryId 0 as Uncategorized, unresolved category IDs as Unknown, calculates changePercent, rounds totals and percentages to two decimals, and sorts category groups by total descending.
9. The frontend displays each category, total, change percentage, and subcategory transaction rows.

### Alternative Flow

AF-1: Select another month
2a. The user changes the HTML month input.
3a. The component requests the new selectedMonth.

AF-2: Uncategorized transaction
8a. A transaction with null categoryId is returned under Uncategorized.

AF-3: Previous category total equals zero
8a. changePercent is 100 when the current total is positive; otherwise it is null.

### Exception Flow

EF-1: Invalid month syntax
4a. The controller returns HTTP 400.

EF-2: No accounts, invalid month number, or no current-month expense rows
5a. The service returns HTTP 404 with its no-data error.

EF-3: Retrieval failure
6a. The backend returns HTTP 500 and the frontend displays its error state.

### Related UI

ExpensesPage; ExpensesBreakdown; month input; route /expenses

### Related API IDs

API-EXPENSE-BREAKDOWN

### Notes

Not specified

## UML Model

~~~plantuml
@startuml

class AuthenticatedRequest <<DTO>> {
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
  itemDescription: String [1]
  amount: Decimal [1]
  status: TransactionStatus [1]
  categoryId: Integer [0..1]
}

class Category <<Entity>> {
  categoryId: Integer [1]
  categoryName: String [1]
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

class ExpenseSubCategory <<DTO>> {
  item_description: String [1]
  amount: Number [1]
  date: String [1]
}

class BreakdownResult <<DTO>> {
  category: String [1]
  total: Number [1]
  changePercent: Number [0..1]
  subCategories: ExpenseSubCategory [1..*] {ordered}
}

class ExpenseBreakdownResponse <<DTO>> {
  data: BreakdownResult [1..*] {ordered}
}

class JwtAuthGuard <<Guard>> {
  validate(token: BearerJWT): AuthenticatedRequest
}

class ExpensesController <<Controller>> {
  getExpensesBreakdown(request: AuthenticatedRequest, month: String): ExpenseBreakdownResponse
}

class ExpensesService <<Service>> {
  getExpensesBreakdown(userId: Integer, month: String): Sequence(BreakdownResult)
}

class ExpensesPage <<UI>> {
  selectedMonth: String [1]
}

class ExpensesBreakdown <<UI>> {
  month: String [1]
  expensesData: BreakdownResult [*]
  fetchExpensesBreakdown(month: String)
}

Account "1" -- "0..*" Transaction : owns transactions
Category "0..1" -- "0..*" Transaction : classifies
ExpensesController ..> JwtAuthGuard : protected by
ExpensesController ..> ExpensesService
ExpensesController ..> ExpenseBreakdownResponse : returns { data }
ExpensesService ..> Account : resolves owned accountIds
ExpensesService ..> Transaction : loads current/previous Expense rows
ExpensesService ..> Category : resolves categoryName
ExpenseBreakdownResponse --> BreakdownResult
BreakdownResult --> ExpenseSubCategory
ExpensesPage --> ExpensesBreakdown : passes selectedMonth
ExpensesBreakdown ..> ExpenseBreakdownResponse : GET /api/v1/expenses/breakdown

note right of ExpensesService
  Current-month and previous-month queries use inclusive
  calendar-month boundaries. January compares with December
  of the preceding year. Groups are sorted by total descending.
end note

note right of ExpensesBreakdown
  Figma 109. Expenses shows category cards with total,
  comparison to last month, and transaction description,
  amount, and date rows.
end note

@enduml
~~~

## Business Rules

~~~text
BR-EXP-07: Authenticated ownership scope

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

pre BR_EXP_07_AuthenticatedIdentity:
  not userId.oclIsUndefined()

post BR_EXP_07_OwnedAccountsOnly:
  result->forAll(item |
    item.subCategories->forAll(detail |
      Transaction.allInstances()->exists(t |
        Account.allInstances()->exists(a |
          a.accountId = t.accountId and
          a.userId = userId
        ) and
        t.type = TransactionType::Expense and
        t.itemDescription = detail.item_description and
        t.amount = detail.amount and
        toIsoDate(t.transactionDate) = detail.date
      )
    )
  )

Technical constraints:
- JwtAuthGuard shall validate a Bearer JWT before the controller reads request.user.userId.
- Transactions owned by another user shall never contribute to the breakdown.

BR-EXP-08: Breakdown month syntax

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

pre BR_EXP_08_Defined:
  not month.oclIsUndefined()

pre BR_EXP_08_ValidSyntax:
  matches(month, '^\d{4}-\d{2}$')

Technical constraint:
- A missing month or a value that does not match YYYY-MM shall be rejected by ExpensesController with HTTP 400.

BR-EXP-09: Valid breakdown calendar month

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

pre BR_EXP_09_ValidMonthNumber:
  let monthNum : Integer = month.substring(6, 7).toInteger()
  in
    monthNum >= 1 and monthNum <= 12

Technical constraint:
- A syntactically valid value whose MM portion is outside 01..12 shall produce the service's HTTP 404 no-data response.

BR-EXP-10: Eligible current-month expenses and no-data handling

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

post BR_EXP_10_CurrentMonthExpenseOnly:
  result->forAll(item |
    item.subCategories->forAll(detail |
      Transaction.allInstances()->exists(t |
        Account.allInstances()->exists(a |
          a.accountId = t.accountId and a.userId = userId
        ) and
        t.type = TransactionType::Expense and
        isWithinInclusiveMonth(t.transactionDate, month) and
        t.itemDescription = detail.item_description and
        t.amount = detail.amount and
        toIsoDate(t.transactionDate) = detail.date
      )
    )
  )

Technical constraints:
- The service shall return HTTP 404 when the user owns no Accounts or when no eligible current-month Expense transactions exist.
- No Transactions.status predicate is applied; Complete, Pending, and Failed rows are eligible when the other predicates match.

BR-EXP-11: Category grouping, totals, and detail mapping

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

post BR_EXP_11_OneGroupPerCategory:
  result->isUnique(item | item.category)

post BR_EXP_11_CategoryTotal:
  result->forAll(item |
    item.total =
      item.subCategories
        ->collect(detail | detail.amount)
        ->sum()
  )

post BR_EXP_11_DetailMapping:
  result->forAll(item |
    item.subCategories->forAll(detail |
      not detail.item_description.oclIsUndefined() and
      not detail.amount.oclIsUndefined() and
      not detail.date.oclIsUndefined()
    )
  )

Technical constraints:
- Current-month rows shall be grouped by categoryId; null categoryId is normalized to key 0.
- Key 0 shall be labeled Uncategorized. An unresolved non-null categoryId shall be labeled Unknown.
- Each detail shall map Transaction.itemDescription to item_description, Number(Transaction.amount) to amount, and transactionDate to an ISO YYYY-MM-DD date string.

BR-EXP-12: Previous-month comparison

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

post BR_EXP_12_ChangePercent:
  result->forAll(item |
    let previousTotal : Decimal =
      previousMonthExpenseTotal(userId, month, item.category)
    in
      if previousTotal = 0 then
        if item.total > 0 then
          item.changePercent = 100
        else
          item.changePercent.oclIsUndefined()
        endif
      else
        item.changePercent =
          ((item.total - previousTotal) / previousTotal) * 100
      endif
  )

Technical constraints:
- The comparison period is the immediately preceding calendar month.
- For January, the previous period is December of the preceding year.
- Previous-month rows use the same ownership, Expense type, inclusive date-boundary, and normalized category-key rules as current-month rows.

BR-EXP-13: Rounding and deterministic ordering

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

post BR_EXP_13_RoundedValues:
  result->forAll(item |
    item.total = round2(item.total) and
    (item.changePercent.oclIsUndefined() or
     item.changePercent = round2(item.changePercent))
  )

post BR_EXP_13_GroupsSortedDescending:
  Sequence{1..result->size()}->forAll(i |
    i < result->size() implies
      result->at(i).total >= result->at(i + 1).total
  )

post BR_EXP_13_DetailsSortedAscending:
  result->forAll(item |
    Sequence{1..item.subCategories->size()}->forAll(i |
      i < item.subCategories->size() implies
        item.subCategories->at(i).date <=
        item.subCategories->at(i + 1).date
    )
  )

BR-EXP-14: Selected-month UI and Figma breakdown mapping

Technical constraints:
- ExpensesPage shall initialize selectedMonth to the client's current YYYY-MM value.
- Changing the month input shall cause ExpensesBreakdown to request GET /api/v1/expenses/breakdown with query.month equal to selectedMonth.
- Each returned BreakdownResult shall be rendered as a breakdown card containing category, total, changePercent compared with the previous month, and its transaction description, amount, and date rows, consistent with Figma frame 109. Expenses.
- A null changePercent shall display as N/A. Loading, no-data, and error states shall replace the card grid when applicable.

BR-EXP-15: Read-only operation and response envelope

context ExpensesService::getExpensesBreakdown(
  userId : Integer,
  month : String
) : Sequence(BreakdownResult)

post BR_EXP_15_AccountIdentityUnchanged:
  Account.allInstances()->collect(a | a.accountId)->asSet() =
  Account.allInstances()@pre->collect(a | a.accountId)->asSet()

post BR_EXP_15_TransactionIdentityUnchanged:
  Transaction.allInstances()->collect(t | t.transactionId)->asSet() =
  Transaction.allInstances()@pre->collect(t | t.transactionId)->asSet()

Technical constraints:
- The operation shall not create, update, or delete Accounts, Transactions, or Categories.
- On HTTP 200, ExpensesController shall return exactly { data: BreakdownResult[] }; it shall not add success or message fields.
~~~

