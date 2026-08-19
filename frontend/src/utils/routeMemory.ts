import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'

// ---------------------------------------------------------------------------
// Route memory: keep the progress of every page the visitor leaves, so they
// never lose what they typed or where they scrolled when they come back.
// Backed by sessionStorage (survives in-tab refreshes, cleared per tab).
// ---------------------------------------------------------------------------

const PREFIX = 'nou.route-memory'

export function routeMemoryKey(key: string): string {
  return `${PREFIX}:${key}`
}

export function saveRouteState(key: string, value: unknown) {
  try {
    sessionStorage.setItem(routeMemoryKey(key), JSON.stringify(value))
  } catch {
    // storage full or blocked - silently ignore
  }
}

export function loadRouteState<T>(key: string, fallback: T): T {
  try {
    const raw = sessionStorage.getItem(routeMemoryKey(key))
    if (raw == null) return fallback
    return JSON.parse(raw) as T
  } catch {
    return fallback
  }
}

/**
 * useRouteMemory: like useState, but the value is saved per route and form,
 * so navigating away to another page and coming back restores exactly what
 * the visitor had typed (a refresh keeps it too).
 */
export function useRouteMemory<T>(key: string, initial: T) {
  const location = useLocation()
  const storageKey = `${location.pathname}:${key}`
  const [value, setValue] = useState<T>(() => loadRouteState(storageKey, initial))
  useEffect(() => {
    saveRouteState(storageKey, value)
  }, [storageKey, value])
  return [value, setValue] as const
}

/**
 * ScrollMemory: remembers where the visitor scrolled on each page and puts
 * them back there when they return (sessionStorage per route).
 */
export function ScrollMemory() {
  const location = useLocation()
  const pathname = location.pathname

  useEffect(() => {
    const key = routeMemoryKey(`scroll:${pathname}`)

    const save = () => {
      try {
        sessionStorage.setItem(key, String(window.scrollY))
      } catch {
        // ignore
      }
    }
    const restore = () => {
      let saved = 0
      try {
        saved = Number(sessionStorage.getItem(key) || 0)
      } catch {
        saved = 0
      }
      if (saved > 0) {
        requestAnimationFrame(() => {
          window.scrollTo({ top: saved, behavior: 'auto' })
        })
      }
    }

    restore()
    window.addEventListener('scroll', save, { passive: true })
    window.addEventListener('beforeunload', save)
    return () => {
      save()
      window.removeEventListener('scroll', save)
      window.removeEventListener('beforeunload', save)
    }
  }, [pathname])

  return null
}
