import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAppSelector } from '../../hooks/useAppSelector'
import api from '../../services/api'

const AdminDashboard = () => {
  const { user } = useAppSelector((state) => state.auth)
  const [stats, setStats] = useState({
    users: 0,
    products: 0,
    jobs: 0,
    applications: 0,
    open_tickets: 0,
    assessments: 0,
    investor_interests: 0,
    projects: 0,
    nou_lite_orders: 0,
    onboarding_pending: 0,
    payments_collected: 0,
    payments_pending: 0,
    payments_pending_count: 0,
    payments_successful_count: 0,
    project_requests: 0,
    requests_awaiting_deposit: 0,
    requests_quotation_issued: 0,
    support_collected: 0,
    support_pending: 0,
    support_count: 0,
  })
  const [providerStatus, setProviderStatus] = useState<{
    mpesa_configured: boolean
    flutterwave_configured: boolean
    simulation_mode: boolean
  } | null>(null)
  const [visits, setVisits] = useState<{
    today: { visits: number; unique: number }
    totals: { visits: number; unique: number }
    daily: { date: string; visits: number; unique: number }[]
    top_pages: { path: string; count: number }[]
  } | null>(null)
  const [health, setHealth] = useState<{
    status: string
    uptime: string
    uptime_seconds: number
    database: string
    environment: string
    version: string
    python_version: string
    ai_keys_configured: number
    ai_keys_failed_today: number
  } | null>(null)
  const [appsCount, setAppsCount] = useState(0)

  useEffect(() => {
    fetchDashboardStats()
    fetchProviderStatus()
    fetchVisits()
    fetchHealth()
    fetchApps()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      const response = await api.get('/admin/dashboard/stats')
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
    }
  }

  const fetchProviderStatus = async () => {
    try {
      const response = await api.get('/payments/status')
      setProviderStatus(response.data)
    } catch (error) {
      console.error('Error fetching payment provider status:', error)
    }
  }

  const fetchVisits = async () => {
    try {
      const response = await api.get('/admin/analytics/visits')
      setVisits(response.data)
    } catch (error) {
      console.error('Error fetching visit analytics:', error)
    }
  }

  const fetchHealth = async () => {
    try {
      const response = await api.get('/admin/system/status')
      setHealth(response.data)
    } catch (error) {
      console.error('Error fetching system status:', error)
    }
  }

  const fetchApps = async () => {
    try {
      const response = await api.get('/admin/apps')
      setAppsCount((response.data.apps || []).length)
    } catch (error) {
      console.error('Error fetching apps:', error)
    }
  }

  const statCards = [
    {
      title: 'Total Users',
      value: stats.users,
      icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
      link: '/admin/users',
      color: 'bg-blue-500',
    },
    {
      title: 'Products',
      value: stats.products,
      icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
      link: '/admin/products',
      color: 'bg-green-500',
    },
    {
      title: 'Job Listings',
      value: stats.jobs,
      icon: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
      link: '/admin/assessments',
      color: 'bg-purple-500',
    },
    {
      title: 'Applications',
      value: stats.applications,
      icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
      link: '/admin/reports',
      color: 'bg-orange-500',
    },
    {
      title: 'Open Tickets',
      value: stats.open_tickets,
      icon: 'M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z',
      link: '/admin/users',
      color: 'bg-red-500',
    },
    {
      title: 'Assessments',
      value: stats.assessments,
      icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
      link: '/admin/assessments',
      color: 'bg-indigo-500',
    },
    {
      title: 'Investor Interests',
      value: stats.investor_interests,
      icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      link: '/admin/investors',
      color: 'bg-teal-500',
    },
    {
      title: 'Onboarding Pending',
      value: stats.onboarding_pending,
      icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
      link: '/admin/onboarding',
      color: 'bg-amber-500',
    },
    {
      title: 'Company Projects',
      value: stats.projects,
      icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
      link: '/admin/projects',
      color: 'bg-cyan-500',
    },
    {
      title: 'N.O.U Lite Orders',
      value: stats.nou_lite_orders,
      icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
      link: '/admin/nou-lite',
      color: 'bg-fuchsia-500',
    },
    {
      title: 'Site Visits Today',
      value: visits?.today?.visits ?? 0,
      icon: 'M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122',
      link: '/admin/reports',
      color: 'bg-rose-500',
    },
    {
      title: 'Mobile Apps',
      value: appsCount,
      icon: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4',
      link: '/admin/apps',
      color: 'bg-slate-600',
    },
  ]

  const quickActions = [
    {
      title: 'Add Product',
      icon: 'M12 6v6m0 0v6m0-6h6m-6 0H6',
      link: '/admin/products',
      color: 'text-primary-600',
    },
    {
      title: 'Create Job Listing',
      icon: 'M12 6v6m0 0v6m0-6h6m-6 0H6',
      link: '/admin/assessments',
      color: 'text-green-600',
    },
    {
      title: 'View Reports',
      icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      link: '/admin/reports',
      color: 'text-purple-600',
    },
    {
      title: 'Manage Users',
      icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
      link: '/admin/users',
      color: 'text-orange-600',
    },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Admin Dashboard
        </h1>
        <p className="text-gray-600">Welcome back, {user?.firstName}. Here's your system overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {statCards.map((stat) => (
          <Link
            key={stat.title}
            to={stat.link}
            className="card hover:scale-105 transition-transform duration-200"
          >
            <div className="flex items-center">
              <div className={`${stat.color} rounded-xl p-3`}>
                <svg
                  className="w-6 h-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d={stat.icon}
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">{stat.title}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="card mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {quickActions.map((action) => (
            <Link
              key={action.title}
              to={action.link}
              className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg
                className={`w-8 h-8 ${action.color} mr-3`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d={action.icon}
                />
              </svg>
              <span className="font-medium text-gray-900">{action.title}</span>
            </Link>
          ))}
        </div>
      </div>

      {/* Payments Summary */}
      <div className="card mb-8">
        <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
          <h2 className="text-lg font-semibold text-gray-900">Payments Summary</h2>
          <div className="flex items-center gap-2 flex-wrap">
            {providerStatus && (
              <span
                className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${
                  providerStatus.simulation_mode
                    ? 'bg-amber-50 text-amber-700 border border-amber-200'
                    : 'bg-green-50 text-green-700 border border-green-200'
                }`}
                title="M-Pesa Daraja + Flutterwave provider configuration"
              >
                <span
                  className={`w-1.5 h-1.5 rounded-full ${
                    providerStatus.simulation_mode ? 'bg-amber-500' : 'bg-green-500'
                  }`}
                />
                {providerStatus.simulation_mode
                  ? 'Simulation mode (configure MPESA_* / FLUTTERWAVE_* in backend/.env)'
                  : `M-Pesa ${providerStatus.mpesa_configured ? 'ready' : 'off'} · Cards ${providerStatus.flutterwave_configured ? 'ready' : 'off'}`}
              </span>
            )}
            <Link to="/admin/project-requests" className="text-sm text-primary-600 hover:text-primary-700">
              Manage requests
            </Link>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="bg-green-50 rounded-lg p-4">
            <p className="text-xs font-medium text-gray-500 mb-1">Total Collected</p>
            <p className="text-xl font-bold text-gray-900">
              {Number(stats.payments_collected || 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}
            </p>
            <p className="text-xs text-gray-400">KSh</p>
          </div>
          <div className="bg-amber-50 rounded-lg p-4">
            <p className="text-xs font-medium text-gray-500 mb-1">Awaiting Verification</p>
            <p className="text-xl font-bold text-gray-900">
              {Number(stats.payments_pending || 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}
            </p>
            <p className="text-xs text-gray-400">
              KSh · {stats.payments_pending_count} payment{stats.payments_pending_count === 1 ? '' : 's'}
            </p>
          </div>
          <div className="bg-primary-50 rounded-lg p-4">
            <p className="text-xs font-medium text-gray-500 mb-1">Successful Payments</p>
            <p className="text-xl font-bold text-gray-900">{stats.payments_successful_count}</p>
            <p className="text-xs text-gray-400">receipts issued</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs font-medium text-gray-500 mb-1">Project Requests</p>
            <p className="text-xl font-bold text-gray-900">{stats.project_requests}</p>
            <p className="text-xs text-gray-400">total</p>
          </div>
          <div className="bg-amber-50 rounded-lg p-4">
            <p className="text-xs font-medium text-gray-500 mb-1">Awaiting Deposit</p>
            <p className="text-xl font-bold text-gray-900">{stats.requests_awaiting_deposit}</p>
            <p className="text-xs text-gray-400">quotations accepted</p>
          </div>
          <div className="bg-primary-50 rounded-lg p-4">
            <p className="text-xs font-medium text-gray-500 mb-1">Quotation Issued</p>
            <p className="text-xl font-bold text-gray-900">{stats.requests_quotation_issued}</p>
            <p className="text-xs text-gray-400">awaiting decision</p>
          </div>
        </div>

        {/* Support contributions (footer donations) - separate from project payments */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
            <div>
              <h3 className="font-semibold text-gray-900">Support Contributions</h3>
              <p className="text-xs text-gray-500">Donations received from the public footer Support page.</p>
            </div>
            <Link to="/admin/support-contributions" className="text-sm text-primary-600 hover:text-primary-700">
              View all
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-green-50 rounded-lg p-4">
              <p className="text-xs font-medium text-gray-500 mb-1">Collected</p>
              <p className="text-xl font-bold text-gray-900">
                {Number(stats.support_collected || 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </p>
              <p className="text-xs text-gray-400">KSh</p>
            </div>
            <div className="bg-amber-50 rounded-lg p-4">
              <p className="text-xs font-medium text-gray-500 mb-1">Pending</p>
              <p className="text-xl font-bold text-gray-900">
                {Number(stats.support_pending || 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </p>
              <p className="text-xs text-gray-400">KSh</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-xs font-medium text-gray-500 mb-1">Total Contributions</p>
              <p className="text-xl font-bold text-gray-900">{stats.support_count || 0}</p>
              <p className="text-xs text-gray-400">all time</p>
            </div>
          </div>
        </div>
      </div>

      {/* Site Traffic + System Health */}
      <div className="card mb-8">
        <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
          <h2 className="text-lg font-semibold text-gray-900">Site Traffic &amp; System Health</h2>
          <div className="flex items-center gap-3">
            <Link to="/admin/reports" className="text-sm text-primary-600 hover:text-primary-700">
              Reports
            </Link>
            <Link to="/admin/ai-pool" className="text-sm text-primary-600 hover:text-primary-700">
              AI Key Pool
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Daily visits */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="grid grid-cols-4 gap-3 mb-5">
              <div>
                <p className="text-xs text-gray-500">Today</p>
                <p className="text-xl font-bold text-gray-900">{visits?.today?.visits ?? 0}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Unique today</p>
                <p className="text-xl font-bold text-gray-900">{visits?.today?.unique ?? 0}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">All visits</p>
                <p className="text-xl font-bold text-gray-900">{visits?.totals?.visits ?? 0}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Unique all</p>
                <p className="text-xl font-bold text-gray-900">{visits?.totals?.unique ?? 0}</p>
              </div>
            </div>

            <h3 className="font-medium text-gray-900 mb-3">Last 14 days</h3>
            <div className="flex items-end gap-1 h-24 mb-4">
              {(visits?.daily || []).map((day) => {
                const max = Math.max(1, ...(visits?.daily || []).map((d) => d.visits))
                const h = Math.max(4, Math.round((day.visits / max) * 88))
                return (
                  <div key={day.date} className="flex-1 flex flex-col items-center gap-1" title={`${day.date}: ${day.visits} visits`}>
                    <div
                      className={`w-full rounded-t ${day.visits > 0 ? 'bg-primary-600' : 'bg-gray-200'}`}
                      style={{ height: `${h}px` }}
                    />
                    <span className="text-[9px] text-gray-400">
                      {new Date(day.date + 'T00:00:00').toLocaleDateString(undefined, { day: 'numeric', month: 'short' })}
                    </span>
                  </div>
                )
              })}
            </div>

            <h3 className="font-medium text-gray-900 mb-2">Most viewed pages</h3>
            <div className="space-y-1.5">
              {(visits?.top_pages || []).slice(0, 6).map((p) => (
                <div key={p.path} className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 font-mono text-xs truncate mr-3">{p.path}</span>
                  <span className="font-medium text-gray-900 shrink-0">{p.count}</span>
                </div>
              ))}
              {(visits?.top_pages || []).length === 0 && (
                <p className="text-xs text-gray-500">No visits recorded yet - the counter activates on the next page view.</p>
              )}
            </div>
          </div>

          {/* System health */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-medium text-gray-900">Uptime &amp; internal running</h3>
              <span
                className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${
                  health?.status === 'up'
                    ? 'bg-green-50 text-green-700 border border-green-200'
                    : 'bg-red-50 text-red-700 border border-red-200'
                }`}
              >
                <span className={`w-1.5 h-1.5 rounded-full ${health?.status === 'up' ? 'bg-green-500' : 'bg-red-500'}`} />
                {health?.status === 'up' ? 'All systems up' : 'Degraded'}
              </span>
            </div>
            <div className="space-y-2.5 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">API uptime</span>
                <span className="font-medium text-gray-900">{health?.uptime || '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Database</span>
                <span className={`font-medium ${health?.database === 'ok' ? 'text-green-600' : 'text-red-600'}`}>
                  {health?.database === 'ok' ? 'Connected' : 'Unreachable'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Environment</span>
                <span className="font-medium text-gray-900">{health?.environment || '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">API version</span>
                <span className="font-medium text-gray-900">v{health?.version || '—'} · Python {health?.python_version || '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">AI keys configured</span>
                <span className="font-medium text-gray-900">{health?.ai_keys_configured ?? 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">AI keys failed today</span>
                <span className={`font-medium ${health?.ai_keys_failed_today ? 'text-red-600' : 'text-green-600'}`}>
                  {health?.ai_keys_failed_today ?? 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Results email worker</span>
                <span className="font-medium text-gray-900">Running (scheduled)</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Project Request Pipeline */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">System Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-2">Request Pipeline</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">New requests</span>
                <span className="font-medium">{stats.project_requests}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Quotations awaiting customer decision</span>
                <span className="font-medium">{stats.requests_quotation_issued}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Deposits awaiting verification</span>
                <span className="font-medium">{stats.payments_pending_count}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Projects awaiting deposit</span>
                <span className="font-medium">{stats.requests_awaiting_deposit}</span>
              </div>
            </div>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-2">Platform Overview</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Active job listings</span>
                <span className="font-medium">{stats.jobs}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Job applications</span>
                <span className="font-medium">{stats.applications}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Company projects</span>
                <span className="font-medium">{stats.projects}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">N.O.U Lite orders</span>
                <span className="font-medium">{stats.nou_lite_orders}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard