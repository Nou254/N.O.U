import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface ProgressReport {
  id: number
  week_label: string
  percentage: number
  admin_percentage: number | null
  summary: string | null
  created_at: string
}

interface Project {
  id: number
  title: string
  description: string | null
  category: string | null
  required_people: number
  status: string
  budget: number | null
  deadline: string | null
  created_at: string
  member_count: number
  docs_released: boolean
  progress_percentage: number | null
  progress_reports: ProgressReport[]
  effective_deadline: string | null
  overdue: boolean
  members: { id: number; name: string; role: string | null; is_team_leader: boolean }[]
}

const STATUS_BADGE: Record<string, string> = {
  open: 'badge-primary',
  in_progress: 'badge-warning',
  review: 'badge-info',
  completed: 'badge-success',
  published: 'badge-gray',
}

const STATUS_LABEL: Record<string, string> = {
  open: 'Open for developers',
  in_progress: 'In progress',
  review: 'Under review',
  completed: 'Completed',
  published: 'Published',
}

const InvestorProjects = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      setLoading(true)
      const response = await api.get('/portal/projects')
      setProjects(response.data.projects)
    } catch (error) {
      console.error('Error fetching projects:', error)
      toast.error('Failed to load company progress')
    } finally {
      setLoading(false)
    }
  }

  const progressPercent = (p: Project) => {
    return Math.min(100, Math.round((p.member_count / p.required_people) * 100))
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Company Projects Progress</h1>
        <p className="text-gray-600">
          Read-only view of N.O.U's ongoing projects. You can track progress but cannot modify anything.
        </p>
      </div>

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
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3v18h18M8 17V9m4 8V5m4 12v-6" />
            </svg>
            <p className="text-gray-600">No company projects yet</p>
            <p className="text-sm text-gray-500 mt-1">Projects posted by management will appear here.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {projects.map((project) => (
              <div
                key={project.id}
                className="border border-gray-200 rounded-lg p-6 hover:border-primary-300 transition-colors"
              >
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 flex-wrap mb-2">
                      <h3 className="font-semibold text-gray-900">{project.title}</h3>
                      <span className={STATUS_BADGE[project.status] || 'badge-gray'}>
                        {STATUS_LABEL[project.status] || project.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                      {project.description || 'No description provided.'}
                    </p>

                    {/* Progress bar */}
                    <div className="mb-2">
                      <div className="flex justify-between text-xs text-gray-500 mb-1">
                        <span>Team size: {project.member_count}/{project.required_people} developers</span>
                        <span>{progressPercent(project)}%</span>
                      </div>
                      <div className="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-primary-500 to-primary-700 rounded-full transition-all duration-500"
                          style={{ width: `${progressPercent(project)}%` }}
                        />
                      </div>
                    </div>

                    {/* Graded weekly progress */}
                    {project.progress_reports && project.progress_reports.length > 0 ? (
                      <div className="mb-4">
                        <div className="flex items-center justify-between mb-1">
                          <p className="text-xs font-medium text-gray-700">
                            Graded weekly progress: {project.progress_percentage}%
                          </p>
                        </div>
                        <div className="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-green-500 rounded-full transition-all duration-500"
                            style={{ width: `${Math.min(100, project.progress_percentage || 0)}%` }}
                          />
                        </div>
                        <div className="mt-3 space-y-2">
                          {project.progress_reports.map((report) => (
                            <div
                              key={report.id}
                              className="bg-gray-50 rounded-lg px-3 py-2 border border-gray-200 flex items-center gap-3"
                            >
                              <div
                                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs shrink-0 ${
                                  report.admin_percentage != null
                                    ? 'bg-green-600 text-white'
                                    : 'bg-green-50 text-green-700'
                                }`}
                              >
                                {report.admin_percentage ?? report.percentage}%
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-xs font-medium text-gray-900">{report.week_label}</p>
                                {report.summary && (
                                  <p className="text-xs text-gray-600 line-clamp-1">{report.summary}</p>
                                )}
                                <p className="text-[10px] text-gray-400">
                                  {new Date(report.created_at).toLocaleString()}
                                  {report.admin_percentage != null && (
                                    <span className="text-green-600 ml-1">· admin verified</span>
                                  )}
                                </p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <p className="text-xs text-gray-400 mb-4">
                        No weekly progress reports yet.
                      </p>
                    )}

                    <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                      {project.category && (
                        <span>Category: {project.category.replace('_', ' ')}</span>
                      )}
                      {project.effective_deadline && (
                        <span className={project.overdue ? 'text-red-600 font-medium' : ''}>
                          Deadline: {project.effective_deadline}
                          {project.overdue ? ' (overdue)' : ''}
                        </span>
                      )}
                      {project.budget && (
                        <span>Budget: KSh {project.budget.toLocaleString()}</span>
                      )}
                      <span>
                        {project.docs_released
                          ? 'Documentation released'
                          : 'Documentation pending team fill'}
                      </span>
                    </div>

                    {project.members.length > 0 && (
                      <div className="mt-4 flex flex-wrap gap-2">
                        {project.members.map((m) => (
                          <span
                            key={m.id}
                            className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700"
                            title={m.role || 'No role set'}
                          >
                            {m.name}{m.is_team_leader ? ' · leader' : ''}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default InvestorProjects
