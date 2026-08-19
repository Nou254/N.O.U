import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Position {
  id: string
  name: string
  modules_list: string[]
  is_active: string
}

interface Category {
  id: string
  name: string
  description: string
  weights: {
    logic: number
    general: number
    category: number
    position: number
    practical: number
    professional: number
  }
  is_active: string
  positions: Position[]
}

const WEIGHT_FIELDS = [
  { key: 'logic', label: 'Logic & Reasoning' },
  { key: 'general', label: 'General Knowledge' },
  { key: 'category', label: 'Category Knowledge' },
  { key: 'position', label: 'Position Knowledge' },
  { key: 'practical', label: 'Practical & Applied' },
  { key: 'professional', label: 'Professional Ethics' },
] as const

const AdminPersonnel = () => {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState<string | null>(null)
  const [showAdd, setShowAdd] = useState(false)
  const [editing, setEditing] = useState<Category | null>(null)
  const [showAddPosition, setShowAddPosition] = useState<Category | null>(null)
  const [newCategory, setNewCategory] = useState({
    name: '',
    description: '',
    weight_logic: 15,
    weight_general: 5,
    weight_category: 25,
    weight_position: 25,
    weight_practical: 25,
    weight_professional: 5,
  })
  const [newPosition, setNewPosition] = useState({ name: '', modules: '' })

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    try {
      const response = await api.get('/personnel/categories?include_inactive=true')
      setCategories(response.data.categories || [])
    } catch (error) {
      console.error('Error fetching categories:', error)
      toast.error('Failed to load personnel categories')
    } finally {
      setLoading(false)
    }
  }

  const weightsTotal = (cat: Category | typeof newCategory) => {
    if ('weights' in cat) {
      const w = cat.weights
      return w.logic + w.general + w.category + w.position + w.practical + w.professional
    }
    return (
      cat.weight_logic +
      cat.weight_general +
      cat.weight_category +
      cat.weight_position +
      cat.weight_practical +
      cat.weight_professional
    )
  }

  const handleAddCategory = async (e: React.FormEvent) => {
    e.preventDefault()
    if (weightsTotal(newCategory) !== 100) {
      toast.error(`Weights must total 100% (currently ${weightsTotal(newCategory)}%)`)
      return
    }
    try {
      await api.post('/personnel/categories', newCategory)
      toast.success('Category created')
      setShowAdd(false)
      setNewCategory({
        name: '',
        description: '',
        weight_logic: 15,
        weight_general: 5,
        weight_category: 25,
        weight_position: 25,
        weight_practical: 25,
        weight_professional: 5,
      })
      fetchCategories()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to create category')
    }
  }

  const handleUpdateCategory = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editing) return
    if (weightsTotal(editing) !== 100) {
      toast.error(`Weights must total 100% (currently ${weightsTotal(editing)}%)`)
      return
    }
    try {
      await api.put(`/personnel/categories/${editing.id}`, {
        description: editing.description,
        weight_logic: editing.weights.logic,
        weight_general: editing.weights.general,
        weight_category: editing.weights.category,
        weight_position: editing.weights.position,
        weight_practical: editing.weights.practical,
        weight_professional: editing.weights.professional,
      })
      toast.success('Category updated')
      setEditing(null)
      fetchCategories()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to update category')
    }
  }

  const handleAddPosition = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!showAddPosition) return
    try {
      await api.post(`/personnel/categories/${showAddPosition.id}/positions`, {
        name: newPosition.name,
        modules: newPosition.modules,
      })
      toast.success('Position added')
      setShowAddPosition(null)
      setNewPosition({ name: '', modules: '' })
      fetchCategories()
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to add position')
    }
  }

  const weightInputs = (value: Category['weights'], onChange: (w: Category['weights']) => void) =>
    WEIGHT_FIELDS.map((f) => (
      <div key={f.key}>
        <label className="label">{f.label} (%)</label>
        <input
          type="number"
          min={0}
          max={100}
          value={value[f.key]}
          onChange={(e) => onChange({ ...value, [f.key]: parseInt(e.target.value) || 0 })}
          className="input"
        />
      </div>
    ))

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Personnel Categories & Positions</h1>
          <p className="text-gray-600">
            Employment categories, positions and per-category assessment weights (weights must total 100%).
          </p>
        </div>
        <button onClick={() => setShowAdd(true)} className="btn-primary">
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add Category
        </button>
      </div>

      {/* Add category modal */}
      {showAdd && (
        <div className="modal-overlay" onClick={() => setShowAdd(false)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Add Personnel Category</h2>
            <form onSubmit={handleAddCategory} className="space-y-4">
              <div>
                <label className="label">Category name</label>
                <input
                  type="text"
                  value={newCategory.name}
                  onChange={(e) => setNewCategory({ ...newCategory, name: e.target.value })}
                  required
                  className="input"
                  placeholder="e.g. Network Engineering"
                />
              </div>
              <div>
                <label className="label">Description</label>
                <textarea
                  value={newCategory.description}
                  onChange={(e) => setNewCategory({ ...newCategory, description: e.target.value })}
                  rows={2}
                  className="input"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                {WEIGHT_FIELDS.map((f) => (
                  <div key={f.key}>
                    <label className="label">{f.label} (%)</label>
                    <input
                      type="number"
                      min={0}
                      max={100}
                      value={newCategory[f.key as keyof typeof newCategory] as number}
                      onChange={(e) =>
                        setNewCategory({
                          ...newCategory,
                          [f.key]: parseInt(e.target.value) || 0,
                        })
                      }
                      className="input"
                    />
                  </div>
                ))}
              </div>
              <p className={`text-sm ${weightsTotal(newCategory) === 100 ? 'text-green-600' : 'text-red-500'}`}>
                Total: {weightsTotal(newCategory)}% {weightsTotal(newCategory) === 100 ? '(valid)' : '(must be 100%)'}
              </p>
              <div className="flex justify-end space-x-3 pt-2">
                <button type="button" onClick={() => setShowAdd(false)} className="btn-secondary">Cancel</button>
                <button type="submit" className="btn-primary">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit category modal */}
      {editing && (
        <div className="modal-overlay" onClick={() => setEditing(null)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Edit: {editing.name}</h2>
            <form onSubmit={handleUpdateCategory} className="space-y-4">
              <div>
                <label className="label">Description</label>
                <textarea
                  value={editing.description || ''}
                  onChange={(e) => setEditing({ ...editing, description: e.target.value })}
                  rows={2}
                  className="input"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                {weightInputs(editing.weights, (weights) => setEditing({ ...editing, weights }))}
              </div>
              <p className={`text-sm ${weightsTotal(editing) === 100 ? 'text-green-600' : 'text-red-500'}`}>
                Total: {weightsTotal(editing)}% {weightsTotal(editing) === 100 ? '(valid)' : '(must be 100%)'}
              </p>
              <div className="flex justify-end space-x-3 pt-2">
                <button type="button" onClick={() => setEditing(null)} className="btn-secondary">Cancel</button>
                <button type="submit" className="btn-primary">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add position modal */}
      {showAddPosition && (
        <div className="modal-overlay" onClick={() => setShowAddPosition(null)}>
          <div className="modal-content max-w-md" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Add position to {showAddPosition.name}</h2>
            <form onSubmit={handleAddPosition} className="space-y-4">
              <div>
                <label className="label">Position name</label>
                <input
                  type="text"
                  value={newPosition.name}
                  onChange={(e) => setNewPosition({ ...newPosition, name: e.target.value })}
                  required
                  className="input"
                  placeholder="e.g. Network Installation Engineer"
                />
              </div>
              <div>
                <label className="label">Knowledge modules (comma separated)</label>
                <input
                  type="text"
                  value={newPosition.modules}
                  onChange={(e) => setNewPosition({ ...newPosition, modules: e.target.value })}
                  className="input"
                  placeholder="Routing, Switching, Fiber Optics"
                />
              </div>
              <div className="flex justify-end space-x-3 pt-2">
                <button type="button" onClick={() => setShowAddPosition(null)} className="btn-secondary">Cancel</button>
                <button type="submit" className="btn-primary">Add</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Categories list */}
      {loading ? (
        <div className="text-center py-12"><div className="spinner mx-auto"></div></div>
      ) : (
        <div className="space-y-4">
          {categories.length === 0 ? (
            <div className="card text-center py-12">
              <p className="text-gray-600">No categories yet. Add one to get started.</p>
            </div>
          ) : (
            categories.map((cat) => (
              <div key={cat.id} className="card">
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="text-lg font-semibold text-gray-900">{cat.name}</h3>
                      <span className={cat.is_active === 'active' ? 'badge-success' : 'badge-gray'}>
                        {cat.is_active === 'active' ? 'Active' : 'Inactive'}
                      </span>
                      <span className="text-xs text-gray-500">{cat.positions?.length || 0} positions</span>
                    </div>
                    {cat.description && <p className="text-sm text-gray-600 mt-1">{cat.description}</p>}
                    <div className="flex flex-wrap gap-2 mt-2">
                      {WEIGHT_FIELDS.map((f) => (
                        <span key={f.key} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                          {f.label}: <strong>{cat.weights[f.key]}%</strong>
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-2 shrink-0 ml-4">
                    <button onClick={() => setEditing(cat)} className="btn-outline text-sm">Edit weights</button>
                    <button onClick={() => { setShowAddPosition(cat); setNewPosition({ name: '', modules: '' }) }} className="btn-secondary text-sm">
                      Add position
                    </button>
                    <button
                      onClick={() => setExpanded(expanded === cat.id ? null : cat.id)}
                      className="text-sm text-primary-600 font-medium"
                    >
                      {expanded === cat.id ? 'Hide positions' : 'View positions'}
                    </button>
                  </div>
                </div>

                {expanded === cat.id && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">Positions</p>
                    {cat.positions?.length === 0 ? (
                      <p className="text-sm text-gray-500">No positions yet.</p>
                    ) : (
                      <div className="grid md:grid-cols-2 gap-3">
                        {cat.positions.map((pos) => (
                          <div key={pos.id} className="border border-gray-200 rounded-lg p-3">
                            <p className="font-medium text-gray-800 text-sm">{pos.name}</p>
                            {pos.modules_list?.length > 0 && (
                              <div className="flex flex-wrap gap-1 mt-2">
                                {pos.modules_list.map((m) => (
                                  <span key={m} className="text-xs bg-primary-50 text-primary-700 px-2 py-0.5 rounded">
                                    {m}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}

export default AdminPersonnel
