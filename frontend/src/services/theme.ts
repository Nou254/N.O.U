/**
 * Theme manager - lets customers choose a light or dark theme.
 *
 * The choice is persisted in localStorage ("nou_theme") and applied by
 * toggling the "dark" class on <html>. index.css defines the dark palette
 * overrides that activate under .dark.
 */

export type ThemePreference = 'light' | 'dark' | 'system'

const STORAGE_KEY = 'nou_theme'

export function getStoredTheme(): ThemePreference {
  const raw = localStorage.getItem(STORAGE_KEY)
  return raw === 'light' || raw === 'dark' || raw === 'system' ? raw : 'system'
}

export function isDarkPreferred(theme: ThemePreference): boolean {
  if (theme === 'system') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  return theme === 'dark'
}

export function applyTheme(theme: ThemePreference): void {
  const dark = isDarkPreferred(theme)
  document.documentElement.classList.toggle('dark', dark)
  document.documentElement.style.colorScheme = dark ? 'dark' : 'light'
  localStorage.setItem(STORAGE_KEY, theme)
}

/** Apply the persisted theme immediately (before first paint). */
export function initTheme(): void {
  const stored = getStoredTheme()
  applyTheme(stored)
  // Keep following the OS preference when the user chose "system".
  if (stored === 'system') {
    window
      .matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', () => applyTheme('system'))
  }
}
