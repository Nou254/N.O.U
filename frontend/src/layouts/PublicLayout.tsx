import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAppSelector } from '../hooks/useAppSelector'
import NouLiteWidget from '../components/NouLiteWidget'
import { ScrollMemory } from '../utils/routeMemory'

// Auth paths that should lock the page — no nav header shown.
const AUTH_PATHS = ['/login', '/register', '/forgot-password']

const PublicLayout = () => {
  const location = useLocation()
  const { isAuthenticated, user } = useAppSelector((state) => state.auth)

  const isAuthPage = AUTH_PATHS.includes(location.pathname)

  const getDashboardLink = () => {
    if (!user) return '/login'
    switch (user.role) {
      case 'admin':
        return '/admin'
      case 'customer':
        return '/customer'
      case 'applicant':
        return '/applicant'
      case 'developer':
        return '/portal'
      case 'investor':
        return '/investor'
      default:
        return '/login'
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Remember scroll position per page so visitors return where they left off */}
      <ScrollMemory />
      {/* Header — hidden on auth pages (login/register/forgot-password) to lock navigation */}
      {!isAuthPage && (
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-800 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">N</span>
              </div>
              <span className="text-xl font-bold text-gray-900">N.O.U Digital</span>
            </Link>

            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link
                to="/"
                className={`text-sm font-medium transition-colors ${
                  location.pathname === '/'
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Home
              </Link>
              <Link
                to="/request-project"
                className={`text-sm font-medium transition-colors ${
                  location.pathname === '/request-project'
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Request a Project
              </Link>
              <Link
                to="/careers"
                className={`text-sm font-medium transition-colors ${
                  location.pathname === '/careers'
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Careers
              </Link>
              <Link
                to="/apps"
                className={`text-sm font-medium transition-colors ${
                  location.pathname.startsWith('/apps')
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Apps
              </Link>
              <Link
                to="/support"
                className={`text-sm font-medium transition-colors ${
                  location.pathname === '/support'
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Support Us
              </Link>
            </nav>

            {/* Auth buttons */}
            <div className="flex items-center space-x-4">
              <Link
                to="/settings"
                title="Settings"
                aria-label="Settings"
                className="w-9 h-9 flex items-center justify-center rounded-lg text-gray-500 hover:text-primary-600 hover:bg-gray-100 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </Link>
              {isAuthenticated ? (
                <Link
                  to={getDashboardLink()}
                  className="btn-primary"
                >
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="text-sm font-medium text-gray-600 hover:text-gray-900"
                  >
                    Sign in
                  </Link>
                  <Link
                    to="/register"
                    className="btn-primary"
                  >
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </header>
      )}

      {/* Main content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* N.O.U Lite floating assistant */}
      <NouLiteWidget />

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Company */}
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">N</span>
                </div>
                <span className="text-xl font-bold">N.O.U Digital</span>
              </div>
              <p className="text-gray-400 text-sm">
                Centralized web platform for customer interaction, software distribution, and competency-based recruitment.
              </p>
            </div>

            {/* Apps & Downloads */}
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">Apps</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/apps" className="text-gray-400 hover:text-white text-sm">
                    Mobile Apps &amp; Downloads
                  </Link>
                </li>
                <li>
                  <Link to="/products" className="text-gray-400 hover:text-white text-sm">
                    Software &amp; Tools
                  </Link>
                </li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">Company</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/" className="text-gray-400 hover:text-white text-sm">
                    About Us
                  </Link>
                </li>
                <li>
                  <Link to="/careers" className="text-gray-400 hover:text-white text-sm">
                    Careers
                  </Link>
                </li>
                <li>
                  <Link to="/investors" className="text-gray-400 hover:text-white text-sm">
                    Investors
                  </Link>
                </li>
                <li>
                  <Link to="/community" className="text-gray-400 hover:text-white text-sm">
                    Community
                  </Link>
                </li>
                <li>
                  <Link to="/" className="text-gray-400 hover:text-white text-sm">
                    Contact
                  </Link>
                </li>
              </ul>
            </div>

            {/* Legal */}
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">Legal</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/privacy" className="text-gray-400 hover:text-white text-sm">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link to="/terms" className="text-gray-400 hover:text-white text-sm">
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>

            {/* Support & Complaints */}
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">Support</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/support" className="text-gray-400 hover:text-white text-sm">
                    Support Us
                  </Link>
                </li>
                <li>
                  <Link to="/support" className="text-gray-400 hover:text-white text-sm">
                    Make a Contribution
                  </Link>
                </li>
                <li>
                  <Link to="/complaints" className="text-gray-400 hover:text-white text-sm">
                    File a Complaint
                  </Link>
                </li>
                <li>
                  <Link to="/support" className="text-gray-400 hover:text-white text-sm">
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center">
            <p className="text-gray-400 text-sm">
              &copy; {new Date().getFullYear()} N.O.U Digital Systems. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default PublicLayout