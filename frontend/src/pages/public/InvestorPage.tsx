import { useState } from 'react'
import { useRouteMemory } from '../../utils/routeMemory'
import api from '../../services/api'
import toast from 'react-hot-toast'

const COUNTRIES = [
  'Kenya', 'United States', 'United Kingdom', 'Canada', 'South Africa',
  'Nigeria', 'Germany', 'France', 'Netherlands', 'Sweden', 'Norway',
  'Switzerland', 'UAE', 'Saudi Arabia', 'India', 'China', 'Singapore',
  'Australia', 'Japan', 'Egypt', 'Ghana', 'Rwanda', 'Uganda', 'Tanzania',
  'Ethiopia', 'Botswana', 'Zambia', 'Other',
]

const InvestorPage = () => {
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  // Route-memory: contact details survive navigating away and coming back.
  const [form, setForm] = useRouteMemory('form', {
    full_name: '',
    email: '',
    phone: '',
    country: '',
    organization: '',
  })

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!form.full_name.trim() || form.full_name.trim().length < 2) {
      toast.error('Please enter your full name')
      return
    }
    if (!form.country) {
      toast.error('Please select your country')
      return
    }

    try {
      setLoading(true)
      await api.post('/investors/interest', {
        full_name: form.full_name,
        email: form.email,
        phone: form.phone || undefined,
        country: form.country,
        organization: form.organization || undefined,
      })
      setSubmitted(true)
      toast.success('Your details have been received!')
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 text-sm font-medium tracking-wide mb-6">
            Investment Opportunities
          </span>
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Partner With Us to Build the Future of Digital Systems
          </h1>
          <p className="text-lg text-primary-100 max-w-3xl mx-auto">
            N.O.U Digital Systems is building a centralized platform for software
            distribution, technical recruitment, and digital services across Africa
            and beyond. We're seeking investors who share our vision.
          </p>
        </div>
      </div>

      {/* Why invest */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          {[
            {
              title: 'Growing Market',
              text: 'A rapidly expanding digital economy with demand for software, assessments, and recruitment tools.',
              icon: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6',
            },
            {
              title: 'Proven Platform',
              text: 'A working product with authentication, career assessments, e-commerce, and admin tools.',
              icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
            },
            {
              title: 'Smart Assessments',
              text: 'Career assessments that grade candidates automatically with detailed feedback.',
              icon: 'M13 10V3L4 14h7v7l9-11h-7z',
            },
          ].map((item) => (
            <div key={item.title} className="card">
              <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-4">
                <svg
                  className="w-6 h-6 text-primary-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.title}</h3>
              <p className="text-gray-600 text-sm">{item.text}</p>
            </div>
          ))}
        </div>

        <div className="max-w-3xl mx-auto">
          {submitted ? (
            <div className="card text-center py-16">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-3">Thank You!</h2>
              <p className="text-gray-600 mb-4 max-w-md mx-auto">
                Your contact details have been received. Our team will contact you
                at <strong>{form.email}</strong> after reviewing your submission.
              </p>
              <button
                onClick={() => {
                  setSubmitted(false)
                  setForm({ full_name: '', email: '', phone: '', country: '', organization: '' })
                }}
                className="btn-primary"
              >
                Submit Another
              </button>
            </div>
          ) : (
            <div className="card">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Share Your Contact Details
                </h2>
                <p className="text-gray-600">
                  Enter your details below and our management team will contact you
                  with more information about investing in N.O.U. Digital Systems.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                  <div>
                    <label htmlFor="phone" className="label">Phone number</label>
                    <input
                      id="phone"
                      name="phone"
                      type="tel"
                      value={form.phone}
                      onChange={handleChange}
                      className="input"
                      placeholder="+254 700 000 000"
                    />
                  </div>
                  <div>
                    <label htmlFor="country" className="label">Country *</label>
                    <select
                      id="country"
                      name="country"
                      value={form.country}
                      onChange={handleChange}
                      required
                      className="input"
                    >
                      <option value="">Select your country</option>
                      {COUNTRIES.map((country) => (
                        <option key={country} value={country}>{country}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label htmlFor="organization" className="label">Organization / Fund (optional)</label>
                  <input
                    id="organization"
                    name="organization"
                    type="text"
                    value={form.organization}
                    onChange={handleChange}
                    className="input"
                    placeholder="Company or investment fund"
                  />
                </div>

                <div className="bg-primary-50 border border-primary-200 rounded-xl p-4">
                  <div className="flex items-start gap-3">
                    <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center shrink-0">
                      <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">What happens next</h3>
                      <p className="text-sm text-gray-600">
                        After you submit your contact details, our management team will review
                        them and contact you directly. There are no joining fees or charges to
                        express interest.
                      </p>
                    </div>
                  </div>
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
                    'Submit My Contact Details'
                  )}
                </button>

                <p className="text-xs text-gray-500 text-center">
                  Your details are kept confidential and will only be reviewed by our management team.
                </p>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default InvestorPage
