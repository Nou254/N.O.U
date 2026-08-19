import { useEffect, useRef, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface ChatMessage {
  id: string
  author: { name: string; email: string | null; username: string | null }
  title: string
  content: string
  status: string
  created_at: string
}

const CommunityChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [name, setName] = useState(() => sessionStorage.getItem('nou_community_name') || '')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  // Ref (not state) so the polling interval never sees a stale closure and
  // only scrolls to the bottom on the first load - a user scrolling up to
  // read older messages is never yanked back down.
  const didInitialScroll = useRef(false)

  const fetchMessages = async () => {
    try {
      const res = await api.get('/community/posts', { params: { limit: 100 } })
      const posts = res.data.posts || []
      setMessages(posts)
      if (!didInitialScroll.current) {
        didInitialScroll.current = true
        setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }), 100)
      }
    } catch (error) {
      console.error('Error fetching community chat:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMessages()
    // Live-ish polling: new messages appear automatically.
    const timer = setInterval(fetchMessages, 12000)
    return () => clearInterval(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    const content = message.trim()
    const displayName = name.trim()
    if (!content) return
    if (displayName.length < 2) {
      toast.error('Please enter your name so we know who is speaking')
      return
    }
    setSending(true)
    try {
      await api.post('/community/posts', {
        content,
        guest_name: displayName,
        category: 'general',
      })
      sessionStorage.setItem('nou_community_name', displayName)
      setMessage('')
      // Publish immediately - refresh the feed so the message shows up now.
      fetchMessages()
      toast.success('Message published to the community!')
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to send your message')
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 bg-gradient-to-br from-primary-600 to-primary-800 rounded-2xl mb-4">
          <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m7.44-2.06A2 2 0 018 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-.586 1.414z" />
          </svg>
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
          N.O.U. Community Chat
        </h1>
        <p className="text-lg text-gray-600 max-w-xl mx-auto">
          A free space for everyone to communicate openly - freedom of expression.
          Every message is published instantly, no login or approval required.
          N.O.U. administration may remove content that violates community guidelines.
        </p>
      </div>

      {/* Chat window */}
      <div className="card overflow-hidden">
        <div className="bg-gradient-to-r from-primary-600 to-primary-800 px-5 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-300 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-400"></span>
            </span>
            <span className="text-white text-sm font-semibold">Community Chat</span>
          </div>
          <span className="text-primary-100 text-xs">{messages.length} message{messages.length === 1 ? '' : 's'}</span>
        </div>

        {/* Messages */}
        <div className="h-[28rem] overflow-y-auto px-5 py-4 space-y-4 bg-gray-50">
          {loading ? (
            <div className="text-center py-16">
              <div className="spinner mx-auto"></div>
              <p className="mt-3 text-sm text-gray-500">Loading the conversation...</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="text-center py-16">
              <svg className="w-14 h-14 text-gray-300 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p className="text-gray-600 font-medium">No messages yet</p>
              <p className="text-sm text-gray-500 mt-1">
                Be the first to start the conversation - your message appears instantly.
              </p>
            </div>
          ) : (
            [...messages]
              .sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
              .map((msg) => (
                <div key={msg.id} className="flex items-start gap-3">
                  <div className="w-9 h-9 rounded-full bg-primary-100 flex items-center justify-center shrink-0">
                    <span className="text-primary-700 font-semibold text-sm">
                      {msg.author?.name?.charAt(0)?.toUpperCase() || 'N'}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-baseline gap-2 flex-wrap">
                      <span className="text-sm font-semibold text-gray-900">
                        {msg.author?.name || 'Community Member'}
                        {msg.author?.username && (
                          <span className="text-primary-600 font-medium ml-1">@{msg.author.username}</span>
                        )}
                      </span>
                      <span className="text-[11px] text-gray-400">
                        {new Date(msg.created_at).toLocaleString()}
                      </span>
                    </div>
                    <div className="mt-1 bg-white rounded-2xl rounded-tl-sm border border-gray-100 px-4 py-2.5 shadow-sm">
                      <p className="text-sm text-gray-800 whitespace-pre-line">{msg.content}</p>
                    </div>
                  </div>
                </div>
              ))
          )}
          <div ref={bottomRef} />
        </div>

        {/* Composer */}
        <form onSubmit={handleSend} className="border-t border-gray-200 px-4 py-4 space-y-3 bg-white">
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input flex-1"
              placeholder="Your name *"
              maxLength={120}
            />
            <span className="text-xs text-gray-400 shrink-0">no login needed</span>
          </div>
          <div className="flex items-end gap-2">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={2}
              className="input flex-1 resize-none"
              placeholder="Share your thoughts freely - your message is published instantly..."
              maxLength={20000}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSend(e)
                }
              }}
            />
            <button
              type="submit"
              disabled={sending || !message.trim()}
              className="btn-primary shrink-0 disabled:opacity-50"
            >
              {sending ? (
                <span className="flex items-center gap-2">
                  <span className="spinner inline-block w-4 h-4 border-2 border-white/40"></span>
                  Sending
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                  Send
                </span>
              )}
            </button>
          </div>
          <p className="text-[11px] text-gray-400">
            Be respectful. N.O.U. administration may remove content that violates
            community guidelines.
          </p>
        </form>
      </div>
    </div>
  )
}

export default CommunityChat
