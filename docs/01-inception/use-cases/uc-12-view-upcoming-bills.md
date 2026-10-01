---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-12
uc_name: "View Upcoming Bills"
source_type: google-sheets
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A257:B275"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# UC-12: View Upcoming Bills

> Canonical source: [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit?gid=0#gid=0), tab Use cases, columns A-B. This frozen repository projection is read-only; source corrections must be made in the spreadsheet and imported as a new revision.

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

View Upcoming Bills

### Description

As an authenticated user, I want to view bills due today or later.

### Actor(s)

Authenticated User

### Priority

Not Specified

### Trigger

The user opens the Bills page.

### Pre-Condition(s)

PRE-1: The user is authenticated.

### Post-Condition(s)

POST-1: The page displays bills owned by the user whose dueDate is on or after the current date at 00:00:00.
POST-2: Bills are ordered by dueDate ascending.
POST-3: If no bills exist, the page displays its empty state.

### Basic Flow

1. The user opens /bills.
2. UpcomingBills sends GET /api/v1/bills.
3. JwtAuthGuard supplies userId.
4. BillService resets the current time to 00:00:00.
5. The service queries bills where bill.userId equals userId and dueDate is greater than or equal to that date, ordered by dueDate ascending.
6. The service maps dates to YYYY-MM-DD and nullable fields to null.
7. The frontend displays each bill's description, due date, last charge date, logo when available, and amount.

### Alternative Flow

AF-1: No upcoming bills
5a. The query returns an empty array.
7a. The frontend displays its no-upcoming-bills state.

AF-2: Retry loading
7b. After an error, the user may select the retry action and the component calls the list API again.

### Exception Flow

EF-1: Retrieval failure
5a. The backend returns HTTP 500 with its bill-fetch message.
5b. The frontend displays the error state.

### Related UI

BillsPage; UpcomingBills; route /bills

### Related API IDs

API-BILL-LIST

### Notes

Scope clarification: This use case covers retrieval and display of upcoming bills only. Executing a bill payment through “Pay Now” is outside scope.

## UML Model

~~~plantuml
@startuml

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class Bill <<Entity>> {
  billId: Integer [1]
  userId: Integer [1]
  dueDate: Date [1]
  logoUrl: String [0..1]
  itemDescription: String [1]
  lastChargeDate: Date [0..1]
  amount: Decimal [1]
}

class BillDto <<DTO>> {
  billId: Integer [1]
  userId: Integer [1]
  itemDescription: String [1]
  logoUrl: String [0..1]
  dueDate: String [1]
  lastChargeDate: String [0..1]
  amount: Decimal [1]
}

class BillsResponseDto <<DTO>> {
  data: BillDto [*]
}

class BillController <<Controller>> {
  getBills(request: AuthenticatedRequest): BillsResponseDto
}

class BillService <<Service>> {
  findUpcomingBillsByUserId(userId: Integer): BillDto [*]
  currentDateAtMidnight(): Date {query}
  formatDate(date: Date): String {query}
}

BillController ..> AuthenticatedRequest
BillController ..> BillsResponseDto
BillController ..> BillService
BillService ..> Bill
BillService ..> BillDto
BillsResponseDto --> BillDto
BillDto ..> Bill : maps from

@enduml
~~~

## Business Rules

~~~text
BR-BILL-01: Bill ownership scope

context BillService::findUpcomingBillsByUserId(
  userId : Integer
) : Sequence(BillDto)

post BR_BILL_01_OwnedBillsOnly:
  result->forAll(
    dto | dto.userId = userId
  )

post BR_BILL_01_MapsToOwnedPersistedBill:
  result->forAll(
    dto |
      Bill.allInstances()->exists(
        bill |
          bill.billId = dto.billId and
          bill.userId = userId
      )
  )

BR-BILL-02: Upcoming date boundary

context BillService::findUpcomingBillsByUserId(
  userId : Integer
) : Sequence(BillDto)

post BR_BILL_02_UpcomingBillsOnly:
  result->forAll(
    dto |
      Bill.allInstances()->exists(
        bill |
          bill.billId = dto.billId and
          bill.dueDate >= self.currentDateAtMidnight()
      )
  )

post BR_BILL_02_AllEligibleBillsReturned:
  result->size() =
    Bill.allInstances()
      ->select(
        bill |
          bill.userId = userId and
          bill.dueDate >= self.currentDateAtMidnight()
      )
      ->size()

Technical constraint:
- currentDateAtMidnight() represents the current system date with hour, minute, second, and millisecond reset to zero before the repository query.

BR-BILL-03: Due-date ordering

context BillService::findUpcomingBillsByUserId(
  userId : Integer
) : Sequence(BillDto)

post BR_BILL_03_DueDateAscending:
  result->size() <= 1 or
  Sequence{1..result->size() - 1}->forAll(
    i |
      let currentBill : Bill =
        Bill.allInstances()->any(
          bill | bill.billId = result->at(i).billId
        ),
      nextBill : Bill =
        Bill.allInstances()->any(
          bill | bill.billId = result->at(i + 1).billId
        )
      in
        currentBill.dueDate <= nextBill.dueDate
  )

BR-BILL-04: Response mapping and normalization

context BillService::findUpcomingBillsByUserId(
  userId : Integer
) : Sequence(BillDto)

post BR_BILL_04_ResponseMapping:
  result->forAll(
    dto |
      Bill.allInstances()->exists(
        bill |
          bill.billId = dto.billId and
          bill.userId = dto.userId and
          bill.itemDescription = dto.itemDescription and
          bill.amount = dto.amount and
          dto.dueDate = self.formatDate(bill.dueDate) and
          (
            bill.lastChargeDate.oclIsUndefined()
            implies dto.lastChargeDate.oclIsUndefined()
          ) and
          (
            not bill.lastChargeDate.oclIsUndefined()
            implies
              dto.lastChargeDate =
                self.formatDate(bill.lastChargeDate)
          ) and
          (
            (bill.logoUrl.oclIsUndefined() or bill.logoUrl.size() = 0)
            implies dto.logoUrl.oclIsUndefined()
          ) and
          (
            (not bill.logoUrl.oclIsUndefined() and bill.logoUrl.size() > 0)
            implies dto.logoUrl = bill.logoUrl
          )
      )
  )

Technical constraints:
- formatDate shall return YYYY-MM-DD.
- amount shall be returned as a number.
- A missing lastChargeDate shall be returned as null.
- A missing or empty logoUrl shall be returned as null.

BR-BILL-05: Empty upcoming-bill result

context BillService::findUpcomingBillsByUserId(
  userId : Integer
) : Sequence(BillDto)

post BR_BILL_05_EmptyWhenNoEligibleBills:
  Bill.allInstances()
    ->select(
      bill |
        bill.userId = userId and
        bill.dueDate >= self.currentDateAtMidnight()
    )
    ->isEmpty()
  implies
    result->isEmpty()

BR-BILL-06: Read-only list operation

Listing upcoming bills shall not create, update, or delete Bill records.

BR-BILL-07: Retrieval failure handling

If the repository query or bill-response mapping fails, the backend shall reject the request with HTTP 500 Internal Server Error and the message "Failed to fetch bills".
~~~

