import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { accountService } from '../../api/account.service'
import { Account } from '../../api/types'
import Loading from '../../components/Loading/Loading'
import Error from '../../components/Error/Error'
import Button from '../../components/Button/Button'
import DeleteAccountModal from '../../components/DeleteAccountModal/DeleteAccountModal'
import { formatCurrency } from '../../utils/format'

interface AccountsResponse {
  user_id: number
  accounts: Account[]
}

const AccountListPage: React.FC = () => {
  const [accounts, setAccounts] = useState<Account[]>([])
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const fetchAccounts = async () => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await accountService.getAccounts()
      
      if (response.success && response.data) {
        const data = response.data as AccountsResponse
        setAccounts(data.accounts || [])
      } else {
        setAccounts([])
      }
    } catch (err: any) {
      // Handle 401 errors - already handled by the axios interceptor
      if (err.response?.status === 401) {
        navigate('/login')
        return
      }

      // Handle server errors (500)
      if (err.response?.status === 500) {
        setError('An error occurred, please try again later.')
      } else {
        setError(err.response?.data?.message || 'An error occurred, please try again later.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchAccounts()
  }, [])

  // Display loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#F4F5F7] p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-[22px] leading-[32px] font-normal text-[#878787] mb-4">
            Balances
          </h1>
          <div className="flex items-center justify-center min-h-[400px]">
            <Loading size="lg" message="Loading account list..." />
          </div>
        </div>
      </div>
    )
  }

  // Display error state
  if (error) {
    return (
      <div className="min-h-screen bg-[#F4F5F7] p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-[22px] leading-[32px] font-normal text-[#878787] mb-4">
            Balances
          </h1>
          <Error message={error} onRetry={fetchAccounts} />
        </div>
      </div>
    )
  }

  // Display empty state
  if (accounts.length === 0) {
    return (
      <div className="min-h-screen bg-[#F4F5F7] p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-[22px] leading-[32px] font-normal text-[#878787] mb-4">
            Balances
          </h1>
          <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] p-24 flex flex-col items-center justify-center gap-4">
            <p className="text-base text-[#9F9F9F] text-center">
              You haven't linked any accounts yet. Please add an account.
            </p>
            <Button
              variant="primary"
              onClick={() => navigate('/accounts/add')}
              className="bg-[#299D91] hover:bg-[#238a7f] text-white px-8 py-3 rounded"
            >
              Add account
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#F4F5F7] p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-[22px] leading-[32px] font-normal text-[#878787] mb-4">
          Balances
        </h1>

        <div className="flex flex-col gap-8">
          {/* Top line - 2 cards */}
          {accounts.length > 0 && (
            <div className="flex flex-row gap-6 flex-wrap">
              {accounts.slice(0, 2).map((account, index) => (
                <AccountCard 
                  key={account.id || account.account_id || `account-${index}`} 
                  account={account}
                  onDelete={fetchAccounts}
                />
              ))}
            </div>
          )}

          {/* Bottom line - remaining cards + Add Account */}
          <div className="flex flex-row gap-6 flex-wrap">
            {accounts.slice(2).map((account, index) => (
              <AccountCard 
                key={account.id || account.account_id || `account-${index + 2}`} 
                account={account}
                onDelete={fetchAccounts}
              />
            ))}
            {/* Add Account Card */}
            <AddAccountCard />
          </div>
        </div>
      </div>
    </div>
  )
}

interface AccountCardProps {
  account: Account
  onDelete?: () => void
}

const AccountCard: React.FC<AccountCardProps> = ({ account, onDelete }) => {
  const navigate = useNavigate()
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  
  const formatAccountNumber = (last4: string | undefined) => {
    if (!last4) return '****'
    return `**** ${last4}`
  }

  const handleDeleteSuccess = () => {
    if (onDelete) {
      onDelete()
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] p-6 w-[352px] flex-shrink-0">
      {/* Header */}
      <div className="flex justify-between items-center pb-3 border-b border-[rgba(210,210,210,0.25)] mb-4">
        <h3 className="text-base font-bold leading-6 text-[#878787] uppercase">
          {account.account_type}
        </h3>
        <div className="flex items-center gap-1">
          <span className="text-xs font-medium leading-4 text-[#666666]">
            {account.bank_name}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="flex flex-col gap-6 mb-6">
        {/* Account Number */}
        <div className="flex flex-col gap-1">
          <p className="text-xl font-semibold leading-7 text-[#191919] uppercase">
            {formatAccountNumber(account.account_number_last_4)}
          </p>
          <p className="text-sm font-normal leading-5 text-[#9F9F9F]">
            Account Number
          </p>
        </div>

        {/* Total amount */}
        <div className="flex flex-col gap-1">
          <p className="text-xl font-semibold leading-7 text-[#191919]">
            {formatCurrency(account.balance)}
          </p>
          <p className="text-sm font-normal leading-5 text-[#9F9F9F]">
            Total amount
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="flex justify-between items-center">
        <button 
          onClick={() => setIsDeleteModalOpen(true)}
          className="text-base font-normal leading-6 text-[#299D91] hover:underline"
        >
          Remove
        </button>
        <button
          onClick={() => navigate(`/accounts/${account.id || account.account_id}`)}
          className="bg-[#299D91] text-white px-5 py-2 rounded flex items-center gap-2 hover:bg-[#238a7f] transition-colors"
        >
          <span className="text-sm font-medium leading-5 uppercase">Details</span>
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M6 12L10 8L6 4"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>

      {/* Delete Account Modal */}
      <DeleteAccountModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        accountId={account.id || account.account_id || 0}
        accountName={account.bank_name}
        accountNumberLast4={account.account_number_last_4 || '****'}
        onSuccess={handleDeleteSuccess}
      />
    </div>
  )
}

const AddAccountCard: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] p-24 flex flex-col items-center justify-center gap-1 w-[352px] flex-shrink-0">
      <button
        onClick={() => navigate('/accounts/add')}
        className="bg-[#299D91] text-white px-8 py-3 rounded mb-1 hover:bg-[#238a7f] transition-colors"
      >
        <span className="text-base font-bold leading-6 uppercase">
          Add accounts
        </span>
      </button>
      <button className="text-base font-medium leading-6 text-[#9F9F9F] hover:text-[#878787] transition-colors">
        Edit Accounts
      </button>
    </div>
  )
}

export default AccountListPage

