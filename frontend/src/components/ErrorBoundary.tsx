import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  message: string
}

/**
 * Top-level error boundary: catches unexpected render/event errors so the user
 * never sees a blank white page. Shows a friendly fallback with a reload
 * action (and reports the error to the console for support).
 */
class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, message: '' }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, message: error?.message || 'Something went wrong' }
  }

  componentDidCatch(error: Error, info: unknown) {
    // Keep the detail in the console for support/debugging (no PII).
    console.error('Unhandled UI error:', error, info)
  }

  handleReload = () => {
    this.setState({ hasError: false, message: '' })
    window.location.href = '/'
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
          <div className="card !p-8 max-w-md w-full text-center">
            <div className="w-14 h-14 rounded-xl bg-primary-600 flex items-center justify-center mx-auto mb-4">
              <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h1 className="text-xl font-bold text-gray-900 mb-2">Something went wrong</h1>
            <p className="text-sm text-gray-600 mb-6">
              An unexpected error occurred while showing this page. Your data is
              safe. Please reload to continue.
            </p>
            <button onClick={this.handleReload} className="btn-primary px-8">
              Reload N.O.U
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}

export default ErrorBoundary
