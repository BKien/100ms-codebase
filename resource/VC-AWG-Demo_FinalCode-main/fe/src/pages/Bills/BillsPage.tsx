import React from 'react'
import UpcomingBills from '../../components/UpcomingBills/UpcomingBills'

const BillsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#F4F5F7] p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-[22px] leading-[32px] font-normal text-[#878787] mb-6">
          Bills
        </h1>
        <UpcomingBills />
      </div>
    </div>
  )
}

export default BillsPage

