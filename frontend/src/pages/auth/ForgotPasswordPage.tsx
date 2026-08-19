import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { authService } from '../../services/authService'
import toast from 'react-hot-toast'

// Persist form state across refresh so the user never loses progress.
const STORAGE_KEY = 'nou.forgotpw.form'

function loadPersisted() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* ignore */ }
  return null
}

type Step = 'email' | 'otp' | 'newpassword'

const ForgotPasswordPage = () => {
  const navigate = useNavigate()
  const persisted = loadPersisted()
  const [step, setStep] = useState<Step>(persisted?.step || 'email')
  const [email, setEmail] = useState(persisted?.email || '')
  const [otp, setOtp] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)

  // Save form state to sessionStorage on every change.
  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ step, email }))
    } catch { /* ignore */ }
  }, [step, email])

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

  const handleSendCode = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await authService.forgotPassword(email)
      setStep('otp')
      toast.success('If that email is registered, a reset code has been sent')
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault()
    setStep('newpassword')
  }

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault()
    if (newPassword !== confirmPassword) {
      toast.error('Passwords do not match')
      return
    }
    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }
    setLoading(true)
    try {
      await authService.resetPassword(email, otp, newPassword)
      try { sessionStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
      toast.success('Password reset successful. Please sign in.')
      navigate('/login')
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Reset failed')
    } finally {
      setLoading(false)
    }
  }

  const handleResend = async () => {
    try {
      await authService.resendOtp(email, 'reset')
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
            {step === 'email' && 'Reset your password'}
            {step === 'otp' && 'Enter verification code'}
            {step === 'newpassword' && 'Choose a new password'}
          </h1>
          <p className="text-gray-600 mt-2">
            {step === 'email' && 'Enter your email and we will send you a reset code'}
            {step === 'otp' && `A code was sent to ${email}`}
            {step === 'newpassword' && 'Minimum 8 characters with uppercase, lowercase and a number'}
          </p>
        </div>

        <div className="card">
          {step === 'email' && (
            <form onSubmit={handleSendCode} className="space-y-6">
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
              <button type="submit" disabled={loading} className="w-full btn-primary py-3">
                {loading ? 'Sending...' : 'Send reset code'}
              </button>
            </form>
          )}

          {step === 'otp' && (
            <form onSubmit={handleVerifyOtp} className="space-y-6">
              <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg">
                <p className="text-sm text-primary-800">
                  Enter the 6-character code emailed to <strong>{email}</strong>.
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
              <button type="submit" className="w-full btn-primary py-3">Continue</button>
              <div className="text-center">
                <button
                  type="button"
                  onClick={handleResend}
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  Resend code
                </button>
              </div>
            </form>
          )}

          {step === 'newpassword' && (
            <form onSubmit={handleReset} className="space-y-6">
              <div>
                <label htmlFor="newPassword" className="label">New password</label>
                <input
                  id="newPassword"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  className="input"
                  placeholder="8+ chars with uppercase, lowercase & number"
                />
              </div>
              <div>
                <label htmlFor="confirmPassword" className="label">Confirm new password</label>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  className="input"
                  placeholder="Confirm your new password"
                />
              </div>
              <button type="submit" disabled={loading} className="w-full btn-primary py-3">
                {loading ? 'Resetting...' : 'Reset password'}
              </button>
            </form>
          )}

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Remembered it?{' '}
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

export default ForgotPasswordPage
