// User Types
export interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  role: 'visitor' | 'customer' | 'applicant' | 'admin' | 'developer' | 'investor'
  isActive: boolean
  lastLogin?: string
  createdAt: string
  updatedAt?: string
  // Company handle (displayed as @handle, e.g. @henrydatabase)
  username?: string | null
  // Place of qualification - the category/position the applicant is assessed in
  qualificationCategoryId?: number | null
  qualificationPositionId?: number | null
  qualificationCategoryName?: string | null
  qualificationPositionName?: string | null
}

export interface Customer extends User {
  companyName?: string
  phone?: string
  address?: string
  city?: string
  country?: string
}

// Auth Types
export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface RegisterData {
  email: string
  password: string
  firstName: string
  lastName: string
  role: string
}

// Product Types
export interface Product {
  id: string
  name: string
  description: string
  category: string
  version: string
  filePath?: string
  fileSize?: number
  downloadCount: number
  isActive: boolean
  createdAt: string
}

export interface ProductVersion {
  id: string
  productId: string
  versionNumber: string
  releaseNotes?: string
  filePath?: string
  fileSize?: number
  isLatest: boolean
  releasedAt: string
}

// Job Types
export interface Job {
  id: string
  title: string
  description: string
  department?: string
  location?: string
  employmentType: string
  requirements?: string
  salaryRange?: string
  status: string
  deadline?: string
  createdAt: string
}

export interface Application {
  id: string
  applicantId: string
  jobId: string
  job?: Job
  coverLetter?: string
  cvFilePath?: string
  status: string
  adminNotes?: string
  submittedAt: string
}

// Assessment Types
export interface Assessment {
  id: string
  title: string
  description?: string
  durationMinutes: number
  totalQuestions: number
  passingScore: number
  isActive: boolean
}

export interface Question {
  id: string
  category: string
  question_text: string
  options?: { id: string; text: string }[]
  correctAnswer?: string
  explanation?: string
  difficultyLevel?: number
  points: number
}

export interface AssessmentSession {
  id: string
  applicantId: string
  assessmentId: string
  startedAt: string
  completedAt?: string
  timeRemaining: number
  score?: number
  percentage?: number
  status: string
}

export interface AssessmentAnswer {
  id: string
  sessionId: string
  questionId: string
  userAnswer?: string
  isCorrect?: boolean
  pointsEarned: number
  answeredAt: string
}

// Support Types
export interface SupportTicket {
  id: string
  customerId: string
  ticketNumber: number
  subject: string
  description: string
  category?: string
  priority: string
  status: string
  assignedTo?: string
  createdAt: string
}

// API Response Types
export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    total: number
    page: number
    limit: number
    pages: number
  }
}

export interface ApiResponse<T> {
  data: T
  message?: string
}

// Dashboard Stats
export interface DashboardStats {
  users: number
  products: number
  jobs: number
  applications: number
  openTickets: number
  assessments: number
}

// Form Types
export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm extends LoginForm {
  firstName: string
  lastName: string
  role: string
  confirmPassword: string
}

export interface TicketForm {
  subject: string
  description: string
  category: string
  priority: string
}

export interface ProjectForm {
  title: string
  description: string
  category: string
  budget?: string
  deadline?: string
}