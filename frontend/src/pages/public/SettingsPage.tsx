import { useEffect, useState } from 'react'
import { applyTheme, getStoredTheme, ThemePreference } from '../../services/theme'
import toast from 'react-hot-toast'

const THEME_OPTIONS: { value: ThemePreference; label: string; description: string; icon: string }[] = [
  {
    value: 'light',
    label: 'Light',
    description: 'Bright, clean interface for daytime use.',
    icon: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z',
  },
  {
    value: 'dark',
    label: 'Dark',
    description: 'Easy on the eyes in low light and at night.',
    icon: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z',
  },
  {
    value: 'system',
    label: 'System',
    description: 'Follow the theme of your device or browser.',
    icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
  },
]

const SettingsPage = () => {
  const [theme, setTheme] = useState<ThemePreference>('system')

  useEffect(() => {
    setTheme(getStoredTheme())
  }, [])

  const handleThemeChange = (value: ThemePreference) => {
    setTheme(value)
    applyTheme(value)
    toast.success(`${value.charAt(0).toUpperCase() + value.slice(1)} theme applied`)
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-gray-600">
          Customize how N.O.U. Digital Systems looks and works for you.
        </p>
      </div>

      {/* Appearance */}
      <div className="card mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-1">Appearance</h2>
        <p className="text-sm text-gray-500 mb-6">
          Choose the theme you prefer. Your choice is saved on this device and applies
          across the whole site.
        </p>

        <div className="grid sm:grid-cols-3 gap-4">
          {THEME_OPTIONS.map((option) => {
            const selected = theme === option.value
            return (
              <button
                key={option.value}
                onClick={() => handleThemeChange(option.value)}
                className={`border-2 rounded-2xl p-5 text-left transition-all ${
                  selected
                    ? 'border-primary-500 bg-primary-50 shadow-sm'
                    : 'border-gray-200 bg-white hover:border-primary-300'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${selected ? 'bg-primary-600' : 'bg-gray-100'}`}>
                    <svg
                      className={`w-6 h-6 ${selected ? 'text-white' : 'text-gray-500'}`}
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={option.icon} />
                    </svg>
                  </div>
                  <span className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${selected ? 'border-primary-600' : 'border-gray-300'}`}>
                    {selected && <span className="w-2.5 h-2.5 rounded-full bg-primary-600"></span>}
                  </span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">{option.label}</h3>
                <p className="text-xs text-gray-500">{option.description}</p>
              </button>
            )
          })}
        </div>
      </div>

      {/* Account (when signed in) */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-1">Account</h2>
        <p className="text-sm text-gray-500 mb-6">
          Manage your profile, password and dashboard access.
        </p>
        <div className="flex flex-wrap gap-3">
          <a href="/change-password" className="btn-secondary">Change password</a>
          <a href="/login" className="btn-primary">Sign in</a>
        </div>
      </div>
    </div>
  )
}

export default SettingsPage
