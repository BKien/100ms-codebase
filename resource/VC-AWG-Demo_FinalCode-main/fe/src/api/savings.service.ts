import axiosInstance from './axiosInstance'
import type { SavingsSummaryResponse } from './types'

export const savingsService = {
  /**
   * Get the monthly savings summary for the specified year
   * @param year - Year to retrieve data for (defaults to the current year)
   */
  getSavingsSummary: async (year?: number): Promise<SavingsSummaryResponse> => {
    const params = year ? { year } : {}
    const response = await axiosInstance.get<SavingsSummaryResponse>('/v1/savings/summary', {
      params,
    })
    return response.data
  },
}

