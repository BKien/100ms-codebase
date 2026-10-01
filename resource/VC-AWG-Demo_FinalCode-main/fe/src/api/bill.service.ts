import axiosInstance from './axiosInstance'
import { Bill } from './types'

export interface BillsResponse {
  data: Bill[]
}

export const billService = {
  // Get the user's upcoming bills
  getUpcomingBills: async (): Promise<BillsResponse> => {
    const response = await axiosInstance.get<BillsResponse>('/v1/bills')
    return response.data
  },
}
