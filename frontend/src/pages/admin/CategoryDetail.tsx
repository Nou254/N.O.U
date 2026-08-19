import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface CategoryResult {
  session_id: number
  applicant: {
    id: number
    name: string
    email: string
    phone: string | null
    cv_file_path: string | null
    policies_accepted_at: string | null
  }
  assessment: { id: number; title: string }
  position_name: string | null
  score: number | null
  percentage: number | null
  recommendation: string | null
  summary: string | null
  completed_at: string | null
  competency_band: string | null
  onboarding_status: string | null
}

const AdminCategoryDetail = () => {
  const { categoryId } = useParams<{ categoryId: string }>()
  const [categoryName, setCategoryName] = useState('')
  const [results, setResults] = useState<CategoryResult[]>([])
  const [pagination, setPagination] = useState({ total: 0, page: 1, limit: 20, pages: 0 })
  const [loading, setLoading] = useState(true)
  const [deciding, setDeciding] = useState<number | null>(null)
  const [showPolicies, setShowPolicies] = useState(false)
  const [policyContent, setPolicyContent] = useState('')
  const [policyTitle, setPolicyTitle] = useState('N.O.U. Organization Policies')
  const [policiesLoading, setPoliciesLoading] = useState(false)

  const fetchResults = async (page = 1) => {
    setLoading(true)
    try {
      const response = await api.get(
        `/admin/categories/${categoryId}/results?page=${page}&limit=${pagination.limit}`
      )
      setCategoryName(response.data.category?.name || '')
      setResults(response.data.results || [])
      setPagination(response.data.pagination)
    } catch (error) {
      console.error('Error fetching category results:', error)
      toast.error('Failed to load this category screen')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (categoryId) fetchResults(1)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [categoryId])

  const togglePolicies = async () => {
    if (showPolicies) {
      setShowPolicies(false)
      return
    }
    setPoliciesLoading(true)
    try {
      const response = await api.get('/policies/')
      setPolicyTitle(response.data.title || policyTitle)
      setPolicyContent(response.data.content || '')
      setShowPolicies(true)
    } catch (error) {
      toast.error('Could not load the organization policies')
    } finally {
      setPoliciesLoading(false)
    }
  }

  const handleDecision = async (sessionId: number, approve: boolean) => {
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

  const getPercentageColor = (percentage: number | null) => {
    if (percentage === null) return 'text-gray-500'
    if (percentage >= 70) return 'text-green-600'
    if (percentage >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Link to="/admin/categories" className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            All categories
          </Link>
        </div>
        <h1 className="text-2xl font-bold text-gray-900">{categoryName || 'Category Screen'}</h1>
        <p className="text-gray-600">
          Candidates assessed in this category with their contact details, results and
          approval status.
        </p>
        <button
          onClick={togglePolicies}
          disabled={policiesLoading}
          className="mt-4 btn-secondary text-sm"
        >
          {policiesLoading ? 'Loading...' : showPolicies ? 'Hide Organization Policies' : 'View Organization Policies'}
        </button>
      </div>

      {showPolicies && (
        <div className="card !p-6 mb-8">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-gray-900">{policyTitle}</h2>
            <span className="text-xs text-gray-500">For reference - approved personnel agree to this on first login</span>
          </div>
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-5 text-sm text-gray-700 leading-relaxed max-h-[60vh] overflow-y-auto whitespace-pre-wrap">
            {policyContent || 'No policies available.'}
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12"><div className="spinner mx-auto"></div></div>
      ) : results.length === 0 ? (
        <div className="card text-center py-12">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No assessments in this category yet</h3>
          <p className="text-gray-600">Candidates who complete an assessment in {categoryName || 'this category'} will appear here.</p>
        </div>
      ) : (
        <>
          <div className="card overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="text-left text-xs uppercase tracking-wide text-gray-500 border-b border-gray-200">
                  <th className="px-4 py-3">Candidate (contact)</th>
                  <th className="px-4 py-3">Position</th>
                  <th className="px-4 py-3 text-center">Score</th>
                  <th className="px-4 py-3 text-center">Verdict</th>
                  <th className="px-4 py-3">Completed</th>
                  <th className="px-4 py-3 text-center">Policies</th>
                  <th className="px-4 py-3 text-center">Approval</th>
                </tr>
              </thead>
              <tbody>
                {results.map((result) => (
                  <tr key={result.session_id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <div className="font-medium text-gray-900">{result.applicant.name}</div>
                      <div className="text-sm text-gray-500">{result.applicant.email}</div>
                      {result.applicant.phone && (
                        <div className="text-xs text-gray-400">{result.applicant.phone}</div>
                      )}
                      {result.applicant.cv_file_path && (
                        <span className="text-xs text-primary-600">CV on file</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-700">{result.position_name || '—'}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`font-bold ${getPercentageColor(result.percentage)}`}>
                        {result.percentage !== null ? `${Number(result.percentage).toFixed(1)}%` : '—'}
                      </span>
                      {result.competency_band && (
                        <div className="text-[11px] text-gray-400">{result.competency_band}</div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className={`text-sm font-medium ${
                        result.recommendation === 'PASS' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {result.recommendation || '—'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      {result.completed_at ? new Date(result.completed_at).toLocaleDateString() : '—'}
                    </td>
                    <td className="px-4 py-3 text-center">
                      {result.applicant.policies_accepted_at ? (
                        <span className="badge-success">Accepted</span>
                      ) : result.onboarding_status === 'approved' ? (
                        <span className="badge-warning">Pending</span>
                      ) : (
                        <span className="text-xs text-gray-400">—</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-center">
                      {result.onboarding_status === 'approved' ? (
                        <span className="badge-success">Approved</span>
                      ) : result.onboarding_status === 'declined' ? (
                        <span className="badge-danger">Rejected</span>
                      ) : result.recommendation === 'PASS' ? (
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
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

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

export default AdminCategoryDetail
