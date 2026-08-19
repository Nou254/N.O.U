import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Order {
  id: number
  customer_id: number
  order_type: string
  summary: string
  details: string
  status: string
  ai_transcript: string | null
  created_at: string
}

const TYPE_BADGE: Record<string, string> = {
  product: 'badge-primary',
  project: 'badge-warning',
  support: 'badge-info',
  inquiry: 'badge-gray',
}

const STATUS_OPTIONS = [
  { value: 'new', label: 'New', color: 'badge-primary' },
  { value: 'in_progress', label: 'In progress', color: 'badge-warning' },
  { value: 'completed', label: 'Completed', color: 'badge-success' },
  { value: 'declined', label: 'Declined', color: 'badge-danger' },
]

const AdminNouLiteOrders = () => {
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')
  const [selected, setSelected] = useState<Order | null>(null)

  const fetchOrders = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (statusFilter) params.append('status_filter', statusFilter)
      const response = await api.get(`/admin/nou-lite/orders?${params}`)
      setOrders(response.data.orders)
    } catch (error) {
      console.error('Error fetching orders:', error)
      toast.error('Failed to load orders')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchOrders()
  }, [statusFilter])

  const handleStatusChange = async (order: Order, status: string) => {
    try {
      await api.put(`/admin/nou-lite/orders/${order.id}/status`, { status })
      toast.success('Status updated')
      setSelected((prev) => (prev && prev.id === order.id ? { ...prev, status } : prev))
      fetchOrders()
    } catch (error) {
      toast.error('Failed to update status')
    }
  }

  const parseDetails = (details: string): Record<string, string> => {
    try {
      return JSON.parse(details)
    } catch {
      return {}
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">N.O.U Lite Orders</h1>
          <p className="text-gray-600">
            Orders placed by customers through the N.O.U Lite AI assistant.
          </p>
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input sm:w-48"
        >
          <option value="">All statuses</option>
          {STATUS_OPTIONS.map((s) => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>
      </div>

      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : orders.length === 0 ? (
          <div className="text-center py-12">
            <svg
              className="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <p className="text-gray-600">No N.O.U Lite orders yet</p>
            <p className="text-sm text-gray-500 mt-1">
              Customer orders placed via the AI assistant will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => {
              const details = parseDetails(order.details)
              return (
                <div
                  key={order.id}
                  className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2 flex-wrap">
                        <span className={TYPE_BADGE[order.order_type] || 'badge-gray'}>
                          {order.order_type}
                        </span>
                        <span className={STATUS_OPTIONS.find((s) => s.value === order.status)?.color || 'badge-gray'}>
                          {order.status.replace('_', ' ')}
                        </span>
                        <span className="text-xs text-gray-400">Customer #{order.customer_id}</span>
                      </div>
                      <h3 className="font-medium text-gray-900 mb-1">{order.summary}</h3>
                      {Object.entries(details).length > 0 && (
                        <div className="flex flex-wrap gap-x-4 gap-y-1 text-sm text-gray-600 mb-2">
                          {Object.entries(details).map(([k, v]) => (
                            <span key={k}><span className="capitalize text-gray-400">{k}:</span> {v}</span>
                          ))}
                        </div>
                      )}
                      <p className="text-xs text-gray-400">
                        {new Date(order.created_at).toLocaleString()}
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-2 shrink-0">
                      <select
                        value={order.status}
                        onChange={(e) => handleStatusChange(order, e.target.value)}
                        className="input text-sm !w-auto"
                      >
                        {STATUS_OPTIONS.map((s) => (
                          <option key={s.value} value={s.value}>{s.label}</option>
                        ))}
                      </select>
                      {order.ai_transcript && (
                        <button
                          onClick={() => setSelected(order)}
                          className="btn-secondary text-sm"
                        >
                          View transcript
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Transcript modal */}
      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div className="modal-content max-w-2xl" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Conversation Transcript
            </h2>
            <div className="space-y-3 max-h-96 overflow-y-auto bg-gray-50 rounded-lg p-4">
              {(() => {
                try {
                  const transcript = JSON.parse(selected.ai_transcript || '[]')
                  return transcript.map((msg: any, idx: number) => (
                    <div
                      key={idx}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg px-4 py-2 text-sm whitespace-pre-wrap ${
                          msg.role === 'user'
                            ? 'bg-primary-600 text-white'
                            : 'bg-white border border-gray-200 text-gray-800'
                        }`}
                      >
                        {msg.role === 'assistant' && (
                          <p className="text-xs text-primary-600 font-medium mb-1">N.O.U Lite</p>
                        )}
                        {msg.content}
                      </div>
                    </div>
                  ))
                } catch {
                  return <p className="text-sm text-gray-500">Transcript unavailable</p>
                }
              })()}
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

export default AdminNouLiteOrders
