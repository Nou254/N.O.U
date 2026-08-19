import { useEffect, useMemo, useState } from 'react'
import api from '../../services/api'
import MathText from '../../components/MathText'

interface AssessmentResult {
  id: string
  assessment: {
    title: string
  }
  score: number
  percentage: number
  status: string
  completedAt: string
  aiSummary?: string | null
  aiRecommendation?: string | null
  passed?: boolean | null
  modules?: string[]
  categoryName?: string | null
  positionName?: string | null
  partScores?: Record<string, number>
  competencyBand?: string | null
  recommendedCategory?: string | null
}

interface FeedbackItem {
  question: string
  module: string
  category: string
  part?: string
  question_type?: string
  points: number
  user_answer?: string | null
  score: number
  max_score: number
  feedback?: string | null
}

interface SessionDetail {
  session: {
    ai_summary?: string | null
    ai_recommendation?: string | null
  }
  feedback: FeedbackItem[]
  partScores?: Record<string, number>
  competencyBand?: string | null
  recommendedCategory?: string | null
  categoryName?: string | null
  positionName?: string | null
}

// Framework qualifying threshold (today.md: 80%+ qualifies for consideration).
const PASS_THRESHOLD_PERCENT = 80

// Display order + labels for the five assessment parts.
const PART_META: Record<string, { label: string; weight: number }> = {
  logic: { label: 'Logic & Reasoning', weight: 15 },
  general: { label: 'General Knowledge', weight: 5 },
  category: { label: 'Category Knowledge', weight: 25 },
  position: { label: 'Position Knowledge', weight: 25 },
  practical: { label: 'Practical & Applied', weight: 25 },
  professional: { label: 'Professional Ethics', weight: 5 },
}

// Competency bands (mirrored from backend assessment_framework.py).
const COMPETENCY_BANDS = [
  { min: 90, label: 'Advanced', color: 'text-green-700', chip: 'bg-green-100 text-green-800' },
  { min: 80, label: 'N.O.U. Qualified', color: 'text-emerald-600', chip: 'bg-emerald-100 text-emerald-800' },
  { min: 65, label: 'Competent', color: 'text-primary-700', chip: 'bg-primary-100 text-primary-800' },
  { min: 50, label: 'Developing', color: 'text-yellow-600', chip: 'bg-yellow-100 text-yellow-800' },
  { min: 0, label: 'Not Qualified', color: 'text-red-600', chip: 'bg-red-100 text-red-800' },
]

interface ModuleBreakdown {
  module: string
  score: number
  max: number
  percentage: number
}

