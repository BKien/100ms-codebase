import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import Button from '../../components/Button/Button'

const Home: React.FC = () => {
  const { isAuthenticated } = useAuth()

  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
        Welcome to Personal Financial Management
      </h1>
      <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
        Manage personal finances smartly and efficiently
      </p>

      {isAuthenticated ? (
        <Link to="/dashboard">
          <Button size="lg">Go to Dashboard</Button>
        </Link>
      ) : (
        <div className="flex justify-center space-x-4">
          <Link to="/login">
            <Button size="lg" variant="primary">
              Log in
            </Button>
          </Link>
          <Link to="/register">
            <Button size="lg" variant="outline">
              Register
            </Button>
          </Link>
        </div>
      )}

      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Account Management
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Track all your bank accounts in one place.
          </p>
        </div>

        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Transaction
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Record and categorize all income and expenditure transactions.
          </p>
        </div>

        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Financial Goals
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Set and track savings and spending goals.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Home

