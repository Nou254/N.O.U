import { Link } from 'react-router-dom'

const SERVICES = [
  { title: 'Software Development', description: 'Custom software engineered to your exact requirements.', icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4' },
  { title: 'Web Development', description: 'Fast, secure and scalable websites and web applications.', icon: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
  { title: 'Mobile Applications', description: 'Android and cross-platform mobile apps that perform.', icon: 'M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z' },
  { title: 'PWA Development', description: 'Installable web apps with offline capability and app-like experience.', icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
  { title: 'Database Design', description: 'Robust database architecture and data management solutions.', icon: 'M4 7v10c0 1.657 3.582 3 8 3s8-1.343 8-3V7M4 7c0 1.657 3.582 3 8 3s8-1.343 8-3M4 7c0-1.657 3.582-3 8-3s8 1.343 8 3' },
  { title: 'Wi-Fi Installation', description: 'Home, office and campus wireless networks designed and installed.', icon: 'M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0' },
  { title: 'CCTV Installation', description: 'Security camera systems with remote viewing and recording.', icon: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z' },
  { title: 'Consultancy', description: 'Digital strategy, software advice and business technology guidance.', icon: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z' },
  { title: 'System Integration', description: 'Connect your systems and data into one seamless operation.', icon: 'M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z' },
  { title: 'Maintenance & Support', description: 'Ongoing system maintenance and dependable technical support.', icon: 'M19 14l-7 7-7-7m14 0l-7-7-7 7' },
]

const VALUES = [
  { title: 'Innovation', description: 'We build modern, forward-thinking technology solutions.' },
  { title: 'Quality', description: 'Every product and service is delivered to a high standard.' },
  { title: 'Integrity', description: 'We operate honestly, transparently and reliably.' },
]

const HomePage = () => {
  return (
    <div>
      {/* Company banner - full width of the screen, ~25% of the screen height */}
      <section className="relative w-full min-h-[25vh] flex items-center bg-gradient-to-br from-primary-900 via-primary-800 to-primary-950 text-white overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="relative w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 md:py-14">
          <div className="flex flex-col lg:flex-row lg:items-center gap-8">
            <div className="lg:w-2/3">
              <div className="flex items-center gap-4 mb-4 animate-fade-in">
                <img
                  src="/banner.png"
                  alt="N.O.U Digital Systems"
                  className="w-20 md:w-28 rounded-xl shadow-2xl ring-1 ring-white/20"
                />
                <div>
                  <p className="text-accent-300 font-semibold tracking-widest uppercase text-sm mb-1">
                    Software. Systems. Innovation.
                  </p>
                  <h1 className="text-3xl md:text-5xl font-bold">
                    N.O.U. Digital Systems
                  </h1>
                </div>
              </div>
              <p className="text-base md:text-lg text-gray-200 max-w-3xl leading-relaxed animate-slide-up">
                N.O.U. Digital Systems is a technology company and software development
                organization based in Kisumu, Kenya. We design, build and maintain software,
                web and mobile applications, and complete digital systems for individuals,
                businesses and institutions. From custom development, web and mobile
                applications, PWA and database design, to Wi-Fi, CCTV, consultancy and system
                integration - we deliver practical technology that keeps our customers,
                developers and investors connected through one central digital experience.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 mt-6 animate-slide-up">
                <Link to="/request-project" className="btn bg-white text-primary-800 hover:bg-accent-50 px-8 py-3 text-base">
                  Request a Project
                </Link>
                <Link to="/careers" className="btn border-2 border-white text-white hover:bg-white hover:text-primary-800 px-8 py-3 text-base">
                  Join Our Team
                </Link>
              </div>
            </div>
            <div className="hidden lg:block lg:w-1/3">
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: 'Software Development', value: 'Custom' },
                  { label: 'Location', value: 'Kisumu, Kenya' },
                  { label: 'Services', value: 'Full Stack' },
                  { label: 'Support', value: 'Remote & On-site' },
                ].map((stat) => (
                  <div key={stat.label} className="bg-white/10 backdrop-blur rounded-2xl p-4 text-center border border-white/10">
                    <p className="text-xl font-bold">{stat.value}</p>
                    <p className="text-xs text-gray-300 mt-1">{stat.label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Our Services</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Technology services delivered by N.O.U. Digital Systems.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {SERVICES.map((service) => (
              <div key={service.title} className="card text-center hover:scale-105 transition-transform duration-200">
                <div className="w-14 h-14 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-7 h-7 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={service.icon} />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{service.title}</h3>
                <p className="text-gray-600 text-sm">{service.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Need a custom solution */}
      <section className="py-20 bg-gradient-to-br from-primary-600 via-primary-800 to-primary-950 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Need a Custom Digital Solution?</h2>
          <p className="text-xl text-gray-200 mb-8 max-w-3xl mx-auto">
            Tell N.O.U. what you need. Our team will review your requirements, determine
            technical feasibility, prepare the project documentation and provide a quotation.
          </p>
          <Link to="/request-project" className="btn bg-white text-primary-800 hover:bg-accent-50 px-10 py-3 text-lg">
            Request a Project
          </Link>
        </div>
      </section>

      {/* Careers + Investors + Support */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-3 gap-8">
          <div className="card p-8">
            <div className="w-14 h-14 bg-primary-100 rounded-2xl flex items-center justify-center mb-4">
              <svg className="w-7 h-7 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Careers</h3>
            <p className="text-gray-600 text-sm mb-6">
              Explore all the careers at N.O.U., apply without an account and take an
              assessment tailored to the career you choose.
            </p>
            <Link to="/careers" className="btn-primary text-sm">Apply for Employment</Link>
          </div>
          <div className="card p-8">
            <div className="w-14 h-14 bg-primary-100 rounded-2xl flex items-center justify-center mb-4">
              <svg className="w-7 h-7 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Customers</h3>
            <p className="text-gray-600 text-sm mb-6">
              Request custom software, chat with N.O.U Lite and get dependable
              support from our team. No account needed to get started.
            </p>
            <Link to="/request-project" className="btn-primary text-sm">Request a Project</Link>
          </div>
          <div className="card p-8">
            <div className="w-14 h-14 bg-primary-100 rounded-2xl flex items-center justify-center mb-4">
              <svg className="w-7 h-7 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Investors</h3>
            <p className="text-gray-600 text-sm mb-6">
              Share your contact details with N.O.U. and our team will reach out to you
              about funding opportunities.
            </p>
            <Link to="/investors" className="btn-primary text-sm">Investor Registration</Link>
          </div>
        </div>
      </section>

      {/* About + Contact */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">About N.O.U. Digital Systems</h2>
            <p className="text-gray-600 mb-4">
              N.O.U. Digital Systems is a technology company and software development
              organization based in Kisumu, Kenya. We build software, applications and
              technology solutions for individuals, businesses and institutions.
            </p>
            <p className="text-gray-600 mb-6">
              Our platform combines software development services, technology consultancy,
              employment assessment, and investor participation - all connected through one
              central digital experience.
            </p>
            <div className="grid grid-cols-3 gap-4">
              {VALUES.map((value) => (
                <div key={value.title} className="bg-gray-50 rounded-lg p-4 text-center">
                  <p className="font-semibold text-gray-900">{value.title}</p>
                  <p className="text-xs text-gray-500 mt-1">{value.description}</p>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Contact Us</h2>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center shrink-0">
                  <svg className="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Email</p>
                  <p className="text-gray-600 text-sm">noudigitalsystem@gmail.com</p>
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
                  <p className="text-gray-600 text-sm">079298662</p>
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
                  <p className="text-gray-600 text-sm">Kisumu, Kenya</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center shrink-0">
                  <svg className="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Support the Company</p>
                  <p className="text-gray-600 text-sm">
                    Forward a voluntary contribution via M-Pesa to <b>0796298662</b> to keep
                    N.O.U. building.
                  </p>
                  <Link to="/support" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                    Support us →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
