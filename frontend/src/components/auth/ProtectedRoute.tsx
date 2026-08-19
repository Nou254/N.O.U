import { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAppSelector } from '../../hooks/useAppSelector'

interface ProtectedRouteProps {
  children: ReactNode
  isAuthenticated: boolean
  allowedRoles: string[]
}

const ProtectedRoute = ({ 
  children, 
  isAuthenticated, 
  allowedRoles
}: ProtectedRouteProps) => {
  const location = useLocation()
  const { user } = useAppSelector((state) => state.auth)

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (user && !allowedRoles.includes(user.role)) {
    // Redirect to appropriate dashboard based on role
    const redirectPath = getRedirectPath(user.role)
    return <Navigate to={redirectPath} replace />
  }

  // First-login consent gate: the user must agree to the Terms & Privacy
  // Policy before they can submit details or use the platform.
  if (user && !user.terms_accepted_at && location.pathname !== '/terms-accept') {
    return <Navigate to="/terms-accept" replace />
  }

  // Organization policies consent gate: approved personnel must agree to the
  // N.O.U. Organization Policies document on their first login (issued with
  // their credentials after the admin approves them). Admins manage the
  // process and view the policies from the category screens instead.
  if (
    user &&
    user.role !== 'admin' &&
    !user.policies_accepted_at &&
    location.pathname !== '/policies-accept'
  ) {
    return <Navigate to="/policies-accept" replace />
  }

  return <>{children}</>
}

function getRedirectPath(role: string): string {
  switch (role) {
    case 'admin':
      return '/admin'
    case 'customer':
      return '/customer'
    case 'applicant':
      return '/applicant'
    case 'developer':
      return '/portal'
    case 'investor':
      return '/investor'
    default:
      return '/'
  }
}

export default ProtectedRoute