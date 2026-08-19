import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAppSelector } from '../../hooks/useAppSelector'
import api from '../../services/api'
import AnnouncementsFeed from '../../components/AnnouncementsFeed'

const CustomerDashboard = () => {
  const { user } = useAppSelector((state) => state.auth)
  const [stats, setStats] = useState({
    downloads: 0,
    tickets: 0,
    projects: 0,
  })
  const [recentTickets, setRecentTickets] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [ticketsRes] = await Promise.all([
        api.get('/support/tickets/me?limit=5'),
      ])
      
      setRecentTickets(ticketsRes.data.tickets || [])
      setStats({
        downloads: 0,
        tickets: ticketsRes.data.pagination?.total || 0,
        projects: 0,
      })
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Downloads',
      value: stats.downloads,
      icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
      link: '/customer/downloads',
      color: 'bg-blue-500',
    },
    {
      title: 'Support Tickets',
      value: stats.tickets,
      icon: 'M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z',
      link: '/customer/support',
      color: 'bg-green-500',
    },
    {
      title: 'Project Requests',
      value: stats.projects,
      icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
      link: '/customer/projects',
      color: 'bg-purple-500',
    },
  ]

  const priorityColors: Record<string, string> = {
    low: 'badge-gray',
    medium: 'badge-warning',
    high: 'badge-danger',
    urgent: 'badge-danger',
  }

  const statusColors: Record<string, string> = {
    open: 'badge-primary',
    in_progress: 'badge-warning',
    resolved: 'badge-success',
    closed: 'badge-gray',
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.firstName}
        </h1>
        <p className="text-gray-600">Here's what's happening with your account.</p>
      </div>

      {/* Company announcements / alerts (maintenance, new services) */}
      <AnnouncementsFeed title="Company Alerts &amp; News" />

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
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
          <Link
            to="/customer/downloads"
            className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <svg className="w-8 h-8 text-primary-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span className="font-medium text-gray-900">Browse Products</span>
          </Link>
          <Link
            to="/customer/support"
            className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <svg className="w-8 h-8 text-green-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span className="font-medium text-gray-900">New Ticket</span>
          </Link>
          <Link
            to="/customer/projects"
            className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <svg className="w-8 h-8 text-purple-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <span className="font-medium text-gray-900">Request Project</span>
          </Link>
          <Link
            to="/products"
            className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <svg className="w-8 h-8 text-orange-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span className="font-medium text-gray-900">Search Products</span>
          </Link>
        </div>
      </div>

      {/* Recent Tickets */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Recent Support Tickets</h2>
          <Link to="/customer/support" className="text-sm text-primary-600 hover:text-primary-700">
            View all
          </Link>
        </div>
        
        {loading ? (
          <div className="text-center py-8">
            <div className="spinner mx-auto"></div>
          </div>
        ) : recentTickets.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600">No support tickets yet</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {recentTickets.map((ticket: any) => (
                  <tr key={ticket.id}>
                    <td className="font-medium">{ticket.subject}</td>
                    <td>
                      <span className={priorityColors[ticket.priority] || 'badge-gray'}>
                        {ticket.priority}
                      </span>
                    </td>
                    <td>
                      <span className={statusColors[ticket.status] || 'badge-gray'}>
                        {ticket.status}
                      </span>
                    </td>
                    <td className="text-gray-500">
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default CustomerDashboard