import api from './api'

export const assessmentService = {
  async getFramework(): Promise<any> {
    const response = await api.get('/assessments/framework')
    return response.data
  },

  async getModules(): Promise<any> {
    const response = await api.get('/assessments/framework')
    return response.data
  },

  async getPersonnelCategories(): Promise<any> {
    const response = await api.get('/personnel/categories')
    return response.data
  },

  async getAssessments(): Promise<any> {
    const response = await api.get('/assessments')
    return response.data
  },

  async getAssessmentById(assessmentId: string): Promise<any> {
    const response = await api.get(`/assessments/${assessmentId}`)
    return response.data
  },

  async startAssessment(
    assessmentId: string,
    electives: string[] = [],
    categoryId?: number,
    positionId?: number,
    guest?: { email: string; fullName?: string; phone?: string }
  ): Promise<any> {
    const payload: any = {}
    if (categoryId && positionId) {
      payload.category_id = categoryId
      payload.position_id = positionId
    } else {
      payload.electives = electives
    }
    if (guest?.email) {
      payload.email = guest.email
      if (guest.fullName) payload.full_name = guest.fullName
      if (guest.phone) payload.phone = guest.phone
    }
    // Groq question generation takes 1-2+ minutes (the axios default is
    // 30s, which would abort the request while the backend is still
    // generating - leaving the applicant with no questions).
    const response = await api.post(`/assessments/${assessmentId}/start`, payload, {
      timeout: 15 * 60 * 1000, // 15 minutes
    })
    return response.data
  },

  async submitAssessment(
    sessionId: string,
    answers: Record<string, string>,
    guestEmail?: string
  ): Promise<any> {
    const payload: any = {
      answers: Object.entries(answers).map(([questionId, answer]) => ({
        question_id: questionId,
        user_answer: answer,
      })),
    }
    if (guestEmail) payload.email = guestEmail
    // AI grading (Groq) of all answers takes several minutes.
    const response = await api.post(`/assessments/sessions/${sessionId}/submit`, payload, {
      timeout: 15 * 60 * 1000, // 15 minutes
    })
    return response.data
  },

  async getSessionStatus(sessionId: string): Promise<any> {
    const response = await api.get(`/assessments/sessions/${sessionId}`)
    return response.data
  },

  async getAssessmentResults(sessionId: string): Promise<any> {
    const response = await api.get(`/assessments/sessions/${sessionId}/results`)
    return response.data
  },

  async getActiveSession(guestEmail?: string): Promise<any> {
    const params = guestEmail ? { email: guestEmail } : {}
    const response = await api.get('/assessments/active', { params })
    return response.data
  },
}