const ApplicantResults = () => {
  const [results, setResults] = useState<AssessmentResult[]>([])
  const [loading, setLoading] = useState(true)
  const [feedbackMap, setFeedbackMap] = useState<Record<string, SessionDetail>>({})
  const [loadingFeedback, setLoadingFeedback] = useState<string | null>(null)

  useEffect(() => {
    fetchResults()
  }, [])

  const fetchResults = async () => {
    try {
      const response = await api.get('/assessments/results/me')
      setResults(response.data.results || [])
    } catch (error) {
      console.error('Error fetching results:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleFeedback = async (sessionId: string) => {
    if (feedbackMap[sessionId]) {
      setFeedbackMap((prev) => {
        const next = { ...prev }
        delete next[sessionId]
        return next
      })
      return
    }
    setLoadingFeedback(sessionId)
    try {
      const response = await api.get(`/assessments/sessions/${sessionId}/results`)
      setFeedbackMap((prev) => ({ ...prev, [sessionId]: response.data }))
    } catch (error) {
      console.error('Error fetching AI feedback:', error)
    } finally {
      setLoadingFeedback(null)
    }
  }

  const moduleBreakdown = (detail: SessionDetail): ModuleBreakdown[] => {
    const totals: Record<string, { score: number; max: number }> = {}
    for (const item of detail.feedback || []) {
      const mod = item.part || item.module || item.category || 'General'
      const entry = totals[mod] || { score: 0, max: 0 }
      entry.score += item.score || 0
      entry.max += item.max_score || item.points || 0
      totals[mod] = entry
    }
    return Object.entries(totals)
      .map(([module, t]) => ({
        module,
        score: t.score,
        max: t.max,
        percentage: t.max > 0 ? (t.score / t.max) * 100 : 0,
      }))
      .sort((a, b) => {
        const order = Object.keys(PART_META)
        return order.indexOf(a.module) - order.indexOf(b.module)
      })
  }

  const bandFor = (percentage: number) =>
    COMPETENCY_BANDS.find((b) => percentage >= b.min) || COMPETENCY_BANDS[COMPETENCY_BANDS.length - 1]

  const getVerdict = (result: AssessmentResult) => {
    if (result.passed === true) {
      return { label: 'Passed', color: 'text-green-600', chip: 'bg-green-100 text-green-700' }
    }
    if (result.passed === false) {
      return { label: 'Not Qualified', color: 'text-red-600', chip: 'bg-red-100 text-red-700' }
    }
    if (result.percentage >= PASS_THRESHOLD_PERCENT) {
      return { label: 'Qualified', color: 'text-green-600', chip: 'bg-green-100 text-green-700' }
    }
    return { label: 'Not Qualified', color: 'text-red-600', chip: 'bg-red-100 text-red-700' }
  }

  const getScoreColor = (percentage: number) => {
    if (percentage >= PASS_THRESHOLD_PERCENT) return 'bg-green-500'
    if (percentage >= 40) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const partRows = (partScores?: Record<string, number> | null) => {
    if (!partScores) return []
    return Object.entries(PART_META)
      .filter(([key]) => typeof partScores[key] === 'number')
      .map(([key, meta]) => ({ key, ...meta, score: partScores[key] as number }))
  }

  const overallAverage = useMemo(
    () =>
      results.length
        ? (results.reduce((acc, r) => acc + (r.percentage || 0), 0) / results.length).toFixed(1)
        : '0',
    [results]
  )

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Assessment Results</h1>
        <p className="text-gray-600">
          Your five-part employment assessment results. A score of 80% or higher qualifies you
          for consideration across the logic, general, category, position, practical and
          professional sections.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading results...</p>
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
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No results yet</h3>
          <p className="text-gray-600 mb-4">Complete an assessment to see your results here.</p>
          <a href="/applicant/assessment" className="btn-primary">
            Take Assessment
          </a>
        </div>
      ) : (
        <div className="space-y-6">
          {results.map((result) => {
            const verdict = getVerdict(result)
            const band = bandFor(result.percentage)
            const detail = feedbackMap[result.id]
            const breakdown = detail ? moduleBreakdown(detail) : []
            const parts = partRows(result.partScores)
            return (
              <div key={result.id} className="card">
                <div className="flex items-start justify-between mb-4 flex-wrap gap-3">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {result.assessment?.title || 'Employment Assessment'}
                    </h3>
                    <p className="text-sm text-gray-500">
                      Completed: {new Date(result.completedAt).toLocaleDateString()}
                    </p>
                    <div className="mt-2 flex items-center gap-2 flex-wrap">
                      <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-semibold ${verdict.chip}`}>
                        {verdict.label}
                      </span>
                      <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-semibold ${band.chip}`}>
                        {band.label}
                      </span>
                    </div>
                    {result.categoryName && (
                      <p className="text-sm text-gray-600 mt-2">
                        Applied for: <span className="font-medium">{result.categoryName}</span>
                        {result.positionName ? ` — ${result.positionName}` : ''}
                      </p>
                    )}
                  </div>
                  <div className="text-right">
                    <div className={`text-3xl font-bold ${verdict.color}`}>
                      {result.percentage?.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-500">{result.score} points</div>
                  </div>
                </div>

                {/* Score bar */}
                <div className="mb-4">
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-gray-600">Overall Score</span>
                    <span className="font-medium">Pass mark: {PASS_THRESHOLD_PERCENT}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`${getScoreColor(result.percentage)} h-3 rounded-full transition-all duration-500`}
                      style={{ width: `${Math.min(result.percentage, 100)}%` }}
                    />
                  </div>
                </div>

                {/* Part scores (5-part framework) */}
                {parts.length > 0 && (
                  <div className="mb-4 pt-4 border-t border-gray-200">
                    <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">
                      Section Scores
                    </p>
                    <div className="grid md:grid-cols-2 gap-x-8 gap-y-3">
                      {parts.map((part) => (
                        <div key={part.key}>
                          <div className="flex items-center justify-between text-sm mb-1">
                            <span className="font-medium text-gray-700">{part.label}</span>
                            <span className="text-gray-500 tabular-nums">
                              {part.score.toFixed(0)}% <span className="text-xs text-gray-400">({part.weight}% weight)</span>
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full transition-all duration-500 ${
                                part.score >= PASS_THRESHOLD_PERCENT ? 'bg-green-500' : part.score >= 40 ? 'bg-yellow-500' : 'bg-red-400'
                              }`}
                              style={{ width: `${Math.min(part.score, 100)}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Alternative category recommendation */}
                {result.recommendedCategory && result.percentage < PASS_THRESHOLD_PERCENT && (
                  <div className="mb-4 p-4 rounded-lg border border-primary-200 bg-primary-50">
                    <p className="text-sm font-semibold text-primary-800 mb-1">
                      Alternative career recommendation
                    </p>
                    <p className="text-sm text-gray-700">
                      Based on your performance, you are better suited for the{' '}
                      <strong>{result.recommendedCategory}</strong> category. Consider retaking the
                      assessment with this category to improve your chances of qualification.
                    </p>
                  </div>
                )}

                {/* Module breakdown */}
                {breakdown.length > 0 && (
                  <div className="mb-4 pt-4 border-t border-gray-200">
                    <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">
                      Question Breakdown
                    </p>
                    <div className="space-y-3">
                      {breakdown.map((mod) => (
                        <div key={mod.module}>
                          <div className="flex items-center justify-between text-sm mb-1">
                            <span className="font-medium text-gray-700">
                              {PART_META[mod.module]?.label || mod.module}
                            </span>
                            <span className="text-gray-500 tabular-nums">{mod.percentage.toFixed(1)}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full transition-all duration-500 ${
                                mod.percentage >= PASS_THRESHOLD_PERCENT ? 'bg-green-500' : 'bg-red-400'
                              }`}
                              style={{ width: `${Math.min(mod.percentage, 100)}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Verdict */}
                <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
                  <div className="text-center">
                    <div className="text-sm text-gray-500">Verdict</div>
                    <div className={`font-medium ${verdict.color}`}>
                      {result.aiRecommendation || verdict.label}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-500">Score</div>
                    <div className="font-medium">{result.score}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-500">Percentage</div>
                    <div className="font-medium">{result.percentage?.toFixed(1)}%</div>
                  </div>
                </div>

                {/* AI Feedback toggle */}
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <button
                    onClick={() => toggleFeedback(result.id)}
                    className="btn-secondary text-sm"
                    disabled={loadingFeedback === result.id}
                  >
                    {loadingFeedback === result.id
                      ? 'Loading feedback...'
                      : feedbackMap[result.id]
                      ? 'Hide Feedback'
                      : 'View Feedback'}
                  </button>

                  {detail && (
                    <div className="mt-4 space-y-4">
                      {(detail.session?.ai_summary || detail.session?.ai_recommendation) && (
                        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                          {detail.session?.ai_recommendation && (
                            <p className="text-sm font-semibold text-primary-800 mb-1">
                              Recommendation: {detail.session?.ai_recommendation}
                            </p>
                          )}
                          {detail.session?.ai_summary && (
                            <p className="text-sm text-gray-700">{detail.session?.ai_summary}</p>
                          )}
                        </div>
                      )}

                      {detail.feedback?.length > 0 ? (
                        detail.feedback.map((item, index) => (
                          <div key={index} className="border border-gray-200 rounded-lg p-4">
                            <div className="flex items-start justify-between mb-2">
                              <div className="min-w-0">
                                <div className="flex items-center gap-2 flex-wrap">
                                  {item.part && (
                                    <span className="badge-primary text-xs">
                                      {PART_META[item.part]?.label || item.part}
                                    </span>
                                  )}
                                  <span className="badge-gray text-xs">{item.question_type || item.category}</span>
                                </div>
                                <p className="font-medium text-gray-900 mt-2">
                                  <MathText text={item.question} />
                                </p>
                              </div>
                              <div className="text-right shrink-0 ml-4">
                                <span className="text-xl font-bold text-gray-900">{item.score}</span>
                                <span className="text-sm text-gray-500"> / {item.max_score}</span>
                              </div>
                            </div>
                            {item.user_answer && (
                              <div className="mb-2">
                                <p className="text-xs font-medium text-gray-500 uppercase mb-1">Your answer</p>
                                <p className="text-sm text-gray-700 bg-gray-50 rounded p-2 whitespace-pre-wrap max-h-32 overflow-y-auto">
                                  <MathText text={item.user_answer} />
                                </p>
                              </div>
                            )}
                            {item.feedback && (
                              <div>
                                <p className="text-xs font-medium text-gray-500 uppercase mb-1">Feedback</p>
                                <p className="text-sm text-gray-700">{item.feedback}</p>
                              </div>
                            )}
                          </div>
                        ))
                      ) : (
                        <p className="text-sm text-gray-500">No feedback available for this session.</p>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )
          })}

          {/* Summary Card */}
          <div className="card bg-gradient-to-r from-primary-600 to-primary-800 text-white">
            <h3 className="text-lg font-semibold mb-4">Performance Summary</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold">{results.length}</div>
                <div className="text-primary-100">Assessments Taken</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold">{overallAverage}%</div>
                <div className="text-primary-100">Average Score</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold">
                  {results.filter((r) => r.passed === true || (r.passed == null && r.percentage >= PASS_THRESHOLD_PERCENT)).length}
                </div>
                <div className="text-primary-100">Qualified</div>
              </div>
            </div>
          </div>

          {/* Email note */}
          <div className="card border border-primary-200 bg-primary-50/50">
            <div className="flex items-start gap-3">
              <svg className="w-6 h-6 text-primary-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <div>
                <h4 className="font-semibold text-gray-900">Results by email</h4>
                <p className="text-sm text-gray-600">
                  A detailed breakdown of this assessment — including per-question feedback — is sent
                  to your registered email address after submission and admin verification.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ApplicantResults
