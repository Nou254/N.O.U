import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface ProjectMember {
  id: string
  user_id: string
  name: string
  role: string
  is_team_leader: boolean
}

interface ProjectDocument {
  id: string
  filename: string
  doc_type: string
  doc_status?: string
  version?: number
}

interface StaffingItem {
  id?: string
  position: string
  count_required: number
  skills?: string | null
  experience_level?: string | null
  availability?: string | null
  duration?: string | null
}

interface ChangeRequest {
  id: string
  title: string
  description: string
  status: string
  impact_analysis?: string | null
  created_at?: string
}

interface Project {
  id: string
  title: string
  category: string
  status: string
  lifecycle_stage: string
  deadline: string
  member_count: number
  required_people: number
  members: ProjectMember[]
  documents: ProjectDocument[]
  staffing_plan: StaffingItem[]
  change_requests: ChangeRequest[]
}

interface Candidate {
  user_id: string
  name: string
  email: string
  source: string
  position?: string | null
  skills?: string | null
  status: string
  active_projects: number
  assessment?: {
    percentage: number
    competency_band: string
    category: string
    position: string
  } | null
  eoi_id: string
}

const LIFECYCLE_STAGES = [
  'requested',
  'initial_review',
  'clarification',
  'analysis',
  'technical_feasibility',
  'documentation',
  'internal_review',
  'estimation',
  'customer_proposal',
  'customer_approval',
  'staffing',
  'team_formation',
  'planning',
  'development',
  'qa',
  'security_review',
  'staging',
  'customer_acceptance',
  'deployment',
  'support',
  'closed',
]

const STAGE_LABELS: Record<string, string> = {
  requested: 'Requested',
  initial_review: 'Initial Review',
  clarification: 'Clarification',
  analysis: 'Analysis',
  technical_feasibility: 'Technical Feasibility',
  documentation: 'Documentation',
  internal_review: 'Internal Review',
  estimation: 'Estimation',
  customer_proposal: 'Customer Proposal',
  customer_approval: 'Customer Approval',
  staffing: 'Staffing',
  team_formation: 'Team Formation',
  planning: 'Planning',
  development: 'Development',
  qa: 'QA',
  security_review: 'Security Review',
  staging: 'Staging',
  customer_acceptance: 'Customer Acceptance',
  deployment: 'Deployment',
  support: 'Support',
  closed: 'Closed',
}

const DOC_ACTIONS = [
  { value: 'submit_for_review', label: 'Submit for review' },
  { value: 'approve', label: 'Approve' },
  { value: 'request_revision', label: 'Request revision' },
  { value: 'lock', label: 'Lock' },
]

