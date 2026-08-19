import api from './api'

interface UserData {
  id: string
  email: string
  first_name: string
  last_name: string
  role: string
}

interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: UserData
}

interface OtpResponse {
  requires_otp: boolean
  email?: string
  message?: string
}

interface RegisterData {
  email: string
  password: string
  firstName: string
  lastName: string
}

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse | OtpResponse> {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  async verifyLoginOtp(email: string, otp: string): Promise<LoginResponse> {
    const response = await api.post('/auth/login/verify', { email, otp })
    return response.data
  },

  async register(data: RegisterData): Promise<OtpResponse> {
    const response = await api.post('/auth/register', {
      email: data.email,
      password: data.password,
      first_name: data.firstName,
      last_name: data.lastName,
    })
    return response.data
  },

  async verifyRegistration(email: string, otp: string): Promise<any> {
    const response = await api.post('/auth/register/verify', { email, otp })
    return response.data
  },

  async forgotPassword(email: string): Promise<any> {
    const response = await api.post('/auth/forgot-password', { email })
    return response.data
  },

  async resetPassword(email: string, otp: string, newPassword: string): Promise<any> {
    const response = await api.post('/auth/reset-password', {
      email,
      otp,
      new_password: newPassword,
    })
    return response.data
  },

  async resendOtp(email: string, purpose: 'login' | 'register' | 'reset'): Promise<any> {
    const response = await api.post('/auth/resend-otp', { email, purpose })
    return response.data
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<any> {
    const response = await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
    return response.data
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout')
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  },

  async refreshToken(refreshToken: string): Promise<LoginResponse> {
    const response = await api.post('/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  },

  async getCurrentUser(): Promise<any> {
    const response = await api.get('/auth/me')
    return response.data
  },

  async acceptTerms(): Promise<any> {
    const response = await api.post('/auth/accept-terms')
    return response.data
  },

  async acceptPolicies(): Promise<any> {
    const response = await api.post('/auth/accept-policies')
    return response.data
  },

  async setUsername(username: string): Promise<any> {
    const response = await api.post('/auth/username', { username })
    return response.data
  },
}
