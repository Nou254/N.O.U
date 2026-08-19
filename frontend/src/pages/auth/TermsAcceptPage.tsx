import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAppSelector, useAppDispatch } from '../../hooks/useAppSelector'
import { acceptTerms, logout } from '../../store/authSlice'
import toast from 'react-hot-toast'

const TermsAcceptPage = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { user } = useAppSelector((state) => state.auth)
  const [accepting, setAccepting] = useState(false)

  const dashboardPath = () => {
    switch (user?.role) {
      case 'admin': return '/admin'
      case 'customer': return '/customer'
      case 'applicant': return '/applicant'
      case 'developer': return '/portal'
      case 'investor': return '/investor'
      default: return '/'
    }
  }

  const handleAccept = async () => {
    setAccepting(true)
    try {
      await dispatch(acceptTerms()).unwrap()
      toast.success('Thank you - you have agreed to the terms')
      navigate(dashboardPath(), { replace: true })
    } catch (err) {
      toast.error(err as string)
    } finally {
      setAccepting(false)
    }
  }

  const handleDecline = () => {
    dispatch(logout())
    navigate('/', { replace: true })
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl w-full">
        <div className="card !p-8">
          <div className="flex items-center justify-center mb-4">
            <img src="/favicon.svg" alt="N.O.U logo" className="w-14 h-14 rounded-xl" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 text-center mb-2">
            Agree to our Terms &amp; Privacy Policy
          </h1>
          <p className="text-sm text-gray-600 text-center mb-6">
            Before you can submit your details and use the platform, you must
            review and agree to our terms.
          </p>

          <div className="bg-gray-50 border border-gray-200 rounded-lg p-5 text-sm text-gray-700 leading-relaxed mb-6 space-y-3">
            <p>
              <strong>Customers:</strong> you confirm you are at least 18 years old where required, will
              keep your credentials safe, and accept that software and deliverables are provided under
              the licence stated on each product page or written agreement.
            </p>
            <p>
              <strong>Developers:</strong> engagement is governed by the individual employment or
              engagement agreement and Kenyan employment law. Any minimum contractual period remains
              subject to applicable employment law and lawful termination rights, and company policies
              are enforced with fair procedure.
            </p>
            <p>
              Your personal data is processed in line with our Privacy Policy and the Kenya Data
              Protection Act, 2019.
            </p>
          </div>

          <div className="flex justify-center gap-3 mb-6 text-sm">
            <Link to="/terms" className="text-primary-600 hover:text-primary-700 underline">Read Terms &amp; Conditions</Link>
            <span className="text-gray-300">|</span>
            <Link to="/privacy" className="text-primary-600 hover:text-primary-700 underline">Read Privacy Policy</Link>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <button onClick={handleAccept} disabled={accepting} className="btn-primary px-8">
              {accepting ? 'Saving...' : 'I agree - continue'}
            </button>
            <button onClick={handleDecline} className="btn-outline px-8">
              Decline and sign out
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TermsAcceptPage
