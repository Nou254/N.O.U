import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../services/api'
import toast from 'react-hot-toast'
import { useAppSelector } from '../../hooks/useAppSelector'
import AnnouncementsFeed from '../../components/AnnouncementsFeed'

interface ProjectMember {
  id: number
  user_id: number
  name: string
  role: string | null
  is_team_leader: boolean
}

interface Project {
  id: number
  title: string
  description: string | null
  category: string | null
  required_people: number
  status: string
  team_leader_id: number | null
  budget: number | null
  deadline: string | null
  created_at: string
  member_count: number
  docs_released: boolean
  members: ProjectMember[]
  documents: { id: number; filename: string; doc_type: string }[]
}

const STATUS_BADGE: Record<string, string> = {
  open: 'badge-primary',
  in_progress: 'badge-warning',
  review: 'badge-info',
  completed: 'badge-success',
  published: 'badge-gray',
}

const ROLE_SUGGESTIONS = [
  'Frontend developer',
  'Backend developer',
  'Database engineer',
  'Network engineer',
  'UI/UX designer',
  'DevOps engineer',
  'QA engineer',
  'Project manager',
  'Security specialist',
]

const DeveloperProjects = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')
  const { user } = useAppSelector((state) => state.auth)
  const myUserId = user ? Number(user.id) : null
  const myDepartment = user?.qualification_category_name || ''
  const [joinProjectId, setJoinProjectId] = useState<number | null>(null)
  const [joinRole, setJoinRole] = useState('')

  const fetchProjects = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (statusFilter) params.append('status_filter', statusFilter)
      const response = await api.get(`/portal/projects?${params}`)
      setProjects(response.data.projects)
    } catch (error) {
      console.error('Error fetching projects:', error)
      toast.error('Failed to load projects')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProjects()
  }, [statusFilter])

  const isMember = (p: Project) => p.members.some((m) => m.user_id === myUserId)

  const handleJoin = async (projectId: number) => {
    try {
      const params = new URLSearchParams()
      if (joinRole) params.append('role', joinRole)
      const response = await api.post(`/portal/projects/${projectId}/join?${params}`)
      toast.success(response.data.docs_released
        ? 'Joined! Project documentation is now available.'
        : 'Joined! Documentation will be released when the team is full.')
      setJoinProjectId(null)
      setJoinRole('')
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to join project')
    }
  }

  const handleLeave = async (projectId: number) => {
    try {
      await api.post(`/portal/projects/${projectId}/leave`)
      toast.success('You have left the project')
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to leave project')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Company Projects</h1>
          <p className="text-gray-600">
            Join projects that match your skills. You can work on up to 3 at a time.
          </p>
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input sm:w-48"
        >
          <option value="">All statuses</option>
          <option value="open">Open</option>
          <option value="in_progress">In progress</option>
          <option value="review">Under review</option>
          <option value="completed">Completed</option>
          <option value="published">Published</option>
        </select>
      </div>

      {/* Department welcome - directed to your department community */}
      {myDepartment && (
        <Link
          to="/portal/department"
          className="block bg-gradient-to-r from-primary-700 to-primary-900 text-white rounded-2xl p-6 mb-8 hover:shadow-lg transition-shadow"
        >
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="inline-block px-3 py-1 rounded-full bg-white/10 text-xs font-medium tracking-wide mb-2">
                Your department
              </span>
              <h2 className="text-2xl font-bold">{myDepartment}</h2>
              <p className="text-primary-100 text-sm mt-1">
                Visit your department community, see your teammates and stay connected.
              </p>
            </div>
            <span className="btn bg-white/10 text-white hover:bg-white/20 text-sm">
              Open department community
            </span>
          </div>
        </Link>
      )}

      {/* Quorum: jokes of the day, quotes, and company communication */}
      <AnnouncementsFeed title="Quorum - from the company" />

      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-12">
            <svg
              className="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <p className="text-gray-600">No projects posted yet</p>
            <p className="text-sm text-gray-500 mt-1">Check back soon for new projects.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {projects.map((project) => {
              const member = isMember(project)
              const leader = project.members.find((m) => m.user_id === myUserId && m.is_team_leader)
              return (
                <div
                  key={project.id}
                  className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2 flex-wrap">
                        <h3 className="font-semibold text-gray-900">{project.title}</h3>
                        <span className={STATUS_BADGE[project.status] || 'badge-gray'}>
                          {project.status.replace('_', ' ')}
                        </span>
                        {project.category && (
                          <span className="text-sm text-gray-500">{project.category.replace('_', ' ')}</span>
                        )}
                      </div>

                      <p className="text-sm text-gray-600 mb-3">
                        {project.description || 'No description provided.'}
                      </p>

                      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                        <span className="flex items-center gap-1">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                          </svg>
                          {project.member_count}/{project.required_people} developers
                        </span>
                        {project.deadline && (
                          <span>Deadline: {project.deadline}</span>
                        )}
                        <span>
                          {project.docs_released
                            ? 'Documentation available'
                            : 'Documentation locked until team is full'}
                        </span>
                      </div>

                      {/* Members */}
                      {project.members.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-3">
                          {project.members.map((m) => (
                            <span
                              key={m.id}
                              className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${
                                m.user_id === myUserId ? 'bg-primary-50 text-primary-700 ring-1 ring-primary-200' : 'bg-gray-100 text-gray-700'
                              }`}
                              title={m.role || 'No role set'}
                            >
                              {m.name}{m.is_team_leader ? ' · leader' : ''}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    <div className="flex flex-col items-end gap-2 shrink-0">
                      {member ? (
                        <>
                          <Link
                            to={`/portal/projects/${project.id}`}
                            className="btn-primary text-sm"
                          >
                            {leader ? 'Manage project' : 'Open project'}
                          </Link>
                          <button
                            onClick={() => handleLeave(project.id)}
                            className="btn-outline text-sm"
                          >
                            Leave
                          </button>
                        </>
                      ) : project.status === 'open' ? (
                        <button
                          onClick={() => setJoinProjectId(project.id)}
                          className="btn-primary text-sm"
                        >
                          Join project
                        </button>
                      ) : (
                        <span className="text-xs text-gray-400">Not accepting members</span>
                      )}
                    </div>
                  </div>

                  {/* Join inline form */}
                  {joinProjectId === project.id && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <label htmlFor={`join-role-${project.id}`} className="label">
                        Your role on this project (e.g. database engineer)
                      </label>
                      <div className="flex gap-3 mt-2">
                        <input
                          id={`join-role-${project.id}`}
                          list="role-suggestions"
                          value={joinRole}
                          onChange={(e) => setJoinRole(e.target.value)}
                          className="input flex-1"
                          placeholder="e.g. network engineer"
                        />
                        <datalist id="role-suggestions">
                          {ROLE_SUGGESTIONS.map((r) => (
                            <option key={r} value={r} />
                          ))}
                        </datalist>
                        <button onClick={() => handleJoin(project.id)} className="btn-primary">
                          Confirm
                        </button>
                        <button
                          onClick={() => { setJoinProjectId(null); setJoinRole('') }}
                          className="btn-outline"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default DeveloperProjects
