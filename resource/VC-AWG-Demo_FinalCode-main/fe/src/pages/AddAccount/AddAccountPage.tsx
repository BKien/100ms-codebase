import React from 'react'
import AddAccountForm from '../../components/AddAccountForm/AddAccountForm'

const AddAccountPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#F4F5F7] p-8">
      <div className="max-w-7xl mx-auto">
        <AddAccountForm />
      </div>
    </div>
  )
}

export default AddAccountPage

