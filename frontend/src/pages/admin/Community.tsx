import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface CommunityPost {
  id: string
  author: { id: string; name: string; email: string | null }
  category: string
  title: string
  content: string
  status: string
  removed_reason: string | null
  created_at: string
}

const CATEGORY_META: Record<string, { label: string; style: string }> = {
  general: { label: 'General', style: 'bg-gray-100 text-gray-600' },
  announcement: { label: 'Announcement', style: 'bg-primary-100 text-primary-700' },
  question: { label: 'Question', style: 'bg-blue-100 text-blue-700' },
  idea: { label: 'Idea', style: 'bg-purple-100 text-purple-700' },
  project: { label: 'Project', style: 'bg-green-100 text-green-700' },
  help: { label: 'Help', style: 'bg-amber-100 text-amber-700' },
  learning: { label: 'Learning', style: 'bg-teal-100 text-teal-700' },
  other: { label: 'Other', style: 'bg-gray-100 text-gray-600' },
}

const AdminCommunity = () => {
  const [posts, setPosts] = useState<CommunityPost[]>([])
  const [tab, setTab] = useState<'published' | 'removed'>('published')
  const [loading, setLoading] = useState(true)
  const [showNewPost, setShowNewPost] = useState(false)
  const [newPost, setNewPost] = useState({ title: '', content: '', category: 'announcement' })
  const [categories, setCategories] = useState<string[]>([])

  useEffect(() => {
    fetchPosts()
  }, [tab])

  const fetchPosts = async () => {
    try {
      const response = await api.get('/community/moderation', {
        params: { status_filter: tab },
      })
      setPosts(response.data.posts || [])
      setCategories(response.data.categories || [])
    } catch (error) {
      console.error('Error fetching moderation queue:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleModerate = async (postId: string, approve: boolean) => {
    try {
      const response = await api.post(`/community/posts/${postId}/moderate`, {
        approve,
        reason: approve ? undefined : 'Removed by N.O.U. administration',
      })
      toast.success(response.data?.message || 'Post moderated')
      fetchPosts()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to moderate post')
    }
  }

  const handleDeletePost = async (postId: string) => {
    if (!window.confirm('Permanently delete this post?')) return
    try {
      await api.delete(`/community/posts/${postId}`)
      toast.success('Post deleted')
      fetchPosts()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to delete post')
    }
  }

  const handleCreatePost = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await api.post('/community/posts', newPost)
      toast.success(response.data?.message || 'Post published')
      setShowNewPost(false)
      setNewPost({ title: '', content: '', category: 'announcement' })
      fetchPosts()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to create post')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Community Chat Moderation</h1>
          <p className="text-gray-600">
            The community chat is open - every message is published instantly (freedom
            of expression, no approval gate). Use this screen to remove content that
            violates community guidelines.
          </p>
        </div>
        <button onClick={() => setShowNewPost(true)} className="btn-primary">
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          New Announcement
        </button>
      </div>

      {/* New Post Modal */}
      {showNewPost && (
        <div className="modal-overlay" onClick={() => setShowNewPost(false)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Create Community Post</h2>
            <form onSubmit={handleCreatePost} className="space-y-4">
              <div>
                <label className="label">Title</label>
                <input
                  type="text"
                  value={newPost.title}
                  onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
                  required
                  minLength={3}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Category</label>
                <select
                  value={newPost.category}
                  onChange={(e) => setNewPost({ ...newPost, category: e.target.value })}
                  className="input"
                >
                  {categories.map((cat) => (
                    <option key={cat} value={cat}>
                      {(CATEGORY_META[cat]?.label || cat).replace('_', ' ')}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="label">Content</label>
                <textarea
                  value={newPost.content}
                  onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
                  required
                  minLength={10}
                  rows={5}
                  className="input"
                />
              </div>
              <div className="bg-primary-50 rounded-lg p-3 text-xs text-primary-700">
                Admin posts are published to the community immediately.
              </div>
              <div className="flex justify-end space-x-3 pt-4">
                <button type="button" onClick={() => setShowNewPost(false)} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary">Publish</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {(['published', 'removed'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-5 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${
              tab === t
                ? 'bg-primary-600 text-white shadow-sm'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Queue */}
      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
        </div>
      ) : posts.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-600">
            No {tab} posts
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {posts.map((post) => {
            const meta = CATEGORY_META[post.category] || CATEGORY_META.general
            return (
              <div key={post.id} className="card">
                <div className="flex items-start justify-between flex-wrap gap-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center shrink-0">
                      <span className="text-primary-700 font-semibold text-sm">
                        {post.author?.name?.charAt(0) || 'N'}
                      </span>
                    </div>
                    <div>
                      <p className="font-medium text-gray-900 text-sm">{post.author?.name || 'Unknown'}</p>
                      <p className="text-xs text-gray-500">
                        {post.author?.email} - {new Date(post.created_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${meta.style}`}>
                    {meta.label}
                  </span>
                </div>
                <h3 className="font-semibold text-gray-900 mt-3">{post.title}</h3>
                <p className="text-gray-600 text-sm mt-1 whitespace-pre-line">{post.content}</p>
                {post.status === 'removed' && post.removed_reason && (
                  <p className="text-xs text-red-500 mt-2">Reason: {post.removed_reason}</p>
                )}
                <div className="flex justify-end gap-2 mt-3">
                  {post.status === 'published' && (
                    <button onClick={() => handleModerate(post.id, false)} className="btn-outline text-xs text-red-600 border-red-300">
                      Remove
                    </button>
                  )}
                  {post.status === 'removed' && (
                    <button onClick={() => handleModerate(post.id, true)} className="btn-primary text-xs">
                      Restore
                    </button>
                  )}
                  <button onClick={() => handleDeletePost(post.id)} className="text-xs text-gray-400 hover:text-red-600 transition-colors">
                    Delete
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default AdminCommunity