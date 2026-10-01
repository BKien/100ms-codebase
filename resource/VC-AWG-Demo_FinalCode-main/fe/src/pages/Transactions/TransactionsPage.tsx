import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { transactionService, GetTransactionsResponse } from '../../api/transaction.service'
import { Transaction } from '../../api/types'
import { formatCurrency, formatDate } from '../../utils/format'
import Loading from '../../components/Loading/Loading'
import Toast from '../../components/Toast/Toast'
import Button from '../../components/Button/Button'

type FilterType = 'All' | 'Revenue' | 'Expense'

const TransactionsPage: React.FC = () => {
  const navigate = useNavigate()
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [filterType, setFilterType] = useState<FilterType>('All')
  const [offset, setOffset] = useState<number>(0)
  const [hasMore, setHasMore] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [showToast, setShowToast] = useState<boolean>(false)
  const [toastMessage, setToastMessage] = useState<string>('')

  /**
   * Function to fetch transactions from the API
   * @param isNewFilter - true for a new filter (reset the list), false for load more
   */
  const fetchTransactions = async (isNewFilter: boolean) => {
    try {
      setIsLoading(true)
      setError(null)

      const currentOffset = isNewFilter ? 0 : offset
      const response: GetTransactionsResponse = await transactionService.getTransactions({
        type: filterType,
        limit: 10,
        offset: currentOffset,
      })

      setIsLoading(false)

      if (isNewFilter) {
        // Replace the old list with new data
        setTransactions(response.data)
        setOffset(response.data.length)
      } else {
        // Append new data to the end of the list
        setTransactions((prev) => [...prev, ...response.data])
        setOffset((prev) => prev + response.data.length)
      }

      setHasMore(response.hasMore)

      // Display a notification if the list is empty
      if (isNewFilter && response.data.length === 0) {
        setError('No transactions have been recorded yet.')
      }
    } catch (err: any) {
      setIsLoading(false)

      // Handle API errors
      if (err.response?.status === 401) {
        // Already handled by the axios interceptor
        return
      }

      const errorMessage =
        err.response?.data?.message ||
        'An error occurred. Please try again later.'
      setError(errorMessage)
      setToastMessage(errorMessage)
      setShowToast(true)
    }
  }

  /**
   * Handle when the user clicks a tab
   */
  const handleTabClick = (type: FilterType) => {
    if (isLoading) return // Disable while loading

    setFilterType(type)
    setOffset(0)
    setTransactions([])
    setError(null)
  }

  /**
   * Handle when the user clicks "Load more"
   */
  const handleLoadMore = () => {
    if (isLoading || !hasMore) return
    fetchTransactions(false)
  }

  // Fetch transactions when filterType changes
  useEffect(() => {
    fetchTransactions(true)
  }, [filterType])

  // Close the toast after 3 seconds
  useEffect(() => {
    if (showToast) {
      const timer = setTimeout(() => {
        setShowToast(false)
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [showToast])

  /**
   * Render an icon for the transaction type
   */
  const getTransactionIcon = (type: string) => {
    if (type === 'Revenue') {
      return (
        <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
          <svg
            className="w-6 h-6 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
        </div>
      )
    } else {
      return (
        <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center">
          <svg
            className="w-6 h-6 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M20 12H4"
            />
          </svg>
        </div>
      )
    }
  }

  /**
   * Render a skeleton loader for the table
   */
  const renderSkeletonLoader = () => {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, index) => (
          <div
            key={index}
            className="bg-white rounded-lg shadow-sm p-4 animate-pulse"
          >
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-gray-200 rounded-full"></div>
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/3"></div>
              </div>
              <div className="h-4 bg-gray-200 rounded w-20"></div>
              <div className="h-4 bg-gray-200 rounded w-24"></div>
              <div className="h-4 bg-gray-200 rounded w-28"></div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#F4F5F7] p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-[22px] leading-[32px] font-normal text-[#878787]">
            Latest Transactions
          </h1>
          <Button
            variant="primary"
            onClick={() => navigate('/transactions/add')}
            className="flex items-center gap-2"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            Add transaction
          </Button>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] mb-6">
          <div className="flex border-b border-[rgba(210,210,210,0.25)]">
            {(['All', 'Revenue', 'Expense'] as FilterType[]).map((type) => (
              <button
                key={type}
                onClick={() => handleTabClick(type)}
                disabled={isLoading}
                className={`flex-1 px-6 py-4 text-base font-medium transition-colors ${
                  filterType === type
                    ? 'text-[#299D91] border-b-2 border-[#299D91]'
                    : 'text-[#878787] hover:text-[#299D91]'
                } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
              >
                {type === 'Expense' ? 'Expenses' : type}
              </button>
            ))}
          </div>
        </div>

        {/* Error Message */}
        {error && !isLoading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        {/* Transactions Table/List */}
        <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] overflow-hidden">
          {isLoading && transactions.length === 0 ? (
            // Skeleton loader during the initial load
            <div className="p-6">{renderSkeletonLoader()}</div>
          ) : transactions.length === 0 ? (
            // Empty state
            <div className="p-24 flex flex-col items-center justify-center">
              <p className="text-base text-[#9F9F9F] text-center">
                No transactions have been recorded yet.
              </p>
            </div>
          ) : (
            <>
              {/* Desktop Table View */}
              <div className="hidden md:block overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-[#F9FAFB] border-b border-[rgba(210,210,210,0.25)]">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                        Items
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                        Shop Name
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                        Payment Method
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium text-[#878787] uppercase tracking-wider">
                        Amount
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-[rgba(210,210,210,0.25)]">
                    {transactions.map((transaction) => (
                      <tr
                        key={transaction.transaction_id}
                        className="hover:bg-gray-50 transition-colors"
                      >
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center gap-3">
                            {getTransactionIcon(transaction.type)}
                            <div>
                              <p className="text-sm font-medium text-[#191919]">
                                {transaction.item_description}
                              </p>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <p className="text-sm text-[#666666]">
                            {transaction.shop_name || '-'}
                          </p>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <p className="text-sm text-[#666666]">
                            {formatDate(transaction.transaction_date)}
                          </p>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <p className="text-sm text-[#666666]">
                            {transaction.payment_method || '-'}
                          </p>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right">
                          <p
                            className={`text-sm font-semibold ${
                              transaction.type === 'Revenue'
                                ? 'text-green-600'
                                : 'text-red-600'
                            }`}
                          >
                            {transaction.type === 'Revenue' ? '+' : '-'}
                            {formatCurrency(transaction.amount)}
                          </p>
                        </td>
                      </tr>
                    ))}
                    {isLoading && transactions.length > 0 && (
                      <tr>
                        <td colSpan={5} className="px-6 py-4">
                          <div className="flex justify-center">
                            <Loading size="sm" message="Loading..." />
                          </div>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Mobile List View */}
              <div className="md:hidden divide-y divide-[rgba(210,210,210,0.25)]">
                {transactions.map((transaction) => (
                  <div
                    key={transaction.transaction_id}
                    className="p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-start gap-3 mb-3">
                      {getTransactionIcon(transaction.type)}
                      <div className="flex-1">
                        <p className="text-sm font-medium text-[#191919] mb-1">
                          {transaction.item_description}
                        </p>
                        <p className="text-xs text-[#666666]">
                          {transaction.shop_name || 'N/A'}
                        </p>
                      </div>
                      <p
                        className={`text-sm font-semibold ${
                          transaction.type === 'Revenue'
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {transaction.type === 'Revenue' ? '+' : '-'}
                        {formatCurrency(transaction.amount)}
                      </p>
                    </div>
                    <div className="flex justify-between text-xs text-[#666666] ml-13">
                      <span>{formatDate(transaction.transaction_date)}</span>
                      <span>{transaction.payment_method || '-'}</span>
                    </div>
                  </div>
                ))}
                {isLoading && transactions.length > 0 && (
                  <div className="p-4 flex justify-center">
                    <Loading size="sm" message="Loading..." />
                  </div>
                )}
              </div>

              {/* Load More Button */}
              {hasMore && !isLoading && (
                <div className="p-6 border-t border-[rgba(210,210,210,0.25)] text-center">
                  <button
                    onClick={handleLoadMore}
                    className="px-6 py-2 bg-[#299D91] text-white rounded hover:bg-[#238a7f] transition-colors text-sm font-medium"
                  >
                    Loading More
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Toast Notification */}
      {showToast && (
        <Toast
          message={toastMessage}
          type="error"
          onClose={() => setShowToast(false)}
        />
      )}
    </div>
  )
}

export default TransactionsPage

