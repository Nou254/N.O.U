import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface OpportunityPosition {
  position: string
  count_required: number
  skills?: string | null
  experience_level?: string | null
  duration?: string | null
}

interface Opportunity {
  project_id: string
  title: string
  category: string
  description: string
  positions: OpportunityPosition[]
  estimated_duration?: string | null
  deadline?: string | null
  stage: string
  already_interested: boolean
}

interface MyInterest {
  project_id: string
  title?: string
  position?: string | null
  status: string
  created_at?: string
}

const DeveloperOpportunities = () => {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [myInterests, setMyInterests] = useState<MyInterest[]>([])
  const [loading, setLoading] = useState(true)
  const [reason, setReason] = useState<string | null>(null)
  const [interestForms, setInterestForms] = useState<Record<string, { position: string; skills: string }>>({})
  const [submitting, setSubmitting] = useState<string | null>(null)

  useEffect(() => {
    fetchAll()
  }, [])

  const fetchAll = async () => {
    try {
      const [oppRes, intRes] = await Promise.all([
        api.get('/portal/opportunities'),
        api.get('/portal/my-interests'),
      ])
      setOpportunities(oppRes.data.opportunities || [])
      setReason(oppRes.data.reason || null)
      setMyInterests(intRes.data.interests || [])
    } catch (error) {
      console.error('Error fetching opportunities:', error)
      toast.error('Failed to load opportunities')
    } finally {
      setLoading(false)
    }
  }

  const expressInterest = async (projectId: string) => {
    const form = interestForms[projectId] || { position: '', skills: '' }
    if (!form.position.trim()) {
      toast.error('Select the position you are applying for')
      return
    }
    setSubmitting(projectId)
    try {
      await api.post(`/portal/projects/${projectId}/express-interest`, {
        position: form.position,
        skills: form.skills || undefined,
      })
      toast.success('Interest expressed. Admin will review your application.')
      fetchAll()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to express interest')
    } finally {
      setSubmitting(null)
    }
  }

  const withdrawInterest = async (projectId: string) => {
    setSubmitting(projectId)
    try {
      await api.delete(`/portal/projects/${projectId}/express-interest`)
      toast.success('Interest withdrawn')
      fetchAll()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to withdraw')
    } finally {
      setSubmitting(null)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-16">
        <div className="spinner mx-auto"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Project Opportunities</h1>
        <p className="text-gray-600">
          Projects currently staffing. Express interest to be considered — the admin selects the
          final team. You may work on up to 3 projects at a time.
        </p>
      </div>

      {reason && (
        <div className="card border border-yellow-200 bg-yellow-50 mb-6">
          <p className="text-sm text-yellow-800">{reason}</p>
        </div>
      )}

      {/* My interests */}
      {myInterests.length > 0 && (
        <div className="card mb-6">
          <h2 className="font-semibold text-gray-900 mb-3">My applications</h2>
          <div className="space-y-2">
            {myInterests.map((interest) => (
              <div key={interest.project_id} className="flex items-center justify-between border border-gray-200 rounded-lg p-3">
                <div>
                  <p className="font-medium text-gray-800 text-sm">
                    {interest.title || `Project #${interest.project_id}`}
                    {interest.position && <span className="text-gray-500"> — {interest.position}</span>}
                  </p>
                  <span className={`badge text-xs mt-1 ${interest.status === 'pending' ? 'badge-gray' : interest.status === 'selected' ? 'badge-success' : 'badge-red'}`}>
                    {interest.status}
                  </span>
                </div>
                {interest.status === 'pending' && (
                  <button
                    onClick={() => withdrawInterest(interest.project_id)}
                    disabled={submitting === interest.project_id}
                    className="btn-outline text-xs"
                  >
                    Withdraw
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {opportunities.length === 0 && !reason ? (
        <div className="card text-center py-16">
          <p className="text-gray-600">No projects are staffing right now. Check back soon.</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          {opportunities.map((opp) => (
            <div key={opp.project_id} className="card">
              <div className="flex items-start justify-between mb-2">
                <h3 className="text-lg font-semibold text-gray-900">{opp.title}</h3>
                <span className="badge-primary text-xs">{opp.stage}</span>
              </div>
              <p className="text-xs text-gray-500 mb-1">{opp.category}</p>
              {opp.description && (
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">{opp.description}</p>
              )}

              <div className="space-y-2 mb-4">
                {opp.positions.map((pos, idx) => (
                  <div key={idx} className="border border-gray-200 rounded-lg p-3">
                    <div className="flex items-center justify-between">
                      <p className="font-medium text-gray-800 text-sm">{pos.position}</p>
                      <span className="badge-gray text-xs">
                        {pos.count_required} needed · {pos.experience_level || 'Any'}
                      </span>
                    </div>
                    {pos.skills && <p className="text-xs text-gray-500 mt-1">Skills: {pos.skills}</p>}
                    {pos.duration && <p className="text-xs text-gray-500">Duration: {pos.duration}</p>}
                  </div>
                ))}
              </div>

              {opp.estimated_duration && (
                <p className="text-xs text-gray-500 mb-2">Estimated duration: {opp.estimated_duration}</p>
              )}
              {opp.deadline && (
                <p className="text-xs text-gray-500 mb-2">Deadline: {new Date(opp.deadline).toLocaleDateString()}</p>
              )}

              {opp.already_interested ? (
                <div className="flex items-center justify-between">
                  <span className="badge-success text-xs">Interest expressed</span>
                  <button
                    onClick={() => withdrawInterest(opp.project_id)}
                    disabled={submitting === opp.project_id}
                    className="btn-outline text-xs"
                  >
                    Withdraw
                  </button>
                </div>
              ) : (
                <div className="space-y-2">
                  <select
                    value={interestForms[opp.project_id]?.position || ''}
                    onChange={(e) =>
                      setInterestForms((prev) => ({
                        ...prev,
                        [opp.project_id]: { ...(prev[opp.project_id] || { skills: '' }), position: e.target.value },
                      }))
                    }
                    className="input text-sm"
                  >
                    <option value="">Select position...</option>
                    {opp.positions.map((pos, idx) => (
                      <option key={idx} value={pos.position}>{pos.position}</option>
                    ))}
                  </select>
                  <input
                    type="text"
                    placeholder="Your relevant skills (optional)"
                    value={interestForms[opp.project_id]?.skills || ''}
                    onChange={(e) =>
                      setInterestForms((prev) => ({
                        ...prev,
                        [opp.project_id]: { ...(prev[opp.project_id] || { position: '' }), skills: e.target.value },
                      }))
                    }
                    className="input text-sm"
                  />
                  <button
                    onClick={() => expressInterest(opp.project_id)}
                    disabled={submitting === opp.project_id}
                    className="btn-primary w-full text-sm"
                  >
                    {submitting === opp.project_id ? 'Applying...' : 'Express interest'}
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default DeveloperOpportunities
