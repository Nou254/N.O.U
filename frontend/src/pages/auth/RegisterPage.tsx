import { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '../../hooks/useAppSelector'
import { register, verifyRegistration } from '../../store/authSlice'
import { authService } from '../../services/authService'
import toast from 'react-hot-toast'

// Persist form state across refresh so the user never loses progress.
const STORAGE_KEY = 'nou.register.form'

function loadPersisted() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* ignore */ }
  return null
}

const RegisterPage = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { loading, error } = useAppSelector((state) => state.auth)

  const persisted = loadPersisted()
  const [step, setStep] = useState<'form' | 'otp'>(persisted?.step || 'form')
  const [formData, setFormData] = useState({
    firstName: persisted?.firstName || '',
    lastName: persisted?.lastName || '',
    email: persisted?.email || '',
    password: persisted?.password || '',
    confirmPassword: '',
  })
  const [otp, setOtp] = useState('')
  const [agreeTerms, setAgreeTerms] = useState(false)

  // Save form state to sessionStorage on every change.
  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
        step,
        firstName: formData.firstName,
        lastName: formData.lastName,
        email: formData.email,
        password: formData.password,
      }))
    } catch { /* ignore */ }
  }, [step, formData])

  // Lock browser back button while on OTP step.
  useEffect(() => {
    if (step !== 'otp') return
    window.history.pushState(null, '', window.location.href)
    const handler = () => {
      window.history.pushState(null, '', window.location.href)
    }
    window.addEventListener('popstate', handler)
    return () => window.removeEventListener('popstate', handler)
  }, [step])

  // Clear persisted state on success.
  const clearPersist = useCallback(() => {
    try { sessionStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }

    if (formData.password.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }

    if (!agreeTerms) {
      toast.error('Please read and agree to the Terms & Privacy Policy to continue')
      return
    }

    try {
      const result = await dispatch(register({
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName,
        lastName: formData.lastName,
      })).unwrap()

      if ((result as any).requires_otp) {
        setStep('otp')
        toast.success('Verification code sent to your email')
        return
      }

      clearPersist()
      toast.success('Registration successful! Please login.')
      navigate('/login')
    } catch (err) {
      toast.error(err as string)
    }
  }

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await dispatch(verifyRegistration({ email: formData.email, otp })).unwrap()
      clearPersist()
      toast.success('Account verified! Please sign in.')
      navigate('/login')
    } catch (err) {
      toast.error(err as string)
    }
  }

  const handleResend = async () => {
    try {
      await authService.resendOtp(formData.email, 'register')
      toast.success('A new code has been sent')
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Could not resend code')
    }
  }

  return (
    <div className="min-h-screen flex items-start sm:items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="mb-4">
          <Link to="/" className="inline-flex items-center text-sm text-gray-600 hover:text-primary-600 transition-colors">
            <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to home
          </Link>
        </div>
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center space-x-2 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-600 to-primary-800 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">N</span>
            </div>
            <span className="text-2xl font-bold text-gray-900">N.O.U Digital</span>
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">
            {step === 'form' ? 'Create an account' : 'Verify your email'}
          </h1>
          <p className="text-gray-600 mt-2">
            {step === 'form'
              ? 'Join N.O.U Digital Systems today'
              : `A verification code was sent to ${formData.email}`}
          </p>
        </div>

        <div className="card">
          {step === 'form' ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  {error}
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="firstName" className="label">First name</label>
                  <input
                    id="firstName"
                    name="firstName"
                    type="text"
                    value={formData.firstName}
                    onChange={handleChange}
                    required
                    className="input"
                    placeholder="John"
                  />
                </div>
                <div>
                  <label htmlFor="lastName" className="label">Last name</label>
                  <input
                    id="lastName"
                    name="lastName"
                    type="text"
                    value={formData.lastName}
                    onChange={handleChange}
                    required
                    className="input"
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="email" className="label">Email address</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="input"
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label htmlFor="password" className="label">Password</label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="input"
                  placeholder="8+ chars with uppercase, lowercase & number"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Minimum 8 characters, including an uppercase letter, a lowercase letter, and a number.
                </p>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="label">Confirm password</label>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  className="input"
                  placeholder="Confirm your password"
                />
              </div>

              <label className="flex items-start gap-3 text-sm text-gray-600 cursor-pointer">
                <input
                  type="checkbox"
                  checked={agreeTerms}
                  onChange={(e) => setAgreeTerms(e.target.checked)}
                  className="mt-0.5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span>
                  I have read and agree to the{' '}
                  <Link to="/terms" target="_blank" className="text-primary-600 hover:text-primary-700 underline">
                    Terms &amp; Conditions
                  </Link>{' '}
                  and{' '}
                  <Link to="/privacy" target="_blank" className="text-primary-600 hover:text-primary-700 underline">
                    Privacy Policy
                  </Link>
                  , including the minimum investment period and developer contract terms.
                </span>
              </label>

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary py-3"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <span className="spinner mr-2"></span>
                    Creating account...
                  </span>
                ) : (
                  'Create account'
                )}
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOtp} className="space-y-6">
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  {error}
                </div>
              )}

              <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg">
                <p className="text-sm text-primary-800">
                  Your account will only be created after you verify the 6-character code
                  emailed to <strong>{formData.email}</strong>.
                </p>
              </div>

              <div>
                <label htmlFor="otp" className="label">Verification code</label>
                <input
                  id="otp"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  required
                  className="input text-center text-xl tracking-[0.5em] font-mono"
                  placeholder="••••••"
                  maxLength={10}
                />
              </div>

              <button type="submit" disabled={loading} className="w-full btn-primary py-3">
                {loading ? (
                  <span className="flex items-center justify-center">
                    <span className="spinner mr-2"></span>
                    Verifying...
                  </span>
                ) : (
                  'Verify & finish'
                )}
              </button>

              <div className="text-center">
                <button
                  type="button"
                  onClick={handleResend}
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  Resend code
                </button>
                <button
                  type="button"
                  onClick={() => setStep('form')}
                  className="text-sm text-gray-500 hover:text-gray-700 ml-4"
                >
                  Back
                </button>
              </div>
            </form>
          )}

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
