import api from './api'

interface ProductParams {
  category?: string
  search?: string
  status?: string
  platform?: string
  featured?: boolean
  sort?: string
  page?: number
  limit?: number
}

export const productService = {
  async getProducts(params: ProductParams = {}): Promise<any> {
    const response = await api.get('/products', { params })
    return response.data
  },

  async getProductById(productId: string): Promise<any> {
    const response = await api.get(`/products/${productId}`)
    return response.data
  },

  async downloadProduct(productId: string): Promise<Blob> {
    const response = await api.get(`/products/${productId}/download`, {
      responseType: 'blob',
    })
    return response.data
  },

  async createProduct(formData: FormData): Promise<any> {
    const response = await api.post('/admin/products', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async updateProduct(productId: string, data: any): Promise<any> {
    const response = await api.put(`/admin/products/${productId}`, data)
    return response.data
  },

  async deleteProduct(productId: string): Promise<void> {
    await api.delete(`/admin/products/${productId}`)
  },
}