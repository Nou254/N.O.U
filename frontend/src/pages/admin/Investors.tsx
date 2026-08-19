import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface InvestorInterest {
  id: number
  full_name: string
  email: string
  phone: string | null
  country: string
  organization: string | null
  investment_amount: number | null
  investment_range: string | null
  monthly_investment: number | null
  expectations: string | null
  risk_knowledge: string | null
  message: string | null
  status: string
  created_at: string
}

const STATUS_OPTIONS = [
  { value: 'new', label: 'New', color: 'badge-primary' },
  { value: 'contacted', label: 'Contacted', color: 'badge-warning' },
  { value: 'declined', label: 'Declined', color: 'badge-danger' },
  { value: 'closed', label: 'Closed', color: 'badge-gray' },
]

const AdminInvestors = () => {
  const [interests, setInterests] = useState<InvestorInterest[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')
  const [selected, setSelected] = useState<InvestorInterest | null>(null)

  const fetchInterests = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (statusFilter) params.append('status_filter', statusFilter)
      const response = await api.get(`/admin/investors?${params}`)
      setInterests(response.data.interests)
    } catch (error) {
      console.error('Error fetching investor interests:', error)
      toast.error('Failed to load investor interests')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchInterests()
  }, [statusFilter])

  const handleStatusChange = async (interest: InvestorInterest, status: string) => {
    try {
      await api.put(`/admin/investors/${interest.id}/status`, { status })
      toast.success('Status updated')
      setSelected((prev) => (prev && prev.id === interest.id ? { ...prev, status } : prev))
      fetchInterests()
    } catch (error) {
      toast.error('Failed to update status')
    }
  }

  const formatAmount = (amount: number | null) => {
    if (!amount) return '—'
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const statusColor = (status: string) => {
    return STATUS_OPTIONS.find((s) => s.value === status)?.color || 'badge-gray'
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Investor Interests</h1>
          <p className="text-gray-600">Funding inquiries submitted from the public investors page.</p>
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input sm:w-48"
        >
          <option value="">All statuses</option>
          {STATUS_OPTIONS.map((s) => (
            <option key={s.value} value={s.value}>
              {s.label}
            </option>
          ))}
        </select>
      </div>

      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : interests.length === 0 ? (
          <div className="text-center py-12">
            <svg
              className="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-600">No investor interests yet</p>
            <p className="text-sm text-gray-500 mt-1">
              Submissions from the /investors page will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {interests.map((interest) => (
              <div
                key={interest.id}
                className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-2 flex-wrap">
                      <h3 className="font-semibold text-gray-900">{interest.full_name}</h3>
                      <span className={statusColor(interest.status)}>
                        {interest.status}
                      </span>
                      {interest.organization && (
                        <span className="text-sm text-gray-500">{interest.organization}</span>
                      )}
                    </div>
                    <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                        {interest.email}
                      </span>
                      {interest.phone && (
                        <span className="flex items-center gap-1">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                          </svg>
                          {interest.phone}
                        </span>
                      )}
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {interest.country}
                      </span>
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {interest.investment_range || formatAmount(interest.investment_amount)}
                      </span>
                    </div>
                    {interest.message && (
                      <p className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3 mb-3">
                        {interest.message}
                      </p>
                    )}
                    <p className="text-xs text-gray-400">
                      Received: {new Date(interest.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-2 shrink-0">
                    <select
                      value={interest.status}
                      onChange={(e) => handleStatusChange(interest, e.target.value)}
                      className="input text-sm !w-auto"
                    >
                      {STATUS_OPTIONS.map((s) => (
                        <option key={s.value} value={s.value}>{s.label}</option>
                      ))}
                    </select>
                    <button
                      onClick={() => setSelected(interest)}
                      className="btn-secondary text-sm"
                    >
                      View details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Detail modal */}
      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Investor Details
            </h2>
            <div className="space-y-3">
              {[
                ['Full name', selected.full_name],
                ['Email', selected.email],
                ['Phone', selected.phone || '—'],
                ['Country', selected.country],
                ['Organization', selected.organization || '—'],
                ['Investment range', selected.investment_range || formatAmount(selected.investment_amount)],
                ['Monthly investment', selected.monthly_investment
                  ? `KSh ${Number(selected.monthly_investment).toLocaleString()}`
                  : '—'],
                ['Risk knowledge', selected.risk_knowledge || '—'],
                ['Status', selected.status],
                ['Received', new Date(selected.created_at).toLocaleString()],
              ].map(([label, value]) => (
                <div key={label} className="flex justify-between gap-4">
                  <span className="text-sm text-gray-500">{label}</span>
                  <span className="text-sm font-medium text-gray-900 text-right">{value}</span>
                </div>
              ))}
              {selected.expectations && (
                <div className="pt-3 border-t border-gray-200">
                  <p className="text-sm text-gray-500 mb-2">Expectations while joining</p>
                  <p className="text-sm text-gray-800 bg-gray-50 rounded-lg p-3">{selected.expectations}</p>
                </div>
              )}
              {selected.message && (
                <div className="pt-3 border-t border-gray-200">
                  <p className="text-sm text-gray-500 mb-2">Message / Requirements</p>
                  <p className="text-sm text-gray-800 bg-gray-50 rounded-lg p-3">{selected.message}</p>
                </div>
              )}
            </div>
            <div className="mt-6 flex justify-end">
              <button onClick={() => setSelected(null)} className="btn-secondary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminInvestors
