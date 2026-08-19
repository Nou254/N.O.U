import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface ProjectPayment {
  id: string
  payment_type: string
  amount: number | null
  currency: string
  status: string
  method: string
  reference: string | null
  receipt_number: string | null
  verified_at: string | null
  created_at: string
}

interface ProjectRequest {
  id: string
  request_number: string
  title: string
  description: string
  service_type: string | null
  location: string | null
  category: string | null
  status: string
  customer: { id: string; name: string; email: string | null }
  budget: number | null
  deadline: string | null
  admin_notes: string | null
  admin_decision: string | null
  quotation_amount: number | null
  quotation_currency: string | null
  deposit_percent: number | null
  deposit_amount: number | null
  payment_schedule: string | null
  scope_included: string | null
  scope_excluded: string | null
  quotation_version: number | null
  quotation_issued_at: string | null
  quotation_accepted_at: string | null
  agreed_amount: number | null
  paid_amount: number | null
  activated_at: string | null
  created_at: string
  payments: ProjectPayment[]
}

const STATUS_FILTERS = ['', 'submitted', 'under_review', 'quotation_issued', 'awaiting_deposit', 'payment_verified', 'project_activated', 'development', 'completed', 'declined', 'cancelled']

const STATUS_BADGES: Record<string, string> = {
  submitted: 'badge-primary',
  under_review: 'badge-primary',
  clarification_required: 'badge-warning',
  quotation_issued: 'badge-warning',
  awaiting_deposit: 'badge-warning',
  payment_verified: 'badge-success',
  project_activated: 'badge-success',
  development: 'badge-primary',
  completed: 'badge-success',
  declined: 'badge-gray',
  cancelled: 'badge-gray',
}

const formatMoney = (n: number | null, currency?: string | null) => {
  if (n == null) return '-'
  const cur = currency || 'KSh'
  return `${cur} ${Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 })}`
}

const SERVICE_LABELS: Record<string, string> = {
  software_development: 'Software Development',
  wifi_installation: 'Wi-Fi Installation',
  cctv_installation: 'CCTV Installation',
  network_setup: 'Network Setup',
  consultancy: 'Consultancy',
  it_support: 'IT Support & Maintenance',
  maintenance: 'Maintenance',
  other: 'Other',
}

