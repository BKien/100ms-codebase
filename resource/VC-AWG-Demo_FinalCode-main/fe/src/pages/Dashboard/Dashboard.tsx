import React, { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { accountService } from '../../api/account.service'
import { transactionService } from '../../api/transaction.service'
import { Account, Transaction } from '../../api/types'
import Loading from '../../components/Loading/Loading'
import Error from '../../components/Error/Error'

const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const [accounts, setAccounts] = useState<Account[]>([])
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true)
        const [accountsRes, transactionsRes] = await Promise.all([
          accountService.getAccounts(),
          transactionService.getTransactions({
            type: 'All',
            limit: 5
          }),
        ])

        if (accountsRes.success && accountsRes.data) {
          // Support multiple response shapes from the backend
          const accountsData = Array.isArray(accountsRes.data)
            ? accountsRes.data
            : accountsRes.data.accounts ?? accountsRes.data.items ?? []

          if (Array.isArray(accountsData)) {
            setAccounts(accountsData)
          } else {
            console.error('Unexpected accounts response shape', accountsRes.data)
            setAccounts([])
          }
        }

        console.log('Transactions Response:', transactionsRes)
        if (transactionsRes.data && Array.isArray(transactionsRes.data)) {
          const txData: Transaction[] = transactionsRes.data

          if (txData.length === 0) {
            console.warn('No transactions available in API response')
          }

          // Sort transactions by time in descending order and get the 5 latest transactions
          const sortedTransactions = txData
            .filter((transaction) => transaction.transaction_date) // Filter transactions with valid dates
            .sort((a: Transaction, b: Transaction) =>
              new Date(b.transaction_date).getTime() - new Date(a.transaction_date).getTime()
            )
          console.log('Sorted Transactions:', sortedTransactions)
          setRecentTransactions(sortedTransactions.slice(0, 5))
        } else {
          console.error('Invalid transactions response structure')
        }
      } catch (err: any) {
        setError(err.message || 'Unable to load data')
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [])

  if (isLoading) {
    return <Loading fullScreen message="Loading..." />
  }

  if (error) {
    return <Error message={error} onRetry={() => window.location.reload()} />
  }

  const totalBalance = Array.isArray(accounts)
    ? accounts.reduce((sum, acc) => sum + (acc.balance || 0), 0)
    : 0

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Welcome, {user?.full_name || user?.username}!
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Your financial overview
        </p>
      </div>

      {/* Total balance */}
      <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
        <h2 className="text-lg font-medium mb-2">Total Balance</h2>
        <p className="text-3xl font-bold">
          {new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND',
          }).format(totalBalance)}
        </p>
      </div>

      {/* Accounts */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          My Accounts
        </h2>
        {accounts.length === 0 ? (
          <p className="text-gray-600 dark:text-gray-400">No accounts available</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {accounts.map((account) => (
              <div
                key={account.account_id}
                className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
              >
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  {account.bank_name}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {account.account_type}
                </p>
                <p className="text-lg font-bold text-blue-600 dark:text-blue-400 mt-2">
                  {new Intl.NumberFormat('vi-VN', {
                    style: 'currency',
                    currency: 'VND',
                  }).format(account.balance)}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent transactions */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Recent Transactions
        </h2>
        {recentTransactions.length === 0 ? (
          <p className="text-gray-600 dark:text-gray-400">No transactions available</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                    Description
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                    Type
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                    Amount
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {recentTransactions.map((transaction, index) => (
                  <tr key={transaction.transaction_id || index}>
                    <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                      {transaction.item_description}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          transaction.type === 'Revenue'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                        }`}
                      >
                        {transaction.type === 'Revenue' ? 'Revenue' : 'Expense'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">
                      {new Intl.NumberFormat('vi-VN', {
                        style: 'currency',
                        currency: 'VND',
                      }).format(transaction.amount)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                      {new Date(transaction.transaction_date).toLocaleDateString('vi-VN')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard

