import React, { useState, useEffect } from 'react'
import { expenseService } from '../../api/expense.service'
import { ExpenseSummaryItem } from '../../api/types'
import { formatCurrency } from '../../utils/format'

/**
 * Component displaying a monthly expense summary bar chart
 */
const ExpenseSummaryChart: React.FC = () => {
  const [summaryData, setSummaryData] = useState<ExpenseSummaryItem[]>([])
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [hoveredMonth, setHoveredMonth] = useState<string | null>(null)

  /**
   * Get expense summary data from the API
   */
  const fetchExpenseSummary = async () => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await expenseService.getExpenseSummary()

      // Check whether the data array is empty
      if (!response.data || response.data.length === 0) {
        setSummaryData([])
        setError('No spending data has been recorded for analysis.')
        return
      }

      // Update state with the received data
      setSummaryData(response.data)
    } catch (err: any) {
      // Handle API errors
      const errorMessage =
        err.response?.data?.error || 'Cannot load expense data. Please try again later.'
      setError(errorMessage)
      setSummaryData([])
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchExpenseSummary()
  }, [])

  /**
   * Determine the current month
   */
  const getCurrentMonth = (): string => {
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    const currentMonthIndex = new Date().getMonth()
    return monthNames[currentMonthIndex]
  }

  /**
   * Calculate bar height based on the maximum value
   */
  const getMaxExpense = (): number => {
    if (summaryData.length === 0) return 1
    return Math.max(...summaryData.map((item) => item.totalExpense))
  }

  /**
   * Calculate the bar height percentage
   */
  const getBarHeight = (expense: number): number => {
    const maxExpense = getMaxExpense()
    if (maxExpense === 0) return 0
    return (expense / maxExpense) * 100
  }

  /**
   * Calculate Y-axis tick values
   */
  const getYAxisValues = (): number[] => {
    const maxExpense = getMaxExpense()
    if (maxExpense === 0) return [0]
    
    // Create 5 ticks: 0%, 25%, 50%, 75%, 100%
    const steps = [0, 0.25, 0.5, 0.75, 1]
    return steps.map((step) => step * maxExpense)
  }

  /**
   * Render a skeleton loader for the chart
   */
  const renderChartSkeletonLoader = () => {
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return (
      <div className="w-full">
        <div className="mb-8">
          <div className="h-7 w-48 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-2" />
          <div className="h-4 w-64 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
        </div>
        <div className="relative w-full h-[320px] flex items-end justify-between gap-3 px-6 pb-12">
          {monthNames.map((month) => (
            <div key={month} className="flex-1 flex flex-col items-center gap-3">
              <div
                className="w-full bg-gray-200 dark:bg-gray-700 rounded-t-lg animate-pulse"
                style={{ height: `${Math.random() * 60 + 20}%` }}
              />
              <div className="h-4 w-8 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
            </div>
          ))}
        </div>
      </div>
    )
  }

  /**
   * Render the bar chart according to the Monthly Comparison design
   */
  const renderChart = () => {
    const currentMonth = getCurrentMonth()
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    // Create a full array of 12 months with data from the API
    const fullYearData = monthNames.map((month) => {
      const found = summaryData.find((item) => item.month === month)
      return found || { month, totalExpense: 0 }
    })

    return (
      <div className="w-full">
        {/* Monthly Comparison title */}
        <div className="mb-8">
          <h2 className="text-[22px] leading-[32px] font-normal text-[#878787] dark:text-gray-400 mb-2">
            Monthly Comparison
          </h2>
          <p className="text-sm text-[#878787] dark:text-gray-500">
            Compare monthly expenses throughout the year {new Date().getFullYear()}
          </p>
        </div>

        {/* Chart container */}
        <div className="relative flex">
          {/* Y-axis - Value labels */}
          <div className="flex flex-col justify-between h-[320px] pb-12 pr-4">
            {getYAxisValues()
              .slice()
              .reverse()
              .map((value, index) => (
                <div
                  key={index}
                  className="text-xs text-[#6B7280] dark:text-gray-500 font-medium text-right"
                  style={{ lineHeight: '1' }}
                >
                  {formatCurrency(value)}
                </div>
              ))}
          </div>

          {/* Main chart */}
          <div className="flex-1 relative">
            {/* Grid lines for the Y-axis */}
            <div className="absolute inset-0 flex flex-col justify-between pb-12">
              {[0, 25, 50, 75, 100].map((percent) => (
                <div
                  key={percent}
                  className="border-t border-gray-200 dark:border-gray-700"
                  style={{ opacity: percent === 0 ? 0 : 0.3 }}
                />
              ))}
            </div>

            {/* Bar chart */}
            <div className="relative w-full h-[320px] flex items-end justify-between gap-3 px-6 pb-12">
            {fullYearData.map((item) => {
              const isCurrentMonth = item.month === currentMonth
              const barHeight = getBarHeight(item.totalExpense)
              const isHovered = hoveredMonth === item.month

              return (
                <div
                  key={item.month}
                  className="flex-1 flex flex-col items-center gap-3 relative group h-full"
                  onMouseEnter={() => setHoveredMonth(item.month)}
                  onMouseLeave={() => setHoveredMonth(null)}
                >
                  {/* Tooltip */}
                  {isHovered && item.totalExpense > 0 && (
                    <div className="absolute bottom-full mb-3 px-4 py-2 bg-[#1A1A1A] text-white text-sm rounded-lg shadow-xl z-20 whitespace-nowrap">
                      <div className="font-semibold mb-1">{item.month}</div>
                      <div className="text-xs opacity-90">{formatCurrency(item.totalExpense)}</div>
                      <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-[#1A1A1A]" />
                    </div>
                  )}

                  {/* Container for the chart bar */}
                  <div className="w-full flex flex-col items-center justify-end h-full relative">
                    {/* Chart bar */}
                    <div
                      className={`w-full rounded-t-lg transition-all duration-300 cursor-pointer ${
                        isCurrentMonth
                          ? 'bg-[#10B981] hover:bg-[#059669] shadow-md'
                          : 'bg-[#D1D5DB] hover:bg-[#9CA3AF]'
                      } ${item.totalExpense === 0 ? 'opacity-20' : ''}`}
                      style={{
                        height: `${Math.max(barHeight, item.totalExpense > 0 ? 3 : 0)}%`,
                        minHeight: item.totalExpense > 0 ? '8px' : '0',
                      }}
                    />
                  </div>

                  {/* Month label */}
                  <div
                    className={`text-xs font-medium ${
                      isCurrentMonth
                        ? 'text-[#10B981] dark:text-green-400'
                        : 'text-[#6B7280] dark:text-gray-500'
                    }`}
                  >
                    {item.month}
                  </div>

                  {/* Value above the bar (if data is available) */}
                  {item.totalExpense > 0 && isHovered && (
                    <div className="absolute bottom-[calc(100%-8px)] left-1/2 transform -translate-x-1/2 -translate-y-full mb-2">
                      <div className="text-xs font-semibold text-gray-700 dark:text-gray-300 whitespace-nowrap">
                        {formatCurrency(item.totalExpense)}
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
            </div>

            {/* X-axis - Baseline */}
            <div className="border-t-2 border-gray-300 dark:border-gray-600 mx-6" />
          </div>
        </div>

        {/* Legend */}
        <div className="mt-6 flex items-center justify-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-[#D1D5DB]"></div>
            <span className="text-sm text-[#6B7280] dark:text-gray-400">Last month</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-[#10B981]"></div>
            <span className="text-sm text-[#6B7280] dark:text-gray-400">Current month</span>
          </div>
        </div>
      </div>
    )
  }

  // Display loading state
  if (isLoading) {
    return (
      <div className="w-full bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-8">
        {renderChartSkeletonLoader()}
      </div>
    )
  }

  // Display error state
  if (error) {
    return (
      <div className="w-full bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-8">
        <div className="flex flex-col items-center justify-center h-[400px] text-center">
          <div className="text-6xl mb-4">📊</div>
          <p className="text-[#878787] dark:text-gray-400 text-lg font-medium">{error}</p>
        </div>
      </div>
    )
  }

  // Display the chart
  return (
    <div className="w-full bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-8">
      {renderChart()}
    </div>
  )
}

export default ExpenseSummaryChart