const AdminProjectRequests = () => {
  const [requests, setRequests] = useState<ProjectRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')
  const [selected, setSelected] = useState<ProjectRequest | null>(null)
  const [reviewNote, setReviewNote] = useState('')
  const [quotation, setQuotation] = useState({
    amount: '',
    currency: 'KSh',
    deposit_percent: '30',
    payment_schedule: '',
    scope_included: '',
    scope_excluded: '',
  })
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    fetchRequests()
  }, [statusFilter])

  const fetchRequests = async () => {
    try {
      const response = await api.get('/admin/project-requests', {
        params: statusFilter ? { status_filter: statusFilter } : {},
      })
      setRequests(response.data.requests || [])
    } catch (error) {
      console.error('Error fetching project requests:', error)
    } finally {
      setLoading(false)
    }
  }

  const openRequest = (r: ProjectRequest) => {
    setSelected(r)
    setReviewNote(r.admin_notes || '')
    setQuotation({
      amount: r.quotation_amount != null ? String(r.quotation_amount) : '',
      currency: r.quotation_currency || 'KSh',
      deposit_percent: String(r.deposit_percent ?? 30),
      payment_schedule: r.payment_schedule || '',
      scope_included: r.scope_included || '',
      scope_excluded: r.scope_excluded || '',
    })
  }

  const refreshAndClose = async (message: string, keepOpen = false) => {
    toast.success(message)
    await fetchRequests()
    if (!keepOpen) setSelected(null)
    else {
      // Refresh the selected request too
      const fresh = requests.find((r) => r.id === selected?.id)
      if (fresh) setSelected(fresh)
    }
  }

  const handleReview = async (decision: 'approve' | 'clarify' | 'decline') => {
    if (!selected) return
    setBusy(true)
    try {
      const response = await api.post(`/admin/project-requests/${selected.id}/review`, {
        decision,
        note: reviewNote || undefined,
      })
      await refreshAndClose(response.data?.message || 'Request reviewed', true)
      setSelected(response.data.request)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to review request')
    } finally {
      setBusy(false)
    }
  }

  const handleFeasibility = async (decision: 'feasible' | 'conditions' | 'clarify' | 'not_feasible') => {
    if (!selected) return
    setBusy(true)
    try {
      const response = await api.post(`/admin/project-requests/${selected.id}/feasibility`, {
        decision,
        note: reviewNote || undefined,
      })
      await refreshAndClose(response.data?.message || 'Feasibility recorded', true)
      setSelected(response.data.request)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to record feasibility')
    } finally {
      setBusy(false)
    }
  }

  const handleIssueQuotation = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selected) return
    setBusy(true)
    try {
      const response = await api.post(`/admin/project-requests/${selected.id}/quotation`, {
        quotation_amount: Number(quotation.amount),
        currency: quotation.currency,
        deposit_percent: Number(quotation.deposit_percent),
        payment_schedule: quotation.payment_schedule || undefined,
        scope_included: quotation.scope_included || undefined,
        scope_excluded: quotation.scope_excluded || undefined,
      })
      await refreshAndClose(response.data?.message || 'Quotation issued', true)
      setSelected(response.data.request)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to issue quotation')
    } finally {
      setBusy(false)
    }
  }

  const handleVerifyPayment = async (paymentId: string, approve: boolean) => {
    if (!selected) return
    setBusy(true)
    try {
      const response = await api.post(
        `/admin/project-requests/${selected.id}/payments/${paymentId}/verify`,
        undefined,
        { params: { approve } }
      )
      await refreshAndClose(response.data?.message || (approve ? 'Payment verified' : 'Payment rejected'), true)
      setSelected(response.data.request)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to verify payment')
    } finally {
      setBusy(false)
    }
  }

  const handleAdvanceStatus = async (status: string) => {
    if (!selected) return
    setBusy(true)
    try {
      const response = await api.post(`/admin/project-requests/${selected.id}/status`, { status })
      await refreshAndClose(response.data?.message || 'Status updated', true)
      setSelected(response.data.request)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to update status')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8 flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customer Project Requests</h1>
          <p className="text-gray-600">Review, quote, verify payments and manage the customer quotation workflow.</p>
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input sm:w-56"
        >
          {STATUS_FILTERS.map((s) => (
            <option key={s} value={s}>
              {s ? `Status: ${s.replace('_', ' ')}` : 'All statuses'}
            </option>
          ))}
        </select>
      </div>

      {/* Requests table */}
      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : requests.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">No project requests found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Request</th>
                  <th>Customer</th>
                  <th>Service</th>
                  <th>Budget</th>
                  <th>Quotation</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {requests.map((r) => (
                  <tr key={r.id}>
                    <td>
                      <div>
                        <p className="font-medium text-gray-900">{r.title}</p>
                        <p className="text-xs text-gray-400 font-mono">{r.request_number}</p>
                      </div>
                    </td>
                    <td>
                      <div>
                        <p className="text-sm text-gray-900">{r.customer?.name || '-'}</p>
                        <p className="text-xs text-gray-500">{r.customer?.email || ''}</p>
                      </div>
                    </td>
                    <td>
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
                        {SERVICE_LABELS[r.service_type || 'other'] || 'Software Development'}
                      </span>
                      {r.location && (
                        <p className="text-[11px] text-gray-400 mt-1">{r.location}</p>
                      )}
                    </td>
                    <td>{r.budget != null ? `$${r.budget.toLocaleString()}` : '-'}</td>
                    <td>{formatMoney(r.quotation_amount, r.quotation_currency)}</td>
                    <td>
                      <span className={`badge-primary capitalize ${STATUS_BADGES[r.status] || ''}`}>
                        {r.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td>
                      <button onClick={() => openRequest(r)} className="btn-secondary text-xs">
                        Manage
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Detail modal */}
      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div className="modal-content max-w-2xl max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between mb-1">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">{selected.title}</h2>
                <p className="text-sm text-gray-500 font-mono">{selected.request_number}</p>
              </div>
              <span className={`badge-primary capitalize ${STATUS_BADGES[selected.status] || ''}`}>
                {selected.status.replace('_', ' ')}
              </span>
            </div>
            <p className="text-sm text-gray-500 mb-4">
              {selected.customer?.name} - {selected.customer?.email} | Created{' '}
              {new Date(selected.created_at).toLocaleDateString()}
            </p>
            <div className="flex items-center gap-2 mb-3 flex-wrap">
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
                {SERVICE_LABELS[selected.service_type || 'other'] || 'Software Development'}
              </span>
              {selected.category && (
                <span className="capitalize text-xs text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full">
                  {selected.category.replace('_', ' ')}
                </span>
              )}
              {selected.location && (
                <span className="text-xs text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full">
                  {selected.location}
                </span>
              )}
            </div>
            <p className="text-gray-700 text-sm mb-4">{selected.description}</p>

            <div className="grid grid-cols-3 gap-3 text-sm mb-4">
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-gray-500">Est. budget</p>
                <p className="font-medium">{selected.budget != null ? `$${selected.budget.toLocaleString()}` : '-'}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-gray-500">Quotation</p>
                <p className="font-medium">{formatMoney(selected.quotation_amount, selected.quotation_currency)}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-gray-500">Paid</p>
                <p className="font-medium text-green-600">
                  {formatMoney(selected.paid_amount, selected.quotation_currency)}
                </p>
              </div>
            </div>

            {/* Payments awaiting verification */}
            {selected.payments && selected.payments.filter((p) => p.status === 'pending').length > 0 && (
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Payments awaiting verification</h3>
                <div className="space-y-2">
                  {selected.payments.filter((p) => p.status === 'pending').map((p) => (
                    <div key={p.id} className="flex items-center justify-between border border-amber-200 bg-amber-50 rounded-lg px-3 py-2 text-sm">
                      <div>
                        <span className="font-medium capitalize">{p.payment_type}</span>
                        <span className="text-gray-600 mx-2">
                          {formatMoney(p.amount, p.currency)} via {p.method}
                        </span>
                        {p.reference && <span className="text-gray-400 text-xs">Ref: {p.reference}</span>}
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleVerifyPayment(p.id, true)}
                          disabled={busy}
                          className="btn-primary text-xs"
                        >
                          Verify
                        </button>
                        <button
                          onClick={() => handleVerifyPayment(p.id, false)}
                          disabled={busy}
                          className="btn-outline text-xs text-red-600 border-red-300"
                        >
                          Reject
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Payment history */}
            {selected.payments && selected.payments.filter((p) => p.status !== 'pending').length > 0 && (
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Payment history</h3>
                <div className="space-y-1">
                  {selected.payments.filter((p) => p.status !== 'pending').map((p) => (
                    <div key={p.id} className="flex items-center justify-between text-sm border border-gray-100 rounded-lg px-3 py-1.5">
                      <span className="text-gray-600">
                        {formatMoney(p.amount, p.currency)} via {p.method}
                      </span>
                      <div className="flex items-center gap-3">
                        {p.receipt_number && (
                          <span className="text-xs font-mono text-primary-600 bg-primary-50 px-2 py-0.5 rounded">
                            {p.receipt_number}
                          </span>
                        )}
                        <span className={`text-xs capitalize ${p.status === 'successful' ? 'text-green-600' : 'text-red-600'}`}>
                          {p.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Admin note */}
            <div className="mb-4">
              <label className="label">Admin notes</label>
              <textarea
                value={reviewNote}
                onChange={(e) => setReviewNote(e.target.value)}
                rows={2}
                className="input"
                placeholder="Notes for the customer or internal record"
              />
            </div>

            {/* Initial review actions */}
            {['submitted', 'under_review', 'clarification_required'].includes(selected.status) && (
              <div className="flex flex-wrap gap-2 mb-4">
                <button onClick={() => handleReview('approve')} disabled={busy} className="btn-primary text-sm">
                  Approve for technical review
                </button>
                <button onClick={() => handleReview('clarify')} disabled={busy} className="btn-secondary text-sm">
                  Request clarification
                </button>
                <button onClick={() => handleReview('decline')} disabled={busy} className="btn-outline text-sm text-red-600 border-red-300">
                  Decline request
                </button>
              </div>
            )}

            {/* Feasibility actions */}
            {['technically_feasible', 'documentation', 'estimation'].includes(selected.status) && (
              <div className="flex flex-wrap gap-2 mb-4">
                <button onClick={() => handleFeasibility('feasible')} disabled={busy} className="btn-primary text-sm">
                  Feasible - prepare quotation
                </button>
                <button onClick={() => handleFeasibility('conditions')} disabled={busy} className="btn-secondary text-sm">
                  Feasible with conditions
                </button>
                <button onClick={() => handleFeasibility('clarify')} disabled={busy} className="btn-secondary text-sm">
                  Clarify requirements
                </button>
                <button onClick={() => handleFeasibility('not_feasible')} disabled={busy} className="btn-outline text-sm text-red-600 border-red-300">
                  Not feasible
                </button>
              </div>
            )}

            {/* Quotation form */}
            {['technically_feasible', 'documentation', 'estimation'].includes(selected.status) && (
              <form onSubmit={handleIssueQuotation} className="border border-gray-200 rounded-lg p-4 mb-4 space-y-3">
                <h3 className="text-sm font-semibold text-gray-700">Issue Quotation</h3>
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="label">Amount</label>
                    <input
                      type="number"
                      min={1}
                      required
                      value={quotation.amount}
                      onChange={(e) => setQuotation({ ...quotation, amount: e.target.value })}
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="label">Currency</label>
                    <select
                      value={quotation.currency}
                      onChange={(e) => setQuotation({ ...quotation, currency: e.target.value })}
                      className="input"
                    >
                      <option value="KSh">KSh</option>
                      <option value="USD">USD</option>
                    </select>
                  </div>
                  <div>
                    <label className="label">Deposit %</label>
                    <input
                      type="number"
                      min={0}
                      max={100}
                      value={quotation.deposit_percent}
                      onChange={(e) => setQuotation({ ...quotation, deposit_percent: e.target.value })}
                      className="input"
                    />
                  </div>
                </div>
                <div>
                  <label className="label">Payment schedule</label>
                  <input
                    type="text"
                    value={quotation.payment_schedule}
                    onChange={(e) => setQuotation({ ...quotation, payment_schedule: e.target.value })}
                    className="input"
                    placeholder="e.g. 30% deposit, 40% mid-development, 30% on delivery"
                  />
                </div>
                <div>
                  <label className="label">Scope included</label>
                  <textarea
                    value={quotation.scope_included}
                    onChange={(e) => setQuotation({ ...quotation, scope_included: e.target.value })}
                    rows={2}
                    className="input"
                  />
                </div>
                <div>
                  <label className="label">Scope excluded</label>
                  <textarea
                    value={quotation.scope_excluded}
                    onChange={(e) => setQuotation({ ...quotation, scope_excluded: e.target.value })}
                    rows={2}
                    className="input"
                  />
                </div>
                <button type="submit" disabled={busy} className="btn-primary text-sm">
                  Issue Quotation
                </button>
              </form>
            )}

            {/* Status advancement */}
            {['awaiting_deposit', 'payment_verified', 'project_activated', 'development', 'testing', 'delivery'].includes(selected.status) && (
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Advance status</h3>
                <div className="flex flex-wrap gap-2">
                  {['payment_verified', 'project_activated', 'development', 'testing', 'delivery', 'completed'].map((s) => (
                    <button
                      key={s}
                      onClick={() => handleAdvanceStatus(s)}
                      disabled={busy}
                      className={`btn-secondary text-xs ${selected.status === s ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                      {s.replace('_', ' ')}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="flex justify-end pt-4 border-t border-gray-100">
              <button onClick={() => setSelected(null)} className="btn-secondary text-sm">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminProjectRequests