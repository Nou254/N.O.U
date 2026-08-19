import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppSelector, useAppDispatch } from '../../hooks/useAppSelector'
import { acceptPolicies, logout } from '../../store/authSlice'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface PolicyDoc {
  title: string
  content: string
  version: string
  updated_at: string | null
}

const PoliciesAcceptPage = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { user } = useAppSelector((state) => state.auth)
  const [policy, setPolicy] = useState<PolicyDoc | null>(null)
  const [loading, setLoading] = useState(true)
  const [accepting, setAccepting] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    api
      .get('/policies/')
      .then((res) => setPolicy(res.data))
      .catch(() => toast.error('Could not load the organization policies'))
      .finally(() => setLoading(false))
  }, [])

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
    if (!scrolled) {
      toast.error('Please read through the document before agreeing')
      return
    }
    setAccepting(true)
    try {
      await dispatch(acceptPolicies()).unwrap()
      toast.success('Thank you - you have agreed to the organization policies')
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

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const el = e.currentTarget
    if (el.scrollTop + el.clientHeight >= el.scrollHeight - 40) {
      setScrolled(true)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl w-full">
        <div className="card !p-8">
          <div className="flex items-center justify-center mb-4">
            <img src="/favicon.svg" alt="N.O.U logo" className="w-14 h-14 rounded-xl" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 text-center mb-2">
            {policy?.title || 'N.O.U. Organization Policies'}
          </h1>
          <p className="text-sm text-gray-600 text-center mb-6">
            As an approved member of N.O.U. Digital Systems you must review the
            organization policies below and agree to them before using the platform.
            This document remains available on your category page for future reference.
          </p>

          {loading ? (
            <div className="text-center py-16">
              <div className="spinner mx-auto"></div>
              <p className="text-sm text-gray-500 mt-4">Loading the policies document...</p>
            </div>
          ) : (
            <div
              onScroll={handleScroll}
              className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-sm text-gray-700 leading-relaxed max-h-[55vh] overflow-y-auto whitespace-pre-wrap mb-4"
            >
              {policy?.content || 'The organization policies document is not available right now.'}
            </div>
          )}

          {!loading && (
            <p className="text-xs text-gray-500 mb-6">
              {policy?.version ? `Version ${policy.version} · ` : ''}
              {scrolled ? '✓ You have reached the end of the document' : 'Scroll to the end of the document to enable the agree button'}
            </p>
          )}

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <button onClick={handleAccept} disabled={accepting || loading} className="btn-primary px-8">
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

export default PoliciesAcceptPage
