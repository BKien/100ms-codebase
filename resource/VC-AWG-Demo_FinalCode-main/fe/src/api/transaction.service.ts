import axiosInstance from './axiosInstance'
import { Transaction } from './types'

export interface GetTransactionsParams {
  type: 'All' | 'Revenue' | 'Expense'
  limit?: number
  offset?: number
}

export interface GetTransactionsResponse {
  success: Transaction[]
  data: Transaction[]
  total: number
  hasMore: boolean
}

export interface CreateTransactionPayload {
  accountId: number
  transactionDate: string
  type: 'Revenue' | 'Expense'
  itemDescription: string
  category_id: number
  amount: number
  shopName?: string
  paymentMethod?: string
  status?: 'Complete' | 'Pending' | 'Failed'
}

export interface CreateTransactionResponse {
  message: string
  data: {
    transactionId: number
    accountId: number
    transactionDate: string
    type: 'Revenue' | 'Expense'
    itemDescription: string
    shopName: string | null
    amount: number
    paymentMethod: string | null
    status: 'Complete' | 'Pending' | 'Failed'
    receiptId: string | null
    createdAt: string
    category_id: number | null
  }
}

export const transactionService = {
  // Get the user's transaction list
  getTransactions: async (params: GetTransactionsParams): Promise<GetTransactionsResponse> => {
    const { type, limit = 10, offset = 0 } = params
    const response = await axiosInstance.get('/v1/transactions', {
      params: {
        type,
        limit,
        offset,
      },
    })
    return response.data
  },

  // Create a new transaction
  createTransaction: async (
    payload: CreateTransactionPayload,
  ): Promise<CreateTransactionResponse> => {
    const response = await axiosInstance.post('/v1/transactions', payload)
    return response.data
  },
}
