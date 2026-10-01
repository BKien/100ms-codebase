---
artifact_type: ocl-utility-definitions
status: Frozen
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A2:B2"
retrieved_at: 2026-08-27T03:49:28.570Z
---

# OCL Utility Definitions

> Exact projection of the utility definitions supplied by the canonical spreadsheet. Do not invent utility semantics during prompt generation.

~~~text
Utility Function Definitions (for Business Rules):

StringNormalizer.trim(s):
- Removes leading and trailing whitespace characters from s.
- Internal whitespace characters remain unchanged.

StringNormalizer.nfc(s):
- Returns the Unicode NFC-normalized representation of s.
- Used to normalize user-provided text before validation and persistence.

StringNormalizer.lower(s):
- Returns the lowercase representation of s.
- Used for case-insensitive comparison, especially email normalization.


StringValidator.matches(s, pattern):
- Returns true if s fully matches the specified regular expression pattern.
- Partial matching is not allowed.


EmailValidator.isEmail(email):
- Returns true if the input value follows a valid email format.
- Used to validate email fields before processing.


PasswordHasher.matches(password, hash):
- Returns true if the provided plaintext password matches the stored password hash.
- Plaintext password shall never be stored or returned.

PasswordHasher.cost(hash):
- Returns the cost factor used to generate the password hash.
- Used to validate password hashing configuration.


DateUtility.toIsoDate(date):
- Converts a date value into ISO date string format (YYYY-MM-DD).
- Used for date comparison and API response formatting.

' =========================
' Utility Classes
' =========================

class StringNormalizer <<Utility>> {
  +trim(s: String): String
  +nfc(s: String): String
  +lower(s: String): String
}


class StringValidator <<Utility>> {
  +matches(s: String, pattern: String): Boolean
}


class EmailValidator <<Utility>> {
  +isEmail(email: String): Boolean
}


class DateUtility <<Utility>> {
  +toIsoDate(date: Date): String
  +isWithinInclusiveMonth(
      date: Date,
      month: String
  ): Boolean
}


class PasswordHasher <<Service>> {
  +hash(
      password: String,
      rounds: Integer
  ): String

  +matches(
      password: String,
      hash: String
  ): Boolean

  +cost(
      hash: String
  ): Integer
}

DateUtility.isWithinInclusiveMonth(date, month):
- Returns true if the date belongs to the specified month.
- The target month follows the YYYY-MM format.
~~~

