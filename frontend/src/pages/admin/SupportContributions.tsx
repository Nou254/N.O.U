import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Contribution {
  id: number
  amount: number
  currency: string
  status: string
  method: string | null
  receipt_number: string | null
  provider_reference: string | null
  notes: string | null
  paid_at: string | null
  created_at: string
}

const STATUS_BADGE: Record<string, string> = {
  successful: 'badge-success',
  processing: 'badge-warning',
  pending: 'badge-warning',
  failed: 'badge-danger',
  cancelled: 'badge-gray',
}

const AdminSupportContributions = () => {
  const [contributions, setContributions] = useState<Contribution[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')

  const fetchContributions = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (statusFilter) params.append('status_filter', statusFilter)
      const response = await api.get(`/admin/support-contributions?${params}`)
      setContributions(response.data.contributions || [])
    } catch (error) {
      console.error('Error fetching support contributions:', error)
      toast.error('Failed to load support contributions')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchContributions()
  }, [statusFilter])

  const totalCollected = contributions
    .filter((c) => c.status === 'successful')
    .reduce((sum, c) => sum + Number(c.amount || 0), 0)

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Support Contributions</h1>
          <p className="text-gray-600">
            Donations sent from the public footer Support page (M-Pesa / card).
          </p>
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input sm:w-48"
        >
          <option value="">All statuses</option>
          <option value="successful">Successful</option>
          <option value="processing">Processing</option>
          <option value="pending">Pending</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="card">
          <p className="text-xs font-medium text-gray-500 mb-1">Total Collected</p>
          <p className="text-2xl font-bold text-gray-900">
            {totalCollected.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </p>
          <p className="text-xs text-gray-400">KSh</p>
        </div>
        <div className="card">
          <p className="text-xs font-medium text-gray-500 mb-1">Successful</p>
          <p className="text-2xl font-bold text-gray-900">
            {contributions.filter((c) => c.status === 'successful').length}
          </p>
          <p className="text-xs text-gray-400">with receipts</p>
        </div>
        <div className="card">
          <p className="text-xs font-medium text-gray-500 mb-1">Awaiting Confirmation</p>
          <p className="text-2xl font-bold text-gray-900">
            {contributions.filter((c) => ['pending', 'processing'].includes(c.status)).length}
          </p>
          <p className="text-xs text-gray-400">provider pending</p>
        </div>
      </div>

      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : contributions.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-600">No support contributions yet</p>
            <p className="text-sm text-gray-500 mt-1">
              Donations from the public /support page will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {contributions.map((c) => (
              <div
                key={c.id}
                className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-2 flex-wrap">
                      <h3 className="font-semibold text-gray-900">
                        KSh {Number(c.amount).toLocaleString()}
                      </h3>
                      <span className={STATUS_BADGE[c.status] || 'badge-gray'}>{c.status}</span>
                      {c.method && (
                        <span className="text-sm text-gray-500 capitalize">{c.method}</span>
                      )}
                    </div>
                    {c.notes && (
                      <p className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3 mb-3">
                        {c.notes}
                      </p>
                    )}
                    <div className="flex flex-wrap gap-4 text-xs text-gray-500">
                      <span>Received: {new Date(c.created_at).toLocaleString()}</span>
                      {c.paid_at && <span>Paid: {new Date(c.paid_at).toLocaleString()}</span>}
                      {c.receipt_number && (
                        <span className="font-medium text-primary-600">{c.receipt_number}</span>
                      )}
                      {c.provider_reference && (
                        <span>Ref: {c.provider_reference}</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminSupportContributions
