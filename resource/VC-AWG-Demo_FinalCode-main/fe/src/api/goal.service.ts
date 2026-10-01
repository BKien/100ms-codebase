import axiosInstance from './axiosInstance'
import { ApiResponse, Goal, GoalsResponse } from './types'

export const goalService = {
  // Get the user's goals
  getGoals: async (): Promise<ApiResponse<GoalsResponse>> => {
    const response = await axiosInstance.get('/v1/goals')
    return response.data
  },

  // Get details of a goal
  getGoal: async (goalId: number): Promise<ApiResponse<Goal>> => {
    const response = await axiosInstance.get(`/goals/${goalId}`)
    return response.data
  },

  // Create a new goal
  createGoal: async (data: {
    goal_type: 'Saving' | 'Expense_Limit'
    category_id?: number | null
    start_date: string
    end_date: string
    target_amount: number
  }): Promise<{ message: string; goal_id: number }> => {
    const response = await axiosInstance.post('/v1/goals', data)
    return response.data
  },

  // Update a goal
  updateGoal: async (
    goalId: number,
    data: { target_amount: number },
  ): Promise<{ message: string; updated_goal: { goal_id: number; target_amount: number } }> => {
    const response = await axiosInstance.put(`/v1/goals/${goalId}`, data)
    return response.data
  },

  // Delete a goal
  deleteGoal: async (goalId: number): Promise<ApiResponse<void>> => {
    const response = await axiosInstance.delete(`/goals/${goalId}`)
    return response.data
  },
}

