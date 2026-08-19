import { Routes, Route, Navigate } from 'react-router-dom'
import { useAppSelector } from './hooks/useAppSelector'

// Layouts
import PublicLayout from './layouts/PublicLayout'
import CustomerLayout from './layouts/CustomerLayout'
import ApplicantLayout from './layouts/ApplicantLayout'
import AdminLayout from './layouts/AdminLayout'
import DeveloperLayout from './layouts/DeveloperLayout'
import InvestorLayout from './layouts/InvestorLayout'

// Public pages
import HomePage from './pages/public/HomePage'
import ProductsPage from './pages/public/ProductsPage'
import CareersPage from './pages/public/CareersPage'
import InvestorPage from './pages/public/InvestorPage'
import RequestProjectPage from './pages/public/RequestProjectPage'
import TermsPage from './pages/public/TermsPage'
import PrivacyPage from './pages/public/PrivacyPage'
import SupportPage from './pages/public/SupportPage'
import ComplaintPage from './pages/public/ComplaintPage'
import AppsPage from './pages/public/AppsPage'
import SettingsPage from './pages/public/SettingsPage'
import CommunityChat from './pages/public/Community'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage'
import ChangePasswordPage from './pages/auth/ChangePasswordPage'
import TermsAcceptPage from './pages/auth/TermsAcceptPage'
import PoliciesAcceptPage from './pages/auth/PoliciesAcceptPage'

// Customer pages
import CustomerDashboard from './pages/customer/Dashboard'
import CustomerDownloads from './pages/customer/Downloads'
import CustomerSupport from './pages/customer/Support'
import CustomerProjects from './pages/customer/Projects'
import CustomerNouLite from './pages/customer/NouLite'

// Applicant pages
import ApplicantApplications from './pages/applicant/Applications'
import AssessmentPage from './pages/applicant/Assessment'
import AssessmentResults from './pages/applicant/Results'

// Admin pages
import AdminDashboard from './pages/admin/Dashboard'
import AdminProducts from './pages/admin/Products'
import AdminUsers from './pages/admin/Users'
import AdminAssessments from './pages/admin/Assessments'
import AdminAssessmentResults from './pages/admin/AssessmentResults'
import AdminQuestionBank from './pages/admin/QuestionBank'
import AdminReports from './pages/admin/Reports'
import AdminInvestors from './pages/admin/Investors'
import AdminOnboarding from './pages/admin/Onboarding'
import AdminCompanyProjects from './pages/admin/CompanyProjects'
import AdminNouLiteOrders from './pages/admin/NouLiteOrders'
import AdminAiPool from './pages/admin/AiPool'
import AdminAnnouncements from './pages/admin/Announcements'
import AdminProjectRequests from './pages/admin/ProjectRequests'
import AdminCommunity from './pages/admin/Community'
import AdminPersonnel from './pages/admin/Personnel'
import AdminLifecycle from './pages/admin/Lifecycle'
import AdminRecruitment from './pages/admin/Recruitment'
import AdminSupportContributions from './pages/admin/SupportContributions'
import AdminApps from './pages/admin/Apps'
import AdminComplaints from './pages/admin/Complaints'
import AdminCategoryScreens from './pages/admin/CategoryScreens'
import AdminCategoryDetail from './pages/admin/CategoryDetail'

// Developer / investor pages
import DeveloperProjects from './pages/developer/Projects'
import DeveloperProjectDetail from './pages/developer/ProjectDetail'
import InvestorProjects from './pages/investor/Projects'
import DeveloperCommunity from './pages/developer/Community'
import DeveloperDepartment from './pages/developer/Department'
import DeveloperOpportunities from './pages/developer/Opportunities'

// Protected route component
import ProtectedRoute from './components/auth/ProtectedRoute'

