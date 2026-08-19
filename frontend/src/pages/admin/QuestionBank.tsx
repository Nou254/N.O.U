import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface BankCategory {
  id: number
  name: string
  positions: number
  per_part: Record<string, number>
  total: number
  ready: boolean
}

const PARTS = ['common', 'category', 'position', 'practical', 'professional']
const PART_LABELS: Record<string, string> = {
  common: 'Common',
  category: 'Category',
  position: 'Position',
  practical: 'Practical',
  professional: 'Professional',
}
const TARGET_PER_PART = 20

const AdminQuestionBank = () => {
  const [categories, setCategories] = useState<BankCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState<number | null>(null)

  const fetchStatus = async () => {
    try {
      const response = await api.get('/admin/question-bank')
      setCategories(response.data.categories || [])
    } catch (error) {
      console.error('Error fetching question bank status:', error)
      toast.error('Failed to load question bank status')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStatus()
  }, [])

  const handleGenerate = async (category: BankCategory) => {
    const confirmed = window.confirm(
      `Generate a 100-question AI bank for "${category.name}"?\n\n` +
        'Groq will write 20 advanced real-world questions per assessment part. ' +
        'This takes about 3-5 minutes the first time (one-time cost). After that, ' +
        'every assessment in this category starts instantly.\n\n' +
        `Currently stored: ${category.total} questions.`
    )
    if (!confirmed) return
    setGenerating(category.id)
    try {
      const response = await api.post(
        `/admin/question-bank/generate/${category.id}`,
        {},
        { timeout: 15 * 60 * 1000 } // Groq takes minutes to write 100 questions
      )
      toast.success(response.data.message || 'Question bank generated')
      fetchStatus()
    } catch (error: any) {
      toast.error(
        error?.response?.data?.message || 'Failed to generate the question bank'
      )
    } finally {
      setGenerating(null)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Question Bank</h1>
          <p className="text-gray-600 mt-1">
            Groq pre-generates 100 advanced questions per career category. Every
            assessment draws 20 random questions from its category's bank - so
            exams start instantly and no AI call runs during the exam.
          </p>
        </div>
        <span className="badge-success">AI Powered</span>
      </div>

      {/* How it works */}
      <div className="card mb-8 bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <h3 className="font-semibold mb-2">How the bank works</h3>
        <div className="grid sm:grid-cols-3 gap-4 text-sm text-primary-100">
          <div>
            <div className="font-medium text-white">1. Generate once</div>
            <div className="text-xs mt-1">
              Click <strong>Generate</strong> on a career category. Groq writes 100
              questions (20 per assessment part) and stores them.
            </div>
          </div>
          <div>
            <div className="font-medium text-white">2. Instant exams</div>
            <div className="text-xs mt-1">
              Each applicant gets 20 questions selected at random from the 100 -
              start is instant, no blank screen, no traffic spike.
            </div>
          </div>
          <div>
            <div className="font-medium text-white">3. AI grading</div>
            <div className="text-xs mt-1">
              After submission, Groq grades the answers and the results go to the
              admin (AI Results) for final review and approval.
            </div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
        </div>
      ) : (
        <div className="card overflow-x-auto">
          <table className="table w-full">
            <thead>
              <tr>
                <th className="text-left">Career Category</th>
                {PARTS.map((part) => (
                  <th key={part} className="text-center text-xs">
                    {PART_LABELS[part]}
                    <span className="block text-gray-400 font-normal">
                      target {TARGET_PER_PART}
                    </span>
                  </th>
                ))}
                <th className="text-center">Total</th>
                <th className="text-center">Status</th>
                <th className="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {categories.length === 0 ? (
                <tr>
                  <td colSpan={8} className="text-center py-8 text-gray-500">
                    No professional categories found.
                  </td>
                </tr>
              ) : (
                categories.map((cat) => {
                  const isGenerating = generating === cat.id
                  return (
                    <tr key={cat.id}>
                      <td className="font-medium text-gray-900">
                        {cat.name}
                        <span className="block text-xs text-gray-400 font-normal">
                          {cat.positions} positions
                        </span>
                      </td>
                      {PARTS.map((part) => (
                        <td key={part} className="text-center">
                          <span
                            className={`inline-flex items-center justify-center w-8 h-8 rounded-full text-xs font-medium ${
                              (cat.per_part[part] || 0) >= TARGET_PER_PART
                                ? 'bg-green-100 text-green-700'
                                : (cat.per_part[part] || 0) > 0
                                ? 'bg-yellow-100 text-yellow-700'
                                : 'bg-gray-100 text-gray-500'
                            }`}
                          >
                            {cat.per_part[part] || 0}
                          </span>
                        </td>
                      ))}
                      <td className="text-center font-semibold text-gray-900">
                        {cat.total}
                        <span className="block text-xs text-gray-400 font-normal">
                          / 100
                        </span>
                      </td>
                      <td className="text-center">
                        {cat.ready ? (
                          <span className="badge-success">Ready - instant exams</span>
                        ) : (
                          <span className="badge-warning">Needs generation</span>
                        )}
                      </td>
                      <td className="text-right">
                        <button
                          onClick={() => handleGenerate(cat)}
                          disabled={isGenerating}
                          className="btn-primary text-sm disabled:opacity-50"
                        >
                          {isGenerating ? (
                            <span className="inline-flex items-center gap-2">
                              <span className="spinner inline-block w-3 h-3 border-2"></span>
                              Generating…
                            </span>
                          ) : cat.ready ? (
                            'Top up / Regenerate'
                          ) : (
                            'Generate Bank'
                          )}
                        </button>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
          <p className="text-xs text-gray-400 mt-4 px-1">
            First generation per category takes ~3-5 minutes (Groq writes 100
            questions in batches). Please keep this page open while it runs.
          </p>
        </div>
      )}
    </div>
  )
}

export default AdminQuestionBank
