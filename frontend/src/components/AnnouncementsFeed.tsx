import { useEffect, useState } from 'react'
import api from '../services/api'

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

const CATEGORY_COLOR: Record<string, string> = {
  joke: 'bg-yellow-100 text-yellow-800',
  quote: 'bg-purple-100 text-purple-800',
  notice: 'bg-blue-100 text-blue-800',
  update: 'bg-green-100 text-green-800',
}

const AnnouncementsFeed = ({ title = 'Company Announcements', limit = 5 }: { title?: string; limit?: number }) => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFeed()
  }, [])

  const fetchFeed = async () => {
    try {
      const response = await api.get('/announcements/feed')
      setAnnouncements((response.data.announcements || []).slice(0, limit))
    } catch (error) {
      console.error('Error fetching announcements:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
        <span className="badge-primary">From the company</span>
      </div>

      {loading ? (
        <div className="text-center py-6">
          <div className="spinner mx-auto"></div>
        </div>
      ) : announcements.length === 0 ? (
        <p className="text-sm text-gray-500 py-4 text-center">No announcements yet.</p>
      ) : (
        <div className="space-y-3">
          {announcements.map((a) => (
            <div
              key={a.id}
              className={`rounded-lg p-4 border ${
                a.pinned
                  ? 'bg-primary-50 border-primary-200'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <div className="flex items-center gap-2 mb-1 flex-wrap">
                <span className={`badge ${CATEGORY_COLOR[a.category] || 'badge-gray'}`}>
                  {CATEGORY_LABEL[a.category] || a.category}
                </span>
                {a.pinned && <span className="badge-gray">Pinned</span>}
                {a.title && <span className="text-sm font-semibold text-gray-900">{a.title}</span>}
              </div>
              <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{a.body}</p>
              <p className="text-[10px] text-gray-400 mt-2">
                {new Date(a.created_at).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default AnnouncementsFeed
