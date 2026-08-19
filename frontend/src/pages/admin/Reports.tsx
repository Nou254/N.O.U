import { useEffect, useState } from 'react'
import api from '../../services/api'

const AdminReports = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalProducts: 0,
    totalDownloads: 0,
    totalApplications: 0,
    totalAssessments: 0,
    averageScore: 0,
  })
  useEffect(() => {
    fetchReportData()
  }, [])

  const fetchReportData = async () => {
    try {
      const response = await api.get('/admin/dashboard/stats')
      setStats({
        totalUsers: response.data.users || 0,
        totalProducts: response.data.products || 0,
        totalDownloads: 0,
        totalApplications: response.data.applications || 0,
        totalAssessments: response.data.assessments || 0,
        averageScore: 0,
      })
    } catch (error) {
      console.error('Error fetching report data:', error)
    }
  }

  const reportCards = [
    {
      title: 'User Growth',
      value: stats.totalUsers,
      change: '+12%',
      positive: true,
      icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
    },
    {
      title: 'Total Downloads',
      value: stats.totalDownloads,
      change: '+8%',
      positive: true,
      icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
    },
    {
      title: 'Job Applications',
      value: stats.totalApplications,
      change: '+15%',
      positive: true,
      icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
    },
    {
      title: 'Assessment Average',
      value: `${stats.averageScore}%`,
      change: '+5%',
      positive: true,
      icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Reports & Analytics</h1>
        <p className="text-gray-600">View system performance and usage statistics.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {reportCards.map((card) => (
          <div key={card.title} className="card">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-primary-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d={card.icon}
                  />
                </svg>
              </div>
              <span
                className={`text-sm font-medium ${
                  card.positive ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {card.change}
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{card.value}</p>
            <p className="text-sm text-gray-600 mt-1">{card.title}</p>
          </div>
        ))}
      </div>

      {/* Charts placeholder */}
      <div className="grid lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">User Registrations</h3>
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <p className="text-gray-500">Chart placeholder - User growth over time</p>
          </div>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Product Downloads</h3>
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <p className="text-gray-500">Chart placeholder - Download statistics</p>
          </div>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Assessment Performance</h3>
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <p className="text-gray-500">Chart placeholder - Score distribution</p>
          </div>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Application Status</h3>
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <p className="text-gray-500">Chart placeholder - Application pipeline</p>
          </div>
        </div>
      </div>

      {/* Export Section */}
      <div className="card mt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Export Data</h3>
        <div className="flex flex-wrap gap-4">
          <button className="btn-secondary">
            <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export Users (CSV)
          </button>
          <button className="btn-secondary">
            <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export Applications (CSV)
          </button>
          <button className="btn-secondary">
            <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export Assessment Results (CSV)
          </button>
        </div>
      </div>
    </div>
  )
}

export default AdminReports