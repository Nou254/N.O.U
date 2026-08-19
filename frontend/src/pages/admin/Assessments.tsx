import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Assessment {
  id: string
  title: string
  description: string
  duration_minutes: number
  total_questions: number
  passing_score: number
  is_active: boolean
}

const AdminAssessments = () => {
  const [assessments, setAssessments] = useState<Assessment[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddAssessment, setShowAddAssessment] = useState(false)
  const [newAssessment, setNewAssessment] = useState({
    title: '',
    description: '',
    durationMinutes: 60,
    totalQuestions: 50,
    passingScore: 60,
  })

  useEffect(() => {
    fetchAssessments()
  }, [])

  const fetchAssessments = async () => {
    try {
      const response = await api.get('/assessments')
      setAssessments(response.data)
    } catch (error) {
      console.error('Error fetching assessments:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddAssessment = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      await api.post('/admin/assessments', newAssessment)
      toast.success('Assessment created successfully')
      setShowAddAssessment(false)
      setNewAssessment({
        title: '',
        description: '',
        durationMinutes: 60,
        totalQuestions: 50,
        passingScore: 60,
      })
      fetchAssessments()
    } catch (error) {
      toast.error('Failed to create assessment')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Assessment Management</h1>
          <p className="text-gray-600">Create and manage technical assessments.</p>
        </div>
        <button onClick={() => setShowAddAssessment(true)} className="btn-primary">
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Create Assessment
        </button>
      </div>

      {/* Add Assessment Modal */}
      {showAddAssessment && (
        <div className="modal-overlay" onClick={() => setShowAddAssessment(false)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Assessment</h2>
            <form onSubmit={handleAddAssessment} className="space-y-4">
              <div>
                <label className="label">Title</label>
                <input
                  type="text"
                  value={newAssessment.title}
                  onChange={(e) => setNewAssessment({ ...newAssessment, title: e.target.value })}
                  required
                  className="input"
                />
              </div>
              <div>
                <label className="label">Description</label>
                <textarea
                  value={newAssessment.description}
                  onChange={(e) => setNewAssessment({ ...newAssessment, description: e.target.value })}
                  rows={3}
                  className="input"
                />
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="label">Duration (min)</label>
                  <input
                    type="number"
                    value={newAssessment.durationMinutes}
                    onChange={(e) => setNewAssessment({ ...newAssessment, durationMinutes: parseInt(e.target.value) })}
                    className="input"
                  />
                </div>
                <div>
                  <label className="label">Questions</label>
                  <input
                    type="number"
                    value={newAssessment.totalQuestions}
                    onChange={(e) => setNewAssessment({ ...newAssessment, totalQuestions: parseInt(e.target.value) })}
                    className="input"
                  />
                </div>
                <div>
                  <label className="label">Pass %</label>
                  <input
                    type="number"
                    value={newAssessment.passingScore}
                    onChange={(e) => setNewAssessment({ ...newAssessment, passingScore: parseInt(e.target.value) })}
                    className="input"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-3 pt-4">
                <button type="button" onClick={() => setShowAddAssessment(false)} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Assessments Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <div className="col-span-full text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : assessments.length === 0 ? (
          <div className="col-span-full card text-center py-12">
            <p className="text-gray-600">No assessments found</p>
          </div>
        ) : (
          assessments.map((assessment: any) => (
            <div key={assessment.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{assessment.title}</h3>
                <span className={assessment.is_active ? 'badge-success' : 'badge-gray'}>
                  {assessment.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{assessment.description}</p>
              <div className="grid grid-cols-3 gap-4 text-center py-4 border-t border-gray-200">
                <div>
                  <p className="text-lg font-bold text-gray-900">{assessment.duration_minutes}</p>
                  <p className="text-xs text-gray-500">Minutes</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-gray-900">{assessment.total_questions}</p>
                  <p className="text-xs text-gray-500">Questions</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-gray-900">{assessment.passing_score}%</p>
                  <p className="text-xs text-gray-500">Pass Score</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default AdminAssessments