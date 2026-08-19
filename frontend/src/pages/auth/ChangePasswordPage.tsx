import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../../services/authService'
import toast from 'react-hot-toast'

const ChangePasswordPage = () => {
  const navigate = useNavigate()
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (newPassword !== confirmPassword) {
      toast.error('New passwords do not match')
      return
    }
    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }
    if (newPassword === currentPassword) {
      toast.error('New password must be different from the current password')
      return
    }

    setLoading(true)
    try {
      await authService.changePassword(currentPassword, newPassword)
      toast.success('Password changed successfully')
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Could not change password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Change password</h1>
        <p className="text-gray-600">Update the password for your account.</p>
      </div>

      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="currentPassword" className="label">Current password</label>
            <input
              id="currentPassword"
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              required
              className="input"
              placeholder="Enter your current password"
            />
          </div>

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
            <p className="mt-1 text-xs text-gray-500">
              Minimum 8 characters, including an uppercase letter, a lowercase letter, and a number.
            </p>
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

          <div className="flex items-center justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? 'Updating...' : 'Change password'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ChangePasswordPage
