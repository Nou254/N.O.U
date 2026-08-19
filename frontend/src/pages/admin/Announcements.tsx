import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Announcement {
  id: number
  title: string | null
  body: string
  category: string
  audience: string
  pinned: boolean
  created_at: string
}

const CATEGORY_LABEL: Record<string, string> = {
  joke: 'Joke of the day',
  quote: 'Quote',
  notice: 'Notice',
  update: 'Update',
}

const AdminAnnouncements = () => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [loading, setLoading] = useState(true)

  // Post form
  const [form, setForm] = useState({
    title: '',
    body: '',
    category: 'update',
    audience: 'all',
    pinned: false,
  })
  const [posting, setPosting] = useState(false)

  // Email broadcast
  const [email, setEmail] = useState({ subject: '', body: '' })
  const [customerCount, setCustomerCount] = useState(0)
  const [sending, setSending] = useState(false)

  const fetchAnnouncements = async () => {
    try {
      const response = await api.get('/announcements/announcements')
      setAnnouncements(response.data.announcements || [])
    } catch (error) {
      console.error('Error fetching announcements:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAnnouncements()
    api
      .get('/announcements/announcements/customers-count')
      .then((res) => setCustomerCount(res.data.customers || 0))
      .catch(() => setCustomerCount(0))
  }, [])

  const handlePost = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.body.trim()) {
      toast.error('Announcement text is required')
      return
    }
    setPosting(true)
    try {
      const response = await api.post('/announcements/announcements', {
        body: form.body.trim(),
        title: form.title.trim() || undefined,
        category: form.category,
        audience: form.audience,
        pinned: form.pinned,
      })
      toast.success(
        `${CATEGORY_LABEL[response.data.category] || response.data.category} posted`
      )
      setForm({ title: '', body: '', category: 'update', audience: 'all', pinned: false })
      fetchAnnouncements()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to post announcement')
    } finally {
      setPosting(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/announcements/announcements/${id}`)
      toast.success('Announcement deleted')
      fetchAnnouncements()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to delete')
    }
  }

  const handleEmail = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email.subject.trim() || !email.body.trim()) {
      toast.error('Subject and body are required for the broadcast')
      return
    }
    setSending(true)
    try {
      const response = await api.post('/announcements/announcements/email', {
        subject: email.subject.trim(),
        body: email.body.trim(),
      })
      toast.success(response.data.message)
      setEmail({ subject: '', body: '' })
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Broadcast failed')
    } finally {
      setSending(false)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Announcements</h1>
          <p className="text-gray-600">
            Post jokes of the day, quotes, notices, or communications for
            developers and customers, and broadcast emails.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Post announcement */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Post to the quorum</h2>
          <form onSubmit={handlePost} className="space-y-4">
            <div>
              <label htmlFor="ann-title" className="label">Title (optional)</label>
              <input
                id="ann-title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                className="input"
                placeholder="e.g. Quote of the day"
              />
            </div>
            <div>
              <label htmlFor="ann-body" className="label">Message *</label>
              <textarea
                id="ann-body"
                value={form.body}
                onChange={(e) => setForm({ ...form, body: e.target.value })}
                rows={4}
                required
                className="input"
                placeholder="What do you want to communicate?"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="ann-cat" className="label">Category</label>
                <select
                  id="ann-cat"
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value })}
                  className="input"
                >
                  <option value="update">Update</option>
                  <option value="notice">Notice</option>
                  <option value="joke">Joke of the day</option>
                  <option value="quote">Quote</option>
                </select>
              </div>
              <div>
                <label htmlFor="ann-aud" className="label">Audience</label>
                <select
                  id="ann-aud"
                  value={form.audience}
                  onChange={(e) => setForm({ ...form, audience: e.target.value })}
                  className="input"
                >
                  <option value="all">Everyone</option>
                  <option value="developers">Developers</option>
                  <option value="customers">Customers</option>
                </select>
              </div>
            </div>
            <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
              <input
                type="checkbox"
                checked={form.pinned}
                onChange={(e) => setForm({ ...form, pinned: e.target.checked })}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              Pin to the top of feeds
            </label>
            <button type="submit" disabled={posting} className="btn-primary w-full">
              {posting ? 'Posting...' : 'Post announcement'}
            </button>
          </form>
        </div>

        {/* Email broadcast */}
        <div className="card">
          <div className="flex items-center justify-between mb-1">
            <h2 className="text-lg font-semibold text-gray-900">Email customers</h2>
            <span className="badge-primary">{customerCount} customer{ customerCount === 1 ? '' : 's'}</span>
          </div>
          <p className="text-sm text-gray-500 mb-4">
            Batch-email all customers (e.g. maintenance windows or incoming services).
          </p>
          <form onSubmit={handleEmail} className="space-y-4">
            <div>
              <label htmlFor="email-subject" className="label">Subject *</label>
              <input
                id="email-subject"
                value={email.subject}
                onChange={(e) => setEmail({ ...email, subject: e.target.value })}
                className="input"
                placeholder="e.g. Scheduled maintenance this Sunday"
              />
            </div>
            <div>
              <label htmlFor="email-body" className="label">Message *</label>
              <textarea
                id="email-body"
                value={email.body}
                onChange={(e) => setEmail({ ...email, body: e.target.value })}
                rows={6}
                required
                className="input"
                placeholder="Write the email body sent to every customer..."
              />
            </div>
            <button type="submit" disabled={sending} className="btn-primary w-full">
              {sending ? 'Sending...' : `Send to ${customerCount} customer${customerCount === 1 ? '' : 's'}`}
            </button>
          </form>
        </div>
      </div>

      {/* List */}
      <div className="card mt-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Published ({announcements.length})
        </h2>
        {loading ? (
          <div className="text-center py-10">
            <div className="spinner mx-auto"></div>
          </div>
        ) : announcements.length === 0 ? (
          <p className="text-sm text-gray-500 text-center py-8">No announcements yet.</p>
        ) : (
          <div className="space-y-3">
            {announcements.map((a) => (
              <div
                key={a.id}
                className={`rounded-lg p-4 border ${
                  a.pinned ? 'bg-primary-50 border-primary-200' : 'bg-gray-50 border-gray-200'
                } flex items-start justify-between gap-4`}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <span className="badge-gray">{CATEGORY_LABEL[a.category] || a.category}</span>
                    <span className="badge-primary">{a.audience}</span>
                    {a.pinned && <span className="badge-warning">Pinned</span>}
                  </div>
                  {a.title && <p className="text-sm font-semibold text-gray-900">{a.title}</p>}
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{a.body}</p>
                  <p className="text-[10px] text-gray-400 mt-2">
                    {new Date(a.created_at).toLocaleString()}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(a.id)}
                  className="btn-outline text-xs !py-1 shrink-0"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminAnnouncements
