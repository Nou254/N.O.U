import { useState } from 'react'
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { useAppSelector, useAppDispatch } from '../hooks/useAppSelector'
import { logout, setUsername } from '../store/authSlice'
import toast from 'react-hot-toast'

const DeveloperLayout = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { user } = useAppSelector((state) => state.auth)
  const [handleInput, setHandleInput] = useState('')
  const [savingHandle, setSavingHandle] = useState(false)

  const handleLogout = () => {
    dispatch(logout())
    navigate('/')
  }

  const handleSaveUsername = async () => {
    const value = handleInput.trim().replace(/^@/, '')
    if (!value) {
      toast.error('Enter a handle (e.g. henrydatabase)')
      return
    }
    setSavingHandle(true)
    try {
      const res = await dispatch(setUsername(value)).unwrap()
      toast.success(res?.message || 'Handle saved')
    } catch (err) {
      toast.error(err as string)
    } finally {
      setSavingHandle(false)
      setHandleInput('')
    }
  }

  const navigation = [
    { name: 'Projects', href: '/portal', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
    { name: 'My Department', href: '/portal/department', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
    { name: 'Opportunities', href: '/portal/opportunities', icon: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
    { name: 'Community', href: '/portal/community', icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' },
    { name: 'Change password', href: '/change-password', icon: 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-4 border-b border-gray-200">
            <Link to="/portal" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-800 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">N</span>
              </div>
              <div>
                <span className="text-lg font-bold text-gray-900">Developer</span>
                <p className="text-xs text-gray-500">Projects Portal</p>
              </div>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                  location.pathname === item.href
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <svg
                  className="mr-3 h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d={item.icon}
                  />
                </svg>
                {item.name}
              </Link>
            ))}
          </nav>

          {/* User info */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center justify-between">                <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <span className="text-primary-700 font-medium">
                    {user?.firstName?.charAt(0)}{user?.lastName?.charAt(0)}
                  </span>
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {user?.firstName} {user?.lastName}
                  </p>
                  <p className="text-xs text-gray-500 truncate">
                    {user?.username ? `@${user.username}` : 'Developer'}
                  </p>
                </div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="mt-3 w-full btn-outline text-sm"
            >
              Sign out
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="main-content">
        {/* Handle setup banner - shown until the developer creates their @handle */}
        {!user?.username && (
          <div className="bg-gradient-to-r from-primary-700 to-primary-900 text-white">
            <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col sm:flex-row sm:items-center gap-3">
              <div className="flex-1 min-w-0">
                <p className="font-semibold">Create your company handle</p>
                <p className="text-sm text-primary-100">
                  Choose a handle (like <span className="font-mono">@henrydatabase</span>) so
                  the team can interact with you in the community and on projects.
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <span className="text-primary-100 font-mono">@</span>
                <input
                  value={handleInput}
                  onChange={(e) => setHandleInput(e.target.value.replace(/\s/g, ''))}
                  maxLength={30}
                  placeholder="henrydatabase"
                  className="rounded-lg px-3 py-1.5 text-sm text-gray-900 bg-white/95 outline-none focus:ring-2 focus:ring-primary-400 w-44"
                />
                <button
                  onClick={handleSaveUsername}
                  disabled={savingHandle}
                  className="btn bg-primary-600 text-white hover:bg-primary-700 text-sm px-4 py-1.5 disabled:opacity-50"
                >
                  {savingHandle ? 'Saving...' : 'Save'}
                </button>
              </div>
            </div>
          </div>
        )}
        <Outlet />
      </div>
    </div>
  )
}

export default DeveloperLayout
