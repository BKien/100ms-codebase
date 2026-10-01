import { useState, useCallback } from 'react'

interface ToastState {
  message: string
  type: 'success' | 'error' | 'info'
  show: boolean
}

export const useToast = () => {
  const [toast, setToast] = useState<ToastState>({
    message: '',
    type: 'info',
    show: false,
  })

  const showToast = useCallback((message: string, type: 'success' | 'error' | 'info' = 'info') => {
    setToast({ message, type, show: true })
  }, [])

  const hideToast = useCallback(() => {
    setToast((prev) => ({ ...prev, show: false }))
  }, [])

  return {
    toast,
    showToast,
    hideToast,
  }
}

