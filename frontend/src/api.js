const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

async function request(path, options = {}) {
  const token = localStorage.getItem('token')
  const headers = options.headers || {}
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const errorPayload = await response.json().catch(() => ({}))
    throw new Error(errorPayload.detail || 'Request failed')
  }

  return response.json()
}

export const api = {
  login: (payload) => request('/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
  register: (payload) => request('/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  me: () => request('/auth/me'),
  tasks: (filters = {}) => {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        params.set(key, value)
      }
    })
    const query = params.toString()
    return request(`/tasks${query ? `?${query}` : ''}`)
  },
  createTask: (payload) => request('/tasks', { method: 'POST', body: JSON.stringify(payload) }),
  updateTaskStatus: (taskId, payload) => request(`/tasks/${taskId}/status`, { method: 'PATCH', body: JSON.stringify(payload) }),
  documents: () => request('/documents'),
  uploadDocument: (formData) => request('/documents', { method: 'POST', body: formData }),
  search: (payload) => request('/search', { method: 'POST', body: JSON.stringify(payload) }),
  analytics: () => request('/analytics'),
}
