import { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '../../hooks/useAppSelector'
import { login, verifyLoginOtp } from '../../store/authSlice'
import { authService } from '../../services/authService'
import toast from 'react-hot-toast'

// Persist form state across refresh so the user never loses progress.
const STORAGE_KEY = 'nou.login.form'

function loadPersisted() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* ignore */ }
  return null
}

const LoginPage = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { loading, error } = useAppSelector((state) => state.auth)

  const persisted = loadPersisted()
  const [step, setStep] = useState<'credentials' | 'otp'>(persisted?.step || 'credentials')
  const [email, setEmail] = useState(persisted?.email || '')
  const [password, setPassword] = useState(persisted?.password || '')
  const [otp, setOtp] = useState('')

  // Save form state to sessionStorage on every change so refresh preserves it.
  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ step, email, password }))
    } catch { /* ignore */ }
  }, [step, email, password])

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

  // Clear persisted state on successful login.
  const clearPersist = useCallback(() => {
    try { sessionStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
  }, [])

  const redirectByRole = (role: string) => {
    clearPersist()
    switch (role) {
      case 'admin':
        navigate('/admin')
        break
      case 'customer':
        navigate('/customer')
        break
      case 'applicant':
        navigate('/applicant')
        break
      case 'developer':
        navigate('/portal')
        break
      case 'investor':
        navigate('/investor')
        break
      default:
        navigate('/')
    }
  }

  const handleCredentialsSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const result = await dispatch(login({ email, password })).unwrap()
      if ((result as any).requiresOtp) {
        setStep('otp')
        toast.success('Verification code sent to your email')
        return
      }
      toast.success('Login successful!')
      redirectByRole((result as any).user?.role)
    } catch (err) {
      toast.error(err as string)
    }
  }

  const handleOtpSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const result = await dispatch(verifyLoginOtp({ email, otp })).unwrap()
      toast.success('Login successful!')
      redirectByRole((result as any).user?.role)
    } catch (err) {
      toast.error(err as string)
    }
  }

  const handleResend = async () => {
    try {
      await authService.resendOtp(email, 'login')
      toast.success('A new code has been sent')
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Could not resend code')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center space-x-2 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-600 to-primary-800 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">N</span>
            </div>
            <span className="text-2xl font-bold text-gray-900">N.O.U Digital</span>
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">
            {step === 'credentials' ? 'Welcome back' : 'Verify your identity'}
          </h1>
          <p className="text-gray-600 mt-2">
            {step === 'credentials'
              ? 'Sign in to your account'
              : `Enter the code sent to ${email}`}
          </p>
        </div>

        <div className="card">
          {step === 'credentials' ? (
            <form onSubmit={handleCredentialsSubmit} className="space-y-6">
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  {error}
                </div>
              )}

              <div>
                <label htmlFor="email" className="label">Email address</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="input"
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label htmlFor="password" className="label">Password</label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="input"
                  placeholder="Enter your password"
                />
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500"></span>
                <Link to="/forgot-password" className="text-sm text-primary-600 hover:text-primary-700">
                  Forgot password?
                </Link>
              </div>

              <button type="submit" disabled={loading} className="w-full btn-primary py-3">
                {loading ? (
                  <span className="flex items-center justify-center">
                    <span className="spinner mr-2"></span>
                    Signing in...
                  </span>
                ) : (
                  'Sign in'
                )}
              </button>
            </form>
          ) : (
            <form onSubmit={handleOtpSubmit} className="space-y-6">
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  {error}
                </div>
              )}

              <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg">
                <p className="text-sm text-primary-800">
                  A 6-character verification code has been sent to <strong>{email}</strong>.
                  Enter it below to complete sign-in.
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
                  'Verify & Sign in'
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
                  onClick={() => setStep('credentials')}
                  className="text-sm text-gray-500 hover:text-gray-700 ml-4"
                >
                  Back
                </button>
              </div>
            </form>
          )}

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Don't have an account?{' '}
              <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage