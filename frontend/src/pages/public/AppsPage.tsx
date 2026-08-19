import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface AppComment {
  id: number
  name: string
  comment: string
  created_at: string
}

interface MobileApp {
  id: number
  name: string
  tagline: string | null
  description: string | null
  version: string
  platform: string
  status: 'upcoming' | 'published'
  banner_url: string | null
  apk_filename: string | null
  apk_size: number | null
  downloads: number
  comments_count: number
  created_at: string
  comments?: AppComment[]
}

const formatSize = (bytes: number | null) => {
  if (!bytes) return ''
  const mb = bytes / (1024 * 1024)
  return mb >= 1 ? `${mb.toFixed(1)} MB` : `${Math.round(bytes / 1024)} KB`
}

const formatDate = (value: string | null) => {
  if (!value) return ''
  try {
    return new Date(value).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  } catch {
    return ''
  }
}

const AppCard = ({ app, onCommentAdded }: { app: MobileApp; onCommentAdded: () => void }) => {
  const [showComments, setShowComments] = useState(false)
  const [comments, setComments] = useState<AppComment[]>(app.comments || [])
  const [name, setName] = useState('')
  const [comment, setComment] = useState('')
  const [posting, setPosting] = useState(false)

  const loadComments = async () => {
    try {
      const res = await api.get(`/apps/${app.id}`)
      setComments(res.data?.app?.comments || [])
    } catch {
      // keep whatever we have
    }
  }

  const toggleComments = async () => {
    const next = !showComments
    setShowComments(next)
    if (next) await loadComments()
  }

  const submitComment = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || name.trim().length < 2) {
      toast.error('Please enter your name')
      return
    }
    if (!comment.trim()) {
      toast.error('Please write a comment')
      return
    }
    try {
      setPosting(true)
      await api.post(`/apps/${app.id}/comments`, {
        name: name.trim(),
        comment: comment.trim(),
      })
      setName('')
      setComment('')
      toast.success('Comment published')
      await loadComments()
      onCommentAdded()
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to post comment. Please try again.')
    } finally {
      setPosting(false)
    }
  }

  return (
    <div className="card overflow-hidden">
      {app.banner_url ? (
        <div className="relative h-44 md:h-56 w-full overflow-hidden bg-gray-900">
          <img
            src={app.banner_url}
            alt={app.name}
            className="w-full h-full object-cover"
            loading="lazy"
          />
          <span
            className={`absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-semibold text-white ${
              app.status === 'published' ? 'bg-green-600' : 'bg-amber-500'
            }`}
          >
            {app.status === 'published' ? 'Available' : 'Coming Soon'}
          </span>
        </div>
      ) : (
        <div className="relative h-24 bg-gradient-to-br from-primary-800 to-primary-950 flex items-center justify-center">
          <span className="text-white font-bold text-2xl">{app.name.charAt(0)}</span>
          <span
            className={`absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-semibold text-white ${
              app.status === 'published' ? 'bg-green-600' : 'bg-amber-500'
            }`}
          >
            {app.status === 'published' ? 'Available' : 'Coming Soon'}
          </span>
        </div>
      )}

      <div className="p-6">
        <div className="flex items-start justify-between gap-4 mb-2">
          <div>
            <h3 className="text-xl font-bold text-gray-900">{app.name}</h3>
            {app.tagline && <p className="text-sm text-primary-600">{app.tagline}</p>}
          </div>
          <div className="text-right text-xs text-gray-500 shrink-0">
            <p>v{app.version} · {app.platform}</p>
            <p>{formatDate(app.created_at)}</p>
          </div>
        </div>

        {app.description && (
          <p className="text-gray-600 text-sm leading-relaxed mb-5 whitespace-pre-line">
            {app.description}
          </p>
        )}

        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-3 text-xs text-gray-500">
            {app.status === 'published' ? (
              <>
                <a
                  href={`/api/v1/apps/${app.id}/download`}
                  className="btn-primary text-sm inline-flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Download APK
                </a>
                <span>
                  {app.apk_filename ? `${app.apk_filename} (${formatSize(app.apk_size)})` : 'Download'}
                </span>
                {app.downloads > 0 && <span>· {app.downloads} download{app.downloads === 1 ? '' : 's'}</span>}
              </>
            ) : (
              <span className="inline-flex items-center gap-2 text-amber-700 bg-amber-50 border border-amber-200 rounded-full px-3 py-1.5 text-sm font-medium">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Available soon
              </span>
            )}
          </div>

          <button
            onClick={toggleComments}
            className="text-sm font-medium text-primary-600 hover:text-primary-700 inline-flex items-center gap-1.5"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Comments ({comments.length})
          </button>
        </div>

        {showComments && (
          <div className="mt-6 pt-5 border-t border-gray-200">
            <div className="space-y-4 mb-5">
              {comments.length === 0 && (
                <p className="text-sm text-gray-500">No comments yet - be the first to share your thoughts.</p>
              )}
              {comments.map((c) => (
                <div key={c.id} className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-semibold text-gray-900">{c.name}</p>
                    <p className="text-xs text-gray-400">{formatDate(c.created_at)}</p>
                  </div>
                  <p className="text-sm text-gray-600">{c.comment}</p>
                </div>
              ))}
            </div>

            <form onSubmit={submitComment} className="space-y-3">
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name *"
                className="input"
                maxLength={120}
              />
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Share your thoughts on this app..."
                rows={3}
                className="input"
                maxLength={2000}
              />
              <button type="submit" disabled={posting} className="btn-primary text-sm">
                {posting ? 'Posting...' : 'Post comment'}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  )
}

const AppsPage = () => {
  const [apps, setApps] = useState<MobileApp[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchApps = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await api.get('/apps')
      setApps(response.data.apps || [])
    } catch (err: any) {
      console.error('Error fetching apps:', err)
      setError('Could not load the apps. The server may be starting up - please retry.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchApps()
  }, [])

  const published = apps.filter((a) => a.status === 'published')
  const upcoming = apps.filter((a) => a.status === 'upcoming')

  return (
    <div className="bg-gray-50">
      {/* Hero */}
      <div className="bg-gradient-to-br from-primary-700 via-primary-800 to-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 text-sm font-medium tracking-wide mb-6">
            Mobile Applications
          </span>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Apps by N.O.U. Digital Systems</h1>
          <p className="text-lg text-primary-100 max-w-3xl mx-auto">
            Download the applications we have released and keep an eye on what is
            coming next. Have a thought about an app? Leave a comment - we read them all.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        {loading ? (
          <div className="text-center py-16">
            <div className="spinner mx-auto"></div>
          </div>
        ) : error ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 mb-4">{error}</p>
            <button onClick={fetchApps} className="btn-primary">
              Retry
            </button>
          </div>
        ) : apps.length === 0 ? (
          <div className="card text-center py-16">
            <h2 className="text-xl font-bold text-gray-900 mb-2">No apps published yet</h2>
            <p className="text-gray-600">
              N.O.U. will announce and publish its applications here soon.
            </p>
          </div>
        ) : (
          <div className="space-y-14">
            {published.length > 0 && (
              <section>
                <div className="flex items-center gap-3 mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Available for Download</h2>
                  <span className="px-3 py-1 rounded-full bg-green-50 text-green-700 border border-green-200 text-xs font-semibold">
                    {published.length} app{published.length === 1 ? '' : 's'}
                  </span>
                </div>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
                  {published.map((app) => (
                    <AppCard key={app.id} app={app} onCommentAdded={fetchApps} />
                  ))}
                </div>
              </section>
            )}

            {upcoming.length > 0 && (
              <section>
                <div className="flex items-center gap-3 mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Coming Soon</h2>
                  <span className="px-3 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200 text-xs font-semibold">
                    {upcoming.length} app{upcoming.length === 1 ? '' : 's'}
                  </span>
                </div>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
                  {upcoming.map((app) => (
                    <AppCard key={app.id} app={app} onCommentAdded={fetchApps} />
                  ))}
                </div>
              </section>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default AppsPage
