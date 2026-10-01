import axiosInstance from './axiosInstance'
import { ApiResponse, User } from './types'

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  fullName: string
  email: string
  password: string
  confirmPassword: string
}

export const authService = {
  // Log in
  login: async (data: LoginRequest): Promise<ApiResponse<{ accessToken: string; user: { id: number; fullName: string; email: string } }>> => {
    const response = await axiosInstance.post('/auth/login', data)
    return response.data
  },

  // Register
  register: async (data: RegisterRequest): Promise<{
    message: string
    user: {
      id: number
      fullName: string
      email: string
    }
    token: string
  }> => {
    const response = await axiosInstance.post('/auth/register', data)
    return response.data
  },

  // Log out
  logout: (): void => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },

  // Get current user information
  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    const response = await axiosInstance.get('/auth/me')
    return response.data
  },
}
