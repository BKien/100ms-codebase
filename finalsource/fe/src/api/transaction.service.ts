import axiosInstance from './axiosInstance'
import { ApiResponse, Transaction } from './types'

export const transactionService = {
  // Get the transaction list
  getTransactions: async (params?: {
    accountId?: number
    categoryId?: number
    type?: 'Revenue' | 'Expense'
    startDate?: string
    endDate?: string
  }): Promise<ApiResponse<Transaction[]>> => {
    const response = await axiosInstance.get('/transactions', { params })
    return response.data
  },

  // Get details of a transaction
  getTransaction: async (transactionId: number): Promise<ApiResponse<Transaction>> => {
    const response = await axiosInstance.get(`/transactions/${transactionId}`)
    return response.data
  },

  // Create a new transaction
  createTransaction: async (data: Omit<Transaction, 'transaction_id'>): Promise<ApiResponse<Transaction>> => {
    const response = await axiosInstance.post('/transactions', data)
    return response.data
  },

  // Update a transaction
  updateTransaction: async (transactionId: number, data: Partial<Transaction>): Promise<ApiResponse<Transaction>> => {
    const response = await axiosInstance.put(`/transactions/${transactionId}`, data)
    return response.data
  },

  // Delete a transaction
  deleteTransaction: async (transactionId: number): Promise<ApiResponse<void>> => {
    const response = await axiosInstance.delete(`/transactions/${transactionId}`)
    return response.data
  },
}

