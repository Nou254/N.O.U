import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { assessmentService } from '../services/assessmentService'

interface Question {
  id: string
  module: string
  category: string
  part?: string
  question_type?: string
  question_text: string
  options?: { id: string; text: string }[]
  points: number
  order_number?: number
}

interface AssessmentSession {
  id: string
  assessment_id: string
  started_at: string
  time_remaining: number
}

interface AssessmentResult {
  sessionId: string
  score: number
  percentage: number
  totalQuestions: number
  correctAnswers: number
  timeTaken: number
}

interface AssessmentState {
  assessments: any[]
  modules: any | null
  categories: any[]
  currentSession: AssessmentSession | null
  questions: Question[]
  answers: Record<string, string>
  currentQuestionIndex: number
  result: AssessmentResult | null
  loading: boolean
  questionLoading: boolean
  questionError: string | null
  questionsTotal: number
  questionsPerPart: Record<string, number>
  error: string | null
}

const initialState: AssessmentState = {
  assessments: [],
  modules: null,
  categories: [],
  currentSession: null,
  questions: [],
  answers: {},
  currentQuestionIndex: 0,
  result: null,
  loading: false,
  questionLoading: false,
  questionError: null,
  questionsTotal: 29,
  questionsPerPart: {},
  error: null,
}

const extractError = (error: any, fallback: string) =>
  error?.response?.data?.detail || error?.response?.data?.message || fallback

// Async thunks
export const fetchModules = createAsyncThunk(
  'assessment/fetchModules',
  async (_, { rejectWithValue }) => {
    try {
      const response = await assessmentService.getModules()
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error, 'Failed to fetch modules'))
    }
  }
)

export const fetchAssessments = createAsyncThunk(
  'assessment/fetchAssessments',
  async (_, { rejectWithValue }) => {
    try {
      const response = await assessmentService.getAssessments()
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error, 'Failed to fetch assessments'))
    }
  }
)

export const fetchActiveSession = createAsyncThunk(
  'assessment/fetchActiveSession',
  async (guestEmail: string | undefined, { rejectWithValue }) => {
    try {
      const response = await assessmentService.getActiveSession(guestEmail)
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error, 'Failed to resume assessment'))
    }
  }
)

export const fetchPersonnelCategories = createAsyncThunk(
  'assessment/fetchPersonnelCategories',
  async (_, { rejectWithValue }) => {
    try {
      const response = await assessmentService.getPersonnelCategories()
      return response.categories || []
    } catch (error: any) {
      return rejectWithValue(extractError(error, 'Failed to fetch professional categories'))
    }
  }
)

export const startAssessment = createAsyncThunk(
  'assessment/startAssessment',
  async (
    args: {
      assessmentId: string
      electives: string[]
      categoryId?: number
      positionId?: number
      guest?: { email: string; fullName?: string; phone?: string }
    },
    { rejectWithValue }
  ) => {
    try {
      const { assessmentId, electives, categoryId, positionId, guest } = args
      const response = await assessmentService.startAssessment(
        assessmentId,
        electives,
        categoryId,
        positionId,
        guest
      )
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error, 'Failed to start assessment'))
    }
  }
)

export const submitAssessment = createAsyncThunk(
  'assessment/submitAssessment',
  async (
    { sessionId, answers, guestEmail }: { sessionId: string; answers: Record<string, string>; guestEmail?: string },
    { rejectWithValue }
  ) => {
    try {
      const response = await assessmentService.submitAssessment(sessionId, answers, guestEmail)
      return response
    } catch (error: any) {
      return rejectWithValue(extractError(error, 'Failed to submit assessment'))
    }
  }
)

const assessmentSlice = createSlice({
  name: 'assessment',
  initialState,
  reducers: {
    setAnswer: (state, action: PayloadAction<{ questionId: string; answer: string }>) => {
      state.answers[action.payload.questionId] = action.payload.answer
    },
    nextQuestion: (state, action: PayloadAction<number | undefined>) => {
      // Questions are generated on demand, so the navigable ceiling is the
      // assessment total, not the number generated so far.
      const total = action.payload ?? state.questionsTotal ?? state.questions.length
      if (state.currentQuestionIndex < total - 1) {
        state.currentQuestionIndex += 1
      }
    },
    previousQuestion: (state) => {
      if (state.currentQuestionIndex > 0) {
        state.currentQuestionIndex -= 1
      }
    },
    goToQuestion: (state, action: PayloadAction<number>) => {
      state.currentQuestionIndex = action.payload
    },
    clearAssessment: (state) => {
      state.currentSession = null
      state.questions = []
      state.answers = {}
      state.currentQuestionIndex = 0
      state.result = null
      state.questionLoading = false
      state.questionError = null
      state.loading = false
    },
    setQuestionIndex: (state, action: PayloadAction<number>) => {
      state.currentQuestionIndex = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch modules
      .addCase(fetchModules.pending, (state) => {
        state.error = null
      })
      .addCase(fetchModules.fulfilled, (state, action) => {
        state.modules = action.payload
      })
      .addCase(fetchModules.rejected, (state, action) => {
        state.error = action.payload as string
      })
      // Fetch personnel categories
      .addCase(fetchPersonnelCategories.fulfilled, (state, action) => {
        state.categories = action.payload
      })
      // Fetch assessments
      .addCase(fetchAssessments.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchAssessments.fulfilled, (state, action) => {
        state.loading = false
        state.assessments = action.payload
      })
      .addCase(fetchAssessments.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Start assessment
      // Resume active session
      .addCase(fetchActiveSession.pending, (state) => {
        state.error = null
      })
      .addCase(fetchActiveSession.fulfilled, (state, action) => {
        const session = action.payload?.session
        if (session) {
          state.currentSession = session
          state.questions = action.payload.questions || []
          state.answers = {}
          state.currentQuestionIndex = 0
          state.questionError = null
          // Keep the navigator total consistent on resume (falls back to
          // the framework's per-part counts when not present).
          if (action.payload.questions_total) {
            state.questionsTotal = action.payload.questions_total
          }
          if (action.payload.questions_per_part) {
            state.questionsPerPart = action.payload.questions_per_part
          }
        }
      })
      .addCase(fetchActiveSession.rejected, (state, action) => {
        state.error = action.payload as string
      })
      // Start assessment
      .addCase(startAssessment.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(startAssessment.fulfilled, (state, action) => {
        state.loading = false
        state.currentSession = action.payload.session
        state.questions = action.payload.questions || []
        state.answers = {}
        state.currentQuestionIndex = 0
        if (action.payload.questions_total) {
          state.questionsTotal = action.payload.questions_total
        }
        if (action.payload.questions_per_part) {
          state.questionsPerPart = action.payload.questions_per_part
        }
        state.questionError = null
      })
      .addCase(startAssessment.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      // Submit assessment
      .addCase(submitAssessment.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(submitAssessment.fulfilled, (state, action) => {
        state.loading = false
        state.result = action.payload
        state.currentSession = null
      })
      .addCase(submitAssessment.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
  },
})

export const {
  setAnswer,
  nextQuestion,
  previousQuestion,
  goToQuestion,
  setQuestionIndex,
  clearAssessment,
  clearError,
} = assessmentSlice.actions

export default assessmentSlice.reducer