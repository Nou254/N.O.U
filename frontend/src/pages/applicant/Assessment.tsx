import { useEffect, useMemo, useRef, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '../../hooks/useAppSelector'
import {
  fetchAssessments,
  fetchModules,
  fetchActiveSession,
  fetchPersonnelCategories,
  startAssessment,
  setAnswer,
  nextQuestion,
  previousQuestion,
  goToQuestion,
  submitAssessment,
  clearAssessment,
} from '../../store/assessmentSlice'
import MathText from '../../components/MathText'
import MathEditor from '../../components/MathEditor'
import toast from 'react-hot-toast'

const PART_LABELS: Record<string, string> = {
  common: 'Common Assessment',
  category: 'Category Assessment',
  position: 'Position Assessment',
  practical: 'Practical Assessment',
  professional: 'Professional Assessment',
}

const AssessmentPage = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const dispatch = useAppDispatch()
  const {
    assessments,
    modules,
    categories,
    currentSession,
    questions,
    answers,
    currentQuestionIndex,
    loading,
    questionLoading,
    questionError,
    questionsTotal,
    questionsPerPart,
    error,
  } = useAppSelector((state) => state.assessment)
  const authUser = useAppSelector((state) => state.auth.user)

  // ---- Local UI state ----------------------------------------------------
  const [selectedAssessmentId, setSelectedAssessmentId] = useState<string | null>(null)
  const [categoryId, setCategoryId] = useState<number | null>(null)
  const [positionId, setPositionId] = useState<number | null>(null)
  const [showConfirm, setShowConfirm] = useState(false)
  const [timeRemaining, setTimeRemaining] = useState(0)
  const [guestEmail, setGuestEmail] = useState('')
  const [guestName, setGuestName] = useState('')
  const [guestPhone, setGuestPhone] = useState('')
  const [savedCategoryName, setSavedCategoryName] = useState('')
  const [submittedEmail, setSubmittedEmail] = useState<string | null>(null)
  const submittedRef = useRef(false)
  // Set when saved progress is restored; the next write is skipped so the
  // slice's reset (answers = {}) can't clobber the restored answers.
  const restorePendingRef = useRef(false)

  // Guests are identified by email - no login required (the assessment is
  // open to everyone; credentials are only issued to those who qualify).
  const isGuest = !authUser

  // Identity + category can arrive from the Careers apply form (via router
  // state) so the applicant goes straight into the assessment.
  const applyState = (location.state || {}) as {
    fullName?: string
    email?: string
    phone?: string
    categoryId?: number
    categoryName?: string
  }

  // ---- Data loading ------------------------------------------------------
  useEffect(() => {
    const fromApply = applyState.email?.trim()
    const savedEmail =
      fromApply || localStorage.getItem('nou_guest_email') || ''
    setGuestEmail(savedEmail)
    if (applyState.fullName) {
      setGuestName(applyState.fullName)
      sessionStorage.setItem('nou_apply_name', applyState.fullName)
    } else {
      const savedName = sessionStorage.getItem('nou_apply_name')
      if (savedName) setGuestName(savedName)
    }
    if (applyState.phone) {
      setGuestPhone(applyState.phone)
      sessionStorage.setItem('nou_apply_phone', applyState.phone)
    } else {
      const savedPhone = sessionStorage.getItem('nou_apply_phone')
      if (savedPhone) setGuestPhone(savedPhone)
    }
    if (fromApply) {
      localStorage.setItem('nou_guest_email', fromApply)
      // Survive a page refresh: remember the category chosen at application.
      if (applyState.categoryId) {
        sessionStorage.setItem('nou_apply_category', String(applyState.categoryId))
      }
      if (applyState.categoryName) {
        sessionStorage.setItem('nou_apply_category_name', applyState.categoryName)
        setSavedCategoryName(applyState.categoryName)
      }
    } else {
      // Page refresh mid-flow: restore the exact position the applicant was
      // at (category, position and chosen assessment) instead of bouncing
      // back to the careers page / assessment list.
      const savedCategory = sessionStorage.getItem('nou_apply_category')
      if (savedCategory) setCategoryId(Number(savedCategory))
      const savedPosition = sessionStorage.getItem('nou_apply_position')
      if (savedPosition) setPositionId(Number(savedPosition))
      const savedAssessment = sessionStorage.getItem('nou_apply_assessment')
      if (savedAssessment) setSelectedAssessmentId(savedAssessment)
      const savedCatName = sessionStorage.getItem('nou_apply_category_name')
      if (savedCatName) setSavedCategoryName(savedCatName)
    }
    dispatch(fetchActiveSession(savedEmail || undefined))
    dispatch(fetchAssessments())
    dispatch(fetchModules())
    dispatch(fetchPersonnelCategories())
    return () => {
      dispatch(clearAssessment())
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dispatch])

  // Arriving from the Careers apply form: pre-select the chosen category and
  // skip the assessment-list phase so the applicant lands on the
  // category/position picker with their identity already filled in.
  useEffect(() => {
    if (!applyState.email || currentSession) return
    if (applyState.categoryId) {
      setCategoryId(applyState.categoryId)
      sessionStorage.setItem('nou_apply_category', String(applyState.categoryId))
    }
    if (!selectedAssessmentId && assessments.length > 0) {
      setSelectedAssessmentId(String(assessments[0].id))
      sessionStorage.setItem('nou_apply_assessment', String(assessments[0].id))
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [applyState.email, assessments, currentSession])

  // Drop a stale restored assessment id if the assessment no longer exists.
  useEffect(() => {
    if (selectedAssessmentId && assessments.length > 0) {
      const exists = assessments.some((a) => String(a.id) === String(selectedAssessmentId))
      if (!exists) {
        setSelectedAssessmentId(null)
        sessionStorage.removeItem('nou_apply_assessment')
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedAssessmentId, assessments])

  // ---- Timer (seeded from the server's session time_remaining) ----------
  useEffect(() => {
    if (currentSession) {
      setTimeRemaining(currentSession.time_remaining)
      submittedRef.current = false
    }
  }, [currentSession])

  useEffect(() => {
    if (timeRemaining > 0 && currentSession) {
      const timer = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            clearInterval(timer)
            handleSubmit(true)
            return 0
          }
          return prev - 1
        })
      }, 1000)
      return () => clearInterval(timer)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeRemaining, currentSession])

  // ---- Exam progress: survive a page refresh mid-assessment ------------
  // Restore typed answers + question index once a (resumed) session loads.
  useEffect(() => {
    if (!currentSession) return
    const key = `nou_assessment_${currentSession.id}`
    try {
      const saved = localStorage.getItem(key)
      if (saved) {
        const parsed = JSON.parse(saved)
        let dispatched = false
        if (parsed.answers && typeof parsed.answers === 'object') {
          Object.entries(parsed.answers).forEach(([qid, ans]) => {
            if (typeof ans === 'string' && ans.trim()) {
              dispatch(setAnswer({ questionId: qid, answer: ans }))
              dispatched = true
            }
          })
        }
        if (typeof parsed.index === 'number') {
          dispatch(goToQuestion(Math.min(parsed.index, totalQuestions - 1)))
          dispatched = true
        }
        if (dispatched) restorePendingRef.current = true
      }
    } catch { /* ignore corrupted storage */ }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentSession])

  // Save answers + position as the applicant works, so a refresh never
  // loses their progress.
  useEffect(() => {
    if (!currentSession) return
    // Right after restoring saved progress, skip one write so the slice's
    // reset (answers = {}) doesn't clobber the answers just restored.
    if (restorePendingRef.current) {
      restorePendingRef.current = false
      return
    }
    const key = `nou_assessment_${currentSession.id}`
    try {
      localStorage.setItem(key, JSON.stringify({ answers, index: currentQuestionIndex }))
    } catch { /* storage full - ignore */ }
  }, [answers, currentQuestionIndex, currentSession])

  // ---- Safety net: a session is active but its questions never landed in
  // state (interrupted start / resume that returned an empty payload).
  // Re-fetch the stored session questions from /active so the exam renders
  // instead of showing an endless "Preparing…" spinner.
  const refetchAttemptedRef = useRef(false)
  const [questionLoadFailed, setQuestionLoadFailed] = useState(false)
  const reloadSessionQuestions = () => {
    setQuestionLoadFailed(false)
    dispatch(fetchActiveSession(isGuest ? guestEmail.trim() : undefined))
      .unwrap()
      .then((payload: any) => {
        // The resume endpoint returned no questions for this session.
        if (!payload?.session || !(payload.questions || []).length) {
          setQuestionLoadFailed(true)
        }
      })
      .catch(() => {
        setQuestionLoadFailed(true)
      })
  }
  useEffect(() => {
    if (!currentSession || questions.length > 0 || refetchAttemptedRef.current) return
    refetchAttemptedRef.current = true
    reloadSessionQuestions()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentSession, questions.length])

  // ---- Derived values ----------------------------------------------------
  const examPhase = Boolean(currentSession)
  const selectionPhase = !examPhase && Boolean(selectedAssessmentId)
  const listPhase = !examPhase && !selectionPhase

  // Total question count drives navigation bounds even when questions are
  // generated one at a time (on demand).
  const totalQuestions =
    questionsTotal > 0
      ? questionsTotal
      : (modules?.parts || []).reduce(
          (sum: number, p: any) => sum + (Number(p.questions) || 0),
          0
        ) || 29

  const currentQuestion = questions[currentQuestionIndex]
  const isMathQuestion = currentQuestion?.module === 'Mathematics'

  const answeredCount = useMemo(
    () => questions.filter((q) => (answers[q.id] || '').trim()).length,
    [questions, answers]
  )

  // Navigator structure: the fixed per-part question counts (common ->
  // category -> position -> practical -> professional) with the count of
  // questions generated so far in each part.
  const questionsByPart = useMemo(() => {
    const counts: Record<string, number> = {}
    for (const q of questions) {
      const key = q.part || 'position'
      counts[key] = (counts[key] || 0) + 1
    }
    const perPart = Object.keys(questionsPerPart).length
      ? questionsPerPart
      : (modules?.parts || []).reduce((acc: Record<string, number>, p: any) => {
          if (p?.part) acc[p.part] = Number(p.questions) || 0
          return acc
        }, {})
    const grouped: {
      part: string
      label: string
      total: number
      generated: number
      startIndex: number
    }[] = []
    let cursor = 0
    for (const part of ['common', 'category', 'position', 'practical', 'professional']) {
      const total = perPart[part] || 0
      if (!total) continue
      grouped.push({
        part,
        label: PART_LABELS[part] || part,
        total,
        generated: counts[part] || 0,
        startIndex: cursor,
      })
      cursor += total
    }
    return grouped
  }, [questions, questionsPerPart, modules])

  const selectedCategory = categories.find((c) => c.id === categoryId)
  const positions = selectedCategory?.positions || []

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    const s = seconds % 60
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }

  // ---- Actions -----------------------------------------------------------
  const handlePickAssessment = (assessmentId: string) => {
    // Normalize to a string: the API returns numeric ids and the stale-check
    // effect below compares with String(a.id), so a raw number here would be
    // cleared immediately and the applicant would bounce back to the list.
    setSelectedAssessmentId(String(assessmentId))
    sessionStorage.setItem('nou_apply_assessment', String(assessmentId))
    // Pre-select the applicant's saved place of qualification (chosen at
    // application/registration) so they are assessed where they chose.
    const savedCategoryId = authUser?.qualification_category_id ?? null
    const savedPositionId = authUser?.qualification_position_id ?? null
    if (savedCategoryId && categories.some((c) => c.id === savedCategoryId)) {
      setCategoryId(savedCategoryId)
      setPositionId(savedPositionId)
    } else {
      setCategoryId(null)
      setPositionId(null)
    }
  }

  const handleStartAssessment = async () => {
    if (!selectedAssessmentId) return
    if (!categoryId) {
      toast.error('Select your professional category to continue')
      return
    }
    if (!positionId) {
      toast.error('Select your position under this category to continue')
      return
    }
    if (isGuest && !guestEmail.trim()) {
      toast.error('Please enter your email address to start the assessment')
      return
    }
    if (isGuest && !guestName.trim()) {
      toast.error('Please enter your full name')
      return
    }
    if (isGuest) {
      localStorage.setItem('nou_guest_email', guestEmail.trim())
    }
    // Persist the exact assessment position so a refresh resumes right here.
    if (categoryId) sessionStorage.setItem('nou_apply_category', String(categoryId))
    if (positionId) sessionStorage.setItem('nou_apply_position', String(positionId))
    if (selectedAssessmentId) sessionStorage.setItem('nou_apply_assessment', selectedAssessmentId)
    if (guestName.trim()) sessionStorage.setItem('nou_apply_name', guestName.trim())
    if (guestPhone.trim()) sessionStorage.setItem('nou_apply_phone', guestPhone.trim())
    try {
      await dispatch(
        startAssessment({
          assessmentId: selectedAssessmentId,
          electives: [],
          categoryId,
          positionId,
          guest: isGuest
            ? { email: guestEmail.trim(), fullName: guestName.trim(), phone: guestPhone.trim() }
            : undefined,
        })
      ).unwrap()
      toast.success('Assessment started! Good luck!')
    } catch (error: any) {
      const message =
        error?.response?.data?.detail || error?.message || String(error)
      // If a previous start attempt actually created the session server-side
      // (e.g. the request was interrupted), resume it instead of erroring so
      // the questions always render.
      if (typeof message === 'string' && /active session/i.test(message)) {
        try {
          await dispatch(
            fetchActiveSession(isGuest ? guestEmail.trim() : undefined)
          ).unwrap()
          toast.success('Resuming your assessment - questions are ready!')
        } catch {
          toast.error('Your session is ready but could not be loaded. Please refresh the page.')
        }
      } else {
        toast.error(message)
      }
    }
  }

  const handleAnswerChange = (questionId: string, answer: string) => {
    dispatch(setAnswer({ questionId, answer }))
  }

  const handleSubmit = async (force = false) => {
    if (!currentSession || submittedRef.current) return
    submittedRef.current = true

    const unansweredCount = questions.length - answeredCount
    if (!force && unansweredCount > 0) {
      submittedRef.current = false
      const confirmed = window.confirm(
        `You have ${unansweredCount} unanswered question(s). Are you sure you want to submit?`
      )
      if (!confirmed) return
    }

    try {
      await dispatch(
        submitAssessment({
          sessionId: currentSession.id,
          answers,
          guestEmail: isGuest ? guestEmail.trim() : undefined,
        })
      ).unwrap()
      // Exam is over - drop the locally saved progress for this session.
      try {
        localStorage.removeItem(`nou_assessment_${currentSession.id}`)
      } catch { /* ignore */ }
      toast.success('Assessment submitted successfully!')
      if (isGuest) {
        // Guests cannot sign in to view results - show a completion screen
        // instead (the results are emailed to the address provided).
        setSubmittedEmail(guestEmail.trim())
      } else {
        navigate('/applicant/results')
      }
    } catch (error) {
      submittedRef.current = false
      toast.error(error as string)
    }
  }

  // =========================================================================
  // EXAM PAGE LOCK
  // =========================================================================
  // While an assessment is in progress the applicant stays on the exam page:
  // in-app navigation (nav links, footer, N.O.U Lite widget, any button that
  // calls navigate()), the browser Back/Forward buttons and tab refresh/close
  // are all intercepted so the exam cannot be left or reset mid-flight. The
  // lock engages the moment a session starts (or is resumed) and releases
  // automatically once the assessment is submitted (currentSession -> null).
  const examLocked = examPhase
  const lockNoticeRef = useRef(0)
  useEffect(() => {
    if (!examLocked) return

    const examPath = window.location.pathname
    const examUrl = examPath + window.location.search

    const notice = () => {
      const now = Date.now()
      if (now - lockNoticeRef.current < 1500) return // throttle toasts
      lockNoticeRef.current = now
      toast.error('You cannot leave the assessment while it is in progress.')
    }

    // 1) Warn on refresh / tab close (native dialog - the exam resumes on
    //    reload, so a confirmed refresh is safe).
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault()
      e.returnValue = ''
    }

    // 2) Block router navigation away from the exam page. Every react-router
    //    <Link>, useNavigate() call and the N.O.U Lite widget go through
    //    window.history.pushState/replaceState, so patching those two
    //    catches all in-app navigation (same-page changes stay allowed).
    const originalPush = window.history.pushState.bind(window.history)
    const originalReplace = window.history.replaceState.bind(window.history)
    const leavesExam = (url: string | URL | null | undefined) => {
      if (!url) return false
      try {
        return new URL(url, window.location.origin).pathname !== examPath
      } catch {
        return false
      }
    }
    const patchedPush: typeof originalPush = (state, title, url) => {
      if (leavesExam(url)) {
        notice()
        return
      }
      return originalPush(state, title, url)
    }
    const patchedReplace: typeof originalReplace = (state, title, url) => {
      if (leavesExam(url)) {
        notice()
        return
      }
      return originalReplace(state, title, url)
    }
    window.history.pushState = patchedPush
    window.history.replaceState = patchedReplace

    // 3) Browser Back/Forward buttons: bounce straight back to the exam URL
    //    (react-router batching keeps the exam mounted - no flicker).
    const handlePopState = () => {
      if (window.location.pathname === examPath) return
      notice()
      navigate(examUrl, { replace: true })
    }
    window.addEventListener('popstate', handlePopState)

    // 4) Backup for raw <a href> links that bypass the router entirely (they
    //    would otherwise trigger a full page reload away from the exam).
    const handleClick = (e: MouseEvent) => {
      const target = e.target as Element | null
      const anchor = target?.closest?.('a[href]') as HTMLAnchorElement | null
      if (!anchor) return
      const href = anchor.getAttribute('href') || ''
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return
      try {
        const url = new URL(href, window.location.origin)
        if (url.origin !== window.location.origin || url.pathname === examPath) return
      } catch {
        return
      }
      e.preventDefault()
      e.stopPropagation()
      notice()
    }
    document.addEventListener('click', handleClick, true)

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
      window.removeEventListener('popstate', handlePopState)
      document.removeEventListener('click', handleClick, true)
      window.history.pushState = originalPush
      window.history.replaceState = originalReplace
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [examLocked])

  // =========================================================================
  // PHASE 1 — Assessment list
  // =========================================================================
  if (listPhase) {
    return (
      <div>
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Employment Assessment</h1>
          <p className="text-gray-600">
            A five-part assessment tailored to your professional category and
            position - 3 hours 30 minutes, 20 questions drawn at random from a bank of
            100 questions built for your career. No multiple-choice questions: you answer
            with written explanations, scenarios, debugging, design and practical tasks.
          </p>
          <p className="text-sm text-primary-700 bg-primary-50 border border-primary-200 rounded-lg px-3 py-2 mt-3">
            No login required. Enter your email and full name to take the assessment - your
            results are emailed to you. Login credentials are only issued if you qualify.
          </p>
        </div>

        {/* Guest identity - no account required */}
        {isGuest && (
          <div className="card mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-1">Your details</h2>
            <p className="text-sm text-gray-500 mb-4">
              Enter the email your results will be sent to.
            </p>
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label className="label">Full name *</label>
                <input
                  type="text"
                  value={guestName}
                  onChange={(e) => setGuestName(e.target.value)}
                  className="input"
                  placeholder="e.g. Jane Mwangi"
                />
              </div>
              <div>
                <label className="label">Email address *</label>
                <input
                  type="email"
                  value={guestEmail}
                  onChange={(e) => setGuestEmail(e.target.value)}
                  className="input"
                  placeholder="you@example.com"
                />
              </div>
              <div>
                <label className="label">Phone number</label>
                <input
                  type="tel"
                  value={guestPhone}
                  onChange={(e) => setGuestPhone(e.target.value)}
                  className="input"
                  placeholder="e.g. 0712 345 678"
                />
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-4">
              Tip: you can also attach your CV when applying via the Careers page - it goes
              straight to our HR team.
            </p>
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : assessments.length === 0 ? (
          <div className="card text-center py-12">
            <h3 className="text-lg font-bold text-gray-900 mb-2">
              Could not load assessments
            </h3>
            <p className="text-gray-600 text-sm mb-6">
              {error || 'The assessment list could not be loaded. Please check your connection and retry.'}
            </p>
            <button
              onClick={() => {
                dispatch(fetchAssessments())
                dispatch(fetchModules())
              }}
              className="btn-primary"
            >
              Retry
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {(assessments as any[]).map((assessment) => (
              <div key={assessment.id} className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {assessment.title}
                </h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {assessment.description}
                </p>
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>210 minutes</span>
                  <span>5 parts · 20 questions</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">Qualifying: 80%</span>
                  <button
                    onClick={() => handlePickAssessment(assessment.id)}
                    className="btn-primary text-sm"
                  >
                    Continue
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }

  // =========================================================================
  // GUEST COMPLETION — results are emailed (no account to sign in to)
  // =========================================================================
  if (submittedEmail && isGuest) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center py-16">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-10 h-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-3">Assessment Submitted!</h2>
          <p className="text-gray-600 mb-2">
            Thank you. Your answers have been recorded and are now being graded.
          </p>
          <p className="text-gray-600 mb-8">
            Your results will be emailed to <strong>{submittedEmail}</strong> within 2 hours.
            If you qualify, the email will include your login credentials.
          </p>
          <div className="flex justify-center gap-3">
            <button
              onClick={() => navigate('/careers')}
              className="btn-secondary"
            >
              Back to Careers
            </button>
            <button
              onClick={() => navigate('/')}
              className="btn-primary"
            >
              Go to Home
            </button>
          </div>
        </div>
      </div>
    )
  }

  // =========================================================================
  // PHASE 2 — Category + position selection
  // =========================================================================
  if (selectionPhase) {
    const frameworkParts = modules?.parts || []
    return (
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Choose Your Profession</h1>
          <p className="text-gray-600">
            Select your professional category and position. The assessment is built around
            your choice - no single exam for every applicant.
          </p>
          {isGuest && (applyState.email || guestEmail) && (
            <div className="text-sm text-primary-700 bg-primary-50 border border-primary-200 rounded-lg px-3 py-2 mt-3 space-y-0.5">
              <p>
                <strong>{applyState.fullName || guestName}</strong> ·{' '}
                <span>{applyState.email || guestEmail}</span>
              </p>
              {(applyState.categoryName || savedCategoryName) && (
                <p>
                  Applied for <strong>{applyState.categoryName || savedCategoryName}</strong>{' '}
                  - keep it or change it below.
                </p>
              )}
            </div>
          )}
          {authUser?.qualification_category_name && (
            <p className="text-sm text-primary-700 bg-primary-50 border border-primary-200 rounded-lg px-3 py-2 mt-3">
              Your saved place of qualification:{' '}
              <strong>{authUser.qualification_category_name}</strong>
              {authUser.qualification_position_name
                ? ` / ${authUser.qualification_position_name}`
                : ''}{' '}
              - you can keep it or change it here.
            </p>
          )}
        </div>

        {/* Rules card */}
        <div className="card mb-8 bg-gradient-to-r from-primary-600 to-primary-800 text-white">
          <h3 className="text-lg font-semibold mb-4">Assessment Structure</h3>
          <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4 text-sm">
            {(frameworkParts as any[]).map((part) => (
              <div key={part.part}>
                <div className="text-primary-100 font-medium">{part.label}</div>
                <div className="text-xs text-primary-100/80 mt-1">
                  {part.questions} questions
                </div>
                <div className="text-xs text-primary-100/60 mt-1">{part.description}</div>
              </div>
            ))}
          </div>
          <p className="text-primary-100 text-sm mt-4">
            Question types: short answer, written explanation, scenario, practical,
            debugging, design and project - strictly no multiple choice. Competency is
            classified as Not Qualified (0-49%), Developing (50-64%), Competent (65-79%),
            N.O.U. Qualified (80-89%) or Advanced (90-100%). 80%+ qualifies you for
            consideration.
          </p>
        </div>

        {/* Category selection */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Professional Category</h2>
          {categories.length === 0 ? (
            <p className="text-sm text-gray-500">Loading categories...</p>
          ) : (
            <div className="grid sm:grid-cols-2 gap-3">
              {(categories as any[]).map((cat) => {
                const selected = categoryId === cat.id
                return (
                  <button
                    key={cat.id}
                    onClick={() => {
                      setCategoryId(cat.id)
                      setPositionId(null)
                      sessionStorage.setItem('nou_apply_category', String(cat.id))
                      sessionStorage.removeItem('nou_apply_position')
                    }}
                    className={`text-left p-4 rounded-xl border-2 transition-all ${
                      selected
                        ? 'border-primary-500 bg-primary-50 shadow-sm'
                        : 'border-gray-200 bg-white hover:border-primary-300 hover:bg-primary-50/50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className={`font-medium ${selected ? 'text-primary-800' : 'text-gray-800'}`}>
                        {cat.name}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {cat.positions?.length || 0} positions
                    </p>
                  </button>
                )
              })}
            </div>
          )}
        </div>

        {/* Position selection */}
        {categoryId && (
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Position</h2>
            <div className="grid sm:grid-cols-2 gap-3">
              {positions.map((pos: any) => {
                const selected = positionId === pos.id
                return (
                  <button
                    key={pos.id}
                    onClick={() => {
                      setPositionId(pos.id)
                      sessionStorage.setItem('nou_apply_position', String(pos.id))
                    }}
                    className={`text-left p-4 rounded-xl border-2 transition-all ${
                      selected
                        ? 'border-primary-500 bg-primary-50 shadow-sm'
                        : 'border-gray-200 bg-white hover:border-primary-300 hover:bg-primary-50/50'
                    }`}
                  >
                    <span className={`font-medium ${selected ? 'text-primary-800' : 'text-gray-800'}`}>
                      {pos.name}
                    </span>
                  </button>
                )
              })}
            </div>
          </div>
        )}

        <div className="flex items-center justify-between">
          <button onClick={() => setSelectedAssessmentId(null)} className="btn-secondary">
            Back
          </button>
          <button
            onClick={handleStartAssessment}
            disabled={!categoryId || !positionId || loading}
            className="btn-primary disabled:opacity-50"
          >
            {loading ? 'Generating questions...' : 'Start Assessment'}
          </button>
        </div>

        {/* Question-generation loading overlay (Groq takes ~1-2 minutes) */}
        {loading && (
          <div className="modal-overlay">
            <div className="card max-w-md w-full text-center py-10 px-8">
              <div className="relative w-20 h-20 mx-auto mb-6">
                <div className="absolute inset-0 rounded-full border-4 border-primary-100 dark:border-primary-900"></div>
                <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-primary-600 animate-spin"></div>
                <div className="absolute inset-3 rounded-full bg-primary-50 dark:bg-primary-900/40 flex items-center justify-center">
                  <svg className="w-8 h-8 text-primary-600 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
              </div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Preparing your assessment</h2>
              <p className="text-gray-600 text-sm mb-6">
                {questionLoading
                  ? 'Drawing your randomized 20 questions from the career question bank…'
                  : 'Please wait a moment — your questions are being prepared.'}
              </p>
              <div className="flex items-center justify-center gap-2 text-primary-600 text-sm font-medium">
                <span className="spinner inline-block w-4 h-4 border-2"></span>
                Preparing…
              </div>
            </div>
          </div>
        )}
      </div>
    )
  }

  // =========================================================================
  // PHASE 3 — Exam in progress (5 parts, questions generated one at a time)
  // =========================================================================
  const progress = ((currentQuestionIndex + 1) / Math.max(totalQuestions, 1)) * 100
  const partLabel = currentQuestion?.part
    ? PART_LABELS[currentQuestion.part] || 'Position Assessment'
    : questionsByPart.find((g) => currentQuestionIndex < g.startIndex + g.total)?.label ||
      'Position Assessment'

  // The current question may still be generating (on-demand) - show a clear
  // loading card instead of a blank screen.
  const questionPending = !currentQuestion && examPhase
  // If the session is active but the questions genuinely cannot be loaded
  // (start/resume returned nothing), show an error card with Retry instead of
  // an endless spinner.
  const showQuestionError = Boolean(questionError || questionLoadFailed)

  return (
    <div className="max-w-4xl mx-auto">
      {/* Sticky header with part + timer */}
      <div className="card mb-6 sticky top-4 z-10">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="badge-primary">{partLabel}</span>
              {currentQuestion?.points != null && <span className="badge-gray">{currentQuestion.points} pts</span>}
              <span className="badge-success">Graded</span>
              {currentQuestion?.question_type && (
                <span className="badge-gray capitalize">
                  {currentQuestion.question_type.replace('_', ' ')}
                </span>
              )}
            </div>
            <h2 className="text-lg font-semibold text-gray-900 mt-2">
              Question {currentQuestionIndex + 1} of {totalQuestions}
            </h2>
            <div className="w-64 bg-gray-200 rounded-full h-2 mt-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${Math.min(progress, 100)}%` }}
              />
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-500 font-medium uppercase tracking-wide mb-1">
              Time Remaining
            </div>
            <div
              className={`text-2xl font-bold tabular-nums ${
                timeRemaining < 600 ? 'text-red-600 animate-pulse' : 'text-gray-900'
              }`}
            >
              {formatTime(timeRemaining)}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {answeredCount} / {totalQuestions} answered
            </div>
          </div>
        </div>
      </div>

      {/* Question card - or the on-demand generation loader */}
      {questionPending ? (
        <div className="card mb-6 text-center py-16">
          {showQuestionError ? (
            <>
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-5">
                <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Could not load your questions
              </h3>
              <p className="text-gray-600 text-sm mb-6">
                {questionError ||
                  'Your session is ready but its questions could not be loaded. Please retry.'}
              </p>
              <div className="flex justify-center gap-3">
                <button
                  onClick={() => {
                    refetchAttemptedRef.current = false
                    reloadSessionQuestions()
                  }}
                  className="btn-primary"
                >
                  Retry
                </button>
                <button onClick={() => window.location.reload()} className="btn-secondary">
                  Reload Page
                </button>
              </div>
            </>
          ) : (
            <>
              <div className="relative w-20 h-20 mx-auto mb-6">
                <div className="absolute inset-0 rounded-full border-4 border-primary-100 dark:border-primary-900"></div>
                <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-primary-600 animate-spin"></div>
                <div className="absolute inset-3 rounded-full bg-primary-50 dark:bg-primary-900/40 flex items-center justify-center">
                  <svg className="w-8 h-8 text-primary-600 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Preparing question {currentQuestionIndex + 1} of {totalQuestions}
              </h3>
              <p className="text-gray-600 text-sm">
                Loading your question from the assessment bank — this only takes a moment.
              </p>
              <div className="flex items-center justify-center gap-2 text-primary-600 text-sm font-medium mt-6">
                <span className="spinner inline-block w-4 h-4 border-2"></span>
                Loading…
              </div>
            </>
          )}
        </div>
      ) : (
        <div className="card mb-6">
          <h3
            className="text-xl text-gray-900 mb-6 leading-relaxed select-none"
            style={{ userSelect: 'none' }}
            onCopy={(e) => e.preventDefault()}
            onCut={(e) => e.preventDefault()}
            onContextMenu={(e) => e.preventDefault()}
            title="Question text is protected — copying is disabled."
          >
            <MathText text={currentQuestion?.question_text} />
          </h3>

          <div>
            <label className="label">
              Your answer
              {isMathQuestion && (
                <span className="ml-2 text-xs font-medium text-primary-600">
                  — show your methods and working
                </span>
              )}
            </label>

            {isMathQuestion ? (
              <MathEditor
                value={answers[currentQuestion?.id] || ''}
                onChange={(value) => handleAnswerChange(currentQuestion?.id, value)}
              />
            ) : (
              <textarea
                value={answers[currentQuestion?.id] || ''}
                onChange={(e) => handleAnswerChange(currentQuestion?.id, e.target.value)}
                onPaste={(e) => e.preventDefault()}
                rows={10}
                className="input w-full"
                placeholder="Write a detailed, well-structured answer. Depth of reasoning, trade-off awareness, and practical experience are evaluated."
              />
            )}

            <p className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 mt-3">
              Pasting is disabled to keep your assessment genuine — please type
              your answer. Questions are protected and answers are screened
              for authenticity.
            </p>

            <p className="text-sm text-gray-500 mt-2 flex items-start gap-1">
              <svg className="w-4 h-4 inline text-primary-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span>
                Your answers are graded and the results are reviewed by our administration.
                No multiple-choice: answer with your own reasoning.
              </span>
            </p>
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={() => dispatch(previousQuestion())}
          disabled={currentQuestionIndex === 0 || questionLoading}
          className="btn-secondary disabled:opacity-40"
        >
          Previous
        </button>

        {currentQuestionIndex < totalQuestions - 1 ? (
          <button
            onClick={() => dispatch(nextQuestion(totalQuestions))}
            disabled={questionPending && !currentQuestion}
            className={`btn-primary ${questionPending && !currentQuestion ? 'disabled:opacity-50' : ''}`}
          >
            {questionPending ? 'Preparing…' : 'Next'}
          </button>
        ) : (
          <button onClick={() => setShowConfirm(true)} className="btn-primary">
            Submit Assessment
          </button>
        )}
      </div>

      {/* Question navigator grouped by part (pending questions shown as placeholders) */}
      <div className="card">
        <h4 className="text-sm font-medium text-gray-700 mb-1">Question Navigator</h4>
        <p className="text-xs text-gray-400 mb-3">
          Your 20 questions were drawn at random from the 100-question bank for your
          career. Each part is weighted into your final score.
        </p>
        <div className="space-y-4">
          {questionsByPart.map((group) => {
            const answeredInGroup = Array.from({ length: group.total }, (_, i) => group.startIndex + i).filter(
              (idx) => {
                const q = questions[idx]
                return q && (answers[q.id] || '').trim()
              }
            ).length
            return (
              <div key={group.part}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-gray-600 uppercase tracking-wide">
                    {group.label}
                  </span>
                  <span className="text-xs text-gray-400">
                    {answeredInGroup}/{group.total} answered · {group.generated} ready
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {Array.from({ length: group.total }, (_, offset) => {
                    const index = group.startIndex + offset
                    const q = questions.find((qq) => qq.order_number === index + 1)
                    if (!q) {
                      return (
                        <button
                          key={`${group.part}-pending-${offset}`}
                          disabled
                          title={`${group.label} - Q${offset + 1} (will be generated when you reach it)`}
                          className="w-9 h-9 rounded-lg text-xs font-medium border-2 border-dashed border-gray-200 text-gray-300 cursor-not-allowed"
                        >
                          {offset + 1}
                        </button>
                      )
                    }
                    const answered = Boolean((answers[q.id] || '').trim())
                    return (
                      <button
                        key={q.id}
                        onClick={() => dispatch(goToQuestion(index))}
                        title={`${group.label} - Q${offset + 1}`}
                        className={`w-9 h-9 rounded-lg text-xs font-medium transition-colors ${
                          index === currentQuestionIndex
                            ? 'bg-primary-500 text-white ring-2 ring-primary-300'
                            : answered
                            ? 'bg-green-100 text-green-700 hover:bg-green-200'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {offset + 1}
                      </button>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Confirm Submit Modal */}
      {showConfirm && (
        <div className="modal-overlay" onClick={() => setShowConfirm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Submit Assessment?</h2>
            <p className="text-gray-600 mb-6">
              You have answered {answeredCount} out of {questions.length} questions.
              {questions.length - answeredCount > 0 && (
                <span className="text-red-600">
                  {' '}You have {questions.length - answeredCount} unanswered question(s).
                </span>
              )}
            </p>
            <p className="text-sm text-gray-500 mb-6">
              Your results will be emailed to you within 2 hours of submission.
            </p>
            <div className="flex justify-end space-x-3">
              <button onClick={() => setShowConfirm(false)} className="btn-secondary">
                Cancel
              </button>
              <button
                onClick={() => {
                  setShowConfirm(false)
                  handleSubmit()
                }}
                disabled={loading}
                className="btn-primary"
              >
                {loading ? 'Submitting...' : 'Submit'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AssessmentPage
