import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { productService } from '../services/productService'

export interface Product {
  id: string
  name: string
  description: string
  category: string
  version: string
  status: string
  platforms: string[]
  licence: string | null
  requirements: string | null
  features: string | null
  featured: boolean
  fileSize: number
  downloadCount: number
  createdAt: string
}

interface ProductState {
  products: Product[]
  selectedProduct: Product | null
  loading: boolean
  error: string | null
  pagination: {
    total: number
    page: number
    limit: number
    pages: number
  }
}

const initialState: ProductState = {
  products: [],
  selectedProduct: null,
  loading: false,
  error: null,
  pagination: {
    total: 0,
    page: 1,
    limit: 20,
    pages: 0,
  },
}

// Async thunks
export const fetchProducts = createAsyncThunk(
  'products/fetchProducts',
  async (
    params: { category?: string; search?: string; status?: string; platform?: string; featured?: boolean; sort?: string; page?: number; limit?: number },
    { rejectWithValue }
  ) => {
    try {
      const response = await productService.getProducts(params)
      return response
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch products')
    }
  }
)

export const fetchProductById = createAsyncThunk(
  'products/fetchProductById',
  async (productId: string, { rejectWithValue }) => {
    try {
      const response = await productService.getProductById(productId)
      return response
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch product')
    }
  }
)

export const downloadProduct = createAsyncThunk(
  'products/downloadProduct',
  async (productId: string, { rejectWithValue }) => {
    try {
      const response = await productService.downloadProduct(productId)
      return response
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to download product')
    }
  }
)

const productSlice = createSlice({
  name: 'products',
  initialState,
  reducers: {
    clearSelectedProduct: (state) => {
      state.selectedProduct = null
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch products
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false
        state.products = action.payload.products
        state.pagination = action.payload.pagination
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Fetch product by ID
      .addCase(fetchProductById.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchProductById.fulfilled, (state, action) => {
        state.loading = false
        state.selectedProduct = action.payload.product
      })
      .addCase(fetchProductById.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Download product
      .addCase(downloadProduct.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(downloadProduct.fulfilled, (state) => {
        state.loading = false
      })
      .addCase(downloadProduct.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
  },
})

export const { clearSelectedProduct, clearError } = productSlice.actions
export default productSlice.reducer