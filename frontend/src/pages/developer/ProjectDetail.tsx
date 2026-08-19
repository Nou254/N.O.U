import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../../services/api'
import toast from 'react-hot-toast'
import { useAppSelector } from '../../hooks/useAppSelector'

interface Member {
  id: number
  user_id: number
  name: string
  role: string | null
  is_team_leader: boolean
}

interface DocumentItem {
  id: number
  filename: string
  doc_type: string
  download_url?: string | null
}

interface ChatMsg {
  id: number
  sender: string
  message: string
  is_ai: boolean
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

interface DeadlineExtension {
  id: number
  requested_days: number
  reason: string | null
  status: string
  requested_by: number
  created_at: string
}

interface HelpRequestItem {
  id: number
  filename: string
  message: string | null
  status: string
  user_id: number
  created_at: string
  download_url?: string | null
}

interface ProjectDetail {
  id: number
  title: string
  description: string | null
  category: string | null
  required_people: number
  status: string
  team_leader_id: number | null
  budget: number | null
  deadline: string | null
  effective_deadline: string | null
  overdue: boolean
  member_count: number
  docs_released: boolean
  progress_percentage: number | null
  progress_reports: ProgressReport[]
  deadline_extensions: DeadlineExtension[]
  help_requests: HelpRequestItem[]
  members: Member[]
  documents: DocumentItem[]
}

const STATUS_BADGE: Record<string, string> = {
  open: 'badge-primary',
  in_progress: 'badge-warning',
  review: 'badge-info',
  completed: 'badge-success',
  published: 'badge-gray',
}

const ProjectDetailPage = () => {
  const { id } = useParams<{ id: string }>()
  const [project, setProject] = useState<ProjectDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const { user } = useAppSelector((state) => state.auth)
  const myUserId = user ? Number(user.id) : null

  // Chat state
  const [messages, setMessages] = useState<ChatMsg[]>([])
  const [chatInput, setChatInput] = useState('')
  const [askAi, setAskAi] = useState(false)
  const [sending, setSending] = useState(false)

  // Extra devs
  const [extraCount, setExtraCount] = useState(1)
  const [extraReason, setExtraReason] = useState('')
  const [requestingExtra, setRequestingExtra] = useState(false)

  // Upload
  const [uploadFile, setUploadFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)

  // Weekly progress report
  const [weekLabel, setWeekLabel] = useState('')
  const [weekPct, setWeekPct] = useState('')
  const [weekSummary, setWeekSummary] = useState('')
  const [submittingProgress, setSubmittingProgress] = useState(false)

  // Help request
  const [helpFile, setHelpFile] = useState<File | null>(null)
  const [helpMessage, setHelpMessage] = useState('')
  const [submittingHelp, setSubmittingHelp] = useState(false)

  // Deadline extension
  const [extDays, setExtDays] = useState(7)
  const [extReason, setExtReason] = useState('')
  const [requestingExt, setRequestingExt] = useState(false)

  const fetchProject = async () => {
    try {
      const response = await api.get(`/portal/projects/${id}`)
      setProject(response.data)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to load project')
    } finally {
      setLoading(false)
    }
  }

  const fetchChat = async () => {
    try {
      const response = await api.get(`/portal/projects/${id}/chat`)
      setMessages(response.data.messages)
    } catch (error) {
      console.error('Error fetching chat:', error)
    }
  }

  useEffect(() => {
    fetchProject()
    fetchChat()
  }, [id])

  const me = project?.members.find((m) => m.user_id === myUserId)
  const isLeader = me?.is_team_leader

  const handleSend = async () => {
    if (!chatInput.trim()) return
    setSending(true)
    try {
      const response = await api.post(`/portal/projects/${id}/chat`, {
        message: chatInput,
        ask_ai: askAi,
      })
      setChatInput('')
      if (response.data.ai_reply) {
        toast.success('N.O.U Lite replied to your question')
      }
      fetchChat()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to send message')
    } finally {
      setSending(false)
    }
  }

  const handleRoleChange = async (member: Member, role: string, isLeaderFlag: boolean) => {
    try {
      await api.put(`/portal/projects/${id}/members/${member.id}/role`, {
        role,
        is_team_leader: isLeaderFlag,
      })
      toast.success('Role updated')
      fetchProject()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to update role')
    }
  }

  const handleRequestExtra = async () => {
    setRequestingExtra(true)
    try {
      await api.post(`/portal/projects/${id}/request-extra`, {
        requested_count: extraCount,
        reason: extraReason || undefined,
      })
      toast.success('Extra developer request submitted for admin approval')
      setExtraReason('')
      setExtraCount(1)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to submit request')
    } finally {
      setRequestingExtra(false)
    }
  }

  const handleUpload = async () => {
    if (!uploadFile) return
    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', uploadFile)
      formData.append('doc_type', 'completed')
      await api.post(`/portal/projects/${id}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast.success('Work uploaded for admin review')
      setUploadFile(null)
      fetchProject()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  const handleProgressSubmit = async () => {
    if (!weekLabel.trim()) {
      toast.error('Please enter a week label (e.g. Week 12)')
      return
    }
    const pct = Number(weekPct)
    if (Number.isNaN(pct) || pct < 0 || pct > 100) {
      toast.error('Progress percentage must be between 0 and 100')
      return
    }
    setSubmittingProgress(true)
    try {
      await api.post(`/portal/projects/${id}/progress`, {
        week_label: weekLabel.trim(),
        percentage: pct,
        summary: weekSummary || undefined,
      })
      toast.success('Weekly progress report submitted')
      setWeekLabel('')
      setWeekPct('')
      setWeekSummary('')
      fetchProject()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to submit report')
    } finally {
      setSubmittingProgress(false)
    }
  }

  const handleHelpSubmit = async () => {
    if (!helpFile) return
    setSubmittingHelp(true)
    try {
      const formData = new FormData()
      formData.append('file', helpFile)
      if (helpMessage) formData.append('message', helpMessage)
      await api.post(`/portal/projects/${id}/help`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast.success('Help request submitted - an admin will review it')
      setHelpFile(null)
      setHelpMessage('')
      fetchProject()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to submit help request')
    } finally {
      setSubmittingHelp(false)
    }
  }

  const handleExtensionRequest = async () => {
    if (!extReason.trim()) {
      toast.error('Please explain why you need the extension')
      return
    }
    setRequestingExt(true)
    try {
      await api.post(`/portal/projects/${id}/extension`, {
        requested_days: extDays,
        reason: extReason.trim(),
      })
      toast.success(`Extension of ${extDays} day(s) submitted for admin approval`)
      setExtReason('')
      fetchProject()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to submit extension request')
    } finally {
      setRequestingExt(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="spinner"></div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="text-center py-24">
        <p className="text-gray-600 mb-4">Project not found or you don't have access.</p>
        <Link to="/portal" className="btn-secondary">Back to projects</Link>
      </div>
    )
  }

  return (
    <div>
      <Link to="/portal" className="text-sm text-primary-600 hover:text-primary-700 mb-4 inline-block">
        Back to projects
      </Link>

      <div className="card mb-8">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h1 className="text-2xl font-bold text-gray-900">{project.title}</h1>
              <span className={STATUS_BADGE[project.status] || 'badge-gray'}>
                {project.status.replace('_', ' ')}
              </span>
            </div>
            <p className="text-gray-600 mt-2">
              {project.description || 'No description provided.'}
            </p>
            <div className="flex flex-wrap gap-4 text-sm text-gray-600 mt-3">
              <span>Category: {project.category?.replace('_', ' ') || 'General'}</span>
              <span>Team: {project.member_count}/{project.required_people}</span>
              {project.effective_deadline && (
                <span className={project.overdue ? 'text-red-600 font-medium' : ''}>
                  Deadline: {project.effective_deadline}{project.overdue ? ' (overdue)' : ''}
                </span>
              )}
              {project.budget && <span>Budget: KSh {project.budget.toLocaleString()}</span>}
            </div>
          </div>
        </div>

        {/* Documentation */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">Project Documentation</h3>
          {project.docs_released ? (
            project.documents.length > 0 ? (
              <ul className="space-y-2">
                {project.documents.map((doc) => (
                  <li key={doc.id} className="flex items-center justify-between bg-white rounded-lg px-3 py-2 border border-gray-200">
                    <span className="text-sm text-gray-700 flex items-center gap-2">
                      <svg className="w-4 h-4 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      {doc.filename}
                      <span className="text-xs text-gray-400">({doc.doc_type})</span>
                    </span>
                    <a
                      href={doc.download_url || `/api/v1/portal/projects/${project.id}/documents/${doc.id}/download`}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-primary-600 hover:text-primary-700"
                    >
                      Download
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-500">Documentation has been released but not uploaded yet.</p>
            )
          ) : (
            <p className="text-sm text-gray-500">
              Documentation is locked. It will be released once the team reaches{' '}
              {project.required_people} members ({project.member_count} joined so far).
            </p>
          )}
        </div>

        {/* Weekly progress reports (visible to investors) */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-1">Weekly Progress Reports</h3>
          <p className="text-xs text-gray-500 mb-3">
            Graded as a percentage so investors can track how the project is going.
            The admin's grade is the official number investors see.
            {isLeader
              ? ' As team leader, you submit the report at the end of every week.'
              : ' Only the team leader can submit reports.'}
          </p>

          {project.progress_reports && project.progress_reports.length > 0 && (
            <div className="space-y-2 mb-4">
              {project.progress_reports.map((report: ProgressReport) => (
                <div key={report.id} className="bg-white rounded-lg px-3 py-2 border border-gray-200 flex items-center gap-3">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm shrink-0 ${
                      report.admin_percentage != null
                        ? 'bg-green-50 text-green-700'
                        : 'bg-primary-50 text-primary-700'
                    }`}
                  >
                    {report.admin_percentage ?? report.percentage}%
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{report.week_label}</p>
                    {report.summary && (
                      <p className="text-xs text-gray-600 line-clamp-2">{report.summary}</p>
                    )}
                    <p className="text-xs text-gray-400">
                      {new Date(report.created_at).toLocaleString()}
                      {report.admin_percentage != null && (
                        <span className="text-green-600 ml-1">· admin-graded</span>
                      )}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {isLeader && (
            <div className="space-y-3">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <input
                  value={weekLabel}
                  onChange={(e) => setWeekLabel(e.target.value)}
                  className="input text-sm"
                  placeholder="Week label (e.g. Week 12)"
                />
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    min={0}
                    max={100}
                    value={weekPct}
                    onChange={(e) => setWeekPct(e.target.value)}
                    className="input text-sm"
                    placeholder="Progress % (0-100)"
                  />
                  <span className="text-sm text-gray-500 shrink-0">%</span>
                </div>
              </div>
              <textarea
                value={weekSummary}
                onChange={(e) => setWeekSummary(e.target.value)}
                rows={2}
                className="input text-sm"
                placeholder="What was accomplished this week? (optional)"
              />
              <button
                onClick={handleProgressSubmit}
                disabled={submittingProgress}
                className="btn-primary text-sm"
              >
                {submittingProgress ? 'Submitting...' : 'Submit weekly report'}
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Members & roles */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Team Members {isLeader && <span className="text-xs text-primary-600 ml-2">(you are team leader)</span>}
          </h2>
          <div className="space-y-3">
            {project.members.map((member) => (
              <div key={member.id} className="flex items-center justify-between gap-3 p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {member.name} {member.is_team_leader}
                  </p>
                  {isLeader || me?.user_id === member.user_id ? (
                    <input
                      value={member.role || ''}
                      onChange={(e) => handleRoleChange(member, e.target.value, member.is_team_leader)}
                      className="input text-xs mt-1 !py-1"
                      placeholder="Set role (e.g. database engineer)"
                    />
                  ) : (
                    <p className="text-xs text-gray-500">{member.role || 'No role set'}</p>
                  )}
                </div>
                {isLeader && (
                  <div className="flex flex-col gap-1">
                    <label className="flex items-center gap-1 text-xs text-gray-600">
                      <input
                        type="checkbox"
                        checked={member.is_team_leader}
                        onChange={(e) => handleRoleChange(member, member.role || 'developer', e.target.checked)}
                      />
                      Team leader
                    </label>
                  </div>
                )}
              </div>
            ))}
            {project.members.length === 0 && (
              <p className="text-sm text-gray-500">No members yet.</p>
            )}
          </div>

          {/* Upload completed work */}
          {me && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-2">Upload Completed Work</h3>
              <p className="text-xs text-gray-500 mb-3">
                Submit your completed files (PDF/DOCX) for admin review.
              </p>
              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                className="input text-sm mb-3"
              />
              <button
                onClick={handleUpload}
                disabled={!uploadFile || uploading}
                className="btn-primary w-full text-sm"
              >
                {uploading ? 'Uploading...' : 'Submit for review'}
              </button>
            </div>
          )}

          {/* Ask the company for help (anytime) */}
          {me && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-2">Ask the Company for Help</h3>
              <p className="text-xs text-gray-500 mb-3">
                Stuck on something? Upload a document about your work and an
                admin will review it. You can do this anytime.
              </p>
              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={(e) => setHelpFile(e.target.files?.[0] || null)}
                className="input text-sm mb-3"
              />
              <textarea
                value={helpMessage}
                onChange={(e) => setHelpMessage(e.target.value)}
                rows={2}
                className="input text-sm mb-3"
                placeholder="What help do you need? (optional)"
              />
              <button
                onClick={handleHelpSubmit}
                disabled={!helpFile || submittingHelp}
                className="btn-secondary w-full text-sm"
              >
                {submittingHelp ? 'Submitting...' : 'Submit help request'}
              </button>

              {project.help_requests && project.help_requests.length > 0 && (
                <div className="mt-3 space-y-2">
                  {project.help_requests.map((req: HelpRequestItem) => (
                    <div key={req.id} className="bg-white rounded-lg px-3 py-2 border border-gray-200 text-xs">
                      <div className="flex items-center justify-between gap-2">
                        <p className="font-medium text-gray-800 truncate">{req.filename}</p>
                        <a
                          href={req.download_url || `/api/v1/portal/projects/${project.id}/help/${req.id}/download`}
                          target="_blank"
                          rel="noreferrer"
                          className="text-primary-600 hover:text-primary-700 shrink-0"
                        >
                          Download
                        </a>
                      </div>
                      {req.message && <p className="text-gray-600 mt-1">{req.message}</p>}
                      <p className="text-gray-400 mt-1">
                        {req.status} · {new Date(req.created_at).toLocaleString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Deadline extension request (team leader) */}
          {me && isLeader && project.deadline && (
            <div className="mt-6 p-4 bg-amber-50 rounded-lg border border-amber-200">
              <h3 className="font-semibold text-gray-900 mb-2">⏰ Request Deadline Extension</h3>
              <p className="text-xs text-gray-600 mb-3">
                Every project must be completed and uploaded before its deadline
                (scheduled: {project.deadline}
                {project.effective_deadline !== project.deadline &&
                  ` · effective: ${project.effective_deadline}`}
                ). If the team cannot finish in time, request an extension of
                up to 4 weeks - an admin must approve it before work can be
                uploaded after the deadline.
              </p>

              {project.deadline_extensions && project.deadline_extensions.length > 0 && (
                <div className="space-y-2 mb-3">
                  {project.deadline_extensions.map((ext) => (
                    <div key={ext.id} className="bg-white rounded-lg px-3 py-2 border border-amber-200 text-xs flex items-center justify-between">
                      <span className="text-gray-700">
                        +{ext.requested_days} days · {ext.status}
                      </span>
                      <span className="text-gray-400">{new Date(ext.created_at).toLocaleDateString()}</span>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex gap-3 mb-3">
                <select
                  value={extDays}
                  onChange={(e) => setExtDays(Number(e.target.value))}
                  className="input sm:w-36"
                >
                  {[7, 14, 21, 28].map((n) => (
                    <option key={n} value={n}>{n} days ({(n / 7).toFixed(0)} week{(n / 7) > 1 ? 's' : ''})</option>
                  ))}
                </select>
                <input
                  value={extReason}
                  onChange={(e) => setExtReason(e.target.value)}
                  className="input flex-1"
                  placeholder="Why do you need more time? (required)"
                />
              </div>
              <button
                onClick={handleExtensionRequest}
                disabled={requestingExt}
                className="btn-secondary text-sm"
              >
                {requestingExt ? 'Submitting...' : 'Request extension'}
              </button>
            </div>
          )}

          {/* Extra developer request */}
          {me && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-2">Request Extra Developers</h3>
              <p className="text-xs text-gray-500 mb-3">
                If the workload is overwhelming, request up to 3 extra developers (admin approves).
              </p>
              <div className="flex gap-3 mb-3">
                <select
                  value={extraCount}
                  onChange={(e) => setExtraCount(Number(e.target.value))}
                  className="input sm:w-32"
                >
                  {[1, 2, 3].map((n) => (
                    <option key={n} value={n}>{n} developer{n > 1 ? 's' : ''}</option>
                  ))}
                </select>
                <input
                  value={extraReason}
                  onChange={(e) => setExtraReason(e.target.value)}
                  className="input flex-1"
                  placeholder="Reason (optional)"
                />
              </div>
              <button
                onClick={handleRequestExtra}
                disabled={requestingExtra}
                className="btn-secondary text-sm"
              >
                {requestingExtra ? 'Submitting...' : 'Request extra developers'}
              </button>
            </div>
          )}
        </div>

        {/* Chat */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Project Chat</h2>
          <div className="h-96 overflow-y-auto bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
            {messages.length === 0 ? (
              <p className="text-sm text-gray-500 text-center pt-10">
                No messages yet. Ask questions, report bugs, or chat with N.O.U Lite for help.
              </p>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.is_ai ? 'justify-start' : 'justify-end'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 text-sm ${
                      msg.is_ai
                        ? 'bg-primary-50 border border-primary-200 text-gray-800'
                        : 'bg-primary-600 text-white'
                    }`}
                  >
                    <p className={`text-xs mb-1 ${msg.is_ai ? 'text-primary-600' : 'text-primary-200'}`}>
                      {msg.is_ai ? 'N.O.U Lite' : msg.sender}
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
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              className="input flex-1"
              placeholder="Type a message..."
            />
            <button
              onClick={handleSend}
              disabled={sending || !chatInput.trim()}
              className="btn-primary"
            >
              Send
            </button>
          </div>
          <label className="flex items-center gap-2 mt-3 text-sm text-gray-600 cursor-pointer">
            <input
              type="checkbox"
              checked={askAi}
              onChange={(e) => setAskAi(e.target.checked)}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            Ask N.O.U Lite for help with this question
          </label>
        </div>
      </div>
    </div>
  )
}

export default ProjectDetailPage
