import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface MobileApp {
  id: number
  name: string
  tagline: string | null
  description: string | null
  version: string
  platform: string
  status: 'upcoming' | 'published'
  banner_image: string | null
  apk_filename: string | null
  apk_size: number | null
  downloads: number
  comments_count: number
  created_at: string
  updated_at: string | null
}

const emptyForm = {
  name: '',
  tagline: '',
  description: '',
  version: '1.0.0',
  platform: 'Android',
  status: 'upcoming' as 'upcoming' | 'published',
}

const formatSize = (bytes: number | null) => {
  if (!bytes) return '-'
  const mb = bytes / (1024 * 1024)
  return mb >= 1 ? `${mb.toFixed(1)} MB` : `${Math.round(bytes / 1024)} KB`
}

const AdminApps = () => {
  const [apps, setApps] = useState<MobileApp[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [bannerFile, setBannerFile] = useState<File | null>(null)
  const [apkFile, setApkFile] = useState<File | null>(null)

  const fetchApps = async () => {
    try {
      setLoading(true)
      const response = await api.get('/admin/apps')
      setApps(response.data.apps || [])
    } catch (error) {
      console.error('Error fetching apps:', error)
      toast.error('Failed to load apps')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchApps()
  }, [])

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.name.trim()) {
      toast.error('Please enter the app name')
      return
    }
    if (form.status === 'published' && !apkFile) {
      toast.error('To publish an app, upload its APK file (or keep it as Coming Soon)')
      return
    }

    try {
      setSaving(true)
      const data = new FormData()
      data.append('name', form.name.trim())
      if (form.tagline.trim()) data.append('tagline', form.tagline.trim())
      if (form.description.trim()) data.append('description', form.description.trim())
      data.append('version', form.version || '1.0.0')
      data.append('platform', form.platform)
      data.append('status', apkFile ? 'published' : form.status)
      if (bannerFile) data.append('banner', bannerFile)
      if (apkFile) data.append('apk', apkFile)

      const response = await api.post('/admin/apps', data, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast.success(response.data.message || 'App published')
      setForm(emptyForm)
      setBannerFile(null)
      setApkFile(null)
      fetchApps()
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to publish app')
    } finally {
      setSaving(false)
    }
  }

  const toggleStatus = async (app: MobileApp) => {
    const next = app.status === 'published' ? 'upcoming' : 'published'
    if (next === 'published' && !app.apk_filename) {
      toast.error('This app has no APK file uploaded - upload one to publish it')
      return
    }
    try {
      const data = new FormData()
      data.append('status', next)
      await api.put(`/admin/apps/${app.id}`, data, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast.success(`App is now ${next === 'published' ? 'published' : 'coming soon'}`)
      fetchApps()
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to update status')
    }
  }

  const deleteApp = async (app: MobileApp) => {
    if (!window.confirm(`Remove "${app.name}" from the site?`)) return
    try {
      await api.delete(`/admin/apps/${app.id}`)
      toast.success('App removed')
      fetchApps()
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to remove app')
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Mobile Apps</h1>
        <p className="text-gray-600">
          Publish applications with a banner and description, and upload the APK
          customers download from the public Apps page.
        </p>
      </div>

      {/* Publish form */}
      <div className="card mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Publish / Announce an App</h2>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label className="label">App name *</label>
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                className="input"
                placeholder="e.g. NOU Store"
                required
              />
            </div>
            <div>
              <label className="label">Version</label>
              <input
                name="version"
                value={form.version}
                onChange={handleChange}
                className="input"
                placeholder="1.0.0"
              />
            </div>
          </div>

          <div>
            <label className="label">Tagline (short line under the name)</label>
            <input
              name="tagline"
              value={form.tagline}
              onChange={handleChange}
              className="input"
              placeholder="e.g. Shop N.O.U products from your phone"
            />
          </div>

          <div>
            <label className="label">Description</label>
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              rows={4}
              className="input"
              placeholder="What does this app do? What is coming in this release?"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label className="label">Platform</label>
              <select name="platform" value={form.platform} onChange={handleChange} className="input">
                <option>Android</option>
                <option>iOS</option>
                <option>Web (PWA)</option>
                <option>Windows</option>
                <option>Cross-platform</option>
              </select>
            </div>
            <div>
              <label className="label">Status</label>
              <select name="status" value={form.status} onChange={handleChange} className="input">
                <option value="upcoming">Coming soon (no download yet)</option>
                <option value="published">Published (APK required)</option>
              </select>
            </div>
            <div>
              <label className="label">Banner image</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setBannerFile(e.target.files?.[0] || null)}
                className="input file:mr-3 file:rounded-lg file:border-0 file:bg-primary-50 file:px-4 file:py-2 file:text-sm file:font-medium file:text-primary-700"
              />
            </div>
          </div>

          <div>
            <label className="label">APK file (download)</label>
            <input
              type="file"
              accept=".apk"
              onChange={(e) => setApkFile(e.target.files?.[0] || null)}
              className="input file:mr-3 file:rounded-lg file:border-0 file:bg-primary-50 file:px-4 file:py-2 file:text-sm file:font-medium file:text-primary-700"
            />
            <p className="text-xs text-gray-500 mt-1">
              Only .apk files. Uploading an APK automatically publishes the app.
            </p>
          </div>

          <button type="submit" disabled={saving} className="btn-primary">
            {saving ? 'Publishing...' : 'Publish App'}
          </button>
        </form>
      </div>

      {/* Apps list */}
      {loading ? (
        <div className="text-center py-16">
          <div className="spinner mx-auto"></div>
        </div>
      ) : apps.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-600">No apps yet - publish your first app above.</p>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {apps.map((app) => (
            <div key={app.id} className="card overflow-hidden">
              {app.banner_image ? (
                <div className="h-32 bg-gray-900 overflow-hidden">
                  <img
                    src={`/api/v1/apps/${app.id}/banner`}
                    alt={app.name}
                    className="w-full h-full object-cover"
                  />
                </div>
              ) : (
                <div className="h-24 bg-gradient-to-br from-primary-800 to-primary-950 flex items-center justify-center">
                  <span className="text-white font-bold text-xl">{app.name.charAt(0)}</span>
                </div>
              )}
              <div className="p-5">
                <div className="flex items-start justify-between gap-3 mb-1">
                  <div>
                    <h3 className="font-bold text-gray-900">{app.name}</h3>
                    {app.tagline && <p className="text-xs text-primary-600">{app.tagline}</p>}
                  </div>
                  <span
                    className={`shrink-0 px-2.5 py-1 rounded-full text-xs font-semibold ${
                      app.status === 'published'
                        ? 'bg-green-50 text-green-700 border border-green-200'
                        : 'bg-amber-50 text-amber-700 border border-amber-200'
                    }`}
                  >
                    {app.status === 'published' ? 'Published' : 'Coming soon'}
                  </span>
                </div>
                <div className="text-xs text-gray-500 mb-3">
                  v{app.version} · {app.platform} · APK: {app.apk_filename || 'not uploaded'} (
                  {formatSize(app.apk_size)}) · {app.downloads} downloads · {app.comments_count} comments
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => toggleStatus(app)}
                    className="btn-secondary text-xs"
                  >
                    {app.status === 'published' ? 'Move to Coming Soon' : 'Publish'}
                  </button>
                  <button
                    onClick={() => deleteApp(app)}
                    className="btn-outline text-xs text-red-600 hover:bg-red-50"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default AdminApps
