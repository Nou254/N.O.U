import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { authService } from '../services/authService'

interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  role: 'visitor' | 'customer' | 'applicant' | 'admin' | 'developer' | 'investor'
  terms_accepted_at?: string | null
  policies_accepted_at?: string | null
  username?: string | null
  qualification_category_id?: number | null
  qualification_position_id?: number | null
  qualification_category_name?: string | null
  qualification_position_name?: string | null
}

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  refreshToken: localStorage.getItem('refreshToken'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  error: null,
}

// FastAPI returns validation errors (422) as an array of {loc, msg} objects.
// Normalize both string and array detail into a readable message.
const extractError = (error: any): string | null => {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((d: any) => d?.msg || '')
      .filter(Boolean)
      .join('; ')
  }
  return null
}

const applyAuth = (state: AuthState, payload: any) => {
  state.isAuthenticated = true
  state.user = {
    id: payload.user.id,
    email: payload.user.email,
    firstName: payload.user.first_name,
    lastName: payload.user.last_name,
    role: payload.user.role as User['role'],
    terms_accepted_at: payload.user.terms_accepted_at ?? null,
    policies_accepted_at: payload.user.policies_accepted_at ?? null,
    username: payload.user.username ?? null,
    qualification_category_id: payload.user.qualification_category_id ?? null,
    qualification_position_id: payload.user.qualification_position_id ?? null,
    qualification_category_name: payload.user.qualification_category_name ?? null,
    qualification_position_name: payload.user.qualification_position_name ?? null,
  }
  state.token = payload.access_token
  state.refreshToken = payload.refresh_token
}

// Async thunks
export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }: { email: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await authService.login(email, password)
      // Admin accounts require an OTP step before tokens are issued.
      if ((response as any).requires_otp) {
        return {
          requiresOtp: true,
          email: (response as any).email || email,
        }
      }
      localStorage.setItem('token', (response as any).access_token)
      localStorage.setItem('refreshToken', (response as any).refresh_token)
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error) || 'Login failed')
    }
  }
)

export const verifyLoginOtp = createAsyncThunk(
  'auth/verifyLoginOtp',
  async ({ email, otp }: { email: string; otp: string }, { rejectWithValue }) => {
    try {
      const response = await authService.verifyLoginOtp(email, otp)
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error) || 'Invalid verification code')
    }
  }
)

export const register = createAsyncThunk(
  'auth/register',
  async (
    userData: {
      email: string
      password: string
      firstName: string
      lastName: string
      role?: string
    },
    { rejectWithValue }
  ) => {
    try {
      const response = await authService.register(userData)
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error) || 'Registration failed')
    }
  }
)

export const verifyRegistration = createAsyncThunk(
  'auth/verifyRegistration',
  async ({ email, otp }: { email: string; otp: string }, { rejectWithValue }) => {
    try {
      const response = await authService.verifyRegistration(email, otp)
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error) || 'Verification failed')
    }
  }
)

export const acceptTerms = createAsyncThunk(
  'auth/acceptTerms',
  async (_, { rejectWithValue }) => {
    try {
      const response = await authService.acceptTerms()
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error) || 'Could not record your agreement')
    }
  }
)

export const acceptPolicies = createAsyncThunk(
  'auth/acceptPolicies',
  async (_, { rejectWithValue }) => {
    try {
      const response = await authService.acceptPolicies()
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error) || 'Could not record your agreement')
    }
  }
)

export const setUsername = createAsyncThunk(
  'auth/setUsername',
  async (username: string, { rejectWithValue }) => {
    try {
      const response = await authService.setUsername(username)
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error) || 'Could not save your handle')
    }
  }
)

export const logout = createAsyncThunk('auth/logout', async () => {
  try {
    await authService.logout()
  } catch {
    // Token may already be invalid - clear locally regardless.
  }
  localStorage.removeItem('token')
  localStorage.removeItem('refreshToken')
})

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(login.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false
        const payload = action.payload as any
        // OTP step only - do not set auth yet.
        if (payload?.access_token) {
          applyAuth(state, payload)
        }
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Verify login OTP (admin 2-step login)
      .addCase(verifyLoginOtp.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(verifyLoginOtp.fulfilled, (state, action) => {
        state.loading = false
        applyAuth(state, action.payload)
      })
      .addCase(verifyLoginOtp.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Register
      .addCase(register.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(register.fulfilled, (state) => {
        state.loading = false
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Verify registration OTP
      .addCase(verifyRegistration.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(verifyRegistration.fulfilled, (state) => {
        state.loading = false
      })
      .addCase(verifyRegistration.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Accept terms (first-login consent gate)
      .addCase(acceptTerms.fulfilled, (state, action) => {
        if (state.user) {
          state.user.terms_accepted_at =
            (action.payload as any)?.terms_accepted_at || new Date().toISOString()
        }
      })
      .addCase(acceptTerms.rejected, (state, action) => {
        state.error = action.payload as string
      })
      // Accept organization policies (approved personnel first login)
      .addCase(acceptPolicies.fulfilled, (state, action) => {
        if (state.user) {
          state.user.policies_accepted_at =
            (action.payload as any)?.policies_accepted_at || new Date().toISOString()
        }
      })
      .addCase(acceptPolicies.rejected, (state, action) => {
        state.error = action.payload as string
      })
      // Set company handle (@username)
      .addCase(setUsername.fulfilled, (state, action) => {
        if (state.user && (action.payload as any)?.user?.username) {
          state.user.username = (action.payload as any).user.username
        }
      })
      .addCase(setUsername.rejected, (state, action) => {
        state.error = action.payload as string
      })
      // Logout
      .addCase(logout.fulfilled, (state) => {
        state.user = null
        state.token = null
        state.refreshToken = null
        state.isAuthenticated = false
      })
  },
})

export const { clearError, setUser } = authSlice.actions
export default authSlice.reducer