const AdminLifecycle = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState<Project | null>(null)
  const [stageTarget, setStageTarget] = useState('')
  const [stageNotes, setStageNotes] = useState('')
  const [stageBusy, setStageBusy] = useState(false)

  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [candidatesLoading, setCandidatesLoading] = useState(false)
  const [decisionBusy, setDecisionBusy] = useState<string | null>(null)

  const [staffingItems, setStaffingItems] = useState<StaffingItem[]>([
    { position: '', count_required: 1, skills: '', experience_level: 'Intermediate', availability: '', duration: '' },
  ])
  const [staffingBusy, setStaffingBusy] = useState(false)

  const [docAction, setDocAction] = useState<Record<string, string>>({})
  const [docBusy, setDocBusy] = useState<string | null>(null)
  const [leaderBusy, setLeaderBusy] = useState(false)

  const fetchProjects = async () => {
    try {
      const response = await api.get('/admin/projects?limit=100')
      setProjects(response.data.projects || [])
    } catch (error) {
      console.error('Error fetching projects:', error)
      toast.error('Failed to load projects')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProjects()
  }, [])

  const openProject = async (project: Project) => {
    setSelected(project)
    setStageTarget('')
    setStageNotes('')
    setStaffingItems(
      project.staffing_plan?.length
        ? project.staffing_plan.map((it) => ({ ...it }))
        : [{ position: '', count_required: 1, skills: '', experience_level: 'Intermediate', availability: '', duration: '' }]
    )
    setCandidates([])
    if (project.lifecycle_stage && ['staffing', 'team_formation', 'planning'].includes(project.lifecycle_stage)) {
      fetchCandidates(project.id)
    }
  }

  const fetchCandidates = async (projectId: string) => {
    setCandidatesLoading(true)
    try {
      const response = await api.get(`/admin/projects/${projectId}/candidates`)
      setCandidates(response.data.candidates || [])
    } catch (error) {
      console.error('Error fetching candidates:', error)
    } finally {
      setCandidatesLoading(false)
    }
  }

  const handleStageTransition = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selected || !stageTarget) return
    setStageBusy(true)
    try {
      const response = await api.post(`/admin/projects/${selected.id}/stage`, {
        stage: stageTarget,
        notes: stageNotes || undefined,
      })
      toast.success(response.data.message)
      const updated = { ...selected, lifecycle_stage: response.data.lifecycle_stage }
      setSelected(updated)
      setProjects((prev) => prev.map((p) => (p.id === updated.id ? updated : p)))
      if (['staffing', 'team_formation', 'planning'].includes(response.data.lifecycle_stage)) {
        fetchCandidates(selected.id)
      }
      setStageNotes('')
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to move stage')
    } finally {
      setStageBusy(false)
    }
  }

  const handleSaveStaffing = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selected) return
    const valid = staffingItems.filter((it) => it.position.trim())
    if (!valid.length) {
      toast.error('Add at least one staffing position')
      return
    }
    setStaffingBusy(true)
    try {
      const response = await api.post(`/admin/projects/${selected.id}/staffing-plan`, valid)
      toast.success(response.data.message)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to save staffing plan')
    } finally {
      setStaffingBusy(false)
    }
  }

  const handleCandidateDecision = async (candidate: Candidate, decision: string) => {
    if (!selected) return
    setDecisionBusy(candidate.eoi_id)
    try {
      const response = await api.post(`/admin/projects/${selected.id}/candidates/${candidate.eoi_id}/decision`, {
        decision,
        role: candidate.position || undefined,
        notes: undefined,
      })
      toast.success(response.data.message)
      fetchCandidates(selected.id)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to update candidate')
    } finally {
      setDecisionBusy(null)
    }
  }

  const handleDocumentAction = async (doc: ProjectDocument, action: string) => {
    if (!selected) return
    setDocBusy(doc.id)
    try {
      const response = await api.post(`/admin/projects/${selected.id}/documents/${doc.id}/review`, {
        action,
        notes: undefined,
      })
      toast.success(response.data.message)
      const updated = {
        ...selected,
        documents: selected.documents.map((d) => (d.id === doc.id ? { ...d, doc_status: response.data.doc_status } : d)),
      }
      setSelected(updated)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to review document')
    } finally {
      setDocBusy(null)
    }
  }

  const handleAppointLeader = async (member: ProjectMember) => {
    if (!selected) return
    setLeaderBusy(true)
    try {
      const response = await api.post(`/admin/projects/${selected.id}/team-leader`, { member_id: member.id })
      toast.success(response.data.message)
      setSelected({
        ...selected,
        members: selected.members.map((m) => ({ ...m, is_team_leader: m.id === member.id })),
      })
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to appoint leader')
    } finally {
      setLeaderBusy(false)
    }
  }

  const currentIdx = selected ? LIFECYCLE_STAGES.indexOf(selected.lifecycle_stage) : -1

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Project Lifecycle Pipeline</h1>
        <p className="text-gray-600">
          Move projects through the controlled lifecycle, set staffing plans, review candidates,
          appoint team leaders and approve project documents.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12"><div className="spinner mx-auto"></div></div>
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Project list */}
          <div className="lg:col-span-1 space-y-3">
            <h2 className="font-semibold text-gray-900">Projects ({projects.length})</h2>
            {projects.length === 0 ? (
              <div className="card text-center py-8">
                <p className="text-gray-600">No company projects yet.</p>
              </div>
            ) : (
              projects.map((project) => (
                <button
                  key={project.id}
                  onClick={() => openProject(project)}
                  className={`w-full text-left card hover:border-primary-300 transition-colors ${
                    selected?.id === project.id ? 'border-primary-400 ring-1 ring-primary-200' : ''
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="font-semibold text-gray-900 truncate">{project.title}</p>
                      <p className="text-xs text-gray-500 mt-0.5">{project.category}</p>
                    </div>
                    <span className="badge-primary text-xs shrink-0">
                      {STAGE_LABELS[project.lifecycle_stage] || project.lifecycle_stage}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
                    <span>{project.member_count}/{project.required_people || 0} members</span>
                    <span>{project.status}</span>
                  </div>
                </button>
              ))
            )}
          </div>

          {/* Detail panel */}
          <div className="lg:col-span-2 space-y-6">
            {!selected ? (
              <div className="card text-center py-16">
                <p className="text-gray-500">Select a project to manage its lifecycle.</p>
              </div>
            ) : (
              <>
                {/* Header */}
                <div className="card">
                  <div className="flex items-start justify-between flex-wrap gap-3">
                    <div>
                      <h2 className="text-xl font-bold text-gray-900">{selected.title}</h2>
                      <p className="text-sm text-gray-600 mt-1">
                        Category: {selected.category} · Status: {selected.status}
                        {selected.deadline && ` · Deadline: ${new Date(selected.deadline).toLocaleDateString()}`}
                      </p>
                    </div>
                    <span className="badge-primary">
                      {STAGE_LABELS[selected.lifecycle_stage] || selected.lifecycle_stage}
                    </span>
                  </div>

                  {/* Stage stepper */}
                  <div className="mt-6">
                    <div className="flex items-center gap-1 overflow-x-auto pb-2">
                      {LIFECYCLE_STAGES.map((stage, idx) => (
                        <div key={stage} className="flex items-center shrink-0">
                          <div
                            className={`flex items-center gap-1.5 px-2 py-1 rounded-lg text-xs font-medium whitespace-nowrap ${
                              idx === currentIdx
                                ? 'bg-primary-600 text-white'
                                : idx < currentIdx
                                ? 'bg-green-100 text-green-700'
                                : 'bg-gray-100 text-gray-500'
                            }`}
                          >
                            {idx < currentIdx ? '✓' : idx + 1}
                            <span>{STAGE_LABELS[stage]}</span>
                          </div>
                          {idx < LIFECYCLE_STAGES.length - 1 && <div className="w-2 h-px bg-gray-300" />}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Stage transition form */}
                  <form onSubmit={handleStageTransition} className="mt-4 pt-4 border-t border-gray-200 flex gap-3 items-end flex-wrap">
                    <div className="flex-1 min-w-[200px]">
                      <label className="label">Move to stage</label>
                      <select value={stageTarget} onChange={(e) => setStageTarget(e.target.value)} className="input">
                        <option value="">Select stage...</option>
                        {LIFECYCLE_STAGES.filter((s) => LIFECYCLE_STAGES.indexOf(s) > currentIdx).map((s) => (
                          <option key={s} value={s}>{STAGE_LABELS[s]}</option>
                        ))}
                      </select>
                    </div>
                    <div className="flex-1 min-w-[200px]">
                      <label className="label">Notes (optional)</label>
                      <input
                        type="text"
                        value={stageNotes}
                        onChange={(e) => setStageNotes(e.target.value)}
                        className="input"
                        placeholder="e.g. Documents approved by PM"
                      />
                    </div>
                    <button type="submit" disabled={!stageTarget || stageBusy} className="btn-primary">
                      {stageBusy ? 'Moving...' : 'Move stage'}
                    </button>
                  </form>
                </div>

                {/* Staffing plan */}
                <div className="card">
                  <h3 className="font-semibold text-gray-900 mb-3">Staffing Plan</h3>
                  <form onSubmit={handleSaveStaffing} className="space-y-3">
                    {staffingItems.map((item, index) => (
                      <div key={index} className="grid grid-cols-6 gap-2 items-end">
                        <input
                          type="text"
                          placeholder="Position (e.g. Backend Dev)"
                          value={item.position}
                          onChange={(e) => {
                            const next = [...staffingItems]
                            next[index] = { ...item, position: e.target.value }
                            setStaffingItems(next)
                          }}
                          className="input col-span-2"
                        />
                        <input
                          type="number"
                          min={1}
                          max={20}
                          placeholder="Count"
                          value={item.count_required}
                          onChange={(e) => {
                            const next = [...staffingItems]
                            next[index] = { ...item, count_required: parseInt(e.target.value) || 1 }
                            setStaffingItems(next)
                          }}
                          className="input"
                        />
                        <select
                          value={item.experience_level || 'Intermediate'}
                          onChange={(e) => {
                            const next = [...staffingItems]
                            next[index] = { ...item, experience_level: e.target.value }
                            setStaffingItems(next)
                          }}
                          className="input"
                        >
                          <option value="Junior">Junior</option>
                          <option value="Intermediate">Intermediate</option>
                          <option value="Senior">Senior</option>
                          <option value="Specialist">Specialist</option>
                        </select>
                        <input
                          type="text"
                          placeholder="Skills"
                          value={item.skills || ''}
                          onChange={(e) => {
                            const next = [...staffingItems]
                            next[index] = { ...item, skills: e.target.value }
                            setStaffingItems(next)
                          }}
                          className="input"
                        />
                        <div className="flex gap-1">
                          <input
                            type="text"
                            placeholder="Duration"
                            value={item.duration || ''}
                            onChange={(e) => {
                              const next = [...staffingItems]
                              next[index] = { ...item, duration: e.target.value }
                              setStaffingItems(next)
                            }}
                            className="input"
                          />
                          {staffingItems.length > 1 && (
                            <button
                              type="button"
                              onClick={() => setStaffingItems(staffingItems.filter((_, i) => i !== index))}
                              className="btn-outline px-2"
                              title="Remove"
                            >
                              ×
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                    <div className="flex gap-3">
                      <button
                        type="button"
                        onClick={() =>
                          setStaffingItems([...staffingItems, { position: '', count_required: 1, skills: '', experience_level: 'Intermediate', availability: '', duration: '' }])
                        }
                        className="btn-outline text-sm"
                      >
                        + Add position
                      </button>
                      <button type="submit" disabled={staffingBusy} className="btn-primary text-sm">
                        {staffingBusy ? 'Saving...' : 'Save staffing plan'}
                      </button>
                    </div>
                  </form>
                </div>

                {/* Candidates */}
                {['staffing', 'team_formation', 'planning'].includes(selected.lifecycle_stage) && (
                  <div className="card">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-gray-900">Candidates</h3>
                      <button onClick={() => fetchCandidates(selected.id)} className="btn-outline text-sm">
                        Refresh
                      </button>
                    </div>
                    {candidatesLoading ? (
                      <div className="text-center py-8"><div className="spinner mx-auto"></div></div>
                    ) : candidates.length === 0 ? (
                      <p className="text-sm text-gray-500 py-6 text-center">
                        No expressions of interest yet. Eligible personnel will appear here.
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {candidates.map((candidate) => (
                          <div key={candidate.eoi_id} className="border border-gray-200 rounded-lg p-4">
                            <div className="flex items-start justify-between gap-3 flex-wrap">
                              <div className="min-w-0">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <p className="font-medium text-gray-900">{candidate.name}</p>
                                  {candidate.assessment && (
                                    <span className="badge-primary text-xs">
                                      {candidate.assessment.percentage}% · {candidate.assessment.competency_band}
                                    </span>
                                  )}
                                  <span className="badge-gray text-xs">
                                    {candidate.active_projects}/3 projects
                                  </span>
                                </div>
                                <p className="text-xs text-gray-500 mt-0.5">{candidate.email}</p>
                                {(candidate.position || candidate.skills) && (
                                  <p className="text-xs text-gray-600 mt-1">
                                    {candidate.position && <span className="font-medium">Position: {candidate.position}</span>}
                                    {candidate.position && candidate.skills && ' · '}
                                    {candidate.skills && <span>Skills: {candidate.skills}</span>}
                                  </p>
                                )}
                                {candidate.assessment && (
                                  <p className="text-xs text-gray-500 mt-1">
                                    Assessed: {candidate.assessment.category}
                                    {candidate.assessment.position ? ` — ${candidate.assessment.position}` : ''}
                                  </p>
                                )}
                              </div>
                              <div className="flex gap-2 shrink-0">
                                <button
                                  onClick={() => handleCandidateDecision(candidate, 'selected')}
                                  disabled={decisionBusy === candidate.eoi_id || candidate.status === 'selected'}
                                  className="btn-primary text-xs"
                                >
                                  {candidate.status === 'selected' ? 'Selected' : 'Select'}
                                </button>
                                <button
                                  onClick={() => handleCandidateDecision(candidate, 'declined')}
                                  disabled={decisionBusy === candidate.eoi_id || candidate.status === 'declined'}
                                  className="btn-outline text-xs"
                                >
                                  {candidate.status === 'declined' ? 'Declined' : 'Decline'}
                                </button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Team members + leader */}
                {selected.members?.length > 0 && (
                  <div className="card">
                    <h3 className="font-semibold text-gray-900 mb-3">Team ({selected.member_count})</h3>
                    <div className="space-y-2">
                      {selected.members.map((member) => (
                        <div key={member.id} className="flex items-center justify-between border border-gray-200 rounded-lg p-3">
                          <div className="flex items-center gap-2">
                            <p className="font-medium text-gray-800 text-sm">{member.name}</p>
                            <span className="badge-gray text-xs">{member.role || 'member'}</span>
                            {member.is_team_leader && <span className="badge-success text-xs">Team Leader</span>}
                          </div>
                          {!member.is_team_leader && (
                            <button
                              onClick={() => handleAppointLeader(member)}
                              disabled={leaderBusy}
                              className="btn-outline text-xs"
                            >
                              Appoint leader
                            </button>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Documents */}
                {selected.documents?.length > 0 && (
                  <div className="card">
                    <h3 className="font-semibold text-gray-900 mb-3">Project Documents</h3>
                    <div className="space-y-2">
                      {selected.documents.map((doc) => (
                        <div key={doc.id} className="flex items-center justify-between gap-3 border border-gray-200 rounded-lg p-3 flex-wrap">
                          <div className="min-w-0">
                            <p className="font-medium text-gray-800 text-sm truncate">{doc.filename}</p>
                            <div className="flex items-center gap-2 mt-0.5">
                              <span className="badge-gray text-xs">{doc.doc_type}</span>
                              <span className={`text-xs ${doc.doc_status === 'approved' ? 'text-green-600' : 'text-gray-500'}`}>
                                {doc.doc_status || 'draft'}{doc.version ? ` · v${doc.version}` : ''}
                              </span>
                            </div>
                          </div>
                          <div className="flex gap-2 shrink-0">
                            <select
                              value={docAction[doc.id] || ''}
                              onChange={(e) => setDocAction((prev) => ({ ...prev, [doc.id]: e.target.value }))}
                              className="input text-sm py-1.5"
                            >
                              <option value="">Action...</option>
                              {DOC_ACTIONS.map((a) => (
                                <option key={a.value} value={a.value}>{a.label}</option>
                              ))}
                            </select>
                            <button
                              onClick={() => handleDocumentAction(doc, docAction[doc.id])}
                              disabled={!docAction[doc.id] || docBusy === doc.id}
                              className="btn-primary text-xs"
                            >
                              {docBusy === doc.id ? '...' : 'Apply'}
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Change requests */}
                {selected.change_requests?.length > 0 && (
                  <div className="card">
                    <h3 className="font-semibold text-gray-900 mb-3">Change Requests</h3>
                    <div className="space-y-2">
                      {selected.change_requests.map((cr) => (
                        <div key={cr.id} className="border border-gray-200 rounded-lg p-3">
                          <div className="flex items-center justify-between gap-2">
                            <p className="font-medium text-gray-800 text-sm">{cr.title}</p>
                            <span className={`badge text-xs ${cr.status === 'pending' ? 'badge-gray' : cr.status === 'approved' ? 'badge-success' : 'badge-red'}`}>
                              {cr.status}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">{cr.description}</p>
                          {cr.impact_analysis && (
                            <p className="text-xs text-gray-500 mt-1">Impact: {cr.impact_analysis}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminLifecycle
