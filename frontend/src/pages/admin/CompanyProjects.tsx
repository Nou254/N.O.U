import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Member {
  id: number
  name: string
  role: string | null
  is_team_leader: boolean
}

interface Project {
  id: number
  title: string
  description: string | null
  category: string | null
  section: string | null
  product_status: string | null
  platform: string | null
  required_people: number
  status: string
  budget: number | null
  deadline: string | null
  effective_deadline: string | null
  overdue: boolean
  member_count: number
  docs_released: boolean
  progress_percentage: number | null
  progress_reports: ProgressReport[]
  help_requests: HelpRequest[]
  deadline_extensions: DeadlineExtension[]
  members: Member[]
  documents: { id: number; filename: string; doc_type: string; download_url?: string | null }[]
  releases: {
    id: number
    filename: string
    version: string | null
    platform: string | null
    file_size: number | null
    downloads: number
    download_url?: string | null
  }[]
}

interface ExtraRequest {
  id: number
  project_id: number
  requested_by: number
  requested_count: number
  reason: string | null
  status: string
  created_at: string
}

interface DeadlineExtension {
  id: number
  project_id: number
  requested_days: number
  reason: string | null
  status: string
  requested_by: number
  created_at: string
}

interface ProgressReport {
  id: number
  week_label: string
  percentage: number
  admin_percentage: number | null
  graded_at: string | null
  summary: string | null
  created_at: string
}

interface HelpRequest {
  id: number
  filename: string
  message: string | null
  status: string
  user_id: number
  created_at: string
  download_url?: string | null
}

interface ChatMsg {
  id: number
  sender: string
  message: string
  is_ai: boolean
  created_at: string
}

const STATUS_BADGE: Record<string, string> = {
  open: 'badge-primary',
  in_progress: 'badge-warning',
  review: 'badge-info',
  completed: 'badge-success',
  published: 'badge-gray',
}

const CATEGORIES = [
  'network_installation',
  'web_development',
  'mobile_app',
  'database_setup',
  'security_audit',
  'software_development',
  'it_support',
  'other',
]

const PUBLISH_SECTIONS = [
  'Games and Entertainment',
  'Bots',
  'Education and Learning',
  'Business and Enterprise',
  'Productivity and Personal Organization',
  'Finance and Accounting',
  'Health and Wellness',
  'Communication and Social Platforms',
  'E-Commerce and Retail',
  'Hospitality and Tourism',
  'Government and Public Administration',
  'Agriculture',
  'Transport and Logistics',
  'Security and Monitoring',
  'Networking and Infrastructure',
  'Developer and IT Tools',
  'Artificial Intelligence',
  'Multimedia and Creative Software',
  'Lifestyle and Personal Applications',
  'Religious and Community Systems',
  'Specialized and Custom Software',
  'Custom Development Services',
  'Other',
]

// N.O.U. product classification (today.md): Free/Paid/Subscription/...
const PRODUCT_STATUSES = ['Free', 'Paid', 'Subscription', 'Freemium', 'Enterprise', 'Custom', 'Internal']
// N.O.U. platform classification (today.md): Web/PWA/Android/...
const PLATFORMS = ['Web', 'PWA', 'Android', 'Windows', 'iOS', 'Cloud/SaaS', 'Multi-Platform']

