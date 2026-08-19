import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface SectionState {
  keys: string[]
  active_key: number
  requests_used: number
  daily_limit: number
  top_up_used: number
}

interface PoolStatus {
  total_keys: number
  configured: boolean
  active: Record<string, SectionState>
  failed: string[]
  cursor: number
  sections_per_day: number
}

interface KeyHealth {
  section: string
  index: number
  masked: string
  requests_today: number
  failed: boolean
  healthy: boolean
}

const AdminAiPool = () => {
  const [status, setStatus] = useState<PoolStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [keyHealth, setKeyHealth] = useState<KeyHealth[]>([])

  const fetchStatus = async () => {
    try {
      setLoading(true)
      const response = await api.get('/admin/ai/pool')
      setStatus(response.data)
    } catch (error) {
      console.error('Error fetching pool status:', error)
      toast.error('Failed to load AI pool status')
    } finally {
      setLoading(false)
    }
  }

  const fetchKeyHealth = async () => {
    try {
      const response = await api.get('/admin/ai/keys')
      setKeyHealth(response.data.keys || [])
    } catch (error) {
      console.error('Error fetching AI key health:', error)
    }
  }

  useEffect(() => {
    fetchStatus()
    fetchKeyHealth()
  }, [])

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">AI Key Pool</h1>
        <p className="text-gray-600">
          Groq API key pool with automatic rotation and per-section daily limits
          (10 keys/day per AI section, +2 top-up if depleted).
        </p>
      </div>

      {loading ? (
        <div className="text-center py-16">
          <div className="spinner mx-auto"></div>
        </div>
      ) : !status ? (
        <div className="card text-center py-12">
          <p className="text-gray-600">Could not load pool status.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card">
              <p className="text-sm text-gray-600">Total keys configured</p>
              <p className="text-3xl font-bold text-gray-900">{status.total_keys}</p>
              <p className="text-xs text-gray-500 mt-1">
                {status.configured ? 'Pool active' : 'No keys configured yet — using the default key'}
              </p>
            </div>
            <div className="card">
              <p className="text-sm text-gray-600">Sections (10 keys/day each)</p>
              <p className="text-3xl font-bold text-gray-900">{Object.keys(status.active || {}).length}</p>
              <p className="text-xs text-gray-500 mt-1">{status.sections_per_day} keys per section per day, +2 top-up</p>
            </div>
            <div className="card">
              <p className="text-sm text-gray-600">Failed keys</p>
              <p className="text-3xl font-bold text-gray-900">{status.failed?.length || 0}</p>
              <p className="text-xs text-gray-500 mt-1">Keys removed from rotation on auth failure</p>
            </div>
          </div>

          {/* Section detail */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Section Usage Today</h2>
            <div className="space-y-4">
              {Object.entries(status.active || {}).map(([section, state]) => {
                const remaining = Math.max(0, state.daily_limit - state.requests_used)
                const pct = Math.min(100, Math.round((state.requests_used / state.daily_limit) * 100))
                return (
                  <div key={section} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <p className="font-medium text-gray-900">{section.replace('_', ' ')}</p>
                        <p className="text-xs text-gray-500">
                          Key #{state.active_key + 1} of {state.keys.length} · top-ups used: {state.top_up_used}
                        </p>
                      </div>
                      <span className="text-sm text-gray-600">
                        {state.requests_used}/{state.daily_limit} requests today ({remaining} left)
                      </span>
                    </div>
                    <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${
                          pct >= 100 ? 'bg-red-500' : pct >= 75 ? 'bg-yellow-500' : 'bg-primary-600'
                        }`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                )
              })}
              {Object.keys(status.active || {}).length === 0 && (
                <p className="text-sm text-gray-500">No sections have been used yet today.</p>
              )}
            </div>
          </div>

          {status.failed && status.failed.length > 0 && (
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Failed Keys</h2>
              <div className="flex flex-wrap gap-2">
                {status.failed.map((key) => (
                  <span key={key} className="badge-danger">
                    ...{key.slice(-8)}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Per-key health report */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">API Key Health Report</h2>
              <button onClick={fetchKeyHealth} className="btn-secondary text-xs">
                Refresh
              </button>
            </div>
            {keyHealth.length === 0 ? (
              <p className="text-sm text-gray-500">No API keys configured - add GROQ_* keys to backend/.env.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200 text-left text-xs text-gray-500 uppercase tracking-wider">
                      <th className="py-2 pr-4">Section</th>
                      <th className="py-2 pr-4">Key</th>
                      <th className="py-2 pr-4">Requests today</th>
                      <th className="py-2">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {keyHealth.map((key) => (
                      <tr key={`${key.section}-${key.index}`} className="border-b border-gray-100">
                        <td className="py-2.5 pr-4 font-medium text-gray-900">{key.section.replace('_', ' ')}</td>
                        <td className="py-2.5 pr-4 font-mono text-xs text-gray-600">{key.masked}</td>
                        <td className="py-2.5 pr-4">{key.requests_today}</td>
                        <td className="py-2.5">
                          {key.failed ? (
                            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-red-50 text-red-700 border border-red-200">
                              <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
                              Failed - skipped today
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
                              <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
                              Healthy
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminAiPool
