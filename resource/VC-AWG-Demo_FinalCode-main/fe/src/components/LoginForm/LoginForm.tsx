import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { authService } from '../../api/auth.service'

const LoginForm: React.FC = () => {
  const navigate = useNavigate()
  const { login } = useAuth()
  
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')

  // Validation function
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!email.trim()) {
      setEmailError('Email address cannot be left blank.')
      return false
    }
    if (!emailRegex.test(email)) {
      setEmailError('Email is invalid.')
      return false
    }
    setEmailError('')
    return true
  }

  const validatePassword = (password: string): boolean => {
    if (!password.trim()) {
      setPasswordError('Password cannot be left blank.')
      return false
    }
    setPasswordError('')
    return true
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    // Client-side validation
    const isEmailValid = validateEmail(email)
    const isPasswordValid = validatePassword(password)
    
    if (!isEmailValid || !isPasswordValid) {
      return
    }

    setIsLoading(true)

    try {
      // Call login from context, which will handle the API call and save the token/user
      await login(email, password)
      
      // Save the token to localStorage or sessionStorage based on rememberMe
      const token = localStorage.getItem('token')
      const userData = localStorage.getItem('user')
      
      if (rememberMe && token && userData) {
        // The token has been saved to localStorage by context
        // No further action is needed
      } else if (token && userData) {
        // If rememberMe is not selected, it can be deleted when the browser closes
        // But keep it in localStorage for context to work
        // Can add deletion logic on logout if needed
      }
      
      // Navigate to the home page
      navigate('/')
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Email or password is incorrect.')
      } else {
        setError(err.response?.data?.message || err.message || 'Login failed. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#F4F5F7] flex items-center justify-center p-4">
      <div className="w-full max-w-[400px] flex flex-col items-center gap-10">
        {/* Logo */}
        <div className="flex flex-col items-center gap-10">
          <h1 className="text-[40px] font-bold text-[#299D91] tracking-[0.08em] text-center font-['Poppins']">
            FINEbank.IO
          </h1>
          
          {/* Login Form */}
          <div className="w-full flex flex-col items-center gap-6">
            <div className="w-full flex flex-col gap-8">
              {/* Input Section */}
              <div className="w-full flex flex-col gap-6">
                {/* Email Input */}
                <div className="w-full flex flex-col gap-2">
                  <label className="text-base font-medium text-[#191D23] leading-6">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => {
                      setEmail(e.target.value)
                      setEmailError('')
                      setError('')
                    }}
                    placeholder="johndoe@email.com"
                    className={`
                      w-full h-12 px-4 py-3 rounded-lg border
                      text-base leading-[22px] font-normal
                      focus:outline-none focus:ring-2 focus:ring-[#299D91]
                      ${emailError || error ? 'border-red-500' : 'border-[#4B5768]'}
                      ${emailError || error ? 'text-[#191D23]' : 'text-[#4B5768]'}
                      placeholder:text-[#4B5768]
                    `}
                    disabled={isLoading}
                  />
                  {emailError && (
                    <p className="text-sm text-red-500 mt-1">{emailError}</p>
                  )}
                </div>

                {/* Password Input */}
                <div className="w-full flex flex-col gap-2">
                  <div className="w-full flex justify-between items-center">
                    <label className="text-base font-medium text-[#191D23] leading-6">
                      Password
                    </label>
                    <Link
                      to="/forgot-password"
                      className="text-xs font-medium text-[#299D91] leading-4 text-right hover:underline"
                    >
                      Forgot Password?
                    </Link>
                  </div>
                  <div className="relative">
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => {
                        setPassword(e.target.value)
                        setPasswordError('')
                        setError('')
                      }}
                      placeholder="●●●●●●●●●●●●●●"
                      className={`
                        w-full h-12 px-4 py-3 rounded-lg border
                        text-base leading-6 font-normal
                        focus:outline-none focus:ring-2 focus:ring-[#299D91]
                        ${passwordError || error ? 'border-red-500' : 'border-[#D0D5DD]'}
                        ${passwordError || error ? 'text-[#191D23]' : 'text-[#999DA3]'}
                        placeholder:text-[#999DA3]
                      `}
                      disabled={isLoading}
                    />
                  </div>
                  {passwordError && (
                    <p className="text-sm text-red-500 mt-1">{passwordError}</p>
                  )}
                </div>
              </div>

              {/* Button Section */}
              <div className="w-full flex flex-col gap-4">
                {/* Remember Me Checkbox */}
                <div className="flex items-center gap-4">
                  <input
                    type="checkbox"
                    id="rememberMe"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-5 h-5 rounded border-[#4B5768] text-[#299D91] focus:ring-[#299D91] cursor-pointer"
                    disabled={isLoading}
                  />
                  <label
                    htmlFor="rememberMe"
                    className="text-base font-light text-[#191D23] leading-6 cursor-pointer"
                  >
                    Keep me signed in
                  </label>
                </div>

                {/* Error Message */}
                {error && (
                  <div className="w-full p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm text-red-600 text-center">{error}</p>
                  </div>
                )}

                {/* Login Button */}
                <button
                  type="submit"
                  onClick={handleLogin}
                  disabled={isLoading}
                  className={`
                    w-full h-12 px-3 py-4 rounded bg-[#299D91] text-white
                    text-base font-semibold leading-6 text-center
                    hover:bg-[#238a7f] transition-colors
                    focus:outline-none focus:ring-2 focus:ring-[#299D91] focus:ring-offset-2
                    disabled:opacity-50 disabled:cursor-not-allowed
                    flex items-center justify-center
                  `}
                >
                  {isLoading ? (
                    <span className="flex items-center gap-2">
                      <svg
                        className="animate-spin h-5 w-5"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        />
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                      Processing...
                    </span>
                  ) : (
                    'Login'
                  )}
                </button>
              </div>
            </div>

            {/* Divider */}
            <div className="w-full relative flex items-center justify-center my-4">
              <div className="absolute w-full h-px bg-[#4B5768] opacity-25"></div>
              <div className="relative bg-[#F4F5F7] px-2">
                <span className="text-sm font-normal text-[#999DA3] leading-5">
                  or sign in with
                </span>
              </div>
            </div>

            {/* Google Button */}
            <button
              type="button"
              className="w-full h-12 px-[69px] py-3 rounded bg-[#E4E7EB] text-[#4B5768] text-base font-normal leading-6 flex items-center justify-center gap-4 hover:bg-[#D0D5DD] transition-colors focus:outline-none focus:ring-2 focus:ring-[#299D91] focus:ring-offset-2"
              disabled={isLoading}
            >
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  fill="#4285F4"
                />
                <path
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  fill="#34A853"
                />
                <path
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  fill="#FBBC05"
                />
                <path
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  fill="#EA4335"
                />
              </svg>
              <span>Continue with Google</span>
            </button>
          </div>
        </div>

        {/* Create Account Link */}
        <Link
          to="/register"
          className="text-base font-semibold text-[#299D91] leading-6 hover:underline"
        >
          Create an account
        </Link>
      </div>
    </div>
  )
}

export default LoginForm

