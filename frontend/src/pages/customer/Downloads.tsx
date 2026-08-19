import { useEffect, useState } from 'react'
import { useAppDispatch, useAppSelector } from '../../hooks/useAppSelector'
import { fetchProducts, downloadProduct } from '../../store/productSlice'
import toast from 'react-hot-toast'

const CustomerDownloads = () => {
  const dispatch = useAppDispatch()
  const { products, loading } = useAppSelector((state) => state.products)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')

  useEffect(() => {
    dispatch(fetchProducts({ search, category }))
  }, [dispatch, search, category])

  const handleDownload = async (productId: string, productName: string) => {
    try {
      await dispatch(downloadProduct(productId)).unwrap()
      toast.success(`Downloading ${productName}...`)
    } catch (error) {
      toast.error('Download failed. Please try again.')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const categories = [
    { value: '', label: 'All Categories' },
    { value: 'software', label: 'Software' },
    { value: 'application', label: 'Applications' },
    { value: 'tool', label: 'Tools' },
    { value: 'library', label: 'Libraries' },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Software Downloads</h1>
        <p className="text-gray-600">Browse and download our software products.</p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search products..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input"
          />
        </div>
        <div className="sm:w-48">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="input"
          >
            {categories.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Products Grid */}
      {loading ? (
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading products...</p>
        </div>
      ) : products.length === 0 ? (
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
              d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
            />
          </svg>
          <p className="text-gray-600">No products found</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id} className="card">
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
                <span className="badge-primary capitalize">{product.category}</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{product.name}</h3>
              <p className="text-gray-600 mb-4 line-clamp-2">{product.description}</p>
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>Version {product.version}</span>
                <span>{formatFileSize(product.fileSize)}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">
                  {product.downloadCount} downloads
                </span>
                <button
                  onClick={() => handleDownload(product.id, product.name)}
                  className="btn-primary text-sm"
                >
                  <svg
                    className="w-4 h-4 mr-2"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default CustomerDownloads