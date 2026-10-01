import React, { useState, useEffect } from 'react'
import Input from '../Input/Input'
import Button from '../Button/Button'
import Toast from '../Toast/Toast'
import { accountService } from '../../api/account.service'
import type { AccountType, AccountDetail } from '../../api/types'
import { useToast } from '../../hooks/useToast'

interface AccountEditFormProps {
  accountId: number
  accountData?: AccountDetail
  onSuccess?: (updatedAccount: any) => void
  onCancel?: () => void
}

const AccountEditForm: React.FC<AccountEditFormProps> = ({
  accountId,
  accountData: initialAccountData,
  onSuccess,
  onCancel,
}) => {
  const { toast, showToast, hideToast } = useToast()

  // Form state
  const [bankName, setBankName] = useState('')
  const [accountType, setAccountType] = useState<AccountType>('Checking')
  const [branchName, setBranchName] = useState('')
  const [accountNumberFull, setAccountNumberFull] = useState('')
  const [balance, setBalance] = useState<string>('')

  // Error state
  const [errors, setErrors] = useState<{
    bank_name?: string
    account_type?: string
    branch_name?: string
    account_number_full?: string
    balance?: string
    general?: string
  }>({})

  // Loading state
  const [isLoading, setIsLoading] = useState(false)
  const [isInitialLoading, setIsInitialLoading] = useState(!initialAccountData)

  // Load account data if not provided
  useEffect(() => {
    if (!initialAccountData && accountId) {
      const fetchAccountData = async () => {
        try {
          setIsInitialLoading(true)
          const data = await accountService.getAccountDetail(accountId)
          setBankName(data.bank_name)
          setAccountType(data.account_type)
          setBranchName(data.branch_name || '')
          setAccountNumberFull(data.account_number_full)
          setBalance(data.balance.toString())
        } catch (error: any) {
          showToast('Unable to load account information. Please try again later.', 'error')
        } finally {
          setIsInitialLoading(false)
        }
      }
      fetchAccountData()
    } else if (initialAccountData) {
      setBankName(initialAccountData.bank_name)
      setAccountType(initialAccountData.account_type)
      setBranchName(initialAccountData.branch_name || '')
      setAccountNumberFull(initialAccountData.account_number_full)
      setBalance(initialAccountData.balance.toString())
    }
  }, [accountId, initialAccountData, showToast])

  // Client-side validation
  const validateForm = (): boolean => {
    const newErrors: typeof errors = {}

    if (!bankName.trim()) {
      newErrors.bank_name = 'Bank name cannot be empty'
    }

    if (!accountType) {
      newErrors.account_type = 'Account type cannot be empty'
    }

    const balanceNum = parseFloat(balance)
    if (isNaN(balanceNum) || balanceNum < 0) {
      newErrors.balance = 'Current balance must be a valid number and cannot be negative'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Handle save changes
  const handleSaveChanges = async (e: React.FormEvent) => {
    e.preventDefault()

    // Clear previous errors
    setErrors({})

    // Client-side validation
    if (!validateForm()) {
      return
    }

    setIsLoading(true)

    try {
      // Prepare payload
      const payload = {
        bank_name: bankName.trim(),
        account_type: accountType,
        branch_name: branchName.trim() || undefined,
        account_number_full: accountNumberFull.trim(),
        account_number_last_4: accountNumberFull.trim().slice(-4),
        balance: parseFloat(balance),
      }

      const response = await accountService.updateAccount(accountId, payload)

      // Success handling
      // 1. Show toast notification
      showToast('Update successful', 'success')

      // 2. Call onSuccess callback with updated account data
      if (onSuccess && response.account) {
        setTimeout(() => {
          onSuccess(response.account)
        }, 500)
      }
    } catch (error: any) {
      setIsLoading(false)

      // Handle different error types
      if (error.response) {
        const status = error.response.status
        const errorData = error.response.data

        if (status === 400) {
          // Validation errors from backend
          const validationErrors: typeof errors = {}
          if (errorData.message) {
            if (Array.isArray(errorData.message)) {
              errorData.message.forEach((msg: string) => {
                if (msg.includes('bank_name') || msg.includes('bank')) {
                  validationErrors.bank_name = msg
                } else if (msg.includes('account_type') || msg.includes('account type')) {
                  validationErrors.account_type = msg
                } else if (msg.includes('account_number_full') || msg.includes('account number')) {
                  validationErrors.account_number_full = msg
                } else if (msg.includes('balance') || msg.includes('balance')) {
                  validationErrors.balance = msg
                }
              })
            } else {
              validationErrors.general = errorData.message
            }
          }
          setErrors(validationErrors)
        } else if (status === 403) {
          // Forbidden - User doesn't own the account
          showToast('You do not have permission to edit this account information.', 'error')
        } else if (status === 500) {
          // Server error
          showToast('An error occurred while saving the data. Please try again later.', 'error')
        } else {
          setErrors({
            general: errorData.message || 'An error has occurred. Please try again later.',
          })
        }
      } else {
        setErrors({
          general: 'An error has occurred. Please try again later.',
        })
      }
    }
  }

  // Show loading state while fetching initial data
  if (isInitialLoading) {
    return (
      <div className="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600 dark:text-gray-400">Loading information...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Edit Account {bankName}
      </h2>

      {errors.general && (
        <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
          <p className="text-sm text-red-600 dark:text-red-400">{errors.general}</p>
        </div>
      )}

      <form onSubmit={handleSaveChanges} className="space-y-4">
        {/* Bank Name */}
        <Input
          label="Bank"
          type="text"
          value={bankName}
          onChange={(e) => setBankName(e.target.value)}
          error={errors.bank_name}
          placeholder="Example: Vietcombank"
          required
        />

        {/* Account Type */}
        <div className="w-full">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Account type
          </label>
          <select
            value={accountType}
            onChange={(e) => setAccountType(e.target.value as AccountType)}
            className={`
              w-full px-4 py-2 border rounded-md
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
              dark:bg-gray-700 dark:border-gray-600 dark:text-white
              ${errors.account_type ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
            `}
            required
          >
            <option value="Checking">Checking</option>
            <option value="Credit Card">Credit Card</option>
            <option value="Savings">Savings</option>
            <option value="Investment">Investment</option>
            <option value="Loan">Loan</option>
          </select>
          {errors.account_type && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.account_type}</p>
          )}
        </div>

        {/* Branch Name */}
        <Input
          label="Branch Name"
          type="text"
          value={branchName}
          onChange={(e) => setBranchName(e.target.value)}
          error={errors.branch_name}
          placeholder="Example: District 3"
        />

        {/* Account Number Full */}
        <Input
          label="Full account number"
          type="text"
          value={accountNumberFull}
          onChange={(e) => setAccountNumberFull(e.target.value)}
          error={errors.account_number_full}
          placeholder="Example: 9704221234567890123"
          required
        />

        {/* Balance */}
        <Input
          label="Current balance"
          type="number"
          value={balance}
          onChange={(e) => setBalance(e.target.value)}
          error={errors.balance}
          placeholder="0"
          min="0"
          step="0.01"
          required
        />

        {/* Action Buttons */}
        <div className="flex justify-end space-x-4 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isLoading}>
            Save Changes
          </Button>
        </div>
      </form>

      {/* Toast Notification */}
      {toast.show && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={hideToast}
        />
      )}
    </div>
  )
}

export default AccountEditForm

