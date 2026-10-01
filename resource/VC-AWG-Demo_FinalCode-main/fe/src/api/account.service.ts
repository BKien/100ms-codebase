import axiosInstance from './axiosInstance'
import { ApiResponse, Account, AccountDetail } from './types'

export const accountService = {
  // Get the user's accounts
  getAccounts: async (): Promise<ApiResponse<any>> => {
    const response = await axiosInstance.get('/v1/accounts')
    return response.data
  },

  // Get details of an account with recent transactions
  getAccountDetail: async (accountId: number): Promise<AccountDetail> => {
    const response = await axiosInstance.get(`/v1/accounts/${accountId}`)
    return response.data
  },

  // Create a new account
  createAccount: async (data: {
    bank_name: string
    account_type: 'Checking' | 'Credit Card' | 'Savings' | 'Investment' | 'Loan'
    branch_name?: string
    account_number_full: string
    balance: number
  }): Promise<{ message: string; account: Account }> => {
    const response = await axiosInstance.post('/v1/accounts', data)
    return response.data
  },

  // Update an account
  updateAccount: async (
    accountId: number,
    data: {
      bank_name: string
      account_type: 'Checking' | 'Credit Card' | 'Savings' | 'Investment' | 'Loan'
      branch_name?: string
      account_number_full: string
      account_number_last_4?: string
      balance: number
    },
  ): Promise<{ message: string; account: any }> => {
    const response = await axiosInstance.put(`/v1/accounts/${accountId}`, data)
    return response.data
  },

  // Delete an account
  deleteAccount: async (accountId: number): Promise<ApiResponse<void>> => {
    const response = await axiosInstance.delete(`/v1/accounts/${accountId}`)
    return response.data
  },
}