const AdminCompanyProjects = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [requests, setRequests] = useState<ExtraRequest[]>([])
  const [extensions, setExtensions] = useState<DeadlineExtension[]>([])
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<'projects' | 'requests' | 'extensions'>('projects')
  const [selected, setSelected] = useState<Project | null>(null)
  const [chat, setChat] = useState<ChatMsg[]>([])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [sendingChat, setSendingChat] = useState(false)

  // Publish modal (section picker)
  const [publishing, setPublishing] = useState<Project | null>(null)
  const [publishSection, setPublishSection] = useState('Games and Entertainment')
  const [publishStatus, setPublishStatus] = useState('Free')
  const [publishPlatform, setPublishPlatform] = useState('Web')
  const [publishingBusy, setPublishingBusy] = useState(false)

  // Progress grading
  const [gradeValues, setGradeValues] = useState<Record<number, string>>({})
  const [gradingId, setGradingId] = useState<number | null>(null)

  // Create form
  const [showCreate, setShowCreate] = useState(false)
  const [creating, setCreating] = useState(false)
  const [form, setForm] = useState({
    title: '',
    description: '',
    category: 'network_installation',
    section: 'Games and Entertainment',
    required_people: '1',
    budget: '',
    deadline: '',
  })
  const [specFile, setSpecFile] = useState<File | null>(null)

  // Software release upload
  const [releaseFile, setReleaseFile] = useState<File | null>(null)
  const [releaseVersion, setReleaseVersion] = useState('1.0.0')
  const [releasePlatform, setReleasePlatform] = useState('')
  const [releaseBusy, setReleaseBusy] = useState(false)

  const fetchProjects = async () => {
    try {
      const response = await api.get('/admin/projects')
      setProjects(response.data.projects)
    } catch (error) {
      console.error('Error fetching projects:', error)
      toast.error('Failed to load projects')
    }
  }

  const fetchRequests = async () => {
    try {
      const response = await api.get('/admin/projects/extra-requests')
      setRequests(response.data.requests)
    } catch (error) {
      console.error('Error fetching requests:', error)
    }
  }

  const fetchExtensions = async () => {
    try {
      const response = await api.get('/admin/projects/extensions')
      setExtensions(response.data.requests || [])
    } catch (error) {
      console.error('Error fetching extensions:', error)
    }
  }

  useEffect(() => {
    const init = async () => {
      setLoading(true)
      await Promise.all([fetchProjects(), fetchRequests(), fetchExtensions()])
      setLoading(false)
    }
    init()
  }, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.title.trim()) {
      toast.error('Project title is required')
      return
    }
    setCreating(true)
    try {
      const body = new FormData()
      body.append('title', form.title)
      body.append('description', form.description)
      body.append('category', form.category)
      body.append('required_people', form.required_people)
      if (form.budget) body.append('budget', form.budget)
      if (form.deadline) body.append('deadline', form.deadline)
      if (specFile) body.append('file', specFile)
      const response = await api.post('/admin/projects', body, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast.success(`Project "${response.data.title}" created`)
      setShowCreate(false)
      setForm({
        title: '', description: '', category: 'network_installation',
        section: 'Games and Entertainment', required_people: '1', budget: '', deadline: '',
      })
      setSpecFile(null)
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to create project')
    } finally {
      setCreating(false)
    }
  }

  const handlePublish = async () => {
    if (!publishing) return
    setPublishingBusy(true)
    try {
      await api.post(`/admin/projects/${publishing.id}/publish`, {
        section: publishSection,
        product_status: publishStatus,
        platform: publishPlatform,
      })
      toast.success(`Published under ${publishSection}`)
      setPublishing(null)
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to publish')
    } finally {
      setPublishingBusy(false)
    }
  }

  const handleGrade = async (project: Project, report: ProgressReport) => {
    const value = Number(gradeValues[report.id])
    if (Number.isNaN(value) || value < 0 || value > 100) {
      toast.error('Grade must be between 0 and 100')
      return
    }
    setGradingId(report.id)
    try {
      await api.post(
        `/portal/projects/${project.id}/progress/${report.id}/grade`,
        { admin_percentage: value }
      )
      toast.success(`Graded ${report.week_label}: ${value}%`)
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to grade report')
    } finally {
      setGradingId(null)
    }
  }

  const handleExtensionDecision = async (ext: DeadlineExtension, approve: boolean) => {
    try {
      const response = await api.post(`/admin/projects/extensions/${ext.id}/decision`, {
        approve,
      })
      toast.success(response.data.message)
      fetchExtensions()
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to process extension')
    }
  }

  const openDetail = async (project: Project) => {
    setSelected(project)
    setChatLoading(true)
    try {
      const response = await api.get(`/portal/projects/${project.id}/chat`)
      setChat(response.data.messages)
    } catch (error) {
      console.error('Error fetching chat:', error)
      toast.error('Failed to load project chat')
    } finally {
      setChatLoading(false)
    }
  }

  const handleAdminChat = async () => {
    if (!chatInput.trim() || !selected) return
    setSendingChat(true)
    try {
      await api.post(`/portal/projects/${selected.id}/chat`, {
        message: chatInput,
        ask_ai: false,
      })
      setChatInput('')
      const response = await api.get(`/portal/projects/${selected.id}/chat`)
      setChat(response.data.messages)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to send message')
    } finally {
      setSendingChat(false)
    }
  }

  const handleReleaseUpload = async () => {
    if (!selected) return
    if (!releaseFile) {
      toast.error('Choose a software file to upload (.apk, .zip, .exe, ...)')
      return
    }
    setReleaseBusy(true)
    try {
      const body = new FormData()
      body.append('file', releaseFile)
      body.append('version', releaseVersion || '1.0.0')
      if (releasePlatform) body.append('platform', releasePlatform)
      const response = await api.post(`/admin/projects/${selected.id}/releases`, body, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast.success(response.data?.message || 'Software uploaded')
      setReleaseFile(null)
      setReleaseVersion('1.0.0')
      setReleasePlatform('')
      fetchProjects()
      // Refresh the open detail
      const fresh = projects.find((p) => p.id === selected.id)
      if (fresh) setSelected(fresh)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to upload software')
    } finally {
      setReleaseBusy(false)
    }
  }

  const handleReleaseDelete = async (releaseId: number) => {
    if (!selected) return
    if (!window.confirm('Remove this software release from downloads?')) return
    try {
      await api.delete(`/admin/projects/${selected.id}/releases/${releaseId}`)
      toast.success('Release removed')
      fetchProjects()
      const fresh = projects.find((p) => p.id === selected.id)
      if (fresh) setSelected(fresh)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to remove release')
    }
  }

  const handleExtraDecision = async (request: ExtraRequest, approve: boolean) => {
    try {
      const response = await api.post(`/admin/projects/extra-requests/${request.id}/decision`, {
        approve,
      })
      toast.success(response.data.message)
      fetchRequests()
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to process request')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Company Projects</h1>
          <p className="text-gray-600">
            Post projects and jobs for developers with required headcount and documentation.
          </p>
        </div>
        <button onClick={() => setShowCreate(true)} className="btn-primary">
          <span className="flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Post new project
          </span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 bg-gray-100 rounded-lg p-1 w-fit flex-wrap">
        <button
          onClick={() => setTab('projects')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            tab === 'projects' ? 'bg-white text-primary-700 shadow-sm' : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Projects ({projects.length})
        </button>
        <button
          onClick={() => setTab('requests')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            tab === 'requests' ? 'bg-white text-primary-700 shadow-sm' : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Extra dev requests ({requests.filter((r) => r.status === 'pending').length})
        </button>
        <button
          onClick={() => setTab('extensions')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            tab === 'extensions' ? 'bg-white text-primary-700 shadow-sm' : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Deadline extensions ({extensions.filter((e) => e.status === 'pending').length})
        </button>
      </div>

      {loading ? (
        <div className="text-center py-16">
          <div className="spinner mx-auto"></div>
        </div>
      ) : tab === 'projects' ? (
        <div className="card">
          {projects.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600">No projects posted yet</p>
              <p className="text-sm text-gray-500 mt-1">Post your first project to get started.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2 flex-wrap">
                        <h3 className="font-semibold text-gray-900">{project.title}</h3>
                        <span className={STATUS_BADGE[project.status] || 'badge-gray'}>
                          {project.status.replace('_', ' ')}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">
                        {project.description || 'No description provided.'}
                      </p>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-2">
                        <span>Category: {project.category?.replace('_', ' ') || 'General'}</span>
                        {project.section && <span>Section: {project.section}</span>}
                        <span>Team: {project.member_count}/{project.required_people}</span>
                        {project.budget && <span>Budget: KSh {project.budget.toLocaleString()}</span>}
                        {project.effective_deadline && (
                          <span className={project.overdue ? 'text-red-600 font-medium' : ''}>
                            Deadline: {project.effective_deadline}{project.overdue ? ' (overdue)' : ''}
                          </span>
                        )}
                        <span>
                          {project.docs_released
                            ? 'Docs released'
                            : 'Docs locked'}
                        </span>
                      </div>
                      {project.documents.length > 0 && (
                        <p className="text-xs text-gray-500 mb-2">
                          Documents: {project.documents.map((d) => d.filename).join(', ')}
                        </p>
                      )}
                      {project.members.length > 0 && (
                        <div className="flex flex-wrap gap-2">
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
                    <div className="flex flex-col items-end gap-2 shrink-0">
                      {project.status === 'review' || project.status === 'completed' ? (
                        <button
                          onClick={() => {
                            setPublishSection(project.section || 'Games and Entertainment')
                            setPublishStatus(project.product_status || 'Free')
                            setPublishPlatform(project.platform || 'Web')
                            setPublishing(project)
                          }}
                          className="btn-primary text-sm"
                        >
                          Publish for customers
                        </button>
                      ) : project.status === 'published' ? (
                        <span className="badge-gray">Published · {project.section || 'General'}</span>
                      ) : null}
                      <button
                        onClick={() => openDetail(project)}
                        className="btn-secondary text-sm"
                      >
                        Chat & progress
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : tab === 'requests' ? (
        <div className="card">
          {requests.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600">No extra developer requests</p>
            </div>
          ) : (
            <div className="space-y-4">
              {requests.map((request) => (
                <div
                  key={request.id}
                  className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2 flex-wrap">
                        <h3 className="font-semibold text-gray-900">Project #{request.project_id}</h3>
                        <span className={request.status === 'pending' ? 'badge-warning' : request.status === 'approved' ? 'badge-success' : 'badge-danger'}>
                          {request.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700 mb-2">
                        Requesting <strong>{request.requested_count} extra developer{request.requested_count > 1 ? 's' : ''}</strong>
                      </p>
                      {request.reason && (
                        <p className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
                          "{request.reason}"
                        </p>
                      )}
                      <p className="text-xs text-gray-400 mt-2">
                        Requested: {new Date(request.created_at).toLocaleString()}
                      </p>
                    </div>
                    {request.status === 'pending' && (
                      <div className="flex flex-col gap-2 shrink-0">
                        <button
                          onClick={() => handleExtraDecision(request, true)}
                          className="btn-primary text-sm"
                        >
                          Approve
                        </button>
                        <button
                          onClick={() => handleExtraDecision(request, false)}
                          className="btn-outline text-sm"
                        >
                          Deny
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="card">
          {extensions.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600">No deadline extension requests</p>
            </div>
          ) : (
            <div className="space-y-4">
              {extensions.map((ext) => {
                const project = projects.find((p) => p.id === ext.project_id)
                return (
                  <div
                    key={ext.id}
                    className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-4 flex-wrap">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-3 mb-2 flex-wrap">
                          <h3 className="font-semibold text-gray-900">
                            {project ? project.title : `Project #${ext.project_id}`}
                          </h3>
                          <span className={ext.status === 'pending' ? 'badge-warning' : ext.status === 'approved' ? 'badge-success' : 'badge-danger'}>
                            {ext.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">
                          Requesting <strong>+{ext.requested_days} day{ext.requested_days > 1 ? 's' : ''}</strong>{' '}
                          past the scheduled deadline (max 4 weeks)
                        </p>
                        {ext.reason && (
                          <p className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3">"{ext.reason}"</p>
                        )}
                        <p className="text-xs text-gray-400 mt-2">
                          Requested: {new Date(ext.created_at).toLocaleString()}
                        </p>
                      </div>
                      {ext.status === 'pending' && (
                        <div className="flex flex-col gap-2 shrink-0">
                          <button
                            onClick={() => handleExtensionDecision(ext, true)}
                            className="btn-primary text-sm"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleExtensionDecision(ext, false)}
                            className="btn-outline text-sm"
                          >
                            Deny
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}

      {/* Publish modal: pick the gallery section */}
      {publishing && (
        <div className="modal-overlay" onClick={() => setPublishing(null)}>
          <div className="modal-content max-w-md" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-1">Publish to the customer gallery</h2>
            <p className="text-sm text-gray-500 mb-4">
              "{publishing.title}" will appear for customers under a gallery section.
            </p>
            <label htmlFor="pub-section" className="label">Gallery section</label>
            <select
              id="pub-section"
              value={publishSection}
              onChange={(e) => setPublishSection(e.target.value)}
              className="input mb-4"
            >
              {PUBLISH_SECTIONS.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
            <label htmlFor="pub-status" className="label">Product status</label>
            <select
              id="pub-status"
              value={publishStatus}
              onChange={(e) => setPublishStatus(e.target.value)}
              className="input mb-4"
            >
              {PRODUCT_STATUSES.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
            <label htmlFor="pub-platform" className="label">Platform</label>
            <select
              id="pub-platform"
              value={publishPlatform}
              onChange={(e) => setPublishPlatform(e.target.value)}
              className="input mb-4"
            >
              {PLATFORMS.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
            <div className="flex justify-end gap-3">
              <button onClick={() => setPublishing(null)} className="btn-outline">Cancel</button>
              <button onClick={handlePublish} disabled={publishingBusy} className="btn-primary">
                {publishingBusy ? 'Publishing...' : 'Publish project'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Project detail modal: progress + help requests + chat (admin is in the chat) */}
      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div className="modal-content max-w-4xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">{selected.title}</h2>
                <p className="text-sm text-gray-500">
                  {selected.status.replace('_', ' ')} · {selected.member_count}/{selected.required_people} developers
                  {selected.progress_percentage != null &&
                    ` · Graded progress: ${selected.progress_percentage}%`}
                </p>
              </div>
              <button onClick={() => setSelected(null)} className="text-gray-400 hover:text-gray-600">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left: progress + help requests */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Weekly Progress (grade it)</h3>
                <div className="space-y-2 mb-5 max-h-56 overflow-y-auto">
                  {selected.progress_reports && selected.progress_reports.length > 0 ? (
                    selected.progress_reports.map((report) => (
                      <div key={report.id} className="bg-gray-50 rounded-lg px-3 py-2 border border-gray-200">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-green-50 text-green-700 flex items-center justify-center font-bold text-xs shrink-0">
                            {report.admin_percentage ?? report.percentage}%
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-xs font-medium text-gray-900">{report.week_label}</p>
                            {report.summary && <p className="text-xs text-gray-600 line-clamp-2">{report.summary}</p>}
                            <p className="text-[10px] text-gray-400">
                              {new Date(report.created_at).toLocaleString()}
                              {report.graded_at && ' · graded ' + new Date(report.graded_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                          <input
                            type="number"
                            min={0}
                            max={100}
                            value={gradeValues[report.id] ?? report.admin_percentage ?? report.percentage}
                            onChange={(e) => setGradeValues((p) => ({ ...p, [report.id]: e.target.value }))}
                            className="input text-xs !py-1 sm:w-24"
                            placeholder="0-100"
                          />
                          <button
                            onClick={() => handleGrade(selected, report)}
                            disabled={gradingId === report.id}
                            className="btn-primary text-xs !py-1"
                          >
                            {gradingId === report.id ? 'Grading...' : report.admin_percentage != null ? 'Regrade' : 'Grade'}
                          </button>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500">No progress reports yet.</p>
                  )}
                </div>

                {selected.deadline_extensions && selected.deadline_extensions.length > 0 && (
                  <>
                    <h3 className="font-semibold text-gray-900 mb-2">⏰ Deadline Extensions</h3>
                    <div className="space-y-2 mb-5 max-h-36 overflow-y-auto">
                      {selected.deadline_extensions.map((ext) => (
                        <div key={ext.id} className="bg-amber-50 rounded-lg px-3 py-2 border border-amber-200 text-xs">
                          <div className="flex items-center justify-between gap-2">
                            <p className="font-medium text-gray-900">+{ext.requested_days} days</p>
                            <span className={ext.status === 'pending' ? 'badge-warning' : ext.status === 'approved' ? 'badge-success' : 'badge-danger'}>
                              {ext.status}
                            </span>
                          </div>
                          {ext.reason && <p className="text-gray-600 mt-1">"{ext.reason}"</p>}
                          {ext.status === 'pending' && (
                            <div className="flex gap-2 mt-2">
                              <button
                                onClick={() => handleExtensionDecision(ext, true)}
                                className="btn-primary text-xs !py-1"
                              >
                                Approve
                              </button>
                              <button
                                onClick={() => handleExtensionDecision(ext, false)}
                                className="btn-outline text-xs !py-1"
                              >
                                Deny
                              </button>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </>
                )}

                <h3 className="font-semibold text-gray-900 mb-2">Developer Help Requests</h3>
                <div className="space-y-2 max-h-44 overflow-y-auto">
                  {selected.help_requests && selected.help_requests.length > 0 ? (
                    selected.help_requests.map((req) => (
                      <div key={req.id} className="bg-gray-50 rounded-lg px-3 py-2 border border-gray-200 text-sm">
                        <div className="flex items-center justify-between gap-2">
                          <p className="font-medium text-gray-900 truncate">{req.filename}</p>
                          <a
                            href={req.download_url || `/api/v1/portal/projects/${selected.id}/help/${req.id}/download`}
                            target="_blank"
                            rel="noreferrer"
                            className="text-xs text-primary-600 hover:text-primary-700 shrink-0"
                          >
                            Download
                          </a>
                        </div>
                        {req.message && <p className="text-gray-600 text-xs mt-1">{req.message}</p>}
                        <p className="text-[10px] text-gray-400 mt-1">
                          {req.status} · {new Date(req.created_at).toLocaleString()}
                        </p>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500">No help requests yet.</p>
                  )}
                </div>

                {/* Software releases: the finished build customers download */}
                <h3 className="font-semibold text-gray-900 mb-2 mt-5">Software Releases (customer downloads)</h3>
                <div className="space-y-2 max-h-44 overflow-y-auto mb-3">
                  {selected.releases && selected.releases.length > 0 ? (
                    selected.releases.map((rel) => (
                      <div key={rel.id} className="bg-gray-50 rounded-lg px-3 py-2 border border-gray-200 text-sm">
                        <div className="flex items-center justify-between gap-2">
                          <div className="min-w-0">
                            <p className="font-medium text-gray-900 truncate">{rel.filename}</p>
                            <p className="text-[11px] text-gray-500">
                              v{rel.version || '1.0.0'}
                              {rel.platform ? ` · ${rel.platform}` : ''}
                              {rel.downloads ? ` · ${rel.downloads} download${rel.downloads === 1 ? '' : 's'}` : ''}
                            </p>
                          </div>
                          <div className="flex items-center gap-2 shrink-0">
                            <a
                              href={rel.download_url || '#'}
                              target="_blank"
                              rel="noreferrer"
                              className="text-xs text-primary-600 hover:text-primary-700"
                            >
                              Open
                            </a>
                            <button
                              onClick={() => handleReleaseDelete(rel.id)}
                              className="text-xs text-red-600 hover:text-red-700"
                            >
                              Remove
                            </button>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500">
                      No software uploaded yet. Upload the finished build (.apk, .zip, .exe...) so customers can download it once published.
                    </p>
                  )}
                </div>
                <div className="bg-primary-50 border border-primary-100 rounded-lg p-3 space-y-2">
                  <input
                    type="file"
                    accept=".apk,.aab,.zip,.exe,.msi,.dmg,.ipa,.jar,.pdf,.docx,.7z,.rar,.tar.gz,.tgz,.whl,.iso"
                    onChange={(e) => setReleaseFile(e.target.files?.[0] || null)}
                    className="input text-xs !py-1.5"
                  />
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="text"
                      value={releaseVersion}
                      onChange={(e) => setReleaseVersion(e.target.value)}
                      className="input text-xs !py-1.5"
                      placeholder="Version (1.0.0)"
                    />
                    <input
                      type="text"
                      value={releasePlatform}
                      onChange={(e) => setReleasePlatform(e.target.value)}
                      className="input text-xs !py-1.5"
                      placeholder="Platform (Android)"
                    />
                  </div>
                  <button
                    onClick={handleReleaseUpload}
                    disabled={releaseBusy}
                    className="btn-primary text-xs !py-1.5 w-full"
                  >
                    {releaseBusy ? 'Uploading...' : 'Upload software build'}
                  </button>
                  <p className="text-[10px] text-gray-500">
                    Appears as a Download button in the customer gallery once the project is published.
                  </p>
                </div>
              </div>

              {/* Right: chat (admin is always in the chat) */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Project Chat</h3>
                <div className="h-72 overflow-y-auto bg-gray-50 rounded-lg p-3 space-y-2 mb-3 border border-gray-200">
                  {chatLoading ? (
                    <p className="text-sm text-gray-400 text-center pt-10">Loading...</p>
                  ) : chat.length === 0 ? (
                    <p className="text-sm text-gray-400 text-center pt-10">No messages yet.</p>
                  ) : (
                    chat.map((msg) => (
                      <div key={msg.id} className={`flex ${msg.is_ai ? 'justify-start' : 'justify-end'}`}>
                        <div
                          className={`max-w-[85%] rounded-lg px-3 py-1.5 text-sm ${
                            msg.is_ai
                              ? 'bg-primary-50 border border-primary-200 text-gray-800'
                              : 'bg-primary-600 text-white'
                          }`}
                        >
                          <p className={`text-[10px] mb-0.5 ${msg.is_ai ? 'text-primary-600' : 'text-primary-200'}`}>
                            {msg.is_ai ? 'N.O.U Lite AI' : msg.sender}
                          </p>
                          <p className="whitespace-pre-wrap">{msg.message}</p>
                        </div>
                      </div>
                    ))
                  )}
                </div>
                <div className="flex gap-2">
                  <input
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAdminChat()}
                    className="input flex-1 text-sm"
                    placeholder="Message the team..."
                  />
                  <button
                    onClick={handleAdminChat}
                    disabled={sendingChat || !chatInput.trim()}
                    className="btn-primary text-sm"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button onClick={() => setSelected(null)} className="btn-secondary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create project modal */}
      {showCreate && (
        <div className="modal-overlay" onClick={() => setShowCreate(false)}>
          <div className="modal-content max-w-2xl" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Post New Project</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label htmlFor="proj-title" className="label">Project title *</label>
                <input
                  id="proj-title"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  required
                  className="input"
                  placeholder="e.g. Campus LAN Network Installation"
                />
              </div>
              <div>
                <label htmlFor="proj-desc" className="label">Description</label>
                <textarea
                  id="proj-desc"
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  rows={3}
                  className="input"
                  placeholder="What does this project involve?"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="proj-cat" className="label">Category</label>
                  <select
                    id="proj-cat"
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    className="input"
                  >
                    {CATEGORIES.map((cat) => (
                      <option key={cat} value={cat}>{cat.replace('_', ' ')}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label htmlFor="proj-section" className="label">Gallery section (when published)</label>
                  <select
                    id="proj-section"
                    value={form.section}
                    onChange={(e) => setForm({ ...form, section: e.target.value })}
                    className="input"
                  >
                    {PUBLISH_SECTIONS.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label htmlFor="proj-people" className="label">Required people *</label>
                  <input
                    id="proj-people"
                    type="number"
                    min={1}
                    max={20}
                    value={form.required_people}
                    onChange={(e) => setForm({ ...form, required_people: e.target.value })}
                    required
                    className="input"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Docs release only when this many developers have joined.
                  </p>
                </div>
                <div>
                  <label htmlFor="proj-budget" className="label">Budget (KSh)</label>
                  <input
                    id="proj-budget"
                    type="number"
                    min={0}
                    value={form.budget}
                    onChange={(e) => setForm({ ...form, budget: e.target.value })}
                    className="input"
                    placeholder="e.g. 150000"
                  />
                </div>
                <div>
                  <label htmlFor="proj-deadline" className="label">Deadline</label>
                  <input
                    id="proj-deadline"
                    type="date"
                    value={form.deadline}
                    onChange={(e) => setForm({ ...form, deadline: e.target.value })}
                    className="input"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="proj-file" className="label">Project documentation (PDF / DOCX)</label>
                <input
                  id="proj-file"
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={(e) => setSpecFile(e.target.files?.[0] || null)}
                  className="input text-sm"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Attach the project specification. It's released to developers once the team is full.
                </p>
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button type="button" onClick={() => setShowCreate(false)} className="btn-outline">
                  Cancel
                </button>
                <button type="submit" disabled={creating} className="btn-primary">
                  {creating ? 'Creating...' : 'Post project'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminCompanyProjects
