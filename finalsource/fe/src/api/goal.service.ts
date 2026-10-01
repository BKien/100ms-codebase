import axiosInstance from './axiosInstance'
import { ApiResponse, Goal } from './types'

export const goalService = {
  // Get the user's goals
  getGoals: async (): Promise<ApiResponse<Goal[]>> => {
    const response = await axiosInstance.get('/goals')
    return response.data
  },

  // Get details of a goal
  getGoal: async (goalId: number): Promise<ApiResponse<Goal>> => {
    const response = await axiosInstance.get(`/goals/${goalId}`)
    return response.data
  },

  // Create a new goal
  createGoal: async (data: Omit<Goal, 'goal_id' | 'last_updated'>): Promise<ApiResponse<Goal>> => {
    const response = await axiosInstance.post('/goals', data)
    return response.data
  },

  // Update a goal
  updateGoal: async (goalId: number, data: Partial<Goal>): Promise<ApiResponse<Goal>> => {
    const response = await axiosInstance.put(`/goals/${goalId}`, data)
    return response.data
  },

  // Delete a goal
  deleteGoal: async (goalId: number): Promise<ApiResponse<void>> => {
    const response = await axiosInstance.delete(`/goals/${goalId}`)
    return response.data
  },
}

