import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Category {
  id: number
  name: string
  positions: { id: number; name: string }[]
}

interface RecruitedDev {
  id: number
  name: string
  email: string
  username: string | null
  role: string
  qualification_category_name: string | null
  qualification_position_name: string | null
  created_at: string | null
}

interface CvReview {
  summary?: string
  highlights?: string[]
  strengths?: string[]
  concerns?: string[]
}

interface ApplicantCv {
  id: number
  name: string
  email: string
  phone?: string | null
  cv_file_path?: string | null
  cv_reviewed?: boolean
  cv_summary?: CvReview | null
  qualification_category?: string | null
  qualification_position?: string | null
}

const AdminRecruitment = () => {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [developers, setDevelopers] = useState<RecruitedDev[]>([])
  const [submitting, setSubmitting] = useState(false)
  const [cvApplicants, setCvApplicants] = useState<ApplicantCv[]>([])
  const [cvTexts, setCvTexts] = useState<Record<string, string>>({})
  const [showCvText, setShowCvText] = useState<Record<string, boolean>>({})
  const [reviewingCv, setReviewingCv] = useState<number | null>(null)
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    category_id: '',
    position_id: '',
    notes: '',
  })

  const fetchData = async () => {
    try {
      setLoading(true)
      const [catRes, devRes, cvRes] = await Promise.all([
        api.get('/personnel/categories'),
        api.get('/admin/recruited'),
        api.get('/admin/cvs'),
      ])
      setCategories(catRes.data.categories || [])
      setDevelopers(devRes.data.developers || [])
      setCvApplicants(cvRes.data.applicants || [])
    } catch (error) {
      console.error('Error loading recruitment data:', error)
      toast.error('Failed to load recruitment data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const selectedCategory = categories.find((c) => c.id === Number(form.category_id))
  const positions = selectedCategory?.positions || []

  // ---- CV actions (view contents + Groq review) -------------------------
  const downloadCv = async (applicant: ApplicantCv) => {
    try {
      const response = await api.get(`/admin/cv/${applicant.id}/download`, {
        responseType: 'blob',
      })
      const ext = (applicant.cv_file_path?.split('.').pop() || 'pdf').toLowerCase()
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.download = `cv_${applicant.id}.${ext}`
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error: any) {
      toast.error(error?.response?.data?.message || 'Could not download the CV')
    }
  }

  const toggleCvText = async (applicant: ApplicantCv) => {
    if (showCvText[applicant.id]) {
      setShowCvText((prev) => ({ ...prev, [applicant.id]: false }))
      return
    }
    if (!cvTexts[applicant.id]) {
      try {
        const response = await api.get(`/admin/cv/${applicant.id}/text`)
        setCvTexts((prev) => ({ ...prev, [applicant.id]: response.data.text || '' }))
      } catch (error: any) {
        toast.error(error?.response?.data?.message || 'Could not read the CV text')
        return
      }
    }
    setShowCvText((prev) => ({ ...prev, [applicant.id]: true }))
  }

  const reviewCv = async (applicant: ApplicantCv) => {
    setReviewingCv(applicant.id)
    try {
      const response = await api.post(
        `/admin/cv/${applicant.id}/review`,
        {},
        { timeout: 15 * 60 * 1000 }
      )
      setCvApplicants((prev) =>
        prev.map((a) =>
          a.id === applicant.id
            ? { ...a, cv_summary: response.data.review, cv_reviewed: true }
            : a
        )
      )
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
        <p className="text-xs font-medium text-primary-700 uppercase mb-1">AI CV Review (Groq)</p>
        <p className="text-sm text-gray-800">{cv.summary}</p>
        {(cv.highlights?.length || 0) > 0 && (
          <div className="mt-2">
            <p className="text-xs font-medium text-gray-500 uppercase mb-1">Highlights</p>
            <ul className="text-sm text-gray-700 list-disc list-inside space-y-0.5">
              {cv.highlights!.map((h, i) => <li key={i}>{h}</li>)}
            </ul>
          </div>
        )}
        {(cv.strengths?.length || 0) > 0 && (
          <div className="mt-2">
            <p className="text-xs font-medium text-gray-500 uppercase mb-1">Strengths</p>
            <ul className="text-sm text-green-700 list-disc list-inside space-y-0.5">
              {cv.strengths!.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
          </div>
        )}
        {(cv.concerns?.length || 0) > 0 && (
          <div className="mt-2">
            <p className="text-xs font-medium text-gray-500 uppercase mb-1">Concerns</p>
            <ul className="text-sm text-amber-700 list-disc list-inside space-y-0.5">
              {cv.concerns!.map((c, i) => <li key={i}>{c}</li>)}
            </ul>
          </div>
        )}
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.category_id) {
      toast.error('Select the place of qualification (professional category)')
      return
    }
    setSubmitting(true)
    try {
      const payload: Record<string, unknown> = {
        first_name: form.first_name.trim(),
        last_name: form.last_name.trim(),
        email: form.email.trim(),
        category_id: Number(form.category_id),
        category_name: selectedCategory?.name,
      }
      if (form.position_id) {
        const position = positions.find((p) => p.id === Number(form.position_id))
        payload.position_id = Number(form.position_id)
        payload.position_name = position?.name
      }
      if (form.notes.trim()) payload.notes = form.notes.trim()

      const response = await api.post('/admin/recruit', payload)
      toast.success(response.data.message)
      if (response.data.developer?.temp_password) {
        toast(
          `Dev credentials: ${response.data.developer.email} / ${response.data.developer.temp_password}`,
          { duration: 15000 }
        )
      }
      setForm({ first_name: '', last_name: '', email: '', category_id: '', position_id: '', notes: '' })
      fetchData()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to recruit developer')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Recruit Developers</h1>
        <p className="text-gray-600">
          Directly recruit a developer by entering their official details and email. Login
          credentials are generated and emailed to them - <strong>no assessment required</strong>.
          They get full access to projects and the community (except the admin section).
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Recruitment form */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">New Recruitment</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label className="label">Official First Name</label>
                <input
                  type="text"
                  value={form.first_name}
                  onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                  required
                  minLength={1}
                  className="input"
                  placeholder="e.g. Henry"
                />
              </div>
              <div>
                <label className="label">Official Last Name</label>
                <input
                  type="text"
                  value={form.last_name}
                  onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                  required
                  minLength={1}
                  className="input"
                  placeholder="e.g. Ochieng"
                />
              </div>
            </div>
            <div>
              <label className="label">Official Email</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
                className="input"
                placeholder="henry.ochieng@company.com"
              />
              <p className="text-xs text-gray-500 mt-1">
                The login credentials will be sent to this address.
              </p>
            </div>
            <div>
              <label className="label">Place of Qualification (Category)</label>
              <select
                value={form.category_id}
                onChange={(e) => setForm({ ...form, category_id: e.target.value, position_id: '' })}
                required
                className="input"
              >
                <option value="">Select a professional category...</option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name}
                  </option>
                ))}
              </select>
              <p className="text-xs text-gray-500 mt-1">
                The category the developer is recruited into (recorded in the talent pool).
              </p>
            </div>
            {selectedCategory && (
              <div>
                <label className="label">Position (optional)</label>
                <select
                  value={form.position_id}
                  onChange={(e) => setForm({ ...form, position_id: e.target.value })}
                  className="input"
                >
                  <option value="">Select a position...</option>
                  {positions.map((pos) => (
                    <option key={pos.id} value={pos.id}>
                      {pos.name}
                    </option>
                  ))}
                </select>
              </div>
            )}
            <div>
              <label className="label">Admin Notes (optional)</label>
              <textarea
                value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })}
                rows={2}
                className="input"
                placeholder="e.g. Referred by the Director - joins the backend team"
              />
            </div>
            <div className="bg-primary-50 border border-primary-200 rounded-lg p-3 text-xs text-primary-800">
              Recruited developers skip the employment assessment entirely and can sign in
              immediately after receiving their credentials.
            </div>
            <button type="submit" disabled={submitting} className="btn-primary w-full">
              {submitting ? 'Recruiting...' : 'Recruit & Send Credentials'}
            </button>
          </form>
        </div>

        {/* Applicant CVs - view contents + activate Groq review */}
        <div className="card lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Applicant CVs</h2>
              <p className="text-sm text-gray-500 mt-1">
                CVs received from the Careers apply form. Read the contents directly, download,
                or press <strong>Review with AI</strong> to have Groq summarise the CV for you.
              </p>
            </div>
            <span className="badge-success">AI Powered</span>
          </div>
          {loading ? (
            <div className="text-center py-8">
              <div className="spinner mx-auto"></div>
            </div>
          ) : cvApplicants.length === 0 ? (
            <div className="text-center py-10 text-gray-500 text-sm">
              No CVs on file yet. CVs arrive when applicants apply via the Careers page.
            </div>
          ) : (
            <div className="space-y-3">
              {cvApplicants.map((applicant) => (
                <div key={applicant.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between gap-3 flex-wrap">
                    <div className="min-w-0">
                      <p className="font-medium text-gray-900">{applicant.name}</p>
                      <p className="text-sm text-gray-500">{applicant.email}</p>
                      <div className="flex flex-wrap gap-3 text-xs text-gray-500 mt-1">
                        {applicant.phone && <span>📞 {applicant.phone}</span>}
                        {(applicant.qualification_category || applicant.qualification_position) && (
                          <span>
                            <span className="font-medium text-gray-700">Qualification:</span>{' '}
                            {applicant.qualification_category || '—'}
                            {applicant.qualification_position
                              ? ` / ${applicant.qualification_position}`
                              : ''}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2 shrink-0">
                      <button
                        onClick={() => toggleCvText(applicant)}
                        className="btn-secondary text-xs"
                      >
                        {showCvText[applicant.id] ? 'Hide Text' : 'Read Text'}
                      </button>
                      <button
                        onClick={() => downloadCv(applicant)}
                        className="btn-secondary text-xs"
                      >
                        Download
                      </button>
                      <button
                        onClick={() => reviewCv(applicant)}
                        disabled={reviewingCv === applicant.id}
                        className="btn-primary text-xs disabled:opacity-50"
                      >
                        {reviewingCv === applicant.id ? (
                          <span className="inline-flex items-center gap-1.5">
                            <span className="spinner inline-block w-3 h-3 border-2"></span>
                            AI Reviewing…
                          </span>
                        ) : applicant.cv_reviewed ? (
                          'Re-review'
                        ) : (
                          'Review with AI'
                        )}
                      </button>
                    </div>
                  </div>

                  {showCvText[applicant.id] && cvTexts[applicant.id] && (
                    <pre className="mt-3 text-xs text-gray-700 bg-gray-50 border border-gray-200 rounded p-3 whitespace-pre-wrap max-h-64 overflow-y-auto">
                      {cvTexts[applicant.id]}
                    </pre>
                  )}
                  {renderCvReview(applicant.cv_summary)}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recruited developers list */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recruited Developers</h2>
          {loading ? (
            <div className="text-center py-8">
              <div className="spinner mx-auto"></div>
            </div>
          ) : developers.length === 0 ? (
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <p className="text-gray-600">No developers recruited yet</p>
              <p className="text-sm text-gray-500 mt-1">
                Recruited developers will appear here with their qualification category.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {developers.map((dev) => (
                <div key={dev.id} className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors">
                  <div className="flex items-center justify-between gap-3">
                    <div className="min-w-0">
                      <p className="font-medium text-gray-900">{dev.name}</p>
                      <p className="text-sm text-gray-500 truncate">{dev.email}</p>
                    </div>
                    <span className="badge-success shrink-0">Recruited</span>
                  </div>
                  <div className="flex flex-wrap gap-3 text-xs text-gray-500 mt-2">
                    <span>
                      <span className="font-medium text-gray-700">Qualification:</span>{' '}
                      {dev.qualification_category_name || '—'}
                      {dev.qualification_position_name ? ` / ${dev.qualification_position_name}` : ''}
                    </span>
                    {dev.username && (
                      <span className="text-primary-600 font-medium">@{dev.username}</span>
                    )}
                    {dev.created_at && (
                      <span>{new Date(dev.created_at).toLocaleDateString()}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminRecruitment
