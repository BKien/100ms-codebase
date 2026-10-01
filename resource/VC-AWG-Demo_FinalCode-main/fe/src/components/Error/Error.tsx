import React from 'react'
import Button from '../Button/Button'

interface ErrorProps {
  message?: string
  onRetry?: () => void
  fullScreen?: boolean
}

const Error: React.FC<ErrorProps> = ({
  message = 'An error has occurred. Please try again later.',
  onRetry,
  fullScreen = false,
}) => {
  const errorContent = (
    <div className="flex flex-col items-center justify-center p-8">
      <div className="text-red-600 dark:text-red-400 mb-4">
        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        An error has occurred
      </h3>
      <p className="text-gray-600 dark:text-gray-400 text-center mb-4">{message}</p>
      {onRetry && (
        <Button onClick={onRetry} variant="primary">
          Try again
        </Button>
      )}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white dark:bg-gray-900 z-50">
        {errorContent}
      </div>
    )
  }

  return (
    <div className="w-full bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
      {errorContent}
    </div>
  )
}

export default Error

