import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { goalService } from '../../api/goal.service'
import { GoalsResponse, SavingGoal, ExpenseGoal } from '../../api/types'
import Loading from '../../components/Loading/Loading'
import Error from '../../components/Error/Error'
import Button from '../../components/Button/Button'
import AdjustGoalModal from '../../components/AdjustGoalModal/AdjustGoalModal'
import CreateGoalModal from '../../components/CreateGoalModal/CreateGoalModal'
import SavingsSummaryChart from '../../components/SavingsSummaryChart/SavingsSummaryChart'

/**
 * Page displaying savings and spending goals
 */
const GoalsPage: React.FC = () => {
  const navigate = useNavigate()
  const [goalsData, setGoalsData] = useState<GoalsResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [adjustModalState, setAdjustModalState] = useState<{
    isOpen: boolean
    goalId: number | null
    targetAmount: number | null
  }>({
    isOpen: false,
    goalId: null,
    targetAmount: null,
  })
  const [createModalOpen, setCreateModalOpen] = useState(false)

  /**
   * Asynchronous function to get goal data from the API
   */
  const fetchGoals = async () => {
    try {
      setIsLoading(true)
      setError('')

      const response = await goalService.getGoals()

      if (response.success && response.data) {
        setGoalsData(response.data)
      } else {
        setError('Unable to load target data')
      }
    } catch (err: any) {
      // Handle 401 Unauthorized errors
      if (err.response?.status === 401) {
        navigate('/login')
        return
      }

      // Handle system errors (500 or other errors)
      const errorMessage =
        err.response?.data?.message ||
        'An error occurred while loading goals, please try again later.'
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchGoals()
  }, [])

  // Display loading state
  if (isLoading) {
    return <Loading fullScreen message="Loading goals..." />
  }

  // Display error state
  if (error) {
    return (
      <div className="min-h-screen bg-[#F4F5F7] dark:bg-gray-900 p-8">
        <div className="max-w-7xl mx-auto">
          <Error message={error} onRetry={fetchGoals} />
        </div>
      </div>
    )
  }

  // Check whether there is no goal data
  const hasNoGoals =
    !goalsData?.savingGoal && (!goalsData?.expenseGoals || goalsData.expenseGoals.length === 0)

  if (hasNoGoals) {
    return (
      <div className="min-h-screen bg-[#F4F5F7] dark:bg-gray-900 p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-[22px] leading-[32px] font-normal text-[#878787] dark:text-gray-400 mb-6">
            Goals
          </h1>
          
          {/* Savings Summary Chart - Display even when there are no goals */}
          <div className="mb-8">
            <SavingsSummaryChart />
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-12 text-center">
            <p className="text-lg text-gray-600 dark:text-gray-400 mb-6">
              You haven't set up any goals yet. Create your first goal!
            </p>
            <Button onClick={() => setCreateModalOpen(true)} variant="primary">
              Create New Goal
            </Button>
          </div>
        </div>
      </div>
    )
  }

  const savingGoal = goalsData?.savingGoal
  const expenseGoals = goalsData?.expenseGoals || []
  const progressPercentage = savingGoal
    ? Math.min((savingGoal.target_achieved / savingGoal.target_amount) * 100, 100)
    : 0

  return (
    <div className="min-h-screen bg-[#F4F5F7] dark:bg-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-[22px] leading-[32px] font-normal text-[#878787] dark:text-gray-400">
            Goals
          </h1>
          <Button onClick={() => setCreateModalOpen(true)} variant="primary" size="sm">
            Create New Goal
          </Button>
        </div>

        {/* Savings Goal and Savings Summary Chart - Display side by side */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Savings Goal Section */}
          {savingGoal && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Savings Goal
                </h2>
                <Button
                  onClick={() =>
                    setAdjustModalState({
                      isOpen: true,
                      goalId: savingGoal.goal_id,
                      targetAmount: savingGoal.target_amount,
                    })
                  }
                  variant="secondary"
                  size="sm"
                >
                  Edit
                </Button>
              </div>

              <div className="space-y-4">
                {/* Target Achieved */}
                <div>
                  <label className="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                    Target Achieved
                  </label>
                  <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {new Intl.NumberFormat('vi-VN', {
                      style: 'currency',
                      currency: 'VND',
                    }).format(savingGoal.target_achieved)}
                  </p>
                </div>

                {/* Target Amount */}
                <div>
                  <label className="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                    Target Amount
                  </label>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {new Intl.NumberFormat('vi-VN', {
                      style: 'currency',
                      currency: 'VND',
                    }).format(savingGoal.target_amount)}
                  </p>
                </div>

                {/* Progress Bar */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Progress</span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {progressPercentage.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className="bg-blue-600 dark:bg-blue-500 h-3 rounded-full transition-all duration-300"
                      style={{ width: `${progressPercentage}%` }}
                    />
                  </div>
                </div>

                {/* Date Range */}
                <div className="flex gap-4 text-sm text-gray-600 dark:text-gray-400">
                  <div>
                    <span className="font-medium">Start: </span>
                    {new Date(savingGoal.start_date).toLocaleDateString('vi-VN')}
                  </div>
                  <div>
                    <span className="font-medium">End: </span>
                    {new Date(savingGoal.end_date).toLocaleDateString('vi-VN')}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Savings Summary Chart Section */}
          <div className={savingGoal ? '' : 'lg:col-span-2'}>
            <SavingsSummaryChart />
          </div>
        </div>

        {/* Expenses Goals by Category Section */}
        {expenseGoals.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
              Expenses Goals by Category
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {expenseGoals.map((goal: ExpenseGoal) => {
                const expenseProgress = Math.min(
                  (goal.current_expense / goal.target_amount) * 100,
                  100,
                )
                const isOverLimit = goal.current_expense > goal.target_amount

                return (
                  <div
                    key={goal.goal_id}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {goal.category}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      Spent (current month)
                    </p>
                    <p
                      className={`text-xl font-bold mb-2 ${
                        isOverLimit
                          ? 'text-red-600 dark:text-red-400'
                          : 'text-orange-600 dark:text-orange-400'
                      }`}
                    >
                      {new Intl.NumberFormat('vi-VN', {
                        style: 'currency',
                        currency: 'VND',
                      }).format(goal.current_expense)}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      Goals:{' '}
                      <span className="font-medium text-gray-900 dark:text-white">
                        {new Intl.NumberFormat('vi-VN', {
                          style: 'currency',
                          currency: 'VND',
                        }).format(goal.target_amount)}
                      </span>
                    </p>
                    {/* Progress Bar */}
                    <div className="mt-3">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-600 dark:text-gray-400">Progress</span>
                        <span
                          className={`text-xs font-medium ${
                            isOverLimit
                              ? 'text-red-600 dark:text-red-400'
                              : 'text-gray-900 dark:text-white'
                          }`}
                        >
                          {expenseProgress.toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all duration-300 ${
                            isOverLimit
                              ? 'bg-red-600 dark:bg-red-500'
                              : 'bg-orange-600 dark:bg-orange-500'
                          }`}
                          style={{ width: `${Math.min(expenseProgress, 100)}%` }}
                        />
                      </div>
                    </div>
                    {/* Edit Button */}
                    <div className="mt-4">
                      <Button
                        onClick={() =>
                          setAdjustModalState({
                            isOpen: true,
                            goalId: goal.goal_id,
                            targetAmount: goal.target_amount,
                          })
                        }
                        variant="secondary"
                        size="sm"
                        className="w-full"
                      >
                        Edit
                      </Button>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Adjust Goal Modal */}
        {adjustModalState.goalId !== null && adjustModalState.targetAmount !== null && (
          <AdjustGoalModal
            isOpen={adjustModalState.isOpen}
            onClose={() =>
              setAdjustModalState({
                isOpen: false,
                goalId: null,
                targetAmount: null,
              })
            }
            goalId={adjustModalState.goalId}
            currentTargetAmount={adjustModalState.targetAmount}
            onSuccess={fetchGoals}
          />
        )}

        {/* Create Goal Modal */}
        <CreateGoalModal
          isOpen={createModalOpen}
          onClose={() => setCreateModalOpen(false)}
          onSuccess={fetchGoals}
        />
      </div>
    </div>
  )
}

export default GoalsPage

