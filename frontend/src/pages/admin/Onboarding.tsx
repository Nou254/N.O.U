import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Candidate {
  session_id: number
  applicant: {
    id: number
    name: string
    email: string
    role: string
  }
  assessment: {
    id: number
    title: string
  }
  percentage: number
  score: number
  completed_at: string | null
  ai_summary: string | null
}

const AdminOnboarding = () => {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [loading, setLoading] = useState(true)
  const [decidingId, setDecidingId] = useState<number | null>(null)
  const [showApprove, setShowApprove] = useState<Candidate | null>(null)
  const [notes, setNotes] = useState('')

  const fetchCandidates = async () => {
    try {
      setLoading(true)
      const response = await api.get('/admin/onboarding/candidates')
      setCandidates(response.data.candidates)
    } catch (error) {
      console.error('Error fetching candidates:', error)
      toast.error('Failed to load onboarding candidates')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCandidates()
  }, [])

  const handleDecision = async (candidate: Candidate, approve: boolean) => {
    setDecidingId(candidate.session_id)
    try {
      const response = await api.post(`/admin/onboarding/${candidate.session_id}/decision`, {
        approve,
        notes: notes || undefined,
      })
      toast.success(response.data.message)
      if (approve && response.data.developer) {
        toast(`Developer login created: ${response.data.developer.email}`, )
      }
      setShowApprove(null)
      setNotes('')
      fetchCandidates()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to process decision')
    } finally {
      setDecidingId(null)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Developer Onboarding</h1>
        <p className="text-gray-600">
          Applicants who passed the assessment threshold. Approving them promotes the
          applicant to developer and emails their results + new login credentials.
        </p>
      </div>

      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : candidates.length === 0 ? (
          <div className="text-center py-12">
            <svg
              className="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-600">No candidates awaiting approval</p>
            <p className="text-sm text-gray-500 mt-1">
              Passed applicants will appear here after completing an assessment.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {candidates.map((candidate) => (
              <div
                key={candidate.session_id}
                className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-2 flex-wrap">
                      <h3 className="font-semibold text-gray-900">{candidate.applicant.name}</h3>
                      <span className="badge-success">PASS</span>
                      <span className="text-sm text-gray-500">{candidate.percentage}%</span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{candidate.applicant.email}</p>
                    <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                      <span>Assessment: {candidate.assessment.title}</span>
                      <span>Score: {candidate.score}</span>
                      {candidate.completed_at && (
                        <span>Completed: {new Date(candidate.completed_at).toLocaleString()}</span>
                      )}
                    </div>
                    {candidate.ai_summary && (
                      <p className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3">
                        {candidate.ai_summary}
                      </p>
                    )}
                  </div>
                  <div className="flex flex-col items-end gap-2 shrink-0">
                    <button
                      onClick={() => {
                        setShowApprove(candidate)
                        setNotes('')
                      }}
                      disabled={decidingId === candidate.session_id}
                      className="btn-primary text-sm"
                    >
                      Approve & promote
                    </button>
                    <button
                      onClick={() => handleDecision(candidate, false)}
                      disabled={decidingId === candidate.session_id}
                      className="btn-outline text-sm"
                    >
                      Decline
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Approve modal */}
      {showApprove && (
        <div className="modal-overlay" onClick={() => setShowApprove(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Approve {showApprove.applicant.name}?
            </h2>
            <p className="text-sm text-gray-600 mb-4">
              This will promote them to <strong>developer</strong>, generate new login
              credentials, and email them their results + credentials (opening the
              company projects portal).
            </p>
            <label htmlFor="approval-notes" className="label">Admin notes (optional)</label>
            <textarea
              id="approval-notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              className="input mb-4"
              placeholder="e.g. Great performance in the network engineering section"
            />
            <div className="flex justify-end gap-3">
              <button onClick={() => setShowApprove(null)} className="btn-outline">
                Cancel
              </button>
              <button
                onClick={() => handleDecision(showApprove, true)}
                disabled={decidingId === showApprove.session_id}
                className="btn-primary"
              >
                {decidingId === showApprove.session_id ? 'Approving...' : 'Confirm approval'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminOnboarding
