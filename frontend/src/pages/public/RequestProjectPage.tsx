import { useState } from 'react'
import { useRouteMemory } from '../../utils/routeMemory'
import { Link } from 'react-router-dom'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface SubmittedRequest {
  request_number: string
  title: string
}

// The services N.O.U offers: software builds, Wi-Fi / CCTV installation,
// consultancy, network setup, IT support and maintenance.
interface ServiceOption {
  value: string
  label: string
  tagline: string
  icon: React.ReactNode
}

const SERVICE_ICONS: Record<string, React.ReactNode> = {
  software: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7} d="M8 9l-3 3 3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
  ),
  wifi: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7} d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.07c3.9-3.9 10.24-3.9 14.14 0M1.879 8.89a15.354 15.354 0 0120.242 0M4.74 12.86a9.75 9.75 0 0114.52 0" />
    </svg>
  ),
  cctv: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
    </svg>
  ),
  consultancy: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
    </svg>
  ),
  network: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
    </svg>
  ),
  support: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7} d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
    </svg>
  ),
  other: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
    </svg>
  ),
}

const SERVICES: ServiceOption[] = [
  {
    value: 'software_development',
    label: 'Software Development',
    tagline: 'Apps, websites, bots, systems and custom software built to order.',
    icon: SERVICE_ICONS.software,
  },
  {
    value: 'wifi_installation',
    label: 'Wi-Fi Installation',
    tagline: 'Home, office and campus wireless networks designed and installed.',
    icon: SERVICE_ICONS.wifi,
  },
  {
    value: 'cctv_installation',
    label: 'CCTV Installation',
    tagline: 'Security camera systems with remote viewing and recording.',
    icon: SERVICE_ICONS.cctv,
  },
  {
    value: 'consultancy',
    label: 'Consultancy',
    tagline: 'Digital strategy, software advice and business technology guidance.',
    icon: SERVICE_ICONS.consultancy,
  },
  {
    value: 'network_setup',
    label: 'Network Setup',
    tagline: 'LANs, servers, VPNs and structured cabling for organisations.',
    icon: SERVICE_ICONS.network,
  },
  {
    value: 'it_support',
    label: 'IT Support & Maintenance',
    tagline: 'Ongoing support, maintenance and training for your systems.',
    icon: SERVICE_ICONS.support,
  },
  {
    value: 'other',
    label: 'Something Else',
    tagline: 'Tell us what you need and we will point you the right way.',
    icon: SERVICE_ICONS.other,
  },
]

// Physical-services need a site address; software does not.
const PHYSICAL_SERVICES = new Set([
  'wifi_installation', 'cctv_installation', 'network_setup',
  'it_support', 'consultancy',
])

const CATEGORIES_BY_SERVICE: Record<string, { value: string; label: string }[]> = {
  software_development: [
    { value: 'web_development', label: 'Web Development' },
    { value: 'mobile_app', label: 'Mobile Application (Android / iOS)' },
    { value: 'desktop_app', label: 'Desktop Application' },
    { value: 'pwa', label: 'PWA / Progressive Web App' },
    { value: 'api_development', label: 'API Development' },
    { value: 'database', label: 'Database Design' },
    { value: 'bot', label: 'Chatbot / Automation Bot' },
    { value: 'system_integration', label: 'System Integration' },
    { value: 'other', label: 'Other' },
  ],
  wifi_installation: [
    { value: 'home_wifi', label: 'Home Wi-Fi Setup' },
    { value: 'office_wifi', label: 'Office / Business Wi-Fi' },
    { value: 'campus_wifi', label: 'Campus / Hotspot Network' },
    { value: 'wifi_optimization', label: 'Wi-Fi Optimisation / Expansion' },
    { value: 'other', label: 'Other' },
  ],
  cctv_installation: [
    { value: 'home_security', label: 'Home Security Cameras' },
    { value: 'office_security', label: 'Office / Business Surveillance' },
    { value: 'outdoor_surveillance', label: 'Outdoor / Perimeter Surveillance' },
    { value: 'remote_monitoring', label: 'Remote Viewing & Monitoring' },
    { value: 'other', label: 'Other' },
  ],
  consultancy: [
    { value: 'software_consultancy', label: 'Software & Technology Advice' },
    { value: 'digital_strategy', label: 'Digital Strategy & Transformation' },
    { value: 'it_audit', label: 'IT Systems Audit' },
    { value: 'business_automation', label: 'Business Automation' },
    { value: 'other', label: 'Other' },
  ],
  network_setup: [
    { value: 'lan_setup', label: 'Local Area Network (LAN)' },
    { value: 'server_setup', label: 'Server Setup & Hosting' },
    { value: 'vpn', label: 'VPN & Secure Remote Access' },
    { value: 'cabling', label: 'Structured Cabling' },
    { value: 'other', label: 'Other' },
  ],
  it_support: [
    { value: 'helpdesk', label: 'Helpdesk Support' },
    { value: 'maintenance', label: 'System Maintenance' },
    { value: 'training', label: 'Staff Training' },
    { value: 'other', label: 'Other' },
  ],
  other: [{ value: 'other', label: 'Other' }],
}

