import axiosInstance from './axiosInstance'
import { ApiResponse, Category } from './types'

export const categoryService = {
  // Get a list of all categories
  getCategories: async (): Promise<ApiResponse<Category[]>> => {
    const response = await axiosInstance.get('/categories')
    return response.data
  },

  // Get details of a category
  getCategory: async (categoryId: number): Promise<ApiResponse<Category>> => {
    const response = await axiosInstance.get(`/categories/${categoryId}`)
    return response.data
  },
}

