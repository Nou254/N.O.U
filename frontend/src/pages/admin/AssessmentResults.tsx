import { Fragment, useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface AssessmentResult {
  session_id: string
  applicant: {
    id: number
    name: string
    email: string
    phone?: string | null
    cv_file_path?: string | null
    cv_reviewed?: boolean
  }
  assessment: { id: string; title: string }
  score: number | null
  percentage: number | null
  recommendation: string | null
  summary: string | null
  completed_at: string | null
  onboarding_status?: string | null
  onboarding_decided_at?: string | null
}

interface FeedbackItem {
  question: string
  category: string
  points: number
  user_answer?: string | null
  score: number
  max_score: number
  feedback?: string | null
}

interface CvReview {
  summary?: string
  highlights?: string[]
  strengths?: string[]
  concerns?: string[]
}

interface ResultDetail {
  session: {
    id: string
    score: number | null
    percentage: number | null
    status: string
    completed_at: string | null
    ai_summary: string | null
    ai_recommendation: string | null
  }
  applicant: {
    id: number
    name: string
    email: string
    phone?: string | null
    cv_file_path?: string | null
    cv_summary?: CvReview | null
  }
  assessment: { id: string; title: string }
  feedback: FeedbackItem[]
}

const AdminAssessmentResults = () => {
  const [results, setResults] = useState<AssessmentResult[]>([])
  const [pagination, setPagination] = useState({ total: 0, page: 1, limit: 20, pages: 0 })
  const [loading, setLoading] = useState(true)
  const [details, setDetails] = useState<Record<string, ResultDetail>>({})
  const [loadingDetail, setLoadingDetail] = useState<string | null>(null)
  const [deciding, setDeciding] = useState<string | null>(null)
  const [reviewingCv, setReviewingCv] = useState<number | null>(null)
  const [cvTexts, setCvTexts] = useState<Record<string, string>>({})
  const [showCvText, setShowCvText] = useState<Record<string, boolean>>({})

  const fetchResults = async (page = 1) => {
    setLoading(true)
    try {
      const response = await api.get(
        `/admin/assessment-results?page=${page}&limit=${pagination.limit}`
      )
      setResults(response.data.results || [])
      setPagination(response.data.pagination)
    } catch (error) {
      console.error('Error fetching assessment results:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchResults(1)
  }, [])

  const toggleDetail = async (sessionId: string) => {
    if (details[sessionId]) {
      setDetails((prev) => {
        const next = { ...prev }
        delete next[sessionId]
        return next
      })
      return
    }
    setLoadingDetail(sessionId)
    try {
      const response = await api.get(`/admin/assessment-results/${sessionId}`)
      setDetails((prev) => ({ ...prev, [sessionId]: response.data }))
    } catch (error) {
      console.error('Error fetching assessment detail:', error)
    } finally {
      setLoadingDetail(null)
    }
  }

  const getRecommendationColor = (recommendation: string | null) => {
    const r = (recommendation || '').toLowerCase()
    if (r.includes('strong hire')) return 'text-green-600'
    if (r.includes('hire')) return 'text-blue-600'
    if (r.includes('lean')) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getPercentageColor = (percentage: number | null) => {
    if (percentage === null) return 'text-gray-500'
    if (percentage >= 70) return 'text-green-600'
    if (percentage >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  const handleDecision = async (sessionId: string, approve: boolean) => {
    setDeciding(sessionId)
    try {
      const response = await api.post(`/admin/onboarding/${sessionId}/decision`, {
        approve,
        notes: approve ? undefined : 'Not selected during admin verification',
      })
      window.alert(response.data.message)
      fetchResults(pagination.page)
    } catch (error: any) {
      window.alert(error?.response?.data?.detail || 'Failed to process decision')
    } finally {
      setDeciding(null)
    }
  }

  // ---- CV actions -------------------------------------------------------
  const downloadCv = async (userId: number, cvPath?: string | null) => {
    try {
      const response = await api.get(`/admin/cv/${userId}/download`, {
        responseType: 'blob',
      })
      const ext = (cvPath?.split('.').pop() || 'pdf').toLowerCase()
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.download = `cv_${userId}.${ext}`
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error: any) {
      toast.error(error?.response?.data?.message || 'Could not download the CV')
    }
  }

  const toggleCvText = async (userId: number) => {
    if (showCvText[userId]) {
      setShowCvText((prev) => ({ ...prev, [userId]: false }))
      return
    }
    if (!cvTexts[userId]) {
      try {
        const response = await api.get(`/admin/cv/${userId}/text`)
        setCvTexts((prev) => ({ ...prev, [userId]: response.data.text || '' }))
      } catch (error: any) {
        toast.error(error?.response?.data?.message || 'Could not read the CV text')
        return
      }
    }
    setShowCvText((prev) => ({ ...prev, [userId]: true }))
  }

  const reviewCv = async (userId: number, sessionId: string) => {
    setReviewingCv(userId)
    try {
      // Groq review takes ~15-40 seconds.
      const response = await api.post(
        `/admin/cv/${userId}/review`,
        {},
        { timeout: 15 * 60 * 1000 }
      )
      setDetails((prev) => {
        const detail = prev[sessionId]
        if (!detail) return prev
        return {
          ...prev,
          [sessionId]: {
            ...detail,
            applicant: { ...detail.applicant, cv_summary: response.data.review },
          },
        }
      })
      toast.success('CV reviewed by AI - summary ready')
    } catch (error: any) {
      toast.error(error?.response?.data?.message || 'Failed to review the CV')
    } finally {
      setReviewingCv(null)
    }
  }

  const renderCvReview = (cv: CvReview | null | undefined) => {
    if (!cv || !cv.summary) return null
    return (
      <div className="mt-3 bg-primary-50 border border-primary-200 rounded-lg p-3">
        <p className="text-xs font-medium text-primary-700 uppercase mb-1">
          AI CV Review (Groq)
        </p>
        <p className="text-sm text-gray-800">{cv.summary}</p>
        {(cv.highlights?.length || 0) > 0 && (
          <div className="mt-2">
            <p className="text-xs font-medium text-gray-500 uppercase mb-1">Highlights</p>
            <ul className="text-sm text-gray-700 list-disc list-inside space-y-0.5">
              {cv.highlights!.map((h, i) => (
                <li key={i}>{h}</li>
              ))}
            </ul>
          </div>
        )}
        {(cv.strengths?.length || 0) > 0 && (
          <div className="mt-2">
            <p className="text-xs font-medium text-gray-500 uppercase mb-1">Strengths</p>
            <ul className="text-sm text-green-700 list-disc list-inside space-y-0.5">
              {cv.strengths!.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        )}
        {(cv.concerns?.length || 0) > 0 && (
          <div className="mt-2">
            <p className="text-xs font-medium text-gray-500 uppercase mb-1">Concerns</p>
            <ul className="text-sm text-amber-700 list-disc list-inside space-y-0.5">
              {cv.concerns!.map((c, i) => (
                <li key={i}>{c}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Assessment Results</h1>
          <p className="text-gray-600">
            Review Groq-graded candidate assessments, AI summaries, CVs and hiring
            recommendations. Results are final only after your approval.
          </p>
        </div>
        <span className="badge-success">AI Powered</span>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
        </div>
      ) : results.length === 0 ? (
        <div className="card text-center py-12">
          <svg
            className="w-16 h-16 text-gray-400 mx-auto mb-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
            />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No assessment results yet</h3>
          <p className="text-gray-600">Completed AI-graded assessments will appear here.</p>
        </div>
      ) : (
        <>
          <div className="card overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="text-left text-xs uppercase tracking-wide text-gray-500 border-b border-gray-200">
                  <th className="px-4 py-3">Candidate</th>
                  <th className="px-4 py-3">Assessment</th>
                  <th className="px-4 py-3 text-center">Score</th>
                  <th className="px-4 py-3 text-center">AI Verdict</th>
                  <th className="px-4 py-3">Completed</th>
                  <th className="px-4 py-3 text-center">Selection</th>
                  <th className="px-4 py-3 text-right">Details</th>
                </tr>
              </thead>
              <tbody>
                {results.map((result) => (
                  <Fragment key={result.session_id}>
                    <tr className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <div className="font-medium text-gray-900">{result.applicant?.name}</div>
                        <div className="text-sm text-gray-500">{result.applicant?.email}</div>
                        {result.applicant?.phone && (
                          <div className="text-xs text-gray-400">{result.applicant.phone}</div>
                        )}
                        {result.applicant?.cv_file_path && (
                          <span className="text-xs text-primary-600">
                            {result.applicant.cv_reviewed ? 'CV reviewed ✓' : 'CV on file'}
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-700">
                        {result.assessment?.title}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={`font-bold ${getPercentageColor(result.percentage)}`}>
                          {result.percentage !== null ? `${Number(result.percentage).toFixed(1)}%` : '—'}
                        </span>
                        <div className="text-xs text-gray-500">
                          {result.score !== null ? `${result.score} pts` : ''}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={`text-sm font-medium ${getRecommendationColor(result.recommendation)}`}>
                          {result.recommendation || '—'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {result.completed_at
                          ? new Date(result.completed_at).toLocaleDateString()
                          : '—'}
                      </td>
                      <td className="px-4 py-3 text-center">
                        {result.onboarding_status === 'approved' ? (
                          <span className="badge-success">Approved</span>
                        ) : result.onboarding_status === 'declined' ? (
                          <span className="badge-danger">Rejected</span>
                        ) : result.onboarding_status === 'pending' ? (
                          <span className="inline-flex flex-col gap-1 items-center">
                            <div className="flex gap-1">
                              <button
                                onClick={() => handleDecision(result.session_id, true)}
                                disabled={deciding === result.session_id}
                                className="btn-primary text-xs !py-1"
                              >
                                {deciding === result.session_id ? '...' : 'Approve'}
                              </button>
                              <button
                                onClick={() => handleDecision(result.session_id, false)}
                                disabled={deciding === result.session_id}
                                className="btn-outline text-xs !py-1"
                              >
                                Reject
                              </button>
                            </div>
                            <span className="text-[10px] text-amber-600">Awaiting your selection</span>
                          </span>
                        ) : (
                          <span className="text-xs text-gray-400">—</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={() => toggleDetail(result.session_id)}
                          disabled={loadingDetail === result.session_id}
                          className="btn-secondary text-xs"
                        >
                          {loadingDetail === result.session_id
                            ? 'Loading...'
                            : details[result.session_id]
                            ? 'Hide'
                            : 'View'}
                        </button>
                      </td>
                    </tr>

                    {details[result.session_id] && (
                      <tr className="bg-gray-50">
                        <td colSpan={7} className="px-6 py-5">
                          {/* CV panel - view contents + activate Groq review */}
                          {details[result.session_id].applicant?.cv_file_path && (
                            <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
                              <div className="flex items-center justify-between flex-wrap gap-3">
                                <div>
                                  <p className="text-xs font-medium text-gray-500 uppercase mb-1">
                                    Candidate CV
                                  </p>
                                  <p className="text-sm text-gray-700">
                                    {details[result.session_id].applicant?.name} ·{' '}
                                    {details[result.session_id].applicant?.email}
                                    {details[result.session_id].applicant?.phone
                                      ? ` · ${details[result.session_id].applicant.phone}`
                                      : ''}
                                  </p>
                                </div>
                                <div className="flex gap-2">
                                  <button
                                    onClick={() => toggleCvText(details[result.session_id].applicant.id)}
                                    className="btn-secondary text-xs"
                                  >
                                    {showCvText[details[result.session_id].applicant.id]
                                      ? 'Hide Text'
                                      : 'Read Text'}
                                  </button>
                                  <button
                                    onClick={() =>
                                      downloadCv(
                                        details[result.session_id].applicant.id,
                                        details[result.session_id].applicant.cv_file_path
                                      )
                                    }
                                    className="btn-secondary text-xs"
                                  >
                                    Download
                                  </button>
                                  <button
                                    onClick={() =>
                                      reviewCv(
                                        details[result.session_id].applicant.id,
                                        result.session_id
                                      )
                                    }
                                    disabled={reviewingCv === details[result.session_id].applicant.id}
                                    className="btn-primary text-xs disabled:opacity-50"
                                  >
                                    {reviewingCv === details[result.session_id].applicant.id ? (
                                      <span className="inline-flex items-center gap-1.5">
                                        <span className="spinner inline-block w-3 h-3 border-2"></span>
                                        AI Reviewing…
                                      </span>
                                    ) : details[result.session_id].applicant.cv_summary?.summary ? (
                                      'Re-review'
                                    ) : (
                                      'Review with AI'
                                    )}
                                  </button>
                                </div>
                              </div>

                              {showCvText[details[result.session_id].applicant.id] &&
                                cvTexts[details[result.session_id].applicant.id] && (
                                  <pre className="mt-3 text-xs text-gray-700 bg-gray-50 border border-gray-200 rounded p-3 whitespace-pre-wrap max-h-64 overflow-y-auto">
                                    {cvTexts[details[result.session_id].applicant.id]}
                                  </pre>
                                )}

                              {renderCvReview(details[result.session_id].applicant.cv_summary)}
                            </div>
                          )}

                          <div className="grid md:grid-cols-2 gap-4 mb-4">
                            <div className="bg-white border border-gray-200 rounded-lg p-4">
                              <p className="text-xs font-medium text-gray-500 uppercase mb-1">
                                AI Summary
                              </p>
                              <p className="text-sm text-gray-700">
                                {details[result.session_id].session?.ai_summary || 'No summary available.'}
                              </p>
                            </div>
                            <div className="bg-white border border-gray-200 rounded-lg p-4">
                              <p className="text-xs font-medium text-gray-500 uppercase mb-1">
                                Recommendation
                              </p>
                              <p className={`text-sm font-semibold ${getRecommendationColor(
                                details[result.session_id].session?.ai_recommendation
                              )}`}>
                                {details[result.session_id].session?.ai_recommendation || '—'}
                              </p>
                            </div>
                          </div>

                          <p className="text-xs font-medium text-gray-500 uppercase mb-2">
                            Per-question AI feedback ({details[result.session_id].feedback?.length || 0})
                          </p>
                          <div className="space-y-3">
                            {(details[result.session_id].feedback || []).map((item, index) => (
                              <div key={index} className="bg-white border border-gray-200 rounded-lg p-4">
                                <div className="flex items-start justify-between mb-2">
                                  <div>
                                    <span className="badge-primary text-xs">{item.category}</span>
                                    <p className="font-medium text-gray-900 mt-2">{item.question}</p>
                                  </div>
                                  <div className="text-right shrink-0 ml-4">
                                    <span className="text-xl font-bold text-gray-900">{item.score}</span>
                                    <span className="text-sm text-gray-500"> / {item.max_score}</span>
                                  </div>
                                </div>
                                {item.user_answer && (
                                  <div className="mb-2">
                                    <p className="text-xs font-medium text-gray-500 uppercase mb-1">
                                      Candidate answer
                                    </p>
                                    <p className="text-sm text-gray-700 bg-gray-50 rounded p-2 whitespace-pre-wrap max-h-32 overflow-y-auto">
                                      {item.user_answer}
                                    </p>
                                  </div>
                                )}
                                {item.feedback && (
                                  <div>
                                    <p className="text-xs font-medium text-gray-500 uppercase mb-1">
                                      AI Feedback
                                    </p>
                                    <p className="text-sm text-gray-700">{item.feedback}</p>
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </td>
                      </tr>
                    )}
                  </Fragment>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {pagination.pages > 1 && (
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-gray-500">
                Page {pagination.page} of {pagination.pages} ({pagination.total} results)
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => fetchResults(pagination.page - 1)}
                  disabled={pagination.page <= 1}
                  className="btn-secondary text-sm"
                >
                  Previous
                </button>
                <button
                  onClick={() => fetchResults(pagination.page + 1)}
                  disabled={pagination.page >= pagination.pages}
                  className="btn-secondary text-sm"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default AdminAssessmentResults