function App() {
  const { isAuthenticated } = useAppSelector((state) => state.auth)

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<PublicLayout />}>
        <Route index element={<HomePage />} />
        <Route path="products" element={<ProductsPage />} />
        <Route path="careers" element={<CareersPage />} />
        <Route path="investors" element={<InvestorPage />} />
        <Route path="request-project" element={<RequestProjectPage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="forgot-password" element={<ForgotPasswordPage />} />
        <Route path="terms" element={<TermsPage />} />
        <Route path="privacy" element={<PrivacyPage />} />
        <Route path="support" element={<SupportPage />} />
        <Route path="complaints" element={<ComplaintPage />} />
        <Route path="apps" element={<AppsPage />} />
        <Route path="settings" element={<SettingsPage />} />
        {/* Community chat - open to everyone, messages publish instantly */}
        <Route path="community" element={<CommunityChat />} />
        {/* Public assessment - NO login required (open to everyone) */}
        <Route path="assessment" element={<AssessmentPage />} />
        <Route path="assessment/:id" element={<AssessmentPage />} />
        {/* N.O.U Lite full chat - NO login/account required (open to everyone) */}
        <Route path="nou-lite" element={<CustomerNouLite />} />
      </Route>

      {/* First-login terms consent gate (any authenticated role) */}
      <Route
        path="/terms-accept"
        element={
          <ProtectedRoute
            isAuthenticated={isAuthenticated}
            allowedRoles={['admin', 'customer', 'applicant', 'developer', 'investor']}
          >
            <TermsAcceptPage />
          </ProtectedRoute>
        }
      />

      {/* First-login organization policies consent gate (approved personnel) */}
      <Route
        path="/policies-accept"
        element={
          <ProtectedRoute
            isAuthenticated={isAuthenticated}
            allowedRoles={['admin', 'customer', 'applicant', 'developer', 'investor']}
          >
            <PoliciesAcceptPage />
          </ProtectedRoute>
        }
      />

      {/* Change password (any authenticated role) */}
      <Route
        path="/change-password"
        element={
          <ProtectedRoute
            isAuthenticated={isAuthenticated}
            allowedRoles={['admin', 'customer', 'applicant', 'developer', 'investor']}
          >
            <ChangePasswordPage />
          </ProtectedRoute>
        }
      />

      {/* Customer routes */}
      <Route
        path="/customer"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated} allowedRoles={['customer']}>
            <CustomerLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<CustomerDashboard />} />
        <Route path="downloads" element={<CustomerDownloads />} />
        <Route path="support" element={<CustomerSupport />} />
        <Route path="projects" element={<CustomerProjects />} />
        <Route path="nou-lite" element={<CustomerNouLite />} />
      </Route>

      {/* Developer portal routes */}
      <Route
        path="/portal"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated} allowedRoles={['developer']}>
            <DeveloperLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DeveloperProjects />} />
        <Route path="opportunities" element={<DeveloperOpportunities />} />
        <Route path="department" element={<DeveloperDepartment />} />
        <Route path="projects/:id" element={<DeveloperProjectDetail />} />
        <Route path="community" element={<DeveloperCommunity />} />
      </Route>

      {/* Investor read-only routes */}
      <Route
        path="/investor"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated} allowedRoles={['investor']}>
            <InvestorLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<InvestorProjects />} />
      </Route>

      {/* Applicant routes */}
      <Route
        path="/applicant"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated} allowedRoles={['applicant']}>
            <ApplicantLayout />
          </ProtectedRoute>
        }
      >
        {/* No applicant dashboard - applicants go straight to the assessment. */}
        <Route index element={<Navigate to="/applicant/assessment/general" replace />} />
        <Route path="applications" element={<ApplicantApplications />} />
        <Route path="assessment/:id" element={<AssessmentPage />} />
        <Route path="results" element={<AssessmentResults />} />
      </Route>

      {/* Admin routes */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated} allowedRoles={['admin']}>
            <AdminLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<AdminDashboard />} />
        <Route path="products" element={<AdminProducts />} />
        <Route path="users" element={<AdminUsers />} />
        <Route path="assessments" element={<AdminAssessments />} />
        <Route path="results" element={<AdminAssessmentResults />} />
        <Route path="question-bank" element={<AdminQuestionBank />} />
        <Route path="reports" element={<AdminReports />} />
        <Route path="investors" element={<AdminInvestors />} />
        <Route path="onboarding" element={<AdminOnboarding />} />
        <Route path="projects" element={<AdminCompanyProjects />} />
        <Route path="nou-lite" element={<AdminNouLiteOrders />} />
        <Route path="ai-pool" element={<AdminAiPool />} />
        <Route path="announcements" element={<AdminAnnouncements />} />
        <Route path="project-requests" element={<AdminProjectRequests />} />
        <Route path="community" element={<AdminCommunity />} />
        <Route path="personnel" element={<AdminPersonnel />} />
        <Route path="lifecycle" element={<AdminLifecycle />} />
        <Route path="recruitment" element={<AdminRecruitment />} />
        <Route path="support-contributions" element={<AdminSupportContributions />} />
        <Route path="apps" element={<AdminApps />} />
        <Route path="complaints" element={<AdminComplaints />} />
        <Route path="categories" element={<AdminCategoryScreens />} />
        <Route path="categories/:categoryId" element={<AdminCategoryDetail />} />
      </Route>

      {/* Catch all - redirect to home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App