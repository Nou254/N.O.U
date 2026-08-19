import { useState } from 'react'
import { useRouteMemory } from '../../utils/routeMemory'
import api from '../../services/api'
import toast from 'react-hot-toast'

const SUPPORT_NUMBER = '0796298662'

interface PledgeResult {
  message: string
  payment: { id: number; amount: number; currency: string; status: string; method: string }
}

const SupportPage = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PledgeResult | null>(null)
  const [form, setForm] = useRouteMemory('form', {
    full_name: '',
    phone: '',
    amount: '',
    reference: '',
    message: '',
  })

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const copyNumber = async () => {
    try {
      await navigator.clipboard.writeText(SUPPORT_NUMBER)
      toast.success('Number copied - paste it into M-Pesa')
    } catch {
      toast.error(`Please note the number: ${SUPPORT_NUMBER}`)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.full_name.trim() || form.full_name.trim().length < 2) {
      toast.error('Please enter your full name')
      return
    }
    if (!form.phone.trim()) {
      toast.error('Please enter your phone number so we can confirm your contribution')
      return
    }

    try {
      setLoading(true)
      setResult(null)
      const amount = form.amount ? Number(form.amount) : undefined
      const response = await api.post('/payments/support/pledge', {
        full_name: form.full_name,
        phone: form.phone,
        amount,
        reference: form.reference || undefined,
        message: form.message || undefined,
      })
      setResult(response.data)
      toast.success('Thank you! We will confirm your contribution')
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
            Support N.O.U
          </span>
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Your Support Keeps Us Building
          </h1>
          <p className="text-lg text-primary-100 max-w-3xl mx-auto">
            N.O.U Digital Systems is an independent company building software,
            technical recruitment and digital services across Africa. Your
            contribution - however small - helps us cover hosting, tools and
            infrastructure so we can keep serving our customers and developers.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* How to support */}
          <div className="card">
            {result ? (
              <div className="py-8 text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-5">
                  <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-3">Thank You!</h2>
                <p className="text-gray-600 mb-2">{result.message}</p>
                <p className="text-sm text-gray-500 mb-6">
                  Our team will confirm your contribution shortly. If you have any
                  questions, call or WhatsApp us on <b>{SUPPORT_NUMBER}</b>.
                </p>
                <button onClick={() => setResult(null)} className="btn-outline">
                  Make another contribution
                </button>
              </div>
            ) : (
              <>
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Forward Your Contribution
                  </h2>
                  <p className="text-gray-600">
                    Send your contribution via M-Pesa to the number below, then notify
                    us with the form so we can confirm receipt.
                  </p>
                </div>

                {/* M-Pesa number */}
                <div className="bg-primary-50 border-2 border-dashed border-primary-300 rounded-2xl p-6 text-center mb-8">
                  <p className="text-sm font-medium text-gray-600 mb-1">M-Pesa Paybill / Till Number</p>
                  <p className="text-4xl md:text-5xl font-bold text-primary-800 tracking-wider mb-4">
                    {SUPPORT_NUMBER}
                  </p>
                  <button onClick={copyNumber} className="btn-primary text-sm">
                    Copy number
                  </button>
                </div>

                <ol className="space-y-3 mb-8 text-sm text-gray-600">
                  <li className="flex items-start gap-3">
                    <span className="w-7 h-7 bg-primary-600 text-white rounded-full flex items-center justify-center shrink-0 font-semibold text-xs">1</span>
                    Open M-Pesa and send your contribution to <b>{SUPPORT_NUMBER}</b>.
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-7 h-7 bg-primary-600 text-white rounded-full flex items-center justify-center shrink-0 font-semibold text-xs">2</span>
                    Fill in the form below with your details and the M-Pesa confirmation code.
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-7 h-7 bg-primary-600 text-white rounded-full flex items-center justify-center shrink-0 font-semibold text-xs">3</span>
                    Our team confirms your contribution and thanks you personally.
                  </li>
                </ol>

                <form onSubmit={handleSubmit} className="space-y-5">
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
                    <label htmlFor="phone" className="label">Your phone number *</label>
                    <input
                      id="phone"
                      name="phone"
                      type="tel"
                      value={form.phone}
                      onChange={handleChange}
                      required
                      className="input"
                      placeholder="e.g. 0712 345 678"
                    />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                      <label htmlFor="amount" className="label">Amount (KSh) - optional</label>
                      <input
                        id="amount"
                        name="amount"
                        type="number"
                        min={1}
                        step="any"
                        value={form.amount}
                        onChange={handleChange}
                        className="input"
                        placeholder="e.g. 1000"
                      />
                    </div>
                    <div>
                      <label htmlFor="reference" className="label">M-Pesa confirmation code</label>
                      <input
                        id="reference"
                        name="reference"
                        type="text"
                        value={form.reference}
                        onChange={handleChange}
                        className="input"
                        placeholder="e.g. QWE3R4T5"
                      />
                    </div>
                  </div>
                  <div>
                    <label htmlFor="message" className="label">Message (optional)</label>
                    <textarea
                      id="message"
                      name="message"
                      value={form.message}
                      onChange={handleChange}
                      rows={3}
                      className="input"
                      placeholder="Anything you would like to tell us..."
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
                      'Notify Us of My Contribution'
                    )}
                  </button>

                  <p className="text-xs text-gray-500 text-center">
                    Contributions are voluntary and support the running of N.O.U Digital Systems.
                  </p>
                </form>
              </>
            )}
          </div>

          {/* Contact / info */}
          <div className="space-y-6">
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
                    <p>{SUPPORT_NUMBER}</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center shrink-0">
                    <svg className="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Location</p>
                    <p>Kisumu, Kenya</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Where your contribution goes</h3>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <svg className="w-5 h-5 text-green-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Server hosting, bandwidth and backups for our platform and customer projects.
                </li>
                <li className="flex items-start gap-2">
                  <svg className="w-5 h-5 text-green-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Developer tools, licences and testing infrastructure.
                </li>
                <li className="flex items-start gap-2">
                  <svg className="w-5 h-5 text-green-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Customer support and community initiatives.
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SupportPage
