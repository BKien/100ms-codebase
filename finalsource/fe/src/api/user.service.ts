import axiosInstance from './axiosInstance'
import { ApiResponse, User } from './types'

export const userService = {
  // Get user information
  getUser: async (userId: number): Promise<ApiResponse<User>> => {
    const response = await axiosInstance.get(`/users/${userId}`)
    return response.data
  },

  // Update user information
  updateUser: async (userId: number, data: Partial<User>): Promise<ApiResponse<User>> => {
    const response = await axiosInstance.put(`/users/${userId}`, data)
    return response.data
  },
}

