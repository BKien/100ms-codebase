import React, { useState, useEffect } from 'react'
import Button from '../Button/Button'
import Input from '../Input/Input'
import { goalService } from '../../api/goal.service'
import { categoryService } from '../../api/category.service'
import { Category } from '../../api/types'
import { useToast } from '../../hooks/useToast'
import Toast from '../Toast/Toast'

interface CreateGoalModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess?: () => void
}

const CreateGoalModal: React.FC<CreateGoalModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const { toast, showToast, hideToast } = useToast()
  const [goalType, setGoalType] = useState<'Saving' | 'Expense_Limit'>('Saving')
  const [categoryId, setCategoryId] = useState<number | null>(null)
  const [targetAmount, setTargetAmount] = useState<string>('')
  const [startDate, setStartDate] = useState<string>('')
  const [endDate, setEndDate] = useState<string>('')
  const [categories, setCategories] = useState<Category[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // Field-specific errors
  const [targetAmountError, setTargetAmountError] = useState<string | null>(null)
  const [startDateError, setStartDateError] = useState<string | null>(null)
  const [endDateError, setEndDateError] = useState<string | null>(null)
  const [categoryError, setCategoryError] = useState<string | null>(null)

  // Fetch categories when modal opens
  useEffect(() => {
    if (isOpen) {
      const fetchCategories = async () => {
        try {
          const response = await categoryService.getCategories()
          if (response.success && response.data) {
            setCategories(response.data)
          }
        } catch (err) {
          console.error('Error fetching categories:', err)
        }
      }
      fetchCategories()
    }
  }, [isOpen])

  // Reset state when modal opens/closes
  useEffect(() => {
    if (isOpen) {
      setGoalType('Saving')
      setCategoryId(null)
      setTargetAmount('')
      setStartDate('')
      setEndDate('')
      setError(null)
      setTargetAmountError(null)
      setStartDateError(null)
      setEndDateError(null)
      setCategoryError(null)
      setIsLoading(false)
    }
  }, [isOpen])

  // Client-side validation
  const validateForm = (): boolean => {
    let isValid = true

    // Clear previous errors
    setTargetAmountError(null)
    setStartDateError(null)
    setEndDateError(null)
    setCategoryError(null)

    // Validate target_amount
    const amount = parseFloat(targetAmount)
    if (!targetAmount || isNaN(amount) || amount <= 0) {
      setTargetAmountError('The target amount must be greater than 0.')
      isValid = false
    }

    // Validate start_date
    if (!startDate) {
      setStartDateError('The start date cannot be left blank.')
      isValid = false
    }

    // Validate end_date
    if (!endDate) {
      setEndDateError('The end date cannot be left blank.')
      isValid = false
    }

    // Validate end_date > start_date
    if (startDate && endDate) {
      const start = new Date(startDate)
      const end = new Date(endDate)
      if (end <= start) {
        setEndDateError('The end date must be after the start date.')
        isValid = false
      }
    }

    // Validate category_id for Expense_Limit
    if (goalType === 'Expense_Limit' && !categoryId) {
      setCategoryError('Category cannot be empty when the goal type is Expense Limit.')
      isValid = false
    }

    return isValid
  }

  // Handle form submission
  const handleSubmit = async () => {
    // Clear previous errors
    setError(null)

    // Client-side validation
    if (!validateForm()) {
      return
    }

    // Set loading state
    setIsLoading(true)

    try {
      // Prepare payload
      const payload = {
        goal_type: goalType,
        category_id: goalType === 'Expense_Limit' ? categoryId : null,
        start_date: startDate,
        end_date: endDate,
        target_amount: parseFloat(targetAmount),
      }

      // Call API
      const response = await goalService.createGoal(payload)

      // Check if response is successful
      if (response.message === 'Goal created successfully' || response.goal_id) {
        // 1. Show success toast
        showToast('Set goals for success.', 'success')

        // 2. Close modal
        onClose()

        // 3. Call onSuccess callback to refresh goals list
        if (onSuccess) {
          onSuccess()
        }
      }
    } catch (err: any) {
      // Handle API errors
      setIsLoading(false)

      if (err.response) {
        const status = err.response.status
        const errorData = err.response.data

        if (status === 400) {
          // Validation error from backend
          const errorMessage = errorData.message || 'Invalid input data.'
          setError(errorMessage)
        } else if (status === 500) {
          // Server error
          setError(
            errorData.message ||
              'Cannot create goal at this time. Please try again later.',
          )
        } else {
          // Other errors
          setError(
            errorData.message || 'Cannot create goal at this time. Please try again later.',
          )
        }
      } else {
        setError('Cannot create goal at this time. Please try again later.')
      }
    }
  }

  // Format currency for display
  const formatCurrency = (value: string): string => {
    const numValue = value.replace(/\D/g, '')
    if (!numValue) return ''
    return new Intl.NumberFormat('vi-VN').format(parseInt(numValue))
  }

  // Handle target amount input change
  const handleTargetAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/\D/g, '')
    setTargetAmount(value)
    setTargetAmountError(null)
  }

  // Don't render if modal is not open
  if (!isOpen) {
    return null
  }

  return (
    <>
      {/* Modal Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        {/* Modal Content */}
        <div
          className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Modal Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Add a new goal
            </h2>
            {/* Close Button */}
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 focus:outline-none transition-colors"
              disabled={isLoading}
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {/* Modal Body */}
          <div className="space-y-4">
            {/* Goal Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Goal Type
              </label>
              <div className="flex gap-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="goalType"
                    value="Saving"
                    checked={goalType === 'Saving'}
                    onChange={(e) => {
                      setGoalType(e.target.value as 'Saving' | 'Expense_Limit')
                      setCategoryId(null)
                      setCategoryError(null)
                    }}
                    disabled={isLoading}
                    className="mr-2"
                  />
                  <span className="text-gray-700 dark:text-gray-300">Overall savings</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="goalType"
                    value="Expense_Limit"
                    checked={goalType === 'Expense_Limit'}
                    onChange={(e) => {
                      setGoalType(e.target.value as 'Saving' | 'Expense_Limit')
                      setCategoryError(null)
                    }}
                    disabled={isLoading}
                    className="mr-2"
                  />
                  <span className="text-gray-700 dark:text-gray-300">Spending limits</span>
                </label>
              </div>
            </div>

            {/* Category Selection - Only show for Expense_Limit */}
            {goalType === 'Expense_Limit' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Category
                </label>
                <select
                  value={categoryId || ''}
                  onChange={(e) => {
                    setCategoryId(e.target.value ? parseInt(e.target.value, 10) : null)
                    setCategoryError(null)
                  }}
                  disabled={isLoading}
                  className={`
                    w-full px-4 py-2 border rounded-md
                    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                    dark:bg-gray-700 dark:border-gray-600 dark:text-white
                    ${categoryError ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
                  `}
                >
                  <option value="">Select a category</option>
                  {categories.map((category) => (
                    <option key={category.category_id} value={category.category_id}>
                      {category.category_name}
                    </option>
                  ))}
                </select>
                {categoryError && (
                  <p className="mt-1 text-sm text-red-600 dark:text-red-400">{categoryError}</p>
                )}
              </div>
            )}

            {/* Target Amount Input */}
            <Input
              label="Target amount"
              type="text"
              value={targetAmount ? formatCurrency(targetAmount) : ''}
              onChange={handleTargetAmountChange}
              error={targetAmountError || undefined}
              disabled={isLoading}
              placeholder="Enter the target amount"
            />

            {/* Start Date Input */}
            <Input
              label="Start date"
              type="date"
              value={startDate}
              onChange={(e) => {
                setStartDate(e.target.value)
                setStartDateError(null)
                setEndDateError(null) // Clear end date error when start date changes
              }}
              error={startDateError || undefined}
              disabled={isLoading}
            />

            {/* End Date Input */}
            <Input
              label="End date"
              type="date"
              value={endDate}
              onChange={(e) => {
                setEndDate(e.target.value)
                setEndDateError(null)
              }}
              error={endDateError || undefined}
              disabled={isLoading}
              min={startDate || undefined}
            />

            {/* General Error Message */}
            {error && (
              <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
                <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
              </div>
            )}
          </div>

          {/* Modal Footer */}
          <div className="flex justify-end gap-3 mt-6">
            <Button
              variant="outline"
              onClick={onClose}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={handleSubmit}
              isLoading={isLoading}
              disabled={isLoading}
            >
              Save
            </Button>
          </div>
        </div>
      </div>

      {/* Toast Notification */}
      {toast.show && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={hideToast}
        />
      )}
    </>
  )
}

export default CreateGoalModal

