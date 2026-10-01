import axiosInstance from './axiosInstance'
import { ApiResponse, Account } from './types'

export const accountService = {
  // Get the user's accounts
  getAccounts: async (): Promise<ApiResponse<Account[]>> => {
    const response = await axiosInstance.get('/accounts')
    return response.data
  },

  // Get details of an account
  getAccount: async (accountId: number): Promise<ApiResponse<Account>> => {
    const response = await axiosInstance.get(`/accounts/${accountId}`)
    return response.data
  },

  // Create a new account
  createAccount: async (data: Omit<Account, 'account_id'>): Promise<ApiResponse<Account>> => {
    const response = await axiosInstance.post('/accounts', data)
    return response.data
  },

  // Update an account
  updateAccount: async (accountId: number, data: Partial<Account>): Promise<ApiResponse<Account>> => {
    const response = await axiosInstance.put(`/accounts/${accountId}`, data)
    return response.data
  },

  // Delete an account
  deleteAccount: async (accountId: number): Promise<ApiResponse<void>> => {
    const response = await axiosInstance.delete(`/accounts/${accountId}`)
    return response.data
  },
}

