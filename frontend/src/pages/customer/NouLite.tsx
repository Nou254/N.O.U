import { useEffect, useRef, useState } from 'react'
import api from '../../services/api'
import { useAppSelector } from '../../hooks/useAppSelector'

interface ChatMsg {
  id: string
  sender: 'user' | 'ai'
  message: string
  order_created?: boolean
}

interface Order {
  id: number
  order_type: string
  summary: string
  details: string
  status: string
  created_at: string
}

const WELCOME = {
  id: 'welcome',
  sender: 'ai' as const,
  message:
    'Hi!  I\'m N.O.U Lite. Tell me what you need — a software product, a project build, or support — and I\'ll place your order instantly. Example: "I would like to order a company website."',
}

const TYPE_BADGE: Record<string, string> = {
  product: 'badge-primary',
  project: 'badge-warning',
  support: 'badge-info',
  inquiry: 'badge-gray',
}

const ORDER_STATUS: Record<string, string> = {
  new: 'badge-primary',
  in_progress: 'badge-warning',
  completed: 'badge-success',
  declined: 'badge-danger',
}

const CustomerNouLite = () => {
  const { isAuthenticated } = useAppSelector((state) => state.auth)
  const [messages, setMessages] = useState<ChatMsg[]>([WELCOME])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [orders, setOrders] = useState<Order[]>([])
  const [loadingOrders, setLoadingOrders] = useState(true)
  const [guestEmail, setGuestEmail] = useState(
    () => localStorage.getItem('nou_lite_guest_email') || ''
  )
  const bodyRef = useRef<HTMLDivElement>(null)

  const fetchOrders = async () => {
    try {
      const response = await api.get('/nou-lite/orders', {
        // Guests are identified by the email they provide (no account needed).
        params: isAuthenticated ? undefined : { email: guestEmail || undefined },
      })
      setOrders(response.data.orders)
    } catch (error) {
      console.error('Error fetching orders:', error)
    } finally {
      setLoadingOrders(false)
    }
  }

  useEffect(() => {
    fetchOrders()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight
    }
  }, [messages, sending])

  const handleSend = async () => {
    if (!input.trim() || sending) return
    const text = input.trim()
    setInput('')
    setMessages((prev) => [...prev, { id: `u-${Date.now()}`, sender: 'user', message: text }])
    setSending(true)
    try {
      const body: Record<string, string> = { message: text }
      if (!isAuthenticated) {
        body.email = guestEmail.trim()
        if (guestEmail.trim()) {
          localStorage.setItem('nou_lite_guest_email', guestEmail.trim())
        }
      }
      const response = await api.post('/nou-lite/chat', body)
      setMessages((prev) => [
        ...prev,
        {
          id: `a-${Date.now()}`,
          sender: 'ai',
          message: response.data.reply,
          order_created: response.data.order_created,
        },
      ])
      if (response.data.order_created) fetchOrders()
    } catch (error: any) {
      const detail =
        error?.response?.data?.detail ||
        'N.O.U Lite is temporarily unavailable. Please try again.'
      setMessages((prev) => [...prev, { id: `e-${Date.now()}`, sender: 'ai', message: detail }])
    } finally {
      setSending(false)
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
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">N.O.U Lite</h1>
        <p className="text-gray-600">
          Your assistant for placing orders, requesting projects, and getting support.
        </p>
      </div>

      {/* Guest identity - optional, NO login/account required */}
      {!isAuthenticated && (
        <div className="card mb-6 flex flex-wrap items-center gap-3">
          <p className="text-sm text-gray-600">
            No account needed — add your email to track the orders you place here.
          </p>
          <input
            type="email"
            value={guestEmail}
            onChange={(e) => setGuestEmail(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                localStorage.setItem('nou_lite_guest_email', guestEmail.trim())
                fetchOrders()
              }
            }}
            placeholder="you@example.com (optional)"
            className="input flex-1 min-w-[220px] text-sm"
          />
          <button
            onClick={() => {
              localStorage.setItem('nou_lite_guest_email', guestEmail.trim())
              fetchOrders()
            }}
            className="btn-secondary text-sm"
          >
            Track my orders
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
        {/* Chat */}
        <div className="lg:col-span-3 card flex flex-col">
          <div ref={bodyRef} className="h-[28rem] overflow-y-auto bg-gray-50 rounded-lg p-4 space-y-3 flex-1">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm whitespace-pre-wrap ${
                    msg.sender === 'user'
                      ? 'bg-primary-600 text-white rounded-br-sm'
                      : 'bg-white border border-gray-200 rounded-bl-sm'
                  }`}
                >
                  {msg.sender === 'ai' && (
                    <p className="text-xs text-primary-600 font-medium mb-1">N.O.U Lite</p>
                  )}
                  {msg.message}
                  {msg.order_created && (
                    <p className="text-xs text-green-600 mt-2 flex items-center gap-1">
                      Order placed! Admin has been notified and will review it.
                    </p>
                  )}
                </div>
              </div>
            ))}
            {sending && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-2 text-sm text-gray-400">
                  <span className="spinner inline-block w-3 h-3 border-2 mr-2"></span>
                  Thinking...
                </div>
              </div>
            )}
          </div>

          <div className="mt-4 flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder='Try: "I would like to order an antivirus software" or "I need a mobile app built"'
              className="input flex-1"
            />
            <button
              onClick={handleSend}
              disabled={sending || !input.trim()}
              className="btn-primary"
            >
              Send
            </button>
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            {[
              'Order a software product',
              'Request a website project',
              'Report a bug',
              'Get company info',
            ].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => {
                  setInput(suggestion)
                }}
                className="text-xs px-3 py-1.5 bg-gray-100 hover:bg-primary-50 hover:text-primary-700 text-gray-600 rounded-full transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* Order history */}
        <div className="lg:col-span-2 card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">My Orders</h2>
          {loadingOrders ? (
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
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <p className="text-gray-600">No orders yet</p>
              <p className="text-sm text-gray-500 mt-1">
                {isAuthenticated
                  ? 'Chat with N.O.U Lite on the left to place your first order.'
                  : 'Chat with N.O.U Lite on the left to place an order, then enter your email above to track it here.'}
              </p>
            </div>
          ) : (
            <div className="space-y-3 max-h-[28rem] overflow-y-auto">
              {orders.map((order) => (
                <div key={order.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className={TYPE_BADGE[order.order_type] || 'badge-gray'}>
                      {order.order_type}
                    </span>
                    <span className={ORDER_STATUS[order.status] || 'badge-gray'}>
                      {order.status.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-gray-900 mb-1">{order.summary}</p>
                  {Object.entries(parseDetails(order.details)).length > 0 && (
                    <div className="text-xs text-gray-500 space-y-0.5">
                      {Object.entries(parseDetails(order.details)).map(([k, v]) => (
                        <p key={k}><span className="capitalize">{k}:</span> {v}</p>
                      ))}
                    </div>
                  )}
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(order.created_at).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default CustomerNouLite
