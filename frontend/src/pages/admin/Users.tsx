import { useEffect, useState } from 'react'
import api from '../../services/api'
import toast from 'react-hot-toast'

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  role: string
  is_active: boolean
  created_at: string
}

const AdminUsers = () => {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [roleFilter, setRoleFilter] = useState('')
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetchUsers()
  }, [roleFilter])

  const fetchUsers = async () => {
    try {
      const params = new URLSearchParams()
      if (roleFilter) params.append('role', roleFilter)
      
      const response = await api.get(`/admin/users?${params}`)
      setUsers(response.data.users)
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleToggleStatus = async (userId: string, currentStatus: boolean) => {
    try {
      await api.put(`/admin/users/${userId}/status`, { is_active: !currentStatus })
      toast.success(`User ${currentStatus ? 'deactivated' : 'activated'} successfully`)
      fetchUsers()
    } catch (error) {
      toast.error('Failed to update user status')
    }
  }

  const fullName = (user: User) => `${user.first_name || ''} ${user.last_name || ''}`.trim()

  const roles = [
    { value: '', label: 'All Roles' },
    { value: 'customer', label: 'Customers' },
    { value: 'applicant', label: 'Applicants' },
    { value: 'admin', label: 'Admins' },
  ]

  const roleColors: Record<string, string> = {
    customer: 'badge-primary',
    applicant: 'badge-success',
    admin: 'badge-warning',
  }

  const filteredUsers = users.filter((user) => {
    const matchesSearch = search === '' || 
      user.email.toLowerCase().includes(search.toLowerCase()) ||
      user.first_name?.toLowerCase().includes(search.toLowerCase()) ||
      user.last_name?.toLowerCase().includes(search.toLowerCase())
    return matchesSearch
  })

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">User Management</h1>
        <p className="text-gray-600">Manage system users and their access.</p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search users..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input"
          />
        </div>
        <div className="sm:w-48">
          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="input"
          >
            {roles.map((role) => (
              <option key={role.value} value={role.value}>{role.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Users Table */}
      <div className="card">
        {loading ? (
          <div className="text-center py-12">
            <div className="spinner mx-auto"></div>
          </div>
        ) : filteredUsers.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">No users found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Joined</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center mr-3">
                          <span className="text-primary-700 font-medium">
                            {user.first_name?.charAt(0)}{user.last_name?.charAt(0)}
                          </span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">
                            {fullName(user)}
                          </p>
                        </div>
                      </div>
                    </td>
                    <td className="text-gray-600">{user.email}</td>
                    <td>
                      <span className={roleColors[user.role] || 'badge-gray'}>
                        {user.role}
                      </span>
                    </td>
                    <td>
                      <span className={user.is_active ? 'badge-success' : 'badge-danger'}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="text-gray-500">
                      {user.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}
                    </td>
                    <td>
                      <button
                        onClick={() => handleToggleStatus(user.id, user.is_active)}
                        className={`text-sm ${user.is_active ? 'text-red-600 hover:text-red-700' : 'text-green-600 hover:text-green-700'}`}
                      >
                        {user.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminUsers