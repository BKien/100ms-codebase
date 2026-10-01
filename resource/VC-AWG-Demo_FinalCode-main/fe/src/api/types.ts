// Define types for API responses

export interface ApiResponse<T = any> {
  success: boolean
  message: string
  data?: T
}

export interface User {
  user_id: number
  full_name: string
  email: string
  username: string
  phone_number?: string
  profile_picture_url?: string
  total_balance: number
}

export type AccountType = 'Checking' | 'Credit Card' | 'Savings' | 'Investment' | 'Loan'

export interface Account {
  id?: number // The backend returns 'id' in getAccounts
  account_id?: number // Fallback for compatibility
  user_id: number
  bank_name: string
  account_type: AccountType
  branch_name?: string
  account_number_full?: string
  account_number_last_4?: string
  balance: number
}

export interface RecentTransaction {
  date: string
  amount: number
  description: string
  status: 'Complete' | 'Pending' | 'Failed'
  receipt_id?: string | null
  type: 'Revenue' | 'Expense'
}

export interface AccountDetail {
  id: number
  bank_name: string
  account_type: AccountType
  branch_name?: string | null
  account_number_full: string
  balance: number
  recent_transactions: RecentTransaction[]
}

export interface Category {
  category_id: number
  category_name: string
}

export interface Transaction {
  transaction_id: number
  account_id: number
  transaction_date: string
  type: 'Revenue' | 'Expense'
  item_description: string
  shop_name?: string
  amount: number
  payment_method?: string
  status: 'Complete' | 'Pending' | 'Failed'
  receipt_id?: string
  category_id?: number
}

export interface Bill {
  billId: number
  userId: number
  dueDate: string
  logoUrl?: string | null
  itemDescription: string
  lastChargeDate?: string | null
  amount: number
}

export interface Goal {
  goal_id: number
  user_id: number
  goal_type: 'Saving' | 'Expense_Limit'
  category_id: number
  start_date: string
  end_date: string
  target_amount: number
  target_achieved: boolean
  last_updated: string
}

export interface SavingGoal {
  goal_id: number
  goal_type: 'Saving'
  target_amount: number
  target_achieved: number
  start_date: string
  end_date: string
}

export interface ExpenseGoal {
  goal_id: number
  category: string
  target_amount: number
  current_expense: number
}

export interface GoalsResponse {
  savingGoal: SavingGoal | null
  expenseGoals: ExpenseGoal[]
}

export interface ExpenseSubCategory {
  item_description: string
  amount: number
  date: string
}

export interface ExpenseBreakdownItem {
  category: string
  total: number
  changePercent: number | null
  subCategories: ExpenseSubCategory[]
}

export interface ExpenseBreakdownResponse {
  data: ExpenseBreakdownItem[]
}

export interface ExpenseSummaryItem {
  month: string
  totalExpense: number
}

export interface ExpenseSummaryResponse {
  data: ExpenseSummaryItem[]
}

export interface MonthlySavings {
  month: string
  amount: number
}

export interface SavingsSummaryResponse {
  user_id: number
  year: number
  summary: {
    this_year: MonthlySavings[]
    last_year: MonthlySavings[]
  }
}

