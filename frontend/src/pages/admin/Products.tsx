import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface Product {
  id: string
  name: string
  description: string
  category: string
  version: string
  file_size: number
  download_count: number
  is_active: boolean
}

const AdminProducts = () => {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddProduct, setShowAddProduct] = useState(false)
  const [newProduct, setNewProduct] = useState({
    name: '',
    description: '',
    category: 'software',
    version: '1.0.0',
    status: 'Available',
    platforms: 'Web',
    licence: '',
    requirements: '',
    features: '',
    featured: false,
  })

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const response = await api.get('/products')
      setProducts(response.data.products)
    } catch (error) {
      console.error('Error fetching products:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddProduct = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const formData = new FormData()
      formData.append('name', newProduct.name)
      formData.append('description', newProduct.description)
      formData.append('category', newProduct.category)
      formData.append('version', newProduct.version)
      formData.append('status', newProduct.status)
      formData.append('platforms', newProduct.platforms)
      if (newProduct.licence) formData.append('licence', newProduct.licence)
      if (newProduct.requirements) formData.append('requirements', newProduct.requirements)
      if (newProduct.features) formData.append('features', newProduct.features)
      formData.append('featured', String(newProduct.featured))
      
      await api.post('/admin/products', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      
      toast.success('Product added successfully')
      setShowAddProduct(false)
      setNewProduct({ name: '', description: '', category: 'software', version: '1.0.0', status: 'Available', platforms: 'Web', licence: '', requirements: '', features: '', featured: false })
      fetchProducts()
    } catch (error) {
      toast.error('Failed to add product')
    }
  }

  const handleDeleteProduct = async (productId: string) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return
    
    try {
      await api.delete(`/admin/products/${productId}`)
      toast.success('Product deleted successfully')
      fetchProducts()
    } catch (error) {
      toast.error('Failed to delete product')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (!bytes) return 'N/A'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const categories = [
    { value: 'software', label: 'Software' },
    { value: 'application', label: 'Application' },
    { value: 'tool', label: 'Tool' },
    { value: 'library', label: 'Library' },
    { value: 'business', label: 'Business & Enterprise' },
    { value: 'education', label: 'Education & Learning' },
    { value: 'finance', label: 'Finance & FinTech' },
    { value: 'healthcare', label: 'Healthcare' },
    { value: 'hospitality', label: 'Hospitality & Tourism' },
    { value: 'government', label: 'Government & Institutional' },
    { value: 'productivity', label: 'Productivity' },
    { value: 'communication', label: 'Communication & Social' },
    { value: 'games', label: 'Games & Entertainment' },
    { value: 'security', label: 'Security & Safety' },
    { value: 'networking', label: 'Networking & Infrastructure' },
    { value: 'developer_tools', label: 'Developer & Technology Tools' },
    { value: 'utilities', label: 'Utilities' },
    { value: 'lifestyle', label: 'Lifestyle & Personal' },
    { value: 'experimental', label: 'Experimental & Innovation' },
  ]

  const productStatuses = ['Coming Soon', 'Beta', 'Early Access', 'Available', 'Updated', 'Maintenance', 'Archived']

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Product Management</h1>
          <p className="text-gray-600">Manage your software products and downloads.</p>
        </div>
        <button onClick={() => setShowAddProduct(true)} className="btn-primary">
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add Product
        </button>
      </div>

      {/* Add Product Modal */}
      {showAddProduct && (
        <div className="modal-overlay" onClick={() => setShowAddProduct(false)}>
          <div className="modal-content max-w-lg" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Product</h2>
            <form onSubmit={handleAddProduct} className="space-y-4">
              <div>
                <label className="label">Product Name</label>
                <input
                  type="text"
                  value={newProduct.name}
                  onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                  required
                  className="input"
                />
              </div>
              <div>
                <label className="label">Description</label>
                <textarea
                  value={newProduct.description}
                  onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
                  rows={3}
                  className="input"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Category</label>
                  <select
                    value={newProduct.category}
                    onChange={(e) => setNewProduct({ ...newProduct, category: e.target.value })}
                    className="input"
                  >
                    {categories.map((cat) => (
                      <option key={cat.value} value={cat.value}>{cat.label}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="label">Version</label>
                  <input
                    type="text"
                    value={newProduct.version}
                    onChange={(e) => setNewProduct({ ...newProduct, version: e.target.value })}
                    className="input"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Status</label>
                  <select
                    value={newProduct.status}
                    onChange={(e) => setNewProduct({ ...newProduct, status: e.target.value })}
                    className="input"
                  >
                    {productStatuses.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="label">Platforms (comma separated)</label>
                  <input
                    type="text"
                    value={newProduct.platforms}
                    onChange={(e) => setNewProduct({ ...newProduct, platforms: e.target.value })}
                    className="input"
                    placeholder="Web, PWA, Android"
                  />
                </div>
              </div>
              <div>
                <label className="label">Licence</label>
                <input
                  type="text"
                  value={newProduct.licence}
                  onChange={(e) => setNewProduct({ ...newProduct, licence: e.target.value })}
                  className="input"
                  placeholder="e.g. Proprietary, MIT, GNU GPL v3"
                />
              </div>
              <div>
                <label className="label">Requirements</label>
                <textarea
                  value={newProduct.requirements}
                  onChange={(e) => setNewProduct({ ...newProduct, requirements: e.target.value })}
                  rows={2}
                  className="input"
                  placeholder="Technical requirements to operate the product"
                />
              </div>
              <div>
                <label className="label">Key Features</label>
                <textarea
                  value={newProduct.features}
                  onChange={(e) => setNewProduct({ ...newProduct, features: e.target.value })}
                  rows={2}
                  className="input"
                  placeholder="Major features of the product"
                />
              </div>
              <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                <input
                  type="checkbox"
                  checked={newProduct.featured}
                  onChange={(e) => setNewProduct({ ...newProduct, featured: e.target.checked })}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                Feature this product on the home screen
              </label>
              <div className="flex justify-end space-x-3 pt-4">
                <button type="button" onClick={() => setShowAddProduct(false)} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary">Add Product</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Products Table */}
      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">No products found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Category</th>
                  <th>Version</th>
                  <th>Size</th>
                  <th>Downloads</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>
                      <div>
                        <p className="font-medium text-gray-900">{product.name}</p>
                        <p className="text-sm text-gray-500 line-clamp-1">{product.description}</p>
                      </div>
                    </td>
                    <td className="capitalize">{product.category}</td>
                    <td>{product.version}</td>
                    <td>{formatFileSize(product.file_size)}</td>
                    <td>{product.download_count}</td>
                    <td>
                      <span className={product.is_active ? 'badge-success' : 'badge-gray'}>
                        {product.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => handleDeleteProduct(product.id)}
                          className="text-red-600 hover:text-red-700 text-sm"
                        >
                          Delete
                        </button>
                      </div>
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

export default AdminProducts