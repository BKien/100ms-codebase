import axiosInstance from './axiosInstance'
import { ApiResponse, Bill } from './types'

export const billService = {
  // Get the user's bills
  getBills: async (): Promise<ApiResponse<Bill[]>> => {
    const response = await axiosInstance.get('/bills')
    return response.data
  },

  // Get details of a bill
  getBill: async (billId: number): Promise<ApiResponse<Bill>> => {
    const response = await axiosInstance.get(`/bills/${billId}`)
    return response.data
  },

  // Create a new bill
  createBill: async (data: Omit<Bill, 'bill_id'>): Promise<ApiResponse<Bill>> => {
    const response = await axiosInstance.post('/bills', data)
    return response.data
  },

  // Update a bill
  updateBill: async (billId: number, data: Partial<Bill>): Promise<ApiResponse<Bill>> => {
    const response = await axiosInstance.put(`/bills/${billId}`, data)
    return response.data
  },

  // Delete a bill
  deleteBill: async (billId: number): Promise<ApiResponse<void>> => {
    const response = await axiosInstance.delete(`/bills/${billId}`)
    return response.data
  },
}

