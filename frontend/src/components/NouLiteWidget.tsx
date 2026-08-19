import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAppSelector } from '../hooks/useAppSelector'

interface ChatMsg {
  id: string
  sender: 'user' | 'ai'
  message: string
  order_created?: boolean
}

const WELCOME = {
  id: 'welcome',
  sender: 'ai' as const,
  message:
    'Hi!  I\'m N.O.U Lite, your personal assistant. I can help you order software products, request projects, or get support. What would you like to do today?',
}

const NouLiteWidget = () => {
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAppSelector((state) => state.auth)
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMsg[]>([WELCOME])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [guestEmail, setGuestEmail] = useState('')
  const [needsEmail, setNeedsEmail] = useState(false)
  const [unread, setUnread] = useState(0)
  // Once the guest skips the email prompt it never blocks again.
  const emailSkippedRef = useRef(false)
  const bodyRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (open && bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight
    }
    if (open) setUnread(0)
  }, [messages, open])

  useEffect(() => {
    if (!isAuthenticated) {
      const saved = localStorage.getItem('nou_lite_guest_email') || ''
      if (saved) {
        setGuestEmail(saved)
        setNeedsEmail(false)
      }
    }
  }, [isAuthenticated])

  const handleSend = async () => {
    if (!input.trim() || sending) return
    const text = input.trim()

    // Guests may optionally provide an email (once, saved locally) so orders
    // can be followed up - this is NOT an account/login requirement and can
    // be skipped entirely.
    if (!isAuthenticated && !guestEmail.trim() && !emailSkippedRef.current) {
      setNeedsEmail(true)
      return
    }
    setNeedsEmail(false)

    setInput('')
    setMessages((prev) => [...prev, { id: `u-${Date.now()}`, sender: 'user', message: text }])
    setSending(true)
    try {
      const body: Record<string, string> = { message: text }
      if (!isAuthenticated) {
        body.email = guestEmail.trim()
        localStorage.setItem('nou_lite_guest_email', guestEmail.trim())
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
    } catch (error: any) {
      const detail =
        error?.response?.data?.detail ||
        'N.O.U Lite is temporarily unavailable. Please try again.'
      setMessages((prev) => [...prev, { id: `e-${Date.now()}`, sender: 'ai', message: detail }])
    } finally {
      setSending(false)
    }
  }

  const skipEmail = () => {
    emailSkippedRef.current = true
    setNeedsEmail(false)
    // Send the pending message without an email (orders are still tracked
    // by the admin via the session).
    handleSend()
  }

  const toggleOpen = () => {
    setOpen((o) => {
      if (!o) setUnread(0)
      return !o
    })
  }

  if (user?.role && ['admin', 'applicant', 'developer', 'investor'].includes(user.role)) {
    return null
  }

  return (
    <>
      {/* Floating button */}
      <button
        onClick={toggleOpen}
        aria-label="Chat with N.O.U Lite"
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-gradient-to-br from-primary-600 to-primary-800 text-white shadow-lg hover:scale-110 transition-transform flex items-center justify-center"
      >
        {open ? (
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        )}
        {!open && unread > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs text-white flex items-center justify-center">
            {unread}
          </span>
        )}
      </button>

      {/* Chat window */}
      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-96 max-w-[calc(100vw-3rem)] bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col dark:border-gray-800 dark:bg-gray-900">
          {/* Header */}
          <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white px-4 py-3 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-lg">
              NOU
            </div>
            <div className="flex-1">
              <p className="font-semibold text-sm">N.O.U Lite</p>
              <p className="text-xs text-primary-100">Your assistant · no login needed</p>
            </div>
            <button
              onClick={() => navigate('/nou-lite')}
              className="text-xs bg-white/20 hover:bg-white/30 rounded-lg px-3 py-1.5 transition-colors"
            >
              Full view
            </button>
          </div>

          {/* Guest email prompt */}
          {needsEmail && (
            <div className="border-b border-gray-200 p-3 bg-primary-50 dark:border-gray-800 dark:bg-primary-900/20">
              <p className="text-xs text-primary-800 dark:text-primary-200 mb-2">
                Please enter your email so we can follow up on any order you place.
              </p>
              <div className="flex gap-2">
                <input
                  type="email"
                  value={guestEmail}
                  onChange={(e) => setGuestEmail(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="you@example.com"
                  className="input text-sm"
                />
                <button onClick={handleSend} className="btn-primary !px-4 text-sm">
                  OK
                </button>
                <button
                  onClick={skipEmail}
                  className="text-xs text-gray-500 hover:text-gray-700 underline self-center"
                >
                  Skip
                </button>
              </div>
            </div>
          )}

          {/* Messages */}
          <div ref={bodyRef} className="h-80 overflow-y-auto p-4 space-y-3 bg-gray-50 dark:bg-gray-950">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm whitespace-pre-wrap ${
                    msg.sender === 'user'
                      ? 'bg-primary-600 text-white rounded-br-sm'
                      : 'bg-white border border-gray-200 rounded-bl-sm dark:bg-gray-900 dark:border-gray-800 dark:text-gray-100'
                  }`}
                >
                  {msg.sender === 'ai' && (
                    <p className="text-xs text-primary-600 font-medium mb-1 dark:text-primary-300">N.O.U Lite</p>
                  )}
                  {msg.message}
                  {msg.order_created && (
                    <p className="text-xs text-green-600 mt-2 flex items-center gap-1 dark:text-green-400">
                      Order placed! Admin has been notified.
                    </p>
                  )}
                </div>
              </div>
            ))}
            {sending && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-2 text-sm text-gray-400 dark:bg-gray-900 dark:border-gray-800">
                  <span className="spinner inline-block w-3 h-3 border-2 mr-2"></span>
                  Thinking...
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-3 flex gap-2 bg-white dark:border-gray-800 dark:bg-gray-900">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your order or question..."
              className="input flex-1 text-sm"
            />
            <button
              onClick={handleSend}
              disabled={sending || !input.trim()}
              className="btn-primary !px-4"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default NouLiteWidget
