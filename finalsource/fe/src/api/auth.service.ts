import axiosInstance from './axiosInstance'
import { ApiResponse, User } from './types'

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  full_name: string
  email: string
  username: string
  password: string
  phone_number?: string
}

export const authService = {
  // Log in
  login: async (data: LoginRequest): Promise<ApiResponse<{ user: User; token: string }>> => {
    const response = await axiosInstance.post('/auth/login', data)
    return response.data
  },

  // Register
  register: async (data: RegisterRequest): Promise<ApiResponse<User>> => {
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
