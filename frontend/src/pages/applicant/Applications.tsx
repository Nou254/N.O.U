import { useEffect, useState } from 'react'
import api from '../../services/api'

interface Application {
  id: string
  job: {
    title: string
    department: string
  }
  status: string
  submitted_at: string
}

const ApplicantApplications = () => {
  const [applications, setApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const response = await api.get('/employment/applications/me')
      setApplications(response.data.applications)
    } catch (error) {
      console.error('Error fetching applications:', error)
    } finally {
      setLoading(false)
    }
  }

  const statusColors: Record<string, string> = {
    submitted: 'badge-primary',
    under_review: 'badge-warning',
    shortlisted: 'badge-success',
    interview_scheduled: 'badge-success',
    offered: 'badge-success',
    rejected: 'badge-danger',
    withdrawn: 'badge-gray',
  }

  const statusLabels: Record<string, string> = {
    submitted: 'Submitted',
    under_review: 'Under Review',
    shortlisted: 'Shortlisted',
    interview_scheduled: 'Interview Scheduled',
    offered: 'Offered',
    rejected: 'Rejected',
    withdrawn: 'Withdrawn',
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">My Applications</h1>
        <p className="text-gray-600">Track the status of your job applications.</p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading applications...</p>
        </div>
      ) : applications.length === 0 ? (
        <div className="card text-center py-12">
          <svg
            className="w-16 h-16 text-gray-400 mx-auto mb-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No applications yet</h3>
          <p className="text-gray-600 mb-4">Start applying for positions to see them here.</p>
          <a href="/careers" className="btn-primary">
            Browse Positions
          </a>
        </div>
      ) : (
        <div className="space-y-4">
          {applications.map((application) => (
            <div
              key={application.id}
              className="card"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {application.job?.title || 'Position'}
                  </h3>
                  {application.job?.department && (
                    <p className="text-sm text-gray-500 mt-1">
                      Department: {application.job.department}
                    </p>
                  )}
                  <p className="text-sm text-gray-500 mt-1">
                    Applied: {new Date(application.submitted_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <span className={statusColors[application.status] || 'badge-gray'}>
                    {statusLabels[application.status] || application.status}
                  </span>
                </div>
              </div>
              
              {/* Progress indicator */}
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Application Progress</span>
                </div>
                <div className="mt-2 flex items-center space-x-2">
                  {['submitted', 'under_review', 'shortlisted', 'interview_scheduled', 'offered'].map((step, index) => (
                    <div
                      key={step}
                      className={`flex-1 h-2 rounded-full ${
                        getStepIndex(application.status) >= index
                          ? 'bg-primary-500'
                          : 'bg-gray-200'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function getStepIndex(status: string): number {
  const steps = ['submitted', 'under_review', 'shortlisted', 'interview_scheduled', 'offered']
  return steps.indexOf(status)
}

export default ApplicantApplications