const SERVICE_LABELS: Record<string, string> = Object.fromEntries(
  SERVICES.map((s) => [s.value, s.label])
)

const RequestProjectPage = () => {
  // Route-memory: the visitor's request draft survives navigation + refresh.
  const [serviceType, setServiceType] = useRouteMemory('serviceType', 'software_development')
  const [form, setForm] = useRouteMemory('form', {
    full_name: '',
    email: '',
    phone: '',
    title: '',
    category: '',
    description: '',
    location: '',
    budget: '',
    deadline: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState<SubmittedRequest | null>(null)

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const selectService = (value: string) => {
    setServiceType(value)
    setForm((f) => ({
      ...f,
      category: '',
      title: value === 'software_development' ? f.title : '',
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      const payload: Record<string, unknown> = {
        full_name: form.full_name,
        email: form.email,
        title: form.title,
        description: form.description,
        service_type: serviceType,
        category: form.category,
      }
      if (form.phone) payload.phone = form.phone
      if (form.location) payload.location = form.location
      if (form.budget) payload.budget = Number(form.budget)
      if (form.deadline) payload.deadline = form.deadline

      const response = await api.post('/projects/public-request', payload)
      setSubmitted({
        request_number: response.data?.request?.request_number,
        title: form.title,
      })
      toast.success('Request submitted successfully')
    } catch (error: any) {
      toast.error(
        error?.response?.data?.message || error?.response?.data?.detail || 'Failed to submit request'
      )
    } finally {
      setSubmitting(false)
    }
  }

  // Success screen
  if (submitted) {
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="card text-center p-10">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-3">Request Submitted</h1>
          <p className="text-gray-600 mb-6">
            Thank you. Your request for <strong>{submitted.title}</strong> has been received
            and is now under review by the N.O.U. team.
          </p>
          {submitted.request_number && (
            <div className="inline-block bg-primary-50 border border-primary-200 rounded-lg px-4 py-2 mb-6">
              <span className="text-sm text-gray-500">Request number: </span>
              <span className="font-mono font-semibold text-primary-700">{submitted.request_number}</span>
            </div>
          )}
          <p className="text-sm text-gray-500 mb-8">
            N.O.U. will review your requirements and contact you at the email you provided.
            No account was needed to submit this request.
          </p>
          <div className="flex justify-center gap-4">
            <Link to="/" className="btn-secondary">
              Back to Home
            </Link>
            <Link to="/products" className="btn-primary">
              Browse Software
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          What can we do for you?
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Request software, a Wi-Fi or CCTV installation, consultancy or IT support.
          Our team reviews your requirements, checks feasibility and sends you a
          quotation. No account or registration required.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="card space-y-6">
        {/* Service type cards */}
        <div>
          <label className="label text-base">1. Choose a service</label>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {SERVICES.map((service) => {
              const active = serviceType === service.value
              return (
                <button
                  type="button"
                  key={service.value}
                  onClick={() => selectService(service.value)}
                  className={`text-left rounded-xl border-2 p-4 transition-all duration-150 ${
                    active
                      ? 'border-primary-600 bg-primary-50 shadow-sm ring-2 ring-primary-100'
                      : 'border-gray-200 bg-white hover:border-primary-300 hover:shadow-sm'
                  }`}
                >
                  <div
                    className={`w-12 h-12 rounded-lg flex items-center justify-center mb-3 transition-colors ${
                      active ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {service.icon}
                  </div>
                  <p className="font-semibold text-gray-900 text-sm mb-0.5">{service.label}</p>
                  <p className="text-xs text-gray-500 leading-relaxed">{service.tagline}</p>
                </button>
              )
            })}
          </div>
        </div>

        {/* Contact details */}
        <div className="grid sm:grid-cols-2 gap-5">
          <div>
            <label className="label">Your Full Name</label>
            <input
              type="text"
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              required
              minLength={3}
              className="input"
              placeholder="e.g. Jane Wanjiku"
            />
          </div>
          <div>
            <label className="label">Email Address</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              className="input"
              placeholder="you@example.com"
            />
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-5">
          <div>
            <label className="label">
              Phone Number <span className="text-gray-400">(optional)</span>
            </label>
            <input
              type="tel"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              className="input"
              placeholder="e.g. 07XX XXX XXX"
            />
          </div>
          <div>
            <label className="label">Category</label>
            <select name="category" value={form.category} onChange={handleChange} required className="input">
              <option value="">Select a category</option>
              {(CATEGORIES_BY_SERVICE[serviceType] || CATEGORIES_BY_SERVICE.other).map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Location for physical services */}
        {PHYSICAL_SERVICES.has(serviceType) && (
          <div>
            <label className="label">
              Site / Location <span className="text-gray-400">(where the work happens)</span>
            </label>
            <input
              type="text"
              name="location"
              value={form.location}
              onChange={handleChange}
              className="input"
              placeholder="e.g. Riverside Drive, Kisumu"
            />
            <p className="text-xs text-gray-500 mt-1">
              A technician may visit this address to assess the site before quoting.
            </p>
          </div>
        )}

        <div>
          <label className="label">
            {serviceType === 'software_development'
              ? 'Project / Product Title'
              : 'Job Title (what you need done)'}
          </label>
          <input
            type="text"
            name="title"
            value={form.title}
            onChange={handleChange}
            required
            minLength={3}
            className="input"
            placeholder={
              serviceType === 'software_development'
                ? 'Name your project'
                : 'e.g. Office Wi-Fi for 25 staff'
            }
          />
        </div>

        <div>
          <label className="label">Description</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            required
            minLength={10}
            rows={5}
            className="input"
            placeholder="Describe what you need in detail - features, number of rooms or users, any equipment, your goals."
          />
        </div>

        <div className="grid sm:grid-cols-2 gap-5">
          <div>
            <label className="label">
              Estimated Budget (USD) <span className="text-gray-400">(optional)</span>
            </label>
            <input
              type="number"
              name="budget"
              value={form.budget}
              onChange={handleChange}
              min={0}
              className="input"
              placeholder="Optional"
            />
          </div>
          <div>
            <label className="label">
              Preferred Date <span className="text-gray-400">(optional)</span>
            </label>
            <input
              type="date"
              name="deadline"
              value={form.deadline}
              onChange={handleChange}
              className="input"
            />
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-500">
          By submitting this request you agree to N.O.U.'s{' '}
          <Link to="/terms" className="text-primary-600 hover:text-primary-700">
            Terms &amp; Conditions
          </Link>{' '}
          and{' '}
          <Link to="/privacy" className="text-primary-600 hover:text-primary-700">
            Privacy Policy
          </Link>
          . No account is created - we simply use your details to contact you about this request.
        </div>

        <div className="flex justify-end pt-2">
          <button type="submit" className="btn-primary" disabled={submitting}>
            {submitting ? 'Submitting...' : `Submit ${SERVICE_LABELS[serviceType] || 'Request'}`}
          </button>
        </div>
      </form>
    </div>
  )
}

export default RequestProjectPage
