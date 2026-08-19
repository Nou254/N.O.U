import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Complaint {
  id: number
  full_name: string
  email: string
  phone: string | null
  subject: string
  category: string
  message: string
  status: string
  admin_notes: string | null
  created_at: string | null
  updated_at: string | null
  resolved_at: string | null
}

const STATUSES = ['new', 'in_progress', 'resolved', 'closed'] as const

const AdminComplaints = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([])
  const [pagination, setPagination] = useState({ total: 0, page: 1, limit: 20, pages: 0 })
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [editing, setEditing] = useState<Complaint | null>(null)
  const [updatingId, setUpdatingId] = useState<number | null>(null)

  const fetchComplaints = async (page = 1, status = statusFilter) => {
    setLoading(true)
    try {
      const params = new URLSearchParams({ page: String(page), limit: String(pagination.limit) })
      if (status) params.set('status_filter', status)
      const response = await api.get(`/admin/complaints?${params.toString()}`)
      setComplaints(response.data.complaints || [])
      setPagination(response.data.pagination)
    } catch (error) {
      console.error('Error fetching complaints:', error)
      toast.error('Failed to load complaints')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchComplaints(1, '')
  }, [])

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editing) return
    setUpdatingId(editing.id)
    try {
      await api.put(`/admin/complaints/${editing.id}/status`, {
        status: editing.status,
        admin_notes: editing.admin_notes || undefined,
      })
      toast.success('Complaint updated')
      setEditing(null)
      fetchComplaints(pagination.page, statusFilter)
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to update complaint')
    } finally {
      setUpdatingId(null)
    }
  }

  const statusBadge = (status: string) => {
    switch (status) {
      case 'new':
        return <span className="badge-danger">New</span>
      case 'in_progress':
        return <span className="badge-primary">In progress</span>
      case 'resolved':
        return <span className="badge-success">Resolved</span>
      case 'closed':
        return <span className="badge-gray">Closed</span>
      default:
        return <span className="badge-gray">{status}</span>
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8 flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Complaints</h1>
          <p className="text-gray-600">
            Complaints forwarded from the public Complaints screen. Review them,
            update their status and add your notes.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value)
              fetchComplaints(1, e.target.value)
            }}
            className="input !w-auto text-sm"
          >
            <option value="">All statuses</option>
            {STATUSES.map((s) => (
              <option key={s} value={s}>{s.replace('_', ' ')}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12"><div className="spinner mx-auto"></div></div>
      ) : complaints.length === 0 ? (
        <div className="card text-center py-12">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No complaints</h3>
          <p className="text-gray-600">
            {statusFilter ? 'No complaints with this status.' : 'Complaints submitted from the website will appear here.'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {complaints.map((complaint) => (
            <div key={complaint.id} className="card">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2 flex-wrap">
                    <h3 className="font-semibold text-gray-900">{complaint.subject}</h3>
                    {statusBadge(complaint.status)}
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                      {complaint.category}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-1">
                    <strong>{complaint.full_name}</strong> · {complaint.email}
                    {complaint.phone ? ` · ${complaint.phone}` : ''}
                  </p>
                  <p className="text-xs text-gray-400 mb-3">
                    Submitted {complaint.created_at ? new Date(complaint.created_at).toLocaleString() : '—'}
                    {complaint.resolved_at ? ` · Resolved ${new Date(complaint.resolved_at).toLocaleString()}` : ''}
                  </p>
                  <p className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3 whitespace-pre-wrap">
                    {complaint.message}
                  </p>
                  {complaint.admin_notes && (
                    <p className="text-sm text-primary-800 bg-primary-50 border border-primary-200 rounded-lg p-3 mt-3">
                      <strong>Your notes:</strong> {complaint.admin_notes}
                    </p>
                  )}
                </div>
                <button
                  onClick={() => setEditing(complaint)}
                  className="btn-secondary text-sm shrink-0"
                >
                  Review / Update
                </button>
              </div>
            </div>
          ))}

          {/* Pagination */}
          {pagination.pages > 1 && (
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-gray-500">
                Page {pagination.page} of {pagination.pages} ({pagination.total} complaints)
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => fetchComplaints(pagination.page - 1)}
                  disabled={pagination.page <= 1}
                  className="btn-secondary text-sm"
                >
                  Previous
                </button>
                <button
                  onClick={() => fetchComplaints(pagination.page + 1)}
                  disabled={pagination.page >= pagination.pages}
                  className="btn-secondary text-sm"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Update modal */}
      {editing && (
        <div className="modal-overlay" onClick={() => setEditing(null)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-1">Review complaint</h2>
            <p className="text-sm text-gray-500 mb-4">
              {editing.subject} — from {editing.full_name} ({editing.email})
            </p>
            <form onSubmit={handleUpdate} className="space-y-4">
              <div>
                <label htmlFor="complaint-status" className="label">Status</label>
                <select
                  id="complaint-status"
                  value={editing.status}
                  onChange={(e) => setEditing({ ...editing, status: e.target.value })}
                  className="input"
                >
                  {STATUSES.map((s) => (
                    <option key={s} value={s}>{s.replace('_', ' ')}</option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="admin-notes" className="label">Admin notes (optional)</label>
                <textarea
                  id="admin-notes"
                  value={editing.admin_notes || ''}
                  onChange={(e) => setEditing({ ...editing, admin_notes: e.target.value })}
                  rows={3}
                  className="input"
                  placeholder="e.g. Called the complainant - issue resolved after refund."
                />
              </div>
              <div className="flex justify-end space-x-3 pt-2">
                <button type="button" onClick={() => setEditing(null)} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" disabled={updatingId === editing.id} className="btn-primary">
                  {updatingId === editing.id ? 'Saving...' : 'Save'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminComplaints
