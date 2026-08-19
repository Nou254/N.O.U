import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../services/api'

interface CategoryScreen {
  id: number
  name: string
  description: string | null
  positions_count: number
  assessed: number
  passed: number
  pending_approval: number
}

const AdminCategoryScreens = () => {
  const [categories, setCategories] = useState<CategoryScreen[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    try {
      const response = await api.get('/admin/categories')
      setCategories(response.data.categories || [])
    } catch (error) {
      console.error('Error fetching category screens:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Category Screens</h1>
        <p className="text-gray-600">
          Each assessed professional category has its own screen - open any category
          to see the candidates assessed in it, their results and approval status.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12"><div className="spinner mx-auto"></div></div>
      ) : categories.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-600">No professional categories found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((cat) => (
            <Link key={cat.id} to={`/admin/categories/${cat.id}`} className="card hover:scale-[1.02] transition-transform duration-200">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-900 leading-snug">{cat.name}</h3>
                <svg className="w-5 h-5 text-primary-600 shrink-0 ml-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
              {cat.description && (
                <p className="text-sm text-gray-500 mb-4 line-clamp-2">{cat.description}</p>
              )}
              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="bg-gray-50 rounded-lg p-2">
                  <p className="text-xl font-bold text-gray-900">{cat.assessed}</p>
                  <p className="text-[11px] text-gray-500">Assessed</p>
                </div>
                <div className="bg-green-50 rounded-lg p-2">
                  <p className="text-xl font-bold text-green-700">{cat.passed}</p>
                  <p className="text-[11px] text-green-600">Passed</p>
                </div>
                <div className="bg-amber-50 rounded-lg p-2">
                  <p className="text-xl font-bold text-amber-700">{cat.pending_approval}</p>
                  <p className="text-[11px] text-amber-600">Pending</p>
                </div>
              </div>
              <p className="text-xs text-gray-400 mt-3">
                {cat.positions_count} position{cat.positions_count === 1 ? '' : 's'} · Open screen
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default AdminCategoryScreens
