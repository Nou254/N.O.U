import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface ProjectPayment {
  id: string
  payment_type: string
  amount: number | null
  currency: string
  status: string
  method: string
  reference: string | null
  receipt_number: string | null
  verified_at: string | null
  created_at: string
}

interface ProjectRequest {
  id: string
  request_number: string
  title: string
  description: string
  service_type: string | null
  location: string | null
  category: string | null
  status: string
  budget: number | null
  deadline: string | null
  admin_notes: string | null
  quotation_amount: number | null
  quotation_currency: string | null
  deposit_percent: number | null
  deposit_amount: number | null
  payment_schedule: string | null
  scope_included: string | null
  scope_excluded: string | null
  quotation_issued_at: string | null
  quotation_accepted_at: string | null
  agreed_amount: number | null
  paid_amount: number | null
  activated_at: string | null
  created_at: string
  payments: ProjectPayment[]
}

interface PublishedProject {
  id: number
  title: string
  description: string | null
  category: string | null
  section: string | null
  product_status: string | null
  platform: string | null
  status: string
  budget: number | null
  deadline: string | null
  member_count: number
  progress_percentage: number | null
  progress_reports: { id: number; week_label: string; percentage: number; summary: string | null; created_at: string }[]
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

// N.O.U. quotation workflow stages (today.md docs 8 + 9)
const STATUS_FLOW: { status: string; label: string }[] = [
  { status: 'submitted', label: 'Submitted' },
  { status: 'under_review', label: 'Under Review' },
  { status: 'clarification_required', label: 'Clarification' },
  { status: 'technically_feasible', label: 'Feasibility' },
  { status: 'documentation', label: 'Documentation' },
  { status: 'estimation', label: 'Estimation' },
  { status: 'quotation_issued', label: 'Quotation' },
  { status: 'customer_decision', label: 'Decision' },
  { status: 'agreement', label: 'Agreement' },
  { status: 'awaiting_deposit', label: 'Deposit' },
  { status: 'payment_verified', label: 'Payment' },
  { status: 'project_activated', label: 'Activated' },
  { status: 'development', label: 'Development' },
  { status: 'testing', label: 'Testing' },
  { status: 'delivery', label: 'Delivery' },
  { status: 'completed', label: 'Completed' },
]

const TERMINAL = ['completed', 'declined', 'cancelled', 'on_hold', 'suspended', 'terminated']

const STATUS_COLORS: Record<string, string> = {
  submitted: 'badge-primary',
  under_review: 'badge-primary',
  clarification_required: 'badge-warning',
  technically_feasible: 'badge-success',
  documentation: 'badge-primary',
  estimation: 'badge-primary',
  quotation_issued: 'badge-warning',
  awaiting_deposit: 'badge-warning',
  payment_verified: 'badge-success',
  project_activated: 'badge-success',
  development: 'badge-primary',
  completed: 'badge-success',
  declined: 'badge-gray',
  cancelled: 'badge-gray',
}

const formatMoney = (n: number | null, currency?: string | null) => {
  if (n == null) return '-'
  const cur = currency || 'KSh'
  return `${cur} ${Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 })}`
}

const SERVICE_LABELS: Record<string, string> = {
  software_development: 'Software Development',
  wifi_installation: 'Wi-Fi Installation',
  cctv_installation: 'CCTV Installation',
  network_setup: 'Network Setup',
  consultancy: 'Consultancy',
  it_support: 'IT Support & Maintenance',
  maintenance: 'Maintenance',
  other: 'Other',
}

const formatFileSize = (bytes: number | null) => {
  if (bytes == null) return ''
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

const CustomerProjects = () => {
  const [projects, setProjects] = useState<ProjectRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [gallery, setGallery] = useState<PublishedProject[]>([])
  const [sections, setSections] = useState<string[]>([])
  const [activeSection, setActiveSection] = useState('All')
  const [loadingGallery, setLoadingGallery] = useState(true)
  const [showNewProject, setShowNewProject] = useState(false)
  const [payingProject, setPayingProject] = useState<ProjectRequest | null>(null)
  const [payment, setPayment] = useState({
    amount: '',
    method: 'mpesa',
    reference: '',
    phone: '',
    email: '',
  })
  const [paymentInfo, setPaymentInfo] = useState<string | null>(null)
  const [submittingPayment, setSubmittingPayment] = useState(false)
  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
    service_type: 'software_development',
    category: '',
    location: '',
    budget: '',
    deadline: '',
  })

