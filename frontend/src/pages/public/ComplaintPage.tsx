import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useRouteMemory } from '../../utils/routeMemory'
import api from '../../services/api'
import toast from 'react-hot-toast'

const COMPLAINT_CATEGORIES = [
  'General',
  'Product / Software',
  'Assessment / Careers',
  'Project / Development',
  'Payment / Billing',
  'Customer Service',
  'Website',
  'Other',
]

const ComplaintPage = () => {
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState<{ subject: string; email: string } | null>(null)
  const [form, setForm] = useRouteMemory('form', {
    full_name: '',
    email: '',
    phone: '',
    subject: '',
    category: 'General',
    message: '',
  })

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.full_name.trim() || form.full_name.trim().length < 2) {
      toast.error('Please enter your full name')
      return
    }
    if (!form.subject.trim() || form.subject.trim().length < 3) {
      toast.error('Please enter a short subject for your complaint')
      return
    }
    if (!form.message.trim() || form.message.trim().length < 10) {
      toast.error('Please describe your complaint in a little more detail (at least 10 characters)')
      return
    }
    try {
      setLoading(true)
      const response = await api.post('/complaints', {
        full_name: form.full_name,
        email: form.email,
        phone: form.phone || undefined,
        subject: form.subject,
        category: form.category,
        message: form.message,
      })
      setSubmitted({
        subject: response.data.complaint?.subject || form.subject,
        email: form.email,
      })
      toast.success('Complaint received')
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to submit. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-50">
      {/* Hero */}
      <div className="bg-gradient-to-br from-primary-700 via-primary-800 to-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 text-sm font-medium tracking-wide mb-6">
            File a Complaint
          </span>
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            We Take Your Feedback Seriously
          </h1>
          <p className="text-lg text-primary-100 max-w-3xl mx-auto">
            If something did not go as expected - a product, an assessment, a
            project or our service - tell us. Your complaint is forwarded directly
            to our administration and we will review it and respond to you.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Complaint form */}
          <div className="card">
            {submitted ? (
              <div className="py-8 text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-5">
                  <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-3">Complaint Received</h2>
                <p className="text-gray-600 mb-2">
                  Your complaint has been forwarded to our administration for review.
                </p>
                <p className="text-sm text-gray-500 mb-6">
                  We will respond to you at <strong>{submitted.email}</strong> once it has been reviewed.
                </p>
                <Link to="/" className="btn-outline">
                  Back to Home
                </Link>
              </div>
            ) : (
              <>
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Submit Your Complaint</h2>
                  <p className="text-gray-600">
                    Provide your contact details so our administration can follow up with you.
                  </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-5">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                      <label htmlFor="full_name" className="label">Full name *</label>
                      <input
                        id="full_name"
                        name="full_name"
                        type="text"
                        value={form.full_name}
                        onChange={handleChange}
                        required
                        className="input"
                        placeholder="e.g. Jane Mwangi"
                      />
                    </div>
                    <div>
                      <label htmlFor="phone" className="label">Phone number</label>
                      <input
                        id="phone"
                        name="phone"
                        type="tel"
                        value={form.phone}
                        onChange={handleChange}
                        className="input"
                        placeholder="e.g. 0712 345 678"
                      />
                    </div>
                  </div>
                  <div>
                    <label htmlFor="email" className="label">Email address *</label>
                    <input
                      id="email"
                      name="email"
                      type="email"
                      value={form.email}
                      onChange={handleChange}
                      required
                      className="input"
                      placeholder="you@example.com"
                    />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                      <label htmlFor="subject" className="label">Subject *</label>
                      <input
                        id="subject"
                        name="subject"
                        type="text"
                        value={form.subject}
                        onChange={handleChange}
                        required
                        className="input"
                        placeholder="e.g. Payment not confirmed"
                      />
                    </div>
                    <div>
                      <label htmlFor="category" className="label">Category</label>
                      <select
                        id="category"
                        name="category"
                        value={form.category}
                        onChange={handleChange}
                        className="input"
                      >
                        {COMPLAINT_CATEGORIES.map((c) => (
                          <option key={c} value={c}>{c}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                  <div>
                    <label htmlFor="message" className="label">Your complaint *</label>
                    <textarea
                      id="message"
                      name="message"
                      value={form.message}
                      onChange={handleChange}
                      required
                      rows={6}
                      className="input"
                      placeholder="Describe what happened, when, and what you would like us to do about it..."
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full btn-primary py-3"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center">
                        <span className="spinner mr-2"></span>
                        Submitting...
                      </span>
                    ) : (
                      'Submit Complaint'
                    )}
                  </button>

                  <p className="text-xs text-gray-500 text-center">
                    Your complaint is forwarded directly to the N.O.U. administration.
                    We will review it and respond to you at the email provided.
                  </p>
                </form>
              </>
            )}
          </div>

          {/* Info */}
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">What happens next?</h3>
              <ol className="space-y-4 text-sm text-gray-600">
                <li className="flex items-start gap-3">
                  <span className="w-7 h-7 bg-primary-600 text-white rounded-full flex items-center justify-center shrink-0 font-semibold text-xs">1</span>
                  Your complaint is forwarded to our administration for review.
                </li>
                <li className="flex items-start gap-3">
                  <span className="w-7 h-7 bg-primary-600 text-white rounded-full flex items-center justify-center shrink-0 font-semibold text-xs">2</span>
                  An administrator reviews the details and investigates the matter.
                </li>
                <li className="flex items-start gap-3">
                  <span className="w-7 h-7 bg-primary-600 text-white rounded-full flex items-center justify-center shrink-0 font-semibold text-xs">3</span>
                  We respond to you at the email address you provided with the outcome.
                </li>
              </ol>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Other ways to reach us</h3>
              <div className="space-y-4 text-sm text-gray-600">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center shrink-0">
                    <svg className="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Email</p>
                    <a href="mailto:noudigitalsystem@gmail.com" className="text-primary-600 hover:text-primary-700">
                      noudigitalsystem@gmail.com
                    </a>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center shrink-0">
                    <svg className="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Call or WhatsApp</p>
                    <p>0796298662</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="card bg-primary-50 border-primary-200">
              <h3 className="text-lg font-semibold text-primary-900 mb-2">Prefer to talk to someone?</h3>
              <p className="text-sm text-primary-800 mb-4">
                Visit our Support page to get help with products, projects and contributions.
              </p>
              <Link to="/support" className="btn-primary text-sm">
                Go to Support
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ComplaintPage
