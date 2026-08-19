import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Ticket {
  id: string
  ticket_number: number
  subject: string
  description: string
  category: string
  priority: string
  status: string
  created_at: string
}

const CustomerSupport = () => {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [showNewTicket, setShowNewTicket] = useState(false)
  const [newTicket, setNewTicket] = useState({
    subject: '',
    description: '',
    category: 'general',
    priority: 'medium',
  })

  useEffect(() => {
    fetchTickets()
  }, [])

  const fetchTickets = async () => {
    try {
      const response = await api.get('/support/tickets/me')
      setTickets(response.data.tickets)
    } catch (error) {
      console.error('Error fetching tickets:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      await api.post('/support/tickets', newTicket)
      toast.success('Support ticket created successfully')
      setShowNewTicket(false)
      setNewTicket({
        subject: '',
        description: '',
        category: 'general',
        priority: 'medium',
      })
      fetchTickets()
    } catch (error) {
      toast.error('Failed to create support ticket')
    }
  }

  const priorityColors: Record<string, string> = {
    low: 'badge-gray',
    medium: 'badge-warning',
    high: 'badge-danger',
    urgent: 'badge-danger',
  }

  const statusColors: Record<string, string> = {
    open: 'badge-primary',
    in_progress: 'badge-warning',
    waiting_customer: 'badge-warning',
    resolved: 'badge-success',
    closed: 'badge-gray',
  }

  const categories = [
    { value: 'general', label: 'General Inquiry' },
    { value: 'technical', label: 'Technical Support' },
    { value: 'billing', label: 'Billing' },
    { value: 'bug_report', label: 'Bug Report' },
    { value: 'feature_request', label: 'Feature Request' },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Support Center</h1>
          <p className="text-gray-600">Get help with our products and services.</p>
        </div>
        <button
          onClick={() => setShowNewTicket(true)}
          className="btn-primary"
        >
          <svg
            className="w-5 h-5 mr-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          New Ticket
        </button>
      </div>

      {/* New Ticket Modal */}
      {showNewTicket && (
        <div className="modal-overlay" onClick={() => setShowNewTicket(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Create Support Ticket</h2>
            <form onSubmit={handleCreateTicket} className="space-y-4">
              <div>
                <label className="label">Subject</label>
                <input
                  type="text"
                  value={newTicket.subject}
                  onChange={(e) => setNewTicket({ ...newTicket, subject: e.target.value })}
                  required
                  className="input"
                  placeholder="Brief description of your issue"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Category</label>
                  <select
                    value={newTicket.category}
                    onChange={(e) => setNewTicket({ ...newTicket, category: e.target.value })}
                    className="input"
                  >
                    {categories.map((cat) => (
                      <option key={cat.value} value={cat.value}>
                        {cat.label}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="label">Priority</label>
                  <select
                    value={newTicket.priority}
                    onChange={(e) => setNewTicket({ ...newTicket, priority: e.target.value })}
                    className="input"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="label">Description</label>
                <textarea
                  value={newTicket.description}
                  onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
                  required
                  rows={4}
                  className="input"
                  placeholder="Detailed description of your issue"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowNewTicket(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Create Ticket
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Tickets List */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Tickets</h2>
        
        {loading ? (
          <div className="text-center py-8">
            <div className="spinner mx-auto"></div>
          </div>
        ) : tickets.length === 0 ? (
          <div className="text-center py-8">
            <svg
              className="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
            <p className="text-gray-600">No support tickets yet</p>
            <p className="text-sm text-gray-500 mt-1">Create a new ticket if you need assistance</p>
          </div>
        ) : (
          <div className="space-y-4">
            {tickets.map((ticket) => (
              <div
                key={ticket.id}
                className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-sm text-gray-500">#{ticket.ticket_number}</span>
                      <h3 className="font-medium text-gray-900">{ticket.subject}</h3>
                    </div>
                    <p className="text-gray-600 text-sm mb-2 line-clamp-2">
                      {ticket.description}
                    </p>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span className="capitalize">{ticket.category.replace('_', ' ')}</span>
                      <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    <span className={priorityColors[ticket.priority]}>
                      {ticket.priority}
                    </span>
                    <span className={statusColors[ticket.status]}>
                      {ticket.status.replace('_', ' ')}
                    </span>
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

export default CustomerSupport