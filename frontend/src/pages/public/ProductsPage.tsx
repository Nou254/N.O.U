import { useEffect, useState } from 'react'
import { useAppDispatch, useAppSelector } from '../../hooks/useAppSelector'
import { fetchProducts, Product } from '../../store/productSlice'

const CATALOGUE_CATEGORIES = [
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

const PLATFORMS = ['Web', 'PWA', 'Android', 'Windows', 'Linux', 'iOS', 'Cloud-SaaS', 'Multi-Platform']

const STATUSES = ['Coming Soon', 'Beta', 'Early Access', 'Available', 'Updated', 'Maintenance', 'Archived']

const STATUS_STYLE: Record<string, string> = {
  'Coming Soon': 'bg-purple-100 text-purple-700',
  Beta: 'bg-amber-100 text-amber-700',
  'Early Access': 'bg-orange-100 text-orange-700',
  Available: 'bg-green-100 text-green-700',
  Updated: 'bg-blue-100 text-blue-700',
  Maintenance: 'bg-yellow-100 text-yellow-700',
  Archived: 'bg-gray-100 text-gray-600',
}

const ProductsPage = () => {
  const dispatch = useAppDispatch()
  const { products, loading, pagination } = useAppSelector((state) => state.products)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [status, setStatus] = useState('')
  const [platform, setPlatform] = useState('')

  useEffect(() => {
    dispatch(fetchProducts({ search, category, status, platform }))
  }, [dispatch, search, category, status, platform])

  const formatFileSize = (bytes: number) => {
    if (bytes === 0 || !bytes) return 'N/A'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          N.O.U. Software Catalogue
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover software developed, published and distributed by N.O.U. Digital Systems.
        </p>
      </div>

      {/* Search + filters */}
      <div className="bg-white border border-gray-200 rounded-xl p-4 mb-8 shadow-sm">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search products, functions, keywords..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input"
            />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 lg:w-auto lg:min-w-[480px]">
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="input"
            >
              <option value="">All Categories</option>
              {CATALOGUE_CATEGORIES.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              className="input"
            >
              <option value="">All Platforms</option>
              {PLATFORMS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="input"
            >
              <option value="">All Statuses</option>
              {STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading products...</p>
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-12">
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
              d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
            />
          </svg>
          <p className="text-gray-600">No products found</p>
          <p className="text-sm text-gray-500 mt-1">Try adjusting your search or filters.</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product: Product) => (
            <div key={product.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
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
                      d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                    />
                  </svg>
                </div>
                <div className="flex items-center gap-2 flex-wrap justify-end">
                  {product.featured && (
                    <span className="bg-primary-600 text-white text-[11px] font-semibold px-2 py-0.5 rounded-full">
                      Featured
                    </span>
                  )}
                  <span
                    className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
                      STATUS_STYLE[product.status] || 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {product.status || 'Available'}
                  </span>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-1">{product.name}</h3>
              <p className="text-xs text-primary-600 uppercase tracking-wide mb-2">
                {product.category?.replace('_', ' ')}
              </p>
              <p className="text-gray-600 mb-4 line-clamp-2">{product.description}</p>

              <div className="flex items-center gap-2 mb-4 flex-wrap">
                {product.platforms && product.platforms.length > 0 ? (
                  product.platforms.map((pl) => (
                    <span key={pl} className="text-[11px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                      {pl}
                    </span>
                  ))
                ) : (
                  <span className="text-[11px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded">Web</span>
                )}
              </div>

              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>Version {product.version}</span>
                <span>{formatFileSize(product.fileSize)}</span>
              </div>

              {product.licence && (
                <p className="text-xs text-gray-400 mb-4 line-clamp-1">
                  Licence: {product.licence}
                </p>
              )}

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">
                  {product.downloadCount} downloads
                </span>
                <button className="btn-primary text-sm">
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {pagination.pages > 1 && (
        <div className="flex justify-center mt-8">
          <nav className="flex items-center space-x-2">
            {Array.from({ length: pagination.pages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => dispatch(fetchProducts({ search, category, status, platform, page }))}
                className={`w-10 h-10 rounded-lg flex items-center justify-center text-sm font-medium transition-colors ${
                  page === pagination.page
                    ? 'bg-primary-600 text-white'
                    : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
                }`}
              >
                {page}
              </button>
            ))}
          </nav>
        </div>
      )}
    </div>
  )
}

export default ProductsPage