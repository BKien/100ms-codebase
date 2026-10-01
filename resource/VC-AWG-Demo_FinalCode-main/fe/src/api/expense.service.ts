import axiosInstance from './axiosInstance'
import type { ExpenseSummaryItem, ExpenseSummaryResponse, ExpenseBreakdownResponse } from './types'

export const expenseService = {
  /**
   * Get the monthly expense summary for the current year
   */
  getExpenseSummary: async (): Promise<ExpenseSummaryResponse> => {
    const response = await axiosInstance.get<ExpenseSummaryResponse>('/v1/expenses/summary')
    return response.data
  },

  /**
   * Get the expense breakdown by category for a specific month
   * @param month - Month string in 'YYYY-MM' format (for example: '2025-11')
   */
  getExpensesBreakdown: async (month: string): Promise<ExpenseBreakdownResponse> => {
    const response = await axiosInstance.get<ExpenseBreakdownResponse>('/v1/expenses/breakdown', {
      params: { month },
    })
    return response.data
  },
}

