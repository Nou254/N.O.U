import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../services/api'
import toast from 'react-hot-toast'
import { useAppSelector } from '../../hooks/useAppSelector'

interface DepartmentMember {
  id: number
  name: string
  username: string | null
  email: string
  role: string
  qualification_category_name: string | null
  qualification_position_name: string | null
}

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

const DeveloperDepartment = () => {
  const { user } = useAppSelector((state) => state.auth)
  const department = user?.qualification_category_name || ''

  const [members, setMembers] = useState<DepartmentMember[]>([])
  const [posts, setPosts] = useState<CommunityPost[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [activeCategory, setActiveCategory] = useState('')
  const [loading, setLoading] = useState(true)
  const [showNewPost, setShowNewPost] = useState(false)
  const [newPost, setNewPost] = useState({ title: '', content: '', category: 'general' })

  useEffect(() => {
    fetchDepartment()
  }, [department, activeCategory])

  const fetchDepartment = async () => {
    if (!department) {
      setLoading(false)
      return
    }
    try {
      setLoading(true)
      const [membersRes, postsRes] = await Promise.all([
        api.get('/community/members', { params: { department } }),
        api.get('/community/posts', {
          params: { department, ...(activeCategory ? { category: activeCategory } : {}) },
        }),
      ])
      setMembers(membersRes.data.members || [])
      setPosts(postsRes.data.posts || [])
      setCategories(postsRes.data.categories || [])
    } catch (error) {
      console.error('Error fetching department:', error)
      toast.error('Failed to load department')
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePost = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await api.post('/community/posts', { ...newPost, department })
      toast.success(response.data?.message || 'Post submitted')
      setShowNewPost(false)
      setNewPost({ title: '', content: '', category: 'general' })
      fetchDepartment()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to create post')
    }
  }

  const handleDeletePost = async (postId: string) => {
    if (!window.confirm('Delete this post?')) return
    try {
      await api.delete(`/community/posts/${postId}`)
      toast.success('Post deleted')
      fetchDepartment()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to delete post')
    }
  }

  if (!department) {
    return (
      <div className="card text-center py-16">
        <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">No department assigned</h2>
        <p className="text-gray-600 text-sm max-w-md mx-auto">
          You have not been assigned a professional category yet. Your department community
          will appear here once the company has placed you in a category.
        </p>
        <Link to="/portal/community" className="btn-primary mt-6 inline-block">
          Visit the general community
        </Link>
      </div>
    )
  }

  return (
    <div>
      {/* Department header */}
      <div className="bg-gradient-to-r from-primary-700 to-primary-900 text-white rounded-2xl p-8 mb-8">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <span className="inline-block px-3 py-1 rounded-full bg-white/10 text-xs font-medium tracking-wide mb-3">
              My Department
            </span>
            <h1 className="text-3xl font-bold">{department}</h1>
            <p className="text-primary-100 mt-1">
              {user?.qualification_position_name
                ? `Position: ${user.qualification_position_name}`
                : 'Your department community - connect with colleagues in the same field.'}
            </p>
          </div>
          <Link to="/portal/community" className="btn bg-white/10 text-white hover:bg-white/20 text-sm">
            General community
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Department community feed */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Department Community</h2>
              <p className="text-sm text-gray-500">Questions, updates and ideas from your department.</p>
            </div>
            <button onClick={() => setShowNewPost(true)} className="btn-primary text-sm">
              New Post
            </button>
          </div>

          {/* Category filter */}
          {categories.length > 0 && (
            <div className="flex gap-2 flex-wrap">
              <button
                onClick={() => setActiveCategory('')}
                className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
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
                  className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
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

          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto"></div>
            </div>
          ) : posts.length === 0 ? (
            <div className="card text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p className="text-gray-600">No posts in this department yet</p>
              <p className="text-sm text-gray-500 mt-1">Be the first to share something with your department.</p>
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
                        {post.status !== 'published' && (
                          <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700">
                            {post.status === 'pending' ? 'Awaiting moderation' : 'Removed'}
                          </span>
                        )}
                      </div>
                    </div>
                    <h3 className="font-semibold text-gray-900 mt-3">{post.title}</h3>
                    <p className="text-gray-600 text-sm mt-1 whitespace-pre-line">{post.content}</p>
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

        {/* Department members */}
        <div>
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Department Members</h3>
            {members.length === 0 ? (
              <p className="text-sm text-gray-500">No members found yet.</p>
            ) : (
              <div className="space-y-3">
                {members.map((member) => (
                  <div key={member.id} className="flex items-center gap-3">
                    <div className="w-9 h-9 bg-primary-100 rounded-full flex items-center justify-center shrink-0">
                      <span className="text-primary-700 font-semibold text-sm">
                        {member.name?.charAt(0) || 'N'}
                      </span>
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {member.name}
                        {member.username && (
                          <span className="text-primary-600 ml-1">@{member.username}</span>
                        )}
                      </p>
                      <p className="text-xs text-gray-500 truncate">
                        {member.qualification_position_name || member.role}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="card mt-6 bg-primary-50 border-primary-100">
            <h4 className="font-semibold text-gray-900 text-sm mb-2">About this department</h4>
            <p className="text-sm text-gray-600">
              Every department has its own community, and the general community links every
              department together. Post here for department-specific discussion, or visit the
              general community to interact with the whole company.
            </p>
          </div>
        </div>
      </div>

      {/* New Post Modal */}
      {showNewPost && (
        <div className="modal-overlay" onClick={() => setShowNewPost(false)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              New Post in {department}
            </h2>
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
                  placeholder="Share your update, question or idea with your department..."
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
    </div>
  )
}

export default DeveloperDepartment