  useEffect(() => {
    fetchProjects()
    fetchGallery()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects/me')
      setProjects(response.data.projects || [])
    } catch (error) {
      console.error('Error fetching projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchGallery = async () => {
    try {
      const response = await api.get('/portal/projects/published')
      setGallery(response.data.projects || [])
      setSections(response.data.sections || [])
    } catch (error) {
      console.error('Error fetching published gallery:', error)
    } finally {
      setLoadingGallery(false)
    }
  }

  const visibleGallery =
    activeSection === 'All'
      ? gallery
      : gallery.filter((p) => p.section === activeSection)

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const payload: Record<string, unknown> = {
        title: newProject.title,
        description: newProject.description,
        service_type: newProject.service_type,
        category: newProject.category,
      }
      if (newProject.location) payload.location = newProject.location
      if (newProject.budget) payload.budget = Number(newProject.budget)
      if (newProject.deadline) payload.deadline = newProject.deadline

      const response = await api.post('/projects', payload)
      toast.success(
        response.data?.request_number
          ? `Request submitted: ${response.data.request_number}`
          : 'Project request submitted successfully'
      )
      setShowNewProject(false)
      setNewProject({
        title: '',
        description: '',
        service_type: 'software_development',
        category: '',
        location: '',
        budget: '',
        deadline: '',
      })
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to submit project request')
    }
  }

  const handleAcceptQuotation = async (project: ProjectRequest) => {
    if (!window.confirm('Accept this quotation and proceed to the initial deposit?')) return
    try {
      const response = await api.post(`/projects/${project.id}/accept-quotation`)
      toast.success(response.data?.message || 'Quotation accepted')
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to accept quotation')
    }
  }

  const handleDeclineQuotation = async (project: ProjectRequest) => {
    if (!window.confirm('Decline this quotation? This will close the request.')) return
    try {
      const response = await api.post(`/projects/${project.id}/decline-quotation`)
      toast.success(response.data?.message || 'Quotation declined')
      fetchProjects()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to decline quotation')
    }
  }

  const openPayment = (project: ProjectRequest) => {
    setPaymentInfo(null)
    setPayment({
      amount: project.deposit_amount != null ? String(project.deposit_amount) : '',
      method: 'mpesa',
      reference: '',
      phone: '',
      email: '',
    })
    setPayingProject(project)
  }

