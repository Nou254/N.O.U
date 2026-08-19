import { useEffect, useState } from 'react'
import { useRouteMemory } from '../../utils/routeMemory'
import { useNavigate } from 'react-router-dom'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Job {
  id: string
  title: string
  description: string
  department: string
  location: string
  employment_type: string
  salary_range: string
  requirements: string | null
}

interface Category {
  id: number
  name: string
  positions: { id: number; name: string }[]
}

const CareersPage = () => {
  const navigate = useNavigate()
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [department, setDepartment] = useState('')
  const [applyingJob, setApplyingJob] = useState<Job | null>(null)
  // Route-memory: the applicant's details survive navigating away and back.
  const [applyForm, setApplyForm] = useRouteMemory('applyForm', {
    full_name: '',
    email: '',
    phone: '',
    cover_letter: '',
    category_id: '',
  })
  const [cvFile, setCvFile] = useState<File | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [categoriesLoading, setCategoriesLoading] = useState(true)
  const [categoriesError, setCategoriesError] = useState('')

  useEffect(() => {
    fetchJobs()
  }, [department])

  const fetchCategories = async () => {
    setCategoriesLoading(true)
    setCategoriesError('')
    try {
      const res = await api.get('/personnel/categories')
      const list = res.data.categories || []
      setCategories(list)
      if (list.length === 0) {
        setCategoriesError('No qualification categories are available yet. An administrator needs to add them.')
      }
    } catch (error) {
      console.error('Failed to load qualification categories:', error)
      setCategoriesError(
        'Could not load the qualification categories. The server may be starting up - please retry.'
      )
    } finally {
      setCategoriesLoading(false)
    }
  }

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchJobs = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (department) params.append('department', department)

      const response = await api.get(`/employment/jobs?${params}`)
      setJobs(response.data.jobs)
    } catch (error) {
      console.error('Error fetching jobs:', error)
    } finally {
      setLoading(false)
    }
  }

  const departments = [
    { value: '', label: 'All Departments' },
    { value: 'Engineering', label: 'Engineering' },
    { value: 'Design', label: 'Design' },
    { value: 'Operations', label: 'Operations' },
    { value: 'Documentation', label: 'Documentation' },
  ]

  const employmentTypes: Record<string, string> = {
    full_time: 'Full Time',
    part_time: 'Part Time',
    contract: 'Contract',
    internship: 'Internship',
  }

  const openApply = (job: Job) => {
    setApplyingJob(job)
    setApplyForm({ full_name: '', email: '', phone: '', cover_letter: '', category_id: '' })
    setCvFile(null)
  }

  const selectedApplyCategory = categories.find((c) => c.id === Number(applyForm.category_id))

  const goToAssessment = () => {
    navigate('/assessment', {
      state: {
        fullName: applyForm.full_name.trim(),
        email: applyForm.email.trim(),
        phone: applyForm.phone.trim(),
        categoryId: Number(applyForm.category_id),
        categoryName: selectedApplyCategory?.name,
      },
    })
  }

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!applyingJob) return
    if (!applyForm.category_id) {
      toast.error('Select your place of qualification (professional category)')
      return
    }
    setSubmitting(true)
    try {
      // Multipart when a CV is attached (carries the file); plain JSON keeps
      // the lightweight path when no CV was chosen.
      if (cvFile) {
        const formData = new FormData()
        formData.append('full_name', applyForm.full_name)
        formData.append('email', applyForm.email)
        formData.append('phone', applyForm.phone)
        formData.append('job_id', applyingJob.id)
        formData.append('category_id', String(applyForm.category_id))
        formData.append('category_name', selectedApplyCategory?.name || '')
        if (applyForm.cover_letter.trim()) formData.append('cover_letter', applyForm.cover_letter)
        formData.append('cv_file', cvFile)
        await api.post('/employment/applications/public-apply', formData)
      } else {
        const payload: Record<string, unknown> = {
          full_name: applyForm.full_name,
          email: applyForm.email,
          phone: applyForm.phone,
          job_id: applyingJob.id,
          category_id: Number(applyForm.category_id),
          category_name: selectedApplyCategory?.name,
        }
        if (applyForm.cover_letter.trim()) payload.cover_letter = applyForm.cover_letter
        await api.post('/employment/applications/public-apply', payload)
      }
      toast.success('Application received! Starting your assessment...')
      goToAssessment()
    } catch (error: any) {
      const detail =
        error?.response?.data?.message ||
        error?.response?.data?.detail ||
        'Failed to submit application'
      if (error?.response?.status === 400 && String(detail).toLowerCase().includes('already applied')) {
        // Already applied for this position - don't block the assessment.
        toast.success('You already applied for this position - continuing to your assessment.')
        goToAssessment()
      } else {
        toast.error(detail)
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Career Opportunities
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Join our team and help build the future of digital systems. Apply directly -
          no account or registration needed. Choose your place of qualification - that is
          exactly where you will be assessed.
        </p>
      </div>

      {/* Filter */}
      <div className="flex justify-center mb-8">
        <div className="w-64">
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="input"
          >
            {departments.map((dept) => (
              <option key={dept.value} value={dept.value}>
                {dept.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Jobs List */}
      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading positions...</p>
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-12">
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
              d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
          <p className="text-gray-600">No positions available at the moment</p>
        </div>
      ) : (
        <div className="space-y-4">
          {jobs.map((job) => (
            <div key={job.id} className="card">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2 flex-wrap">
                    <h3 className="text-xl font-semibold text-gray-900">{job.title}</h3>
                    <span className="badge-primary">{employmentTypes[job.employment_type] || job.employment_type}</span>
                  </div>
                  <p className="text-gray-600 mb-3 line-clamp-2">{job.description}</p>
                  <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                    {job.department && (
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                        {job.department}
                      </span>
                    )}
                    {job.location && (
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {job.location}
                      </span>
                    )}
                    {job.salary_range && (
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {job.salary_range}
                      </span>
                    )}
                  </div>
                  {job.requirements && (
                    <p className="text-sm text-gray-500 mt-2 line-clamp-2">
                      <span className="font-medium text-gray-700">Requirements: </span>
                      {job.requirements}
                    </p>
                  )}
                </div>
                <div className="mt-4 md:mt-0 md:ml-6">
                  <button onClick={() => openApply(job)} className="btn-primary">
                    Apply Now
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Apply Modal */}
      {applyingJob && (
        <div className="modal-overlay" onClick={() => setApplyingJob(null)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-1">Apply for {applyingJob.title}</h2>
            <p className="text-sm text-gray-500 mb-4">
              No account needed. Enter your details, choose your place of qualification, and
              you will be taken straight into your assessment.
            </p>

            <form onSubmit={handleApply} className="space-y-4">
              <div>
                <label className="label">Official Names</label>
                <input
                  type="text"
                  value={applyForm.full_name}
                  onChange={(e) => setApplyForm({ ...applyForm, full_name: e.target.value })}
                  required
                  minLength={3}
                  className="input"
                  placeholder="e.g. John Kamau"
                />
              </div>
              <div>
                <label className="label">Email Address</label>
                <input
                  type="email"
                  value={applyForm.email}
                  onChange={(e) => setApplyForm({ ...applyForm, email: e.target.value })}
                  required
                  className="input"
                  placeholder="you@example.com"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Your results will be sent to this email.
                </p>
              </div>
              <div>
                <label className="label">Phone Number</label>
                <input
                  type="tel"
                  value={applyForm.phone}
                  onChange={(e) => setApplyForm({ ...applyForm, phone: e.target.value })}
                  className="input"
                  placeholder="e.g. 0712 345 678"
                />
                <p className="text-xs text-gray-500 mt-1">
                  So N.O.U. can reach you about your application.
                </p>
              </div>
              <div>
                <label className="label">Place of Qualification</label>
                {categoriesLoading ? (
                  <div className="input flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Loading categories...</span>
                    <span className="spinner inline-block w-4 h-4 border-2"></span>
                  </div>
                ) : categoriesError ? (
                  <div className="rounded-lg border border-red-200 bg-red-50 p-3">
                    <p className="text-sm text-red-600">{categoriesError}</p>
                    <button
                      type="button"
                      onClick={fetchCategories}
                      className="text-xs font-medium text-red-700 underline mt-1"
                    >
                      Retry loading categories
                    </button>
                  </div>
                ) : (
                  <select
                    value={applyForm.category_id}
                    onChange={(e) => setApplyForm({ ...applyForm, category_id: e.target.value })}
                    required
                    className="input"
                  >
                    <option value="">Select where you will be assessed...</option>
                    {categories.map((cat) => (
                      <option key={cat.id} value={cat.id}>
                        {cat.name}
                      </option>
                    ))}
                  </select>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  You will be assessed in the category you choose - e.g. choose Software
                  Engineering and you are assessed on Software Engineering.
                </p>
              </div>
              <div>
                <label className="label">
                  CV / Resume <span className="text-gray-400">(optional, PDF / Word)</span>
                </label>
                {cvFile ? (
                  <div className="flex items-center justify-between rounded-lg border border-primary-200 bg-primary-50 px-3 py-2.5">
                    <span className="text-sm text-primary-800 truncate flex items-center gap-2">
                      <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      {cvFile.name}
                      <span className="text-primary-500 text-xs">
                        ({(cvFile.size / 1024).toFixed(0)} KB)
                      </span>
                    </span>
                    <button
                      type="button"
                      onClick={() => setCvFile(null)}
                      className="text-xs font-medium text-red-600 hover:text-red-700"
                    >
                      Remove
                    </button>
                  </div>
                ) : (
                  <label className="flex items-center justify-center gap-2 rounded-lg border-2 border-dashed border-gray-300 hover:border-primary-400 hover:bg-primary-50/50 transition-colors cursor-pointer px-4 py-4">
                    <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                    </svg>
                    <span className="text-sm text-gray-500">Click to upload your CV</span>
                    <input
                      type="file"
                      accept=".pdf,.doc,.docx,.txt,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0] || null
                        if (file && file.size > 10 * 1024 * 1024) {
                          toast.error('CV must be under 10MB')
                          return
                        }
                        setCvFile(file)
                      }}
                    />
                  </label>
                )}
              </div>
              <div>
                <label className="label">
                  Cover Letter <span className="text-gray-400">(optional)</span>
                </label>
                <textarea
                  value={applyForm.cover_letter}
                  onChange={(e) => setApplyForm({ ...applyForm, cover_letter: e.target.value })}
                  rows={3}
                  className="input"
                  placeholder="Tell us briefly why you're a good fit."
                />
              </div>
              <div className="flex justify-end space-x-3 pt-2">
                <button
                  type="button"
                  onClick={() => setApplyingJob(null)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={submitting || categoriesLoading}>
                  {submitting ? 'Submitting...' : 'Submit & Start Assessment'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* CTA */}
      <div className="mt-16 text-center bg-gray-50 rounded-2xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Don't see what you're looking for?
        </h2>
        <p className="text-gray-600 mb-6">
          We're always looking for talented individuals. Apply to any position directly
          with your names, email and CV - no registration required. You are taken straight
          into your assessment, and your results are emailed to you afterwards.
        </p>
        <a href="mailto:noudigitalsystem@gmail.com" className="btn-primary">
          Contact Us
        </a>
      </div>
    </div>
  )
}

export default CareersPage
