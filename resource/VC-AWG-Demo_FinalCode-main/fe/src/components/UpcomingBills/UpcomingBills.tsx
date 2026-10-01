import React, { useState, useEffect } from 'react'
import { billService } from '../../api/bill.service'
import { Bill } from '../../api/types'
import { formatCurrency, formatDate } from '../../utils/format'
import Loading from '../Loading/Loading'

const UpcomingBills: React.FC = () => {
  const [bills, setBills] = useState<Bill[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchUpcomingBills = async () => {
    try {
      setIsLoading(true)
      setError(null)
      
      const response = await billService.getUpcomingBills()
      
      if (response.data) {
        setBills(response.data)
      } else {
        setBills([])
      }
    } catch (err: any) {
      console.error('Error fetching bills:', err)
      setError('Unable to load the invoice list. Please try again.')
      setBills([])
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchUpcomingBills()
  }, [])

  const handlePayNow = (billId: number) => {
    // TODO: Implement payment logic
    console.log('Pay now for bill:', billId)
  }

  /**
   * Render a skeleton loader for bills
   */
  const renderSkeletonLoader = () => {
    return (
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-[#F9FAFB] border-b border-[rgba(210,210,210,0.25)]">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                Logo
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                Item Description
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                Due Date
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                Last Charge
              </th>
              <th className="px-6 py-4 text-right text-xs font-medium text-[#878787] uppercase tracking-wider">
                Amount
              </th>
              <th className="px-6 py-4 text-center text-xs font-medium text-[#878787] uppercase tracking-wider">
                Action
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-[rgba(210,210,210,0.25)]">
            {[...Array(3)].map((_, index) => (
              <tr key={index} className="animate-pulse">
                <td className="px-6 py-4">
                  <div className="w-16 h-16 bg-gray-200 rounded-lg"></div>
                </td>
                <td className="px-6 py-4">
                  <div className="h-4 bg-gray-200 rounded w-32"></div>
                </td>
                <td className="px-6 py-4">
                  <div className="h-4 bg-gray-200 rounded w-24"></div>
                </td>
                <td className="px-6 py-4">
                  <div className="h-4 bg-gray-200 rounded w-24"></div>
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="h-4 bg-gray-200 rounded w-20 ml-auto"></div>
                </td>
                <td className="px-6 py-4 text-center">
                  <div className="h-10 bg-gray-200 rounded w-24 mx-auto"></div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] p-6">
        {renderSkeletonLoader()}
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] p-24 flex flex-col items-center justify-center">
        <p className="text-base text-[#9F9F9F] mb-4 text-center">{error}</p>
        <button
          onClick={fetchUpcomingBills}
          className="bg-[#299D91] text-white px-6 py-2 rounded hover:bg-[#238a7f] transition-colors text-sm font-medium"
        >
          Try again
        </button>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-[0px_20px_25px_0px_rgba(76,103,100,0.1)] overflow-hidden">
      {bills.length === 0 ? (
        <div className="p-24 flex flex-col items-center justify-center">
          <p className="text-base text-[#9F9F9F] text-center">
            You do not have any upcoming bills to pay.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          {/* Desktop Table View */}
          <table className="w-full">
            <thead className="bg-[#F9FAFB] border-b border-[rgba(210,210,210,0.25)]">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                  Logo
                </th>
                <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                  Item Description
                </th>
                <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                  Due Date
                </th>
                <th className="px-6 py-4 text-left text-xs font-medium text-[#878787] uppercase tracking-wider">
                  Last Charge
                </th>
                <th className="px-6 py-4 text-right text-xs font-medium text-[#878787] uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-4 text-center text-xs font-medium text-[#878787] uppercase tracking-wider">
                  Action
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-[rgba(210,210,210,0.25)]">
              {bills.map((bill) => (
                <tr
                  key={bill.billId}
                  className="hover:bg-gray-50 transition-colors"
                >
                  {/* Logo Column */}
                  <td className="px-6 py-4 whitespace-nowrap">
                    {bill.logoUrl ? (
                      <img
                        src={bill.logoUrl}
                        alt={bill.itemDescription}
                        className="w-16 h-16 rounded-lg object-cover"
                        onError={(e) => {
                          // Fallback if the logo cannot load
                          const target = e.target as HTMLImageElement
                          target.style.display = 'none'
                        }}
                      />
                    ) : (
                      <div className="w-16 h-16 rounded-lg bg-[#F4F5F7] flex items-center justify-center">
                        <span className="text-[#878787] text-lg font-semibold">
                          {bill.itemDescription.charAt(0).toUpperCase()}
                        </span>
                      </div>
                    )}
                  </td>

                  {/* Item Description Column */}
                  <td className="px-6 py-4">
                    <p className="text-sm font-medium text-[#191919]">
                      {bill.itemDescription}
                    </p>
                  </td>

                  {/* Due Date Column */}
                  <td className="px-6 py-4 whitespace-nowrap">
                    <p className="text-sm text-[#666666]">
                      {formatDate(bill.dueDate)}
                    </p>
                  </td>

                  {/* Last Charge Column */}
                  <td className="px-6 py-4 whitespace-nowrap">
                    <p className="text-sm text-[#666666]">
                      {bill.lastChargeDate ? formatDate(bill.lastChargeDate) : '-'}
                    </p>
                  </td>

                  {/* Amount Column */}
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <p className="text-sm font-semibold text-[#191919]">
                      {formatCurrency(bill.amount)}
                    </p>
                  </td>

                  {/* Pay Now Button Column */}
                  <td className="px-6 py-4 whitespace-nowrap text-center">
                    <button
                      onClick={() => handlePayNow(bill.billId)}
                      className="bg-[#299D91] text-white px-6 py-2 rounded hover:bg-[#238a7f] transition-colors text-sm font-medium"
                    >
                      Pay Now
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default UpcomingBills