  const handleSubmitPayment = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!payingProject) return
    setSubmittingPayment(true)
    setPaymentInfo(null)
    try {
      if (payment.method === 'mpesa' || payment.method === 'card') {
        // Provider flow: M-Pesa STK push or Flutterwave card checkout.
        const response = await api.post('/payments/initiate', {
          project_request_id: payingProject.id,
          payment_type: 'deposit',
          amount: Number(payment.amount),
          method: payment.method,
          currency: payingProject.quotation_currency || 'KSh',
          phone: payment.method === 'mpesa' ? payment.phone : undefined,
          email: payment.method === 'card' ? (payment.email || undefined) : undefined,
        })
        const checkout = response.data?.checkout_url
        if (checkout) {
          toast.success('Opening secure card payment page...')
          window.open(checkout, '_blank')
          setPaymentInfo(
            'Card checkout opened in a new tab. Once you complete the payment, your project will be activated automatically.'
          )
          setPayingProject(null)
        } else {
          const msg = response.data?.message || 'Payment initiated'
          toast.success(msg)
          setPaymentInfo(
            response.data?.simulated
              ? 'M-Pesa is not configured yet (simulation mode). The payment was recorded - an admin can verify it, or configure MPESA_* keys in backend/.env for live STK push.'
              : 'A payment prompt has been sent to your phone. Enter your M-Pesa PIN to complete the payment - your project activates automatically once confirmed.'
          )
          setPayingProject(null)
        }
        fetchProjects()
      } else {
        // Bank / manual: record the reference for admin verification.
        await api.post(`/projects/${payingProject.id}/payments`, {
          payment_type: 'deposit',
          amount: Number(payment.amount),
          method: payment.method,
          reference: payment.reference || undefined,
        })
        toast.success('Payment submitted for verification')
        setPayingProject(null)
        fetchProjects()
      }
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to submit payment')
    } finally {
      setSubmittingPayment(false)
    }
  }

  const categories = [
    { value: 'web_development', label: 'Web Development' },
    { value: 'mobile_app', label: 'Mobile Application' },
    { value: 'desktop_app', label: 'Desktop Application' },
    { value: 'api_development', label: 'API Development' },
    { value: 'database', label: 'Database Design' },
    { value: 'other', label: 'Other' },
  ]

  const SERVICE_OPTIONS = [
    { value: 'software_development', label: 'Software Development' },
    { value: 'wifi_installation', label: 'Wi-Fi Installation' },
    { value: 'cctv_installation', label: 'CCTV Installation' },
    { value: 'network_setup', label: 'Network Setup' },
    { value: 'consultancy', label: 'Consultancy' },
    { value: 'it_support', label: 'IT Support & Maintenance' },
    { value: 'other', label: 'Other' },
  ]

  const isPhysicalService = ['wifi_installation', 'cctv_installation', 'network_setup', 'it_support', 'consultancy'].includes(newProject.service_type)

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Project Requests</h1>
          <p className="text-gray-600">Submit and track your software development requests through the quotation workflow.</p>
        </div>
        <button
          onClick={() => setShowNewProject(true)}
          className="btn-primary"
        >
          <svg
            className="w-5 h-5 mr-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          New Request
        </button>
      </div>

      {/* New Project Modal */}
      {showNewProject && (
        <div className="modal-overlay" onClick={() => setShowNewProject(false)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Submit Project Request</h2>
            <form onSubmit={handleCreateProject} className="space-y-4">
              <div>
                <label className="label">Service type</label>
                <select
                  value={newProject.service_type}
                  onChange={(e) => setNewProject({ ...newProject, service_type: e.target.value })}
                  className="input"
                >
                  {SERVICE_OPTIONS.map((s) => (
                    <option key={s.value} value={s.value}>
                      {s.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="label">Title</label>
                <input
                  type="text"
                  value={newProject.title}
                  onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
                  required
                  className="input"
                  placeholder={
                    newProject.service_type === 'software_development'
                      ? 'Name your project'
                      : 'e.g. Office Wi-Fi for 25 staff'
                  }
                />
              </div>
              <div>
                <label className="label">Category</label>
                <select
                  value={newProject.category}
                  onChange={(e) => setNewProject({ ...newProject, category: e.target.value })}
                  className="input"
                >
                  <option value="">Select a category</option>
                  {categories.map((cat) => (
                    <option key={cat.value} value={cat.value}>
                      {cat.label}
                    </option>
                  ))}
                </select>
              </div>
              {isPhysicalService && (
                <div>
                  <label className="label">Site / Location</label>
                  <input
                    type="text"
                    value={newProject.location}
                    onChange={(e) => setNewProject({ ...newProject, location: e.target.value })}
                    className="input"
                    placeholder="Address where the work happens"
                  />
                </div>
              )}
              <div>
                <label className="label">Description</label>
                <textarea
                  value={newProject.description}
                  onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                  required
                  rows={4}
                  className="input"
                  placeholder="Describe your project requirements in detail"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Estimated Budget (USD)</label>
                  <input
                    type="number"
                    value={newProject.budget}
                    onChange={(e) => setNewProject({ ...newProject, budget: e.target.value })}
                    className="input"
                    placeholder="Optional"
                  />
                </div>
                <div>
                  <label className="label">Preferred Deadline</label>
                  <input
                    type="date"
                    value={newProject.deadline}
                    onChange={(e) => setNewProject({ ...newProject, deadline: e.target.value })}
                    className="input"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowNewProject(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Submit Request
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Payment Modal */}
      {payingProject && (
        <div className="modal-overlay" onClick={() => setPayingProject(null)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-1">Initial Deposit</h2>
            <p className="text-sm text-gray-500 mb-4">
              {payingProject.request_number} - {payingProject.title}
            </p>
            {payingProject.quotation_amount != null && (
              <div className="bg-primary-50 rounded-lg p-4 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Quotation total</span>
                  <span className="font-medium text-gray-900">
                    {formatMoney(payingProject.quotation_amount, payingProject.quotation_currency)}
                  </span>
                </div>
                <div className="flex justify-between text-sm mt-1">
                  <span className="text-gray-600">Deposit ({payingProject.deposit_percent || 30}%)</span>
                  <span className="font-semibold text-primary-700">
                    {formatMoney(payingProject.deposit_amount, payingProject.quotation_currency)}
                  </span>
                </div>
              </div>
            )}
            <form onSubmit={handleSubmitPayment} className="space-y-4">
              <div>
                <label className="label">Amount ({payingProject.quotation_currency || 'KSh'})</label>
                <input
                  type="number"
                  value={payment.amount}
                  onChange={(e) => setPayment({ ...payment, amount: e.target.value })}
                  required
                  min={1}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Payment Method</label>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { value: 'mpesa', label: 'M-Pesa', hint: 'STK push to your phone' },
                    { value: 'card', label: 'Card', hint: 'Visa / Mastercard (Flutterwave)' },
                    { value: 'bank', label: 'Bank Transfer', hint: 'Record a bank reference' },
                    { value: 'manual', label: 'Manual / Cash', hint: 'Pay at our offices' },
                  ].map((opt) => (
                    <button
                      type="button"
                      key={opt.value}
                      onClick={() => setPayment({ ...payment, method: opt.value })}
                      className={`text-left rounded-lg border-2 px-3 py-2 transition-all ${
                        payment.method === opt.value
                          ? 'border-primary-600 bg-primary-50'
                          : 'border-gray-200 hover:border-primary-300'
                      }`}
                    >
                      <p className="text-sm font-semibold text-gray-900">{opt.label}</p>
                      <p className="text-[11px] text-gray-500">{opt.hint}</p>
                    </button>
                  ))}
                </div>
              </div>
              {payment.method === 'mpesa' && (
                <div>
                  <label className="label">M-Pesa Phone Number</label>
                  <input
                    type="tel"
                    value={payment.phone}
                    onChange={(e) => setPayment({ ...payment, phone: e.target.value })}
                    required
                    className="input"
                    placeholder="e.g. 0712 345 678"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    We send a payment prompt to this phone - confirm with your M-Pesa PIN.
                  </p>
                </div>
              )}
              {payment.method === 'card' && (
                <div>
                  <label className="label">
                    Email for the payment receipt <span className="text-gray-400">(optional)</span>
                  </label>
                  <input
                    type="email"
                    value={payment.email}
                    onChange={(e) => setPayment({ ...payment, email: e.target.value })}
                    className="input"
                    placeholder="you@example.com"
                  />
                </div>
              )}
              {(payment.method === 'bank' || payment.method === 'manual') && (
                <div>
                  <label className="label">Transaction Reference</label>
                  <input
                    type="text"
                    value={payment.reference}
                    onChange={(e) => setPayment({ ...payment, reference: e.target.value })}
                    className="input"
                    placeholder="Bank reference / receipt code"
                  />
                </div>
              )}
              <div className="bg-gray-50 rounded-lg p-3 text-xs text-gray-500">
                {payment.method === 'mpesa' || payment.method === 'card'
                  ? 'M-Pesa and card payments are confirmed automatically by the payment provider and your project activates instantly.'
                  : 'Your payment will be reviewed and verified by N.O.U. administration before the project is activated.'}
              </div>
              {paymentInfo && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-sm text-green-800">
                  {paymentInfo}
                </div>
              )}
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setPayingProject(null)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={submittingPayment}>
                  {submittingPayment ? 'Processing...' : 'Pay Now'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Projects List */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Project Requests</h2>
        
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : projects.length === 0 ? (
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
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <p className="text-gray-600">No project requests yet</p>
            <p className="text-sm text-gray-500 mt-1">Submit a new request to get started</p>
          </div>
        ) : (
          <div className="space-y-5">
            {projects.map((project) => {
              const flowIndex = STATUS_FLOW.findIndex((s) => s.status === project.status)
              const isTerminal = TERMINAL.includes(project.status)
              return (
                <div
                  key={project.id}
                  className="border border-gray-200 rounded-lg p-5 hover:border-gray-300 transition-colors"
                >
                  <div className="flex items-start justify-between flex-wrap gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-medium text-gray-900">{project.title}</h3>
                        {project.request_number && (
                          <span className="text-xs text-gray-400 font-mono">{project.request_number}</span>
                        )}
                      </div>
                      <p className="text-gray-600 text-sm mt-1 line-clamp-2">{project.description}</p>
                      <div className="flex items-center gap-4 mt-2 text-sm text-gray-500 flex-wrap">
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
                          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                          </svg>
                          {SERVICE_LABELS[project.service_type || 'other'] || 'Software Development'}
                        </span>
                        {project.category && (
                          <span className="capitalize">{project.category.replace('_', ' ')}</span>
                        )}
                        {project.location && <span className="truncate max-w-[200px]">{project.location}</span>}
                        {project.budget != null && (
                          <span>Est. budget: ${project.budget.toLocaleString()}</span>
                        )}
                        <span>Created: {new Date(project.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <span className={`badge-primary capitalize ${STATUS_COLORS[project.status] || 'badge-primary'}`}>
                      {project.status.replace('_', ' ')}
                    </span>
                  </div>

                  {/* Workflow progress */}
                  {!isTerminal && flowIndex >= 0 && (
                    <div className="mt-4">
                      <div className="flex items-center gap-1 flex-wrap">
                        {STATUS_FLOW.slice(0, Math.max(flowIndex + 1, 1)).map((stage, i) => (
                          <div key={stage.status} className="flex items-center">
                            <span
                              className={`text-[11px] px-2 py-0.5 rounded-full font-medium ${
                                i === flowIndex
                                  ? 'bg-primary-600 text-white'
                                  : i < flowIndex
                                    ? 'bg-primary-100 text-primary-700'
                                    : 'bg-gray-100 text-gray-400'
                              }`}
                            >
                              {stage.label}
                            </span>
                            {i < flowIndex && <span className="text-primary-300 mx-1 text-xs">→</span>}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Admin notes */}
                  {project.admin_notes && (
                    <div className="mt-3 bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-sm text-yellow-800">
                      <span className="font-medium">Admin note: </span>
                      {project.admin_notes}
                    </div>
                  )}

                  {/* Quotation actions */}
                  {project.status === 'quotation_issued' && project.quotation_amount != null && (
                    <div className="mt-4 border border-primary-200 bg-primary-50 rounded-lg p-4">
                      <div className="flex items-center justify-between flex-wrap gap-2 mb-2">
                        <h4 className="font-semibold text-gray-900">Quotation Issued</h4>
                        <span className="text-xs text-primary-600 font-medium">
                          {project.quotation_issued_at
                            ? new Date(project.quotation_issued_at).toLocaleDateString()
                            : ''}
                        </span>
                      </div>
                      <div className="grid sm:grid-cols-2 gap-3 text-sm mb-3">
                        <div>
                          <p className="text-gray-500">Total quotation</p>
                          <p className="font-bold text-gray-900 text-lg">
                            {formatMoney(project.quotation_amount, project.quotation_currency)}
                          </p>
                        </div>
                        <div>
                          <p className="text-gray-500">Initial deposit ({project.deposit_percent || 30}%)</p>
                          <p className="font-semibold text-gray-900">
                            {formatMoney(project.deposit_amount, project.quotation_currency)}
                          </p>
                        </div>
                      </div>
                      {project.scope_included && (
                        <div className="text-sm text-gray-600 mb-2">
                          <span className="font-medium text-gray-900">Included: </span>
                          {project.scope_included}
                        </div>
                      )}
                      {project.scope_excluded && (
                        <div className="text-sm text-gray-600 mb-2">
                          <span className="font-medium text-gray-900">Excluded: </span>
                          {project.scope_excluded}
                        </div>
                      )}
                      {project.payment_schedule && (
                        <div className="text-sm text-gray-600 mb-4">
                          <span className="font-medium text-gray-900">Payment schedule: </span>
                          {project.payment_schedule}
                        </div>
                      )}
                      <div className="flex gap-3">
                        <button
                          onClick={() => handleAcceptQuotation(project)}
                          className="btn-primary text-sm"
                        >
                          Accept Quotation
                        </button>
                        <button
                          onClick={() => handleDeclineQuotation(project)}
                          className="btn-outline text-sm text-red-600 border-red-300 hover:bg-red-50"
                        >
                          Decline
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Deposit / payment actions */}
                  {project.status === 'awaiting_deposit' && (
                    <div className="mt-4 flex items-center justify-between flex-wrap gap-3 border border-amber-200 bg-amber-50 rounded-lg p-4">
                      <div>
                        <p className="font-medium text-gray-900">Initial deposit due</p>
                        <p className="text-sm text-gray-600">
                          {formatMoney(project.deposit_amount, project.quotation_currency)} - pay to activate your project
                        </p>
                      </div>
                      <button onClick={() => openPayment(project)} className="btn-primary text-sm">
                        Make Payment
                      </button>
                    </div>
                  )}

                  {/* Payments & receipts */}
                  {project.payments && project.payments.length > 0 && (
                    <div className="mt-4">
                      <h4 className="text-sm font-semibold text-gray-700 mb-2">Payments</h4>
                      <div className="space-y-2">
                        {project.payments.map((p) => (
                          <div
                            key={p.id}
                            className="flex items-center justify-between text-sm border border-gray-100 rounded-lg px-3 py-2"
                          >
                            <div>
                              <span className="font-medium capitalize">{p.payment_type}</span>
                              <span className="text-gray-500 mx-2">
                                {formatMoney(p.amount, p.currency)} via {p.method}
                              </span>
                            </div>
                            <div className="flex items-center gap-3">
                              {p.receipt_number && (
                                <span className="text-xs font-mono text-primary-600 bg-primary-50 px-2 py-0.5 rounded">
                                  {p.receipt_number}
                                </span>
                              )}
                              <span
                                className={`text-xs font-medium capitalize ${
                                  p.status === 'successful'
                                    ? 'text-green-600'
                                    : p.status === 'failed'
                                      ? 'text-red-600'
                                      : 'text-amber-600'
                                }`}
                              >
                                {p.status}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Company portfolio gallery (published projects) */}
      <div className="card mt-8">
        <div className="flex items-center justify-between mb-1">
          <h2 className="text-lg font-semibold text-gray-900">Company Portfolio</h2>
          <span className="badge-success">Published</span>
        </div>
        <p className="text-sm text-gray-500 mb-4">
          Projects our development teams have completed and published.
        </p>

        {sections.length > 0 && !loadingGallery && (
          <div className="flex gap-2 mb-5 flex-wrap">
            {['All', ...sections].map((section) => (
              <button
                key={section}
                onClick={() => setActiveSection(section)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                  activeSection === section
                    ? 'bg-primary-600 text-white shadow-sm'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {section}
              </button>
            ))}
          </div>
        )}

        {loadingGallery ? (
          <div className="text-center py-10">
            <div className="spinner mx-auto"></div>
          </div>
        ) : visibleGallery.length === 0 ? (
          <div className="text-center py-10">
            <svg
              className="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-600">No published projects in this section yet</p>
            <p className="text-sm text-gray-500 mt-1">
              Completed projects approved by management will appear here.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {visibleGallery.map((project) => (
              <div
                key={project.id}
                className="border border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors"
              >
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <h3 className="font-semibold text-gray-900">{project.title}</h3>
                  {project.section && <span className="badge-primary text-xs">{project.section}</span>}
                  {project.product_status && <span className="badge-success text-xs">{project.product_status}</span>}
                  {project.platform && <span className="badge-warning text-xs">{project.platform}</span>}
                </div>
                {project.category && (
                  <p className="text-xs text-primary-600 uppercase tracking-wide mb-2">
                    {project.category.replace('_', ' ')}
                  </p>
                )}
                <p className="text-sm text-gray-600 line-clamp-2 mb-3">
                  {project.description || 'No description provided.'}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500 mb-2">
                  <span>Team: {project.member_count} developer{project.member_count === 1 ? '' : 's'}</span>
                  {project.progress_percentage != null && (
                    <span className="font-medium text-green-600">
                      Completed {project.progress_percentage}%
                    </span>
                  )}
                </div>
                {project.documents && project.documents.length > 0 && (
                  <div className="space-y-1">
                    {project.documents.map((doc) => (
                      <a
                        key={doc.id}
                        href={doc.download_url || `#`}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-2 text-xs text-primary-600 hover:text-primary-700"
                      >
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        {doc.filename}
                      </a>
                    ))}
                  </div>
                )}
                {project.releases && project.releases.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <p className="text-[11px] uppercase tracking-wide text-gray-400 font-semibold mb-2">
                      Download the software
                    </p>
                    <div className="space-y-2">
                      {project.releases.map((release) => (
                        <a
                          key={release.id}
                          href={release.download_url || `#`}
                          className="flex items-center justify-between gap-2 w-full rounded-lg border border-primary-200 bg-primary-50 hover:bg-primary-100 transition-colors px-3 py-2"
                        >
                          <div className="flex items-center gap-2 min-w-0">
                            <svg className="w-5 h-5 text-primary-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                            <div className="min-w-0">
                              <p className="text-sm font-medium text-primary-700 truncate">
                                {release.filename}
                              </p>
                              <p className="text-[11px] text-gray-500">
                                {release.version ? `v${release.version}` : ''}
                                {release.platform ? ` · ${release.platform}` : ''}
                                {formatFileSize(release.file_size)}
                              </p>
                            </div>
                          </div>
                          <span className="text-xs font-semibold text-primary-700 shrink-0">Download</span>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default CustomerProjects