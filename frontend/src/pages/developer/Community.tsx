import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../services/api'
import toast from 'react-hot-toast'
import { useAppSelector } from '../../hooks/useAppSelector'

interface CommunityPost {
  id: string
  author: { id: string; name: string; email: string | null; username: string | null }
  category: string
  department: string | null
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

const DeveloperCommunity = () => {
  const { user } = useAppSelector((state) => state.auth)
  const myDepartment = user?.qualification_category_name || ''
  const [posts, setPosts] = useState<CommunityPost[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [departments, setDepartments] = useState<string[]>([])
  const [activeCategory, setActiveCategory] = useState('')
  const [activeDepartment, setActiveDepartment] = useState('')
  const [loading, setLoading] = useState(true)
  const [showNewPost, setShowNewPost] = useState(false)
  const [newPost, setNewPost] = useState({ title: '', content: '', category: 'general' })

  useEffect(() => {
    fetchPosts()
    fetchDepartments()
  }, [activeCategory, activeDepartment])

  const fetchPosts = async () => {
    try {
      const params: any = {}
      if (activeCategory) params.category = activeCategory
      if (activeDepartment) params.department = activeDepartment
      const response = await api.get('/community/posts', { params })
      setPosts(response.data.posts || [])
      setCategories(response.data.categories || [])
    } catch (error) {
      console.error('Error fetching community posts:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchDepartments = async () => {
    try {
      const response = await api.get('/personnel/categories')
      const list = (response.data.categories || []).map((c: any) => c.name)
      setDepartments(list)
    } catch (error) {
      console.error('Error fetching departments:', error)
    }
  }

  const handleCreatePost = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await api.post('/community/posts', {
        ...newPost,
        department: activeDepartment || undefined,
      })
      toast.success(response.data?.message || 'Post submitted')
      setShowNewPost(false)
      setNewPost({ title: '', content: '', category: 'general' })
      fetchPosts()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to create post')
    }
  }

  const handleDeletePost = async (postId: string) => {
    if (!window.confirm('Delete this post?')) return
    try {
      await api.delete(`/community/posts/${postId}`)
      toast.success('Post deleted')
      fetchPosts()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to delete post')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">N.O.U. Community</h1>
          <p className="text-gray-600">Share updates, ask questions and collaborate with fellow personnel.</p>
        </div>
        <button onClick={() => setShowNewPost(true)} className="btn-primary">
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          New Post
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
                  placeholder="Post title"
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
                  placeholder="Share your update, question or idea..."
                />
              </div>
              <div className="bg-gray-50 rounded-lg p-3 text-xs text-gray-500">
                Posts are reviewed by N.O.U. administration before publication.
              </div>
              <div className="flex justify-end space-x-3 pt-4">
                <button type="button" onClick={() => setShowNewPost(false)} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary">Submit Post</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Department filter - the general community links every department */}
      {departments.length > 0 && (
        <div className="mb-6">
          <div className="flex gap-2 flex-wrap items-center">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide mr-1">Department:</span>
            <button
              onClick={() => setActiveDepartment('')}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                activeDepartment === ''
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              All departments
            </button>
            {departments.map((dept) => (
              <button
                key={dept}
                onClick={() => setActiveDepartment(activeDepartment === dept ? '' : dept)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                  activeDepartment === dept
                    ? 'bg-primary-600 text-white shadow-sm'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {dept}
              </button>
            ))}
          </div>
          {myDepartment && (
            <Link
              to="/portal/department"
              className="text-xs text-primary-600 hover:text-primary-700 mt-2 inline-block"
            >
              View my department community: {myDepartment}
            </Link>
          )}
        </div>
      )}

      {/* Category filter */}
      {categories.length > 0 && (
        <div className="flex gap-2 mb-6 flex-wrap">
          <button
            onClick={() => setActiveCategory('')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              activeCategory === ''
                ? 'bg-primary-600 text-white shadow-sm'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            All
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                activeCategory === cat
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {CATEGORY_META[cat]?.label || cat.replace('_', ' ')}
            </button>
          ))}
        </div>
      )}

      {/* Posts feed */}
      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
        </div>
      ) : posts.length === 0 ? (
        <div className="card text-center py-12">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p className="text-gray-600">No community posts yet</p>
          <p className="text-sm text-gray-500 mt-1">Be the first to share something with the team.</p>
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
                      <p className="font-medium text-gray-900 text-sm">
                        {post.author?.name || 'N.O.U. Personnel'}
                        {post.author?.username && (
                          <span className="text-primary-600 font-medium ml-1.5">@{post.author.username}</span>
                        )}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(post.created_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${meta.style}`}>
                      {meta.label}
                    </span>
                    {post.department && (
                      <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
                        {post.department}
                      </span>
                    )}
                    {post.status !== 'published' && (
                      <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700">
                        {post.status === 'pending' ? 'Awaiting moderation' : 'Removed'}
                      </span>
                    )}
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 mt-3">{post.title}</h3>
                <p className="text-gray-600 text-sm mt-1 whitespace-pre-line">{post.content}</p>
                {post.status === 'removed' && post.removed_reason && (
                  <p className="text-xs text-red-500 mt-2">
                    Reason: {post.removed_reason}
                  </p>
                )}
                <div className="flex justify-end mt-3">
                  <button
                    onClick={() => handleDeletePost(post.id)}
                    className="text-xs text-gray-400 hover:text-red-600 transition-colors"
                  >
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

export default DeveloperCommunity