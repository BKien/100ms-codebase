
---

# 📘 **Database – `financial1`**

## **Entities & Relationships (Concise Definition)**

```
Users {
    user_id PK
    full_name
    email UNIQUE
    username UNIQUE
    password
    phone_number
    profile_picture_url
    total_balance
}

Accounts {
    account_id PK
    user_id FK -> Users.user_id
    bank_name
    account_type ENUM('Checking','Credit Card','Savings','Investment','Loan')
    branch_name
    account_number_full
    account_number_last_4
    balance
}

Categories {
    category_id PK
    category_name UNIQUE
}

Transactions {
    transaction_id PK
    account_id FK -> Accounts.account_id
    transaction_date
    type ENUM('Revenue','Expense')
    item_description
    shop_name
    amount
    payment_method
    status ENUM('Complete','Pending','Failed')
    receipt_id
    category_id FK (nullable) -> Categories.category_id
}

Bills {
    bill_id PK
    user_id FK -> Users.user_id
    due_date
    logo_url
    item_description
    last_charge_date
    amount
}

Goals {
    goal_id PK
    user_id FK -> Users.user_id
    goal_type ENUM('Saving','Expense_Limit')
    category_id FK -> Categories.category_id
    start_date
    end_date
    target_amount
    last_updated
}
```

---

## **Relationships Overview**

```
Users 1—N Accounts
Users 1—N Bills
Users 1—N Goals

Accounts 1—N Transactions

Categories 1—N Transactions (optional)
Categories 1—N Goals
```

---

## **ERD Compact**

```
Users 
 ├── Accounts ─── Transactions
 ├── Bills
 └── Goals ─── Categories
Transactions ─── Categories (nullable)
```

---

## **Usage Notes for Code Generators**

* All PK fields are `INT AUTO_INCREMENT`.
* All FK constraints follow the `table.field -> table.field` mapping above.
* `Transactions.category_id` is **nullable**.
* ENUM fields should map to string-based enums in code (TypeScript, Java, etc.).
* No cascade rules specified → default behavior used.

---

