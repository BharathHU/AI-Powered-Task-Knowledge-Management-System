import { useEffect, useMemo, useState } from 'react'
import { api } from './api'

const emptyLogin = { email: '', password: '' }
const emptyRegister = { name: '', email: '', password: '' }
const emptyTask = { title: '', description: '', assigned_to: '' }
const emptySearch = { query: '', top_k: 5 }

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('token') || '')
  const [user, setUser] = useState(null)
  const [showRegister, setShowRegister] = useState(false)
  const [loginForm, setLoginForm] = useState(emptyLogin)
  const [registerForm, setRegisterForm] = useState(emptyRegister)
  const [taskForm, setTaskForm] = useState(emptyTask)
  const [searchForm, setSearchForm] = useState(emptySearch)
  const [documentTitle, setDocumentTitle] = useState('')
  const [documentFile, setDocumentFile] = useState(null)
  const [tasks, setTasks] = useState([])
  const [documents, setDocuments] = useState([])
  const [searchResults, setSearchResults] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [taskFilters, setTaskFilters] = useState({ status: '', assigned_to: '' })
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  const isAdmin = user?.role?.name === 'admin'

  const loadDashboard = async () => {
    const taskRequests = [api.tasks(taskFilters)]
    if (isAdmin) {
      taskRequests.push(api.analytics())
    }

    const [taskData, analyticsData] = await Promise.all(taskRequests)
    setTasks(taskData)
    setAnalytics(isAdmin ? analyticsData : null)
    if (isAdmin) {
      const docs = await api.documents()
      setDocuments(docs)
    }
  }

  useEffect(() => {
    const init = async () => {
      if (!token) return
      try {
        const me = await api.me()
        setUser(me)
      } catch (error) {
        localStorage.removeItem('token')
        setToken('')
      }
    }
    init()
  }, [token])

  useEffect(() => {
    if (!user) return
    loadDashboard().catch((error) => setMessage(error.message))
  }, [user, taskFilters])

  const handleLogin = async (event) => {
    event.preventDefault()
    setBusy(true)
    setMessage('')
    try {
      const response = await api.login(loginForm)
      localStorage.setItem('token', response.access_token)
      setToken(response.access_token)
      const me = await api.me()
      setUser(me)
      setMessage('Logged in successfully')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setBusy(false)
    }
  }

  const handleRegister = async (event) => {
    event.preventDefault()
    setBusy(true)
    setMessage('')
    try {
      const response = await api.register(registerForm)
      localStorage.setItem('token', response.access_token)
      setToken(response.access_token)
      const me = await api.me()
      setUser(me)
      setMessage('Account created successfully')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setBusy(false)
    }
  }

  const handleTaskCreate = async (event) => {
    event.preventDefault()
    setBusy(true)
    try {
      await api.createTask({
        title: taskForm.title,
        description: taskForm.description,
        assigned_to: taskForm.assigned_to ? Number(taskForm.assigned_to) : null,
      })
      setTaskForm(emptyTask)
      await loadDashboard()
      setMessage('Task created')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setBusy(false)
    }
  }

  const handleUpload = async (event) => {
    event.preventDefault()
    if (!documentFile) return
    setBusy(true)
    try {
      const formData = new FormData()
      formData.append('title', documentTitle)
      formData.append('file', documentFile)
      await api.uploadDocument(formData)
      setDocumentTitle('')
      setDocumentFile(null)
      await loadDashboard()
      setMessage('Document uploaded')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setBusy(false)
    }
  }

  const handleSearch = async (event) => {
    event.preventDefault()
    setBusy(true)
    try {
      const results = await api.search({
        query: searchForm.query,
        top_k: Number(searchForm.top_k),
      })
      setSearchResults(results)
      await loadDashboard()
      setMessage('Search complete')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setBusy(false)
    }
  }

  const handleTaskComplete = async (taskId) => {
    setBusy(true)
    try {
      await api.updateTaskStatus(taskId, { status: 'completed' })
      await loadDashboard()
      setMessage('Task marked completed')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setBusy(false)
    }
  }

const handleTaskDelete = async (taskId) => {
    setBusy(true)
    try {
      await api.deleteTask(taskId)
      await loadDashboard()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setBusy(false)
    }
  }

  const stats = useMemo(() => {
    if (!analytics) {
      return []
    }
    return [
      { label: 'Total Tasks', value: analytics.total_tasks },
      { label: 'Completed', value: analytics.completed_tasks },
      { label: 'Pending', value: analytics.pending_tasks },
    ]
  }, [analytics])

  if (!user) {
    return (
      <div className="auth-shell">
        <div className="auth-card">
          <p className="eyebrow">AI Task & Knowledge</p>
          {showRegister ? (
            <>
              <h1>Create Account</h1>
              <p className="muted">Register a new user account to get started.</p>
              <form className="stack" onSubmit={handleRegister}>
                <label>
                  Name
                  <input value={registerForm.name} onChange={(event) => setRegisterForm({ ...registerForm, name: event.target.value })} />
                </label>
                <label>
                  Email
                  <input value={registerForm.email} onChange={(event) => setRegisterForm({ ...registerForm, email: event.target.value })} />
                </label>
                <label>
                  Password
                  <input type="password" value={registerForm.password} onChange={(event) => setRegisterForm({ ...registerForm, password: event.target.value })} />
                </label>
                <button disabled={busy} type="submit">{busy ? 'Registering...' : 'Register'}</button>
              </form>
              <p className="muted" style={{ marginTop: 12, textAlign: 'center' }}>
                Already have an account?{' '}
                <button className="secondary" style={{ display: 'inline', padding: '4px 12px' }} onClick={() => setShowRegister(false)}>
                  Sign in
                </button>
              </p>
            </>
          ) : (
            <>
              <h1>Sign in</h1>
              <p className="muted">Use your account or register a new one.</p>
              <form className="stack" onSubmit={handleLogin}>
                <label>
                  Email
                  <input value={loginForm.email} onChange={(event) => setLoginForm({ ...loginForm, email: event.target.value })} />
                </label>
                <label>
                  Password
                  <input type="password" value={loginForm.password} onChange={(event) => setLoginForm({ ...loginForm, password: event.target.value })} />
                </label>
                <button disabled={busy} type="submit">{busy ? 'Signing in...' : 'Login'}</button>
              </form>
              <p className="muted" style={{ marginTop: 12, textAlign: 'center' }}>
                Don't have an account?{' '}
                <button className="secondary" style={{ display: 'inline', padding: '4px 12px' }} onClick={() => setShowRegister(true)}>
                  Register
                </button>
              </p>
            </>
          )}
          {message ? <p className="message">{message}</p> : null}
        </div>
      </div>
    )
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">AI-Powered Task & Knowledge Management</p>
          <h1>Task operations, semantic search, and analytics in one dashboard.</h1>
          <p className="muted">Signed in as {user.name} · {user.role.name}</p>
        </div>
        <button
          className="secondary"
          onClick={() => {
            localStorage.removeItem('token')
            setToken('')
            setUser(null)
            setTasks([])
            setDocuments([])
            setAnalytics(null)
            setSearchResults([])
          }}
        >
          Log out
        </button>
      </header>

      {message ? <div className="notice">{message}</div> : null}

      <section className="stats-grid">
        {stats.map((stat) => (
          <article key={stat.label} className="stat-card">
            <span>{stat.label}</span>
            <strong>{stat.value}</strong>
          </article>
        ))}
      </section>

      <section className="content-grid">
        <div className="panel">
          <div className="panel-head">
            <h2>Tasks</h2>
            <div className="filters">
              <select value={taskFilters.status} onChange={(event) => setTaskFilters({ ...taskFilters, status: event.target.value })}>
                <option value=""  style={{backgroundColor:'darkblue'}}>All</option>
                <option value="pending"  style={{backgroundColor:'darkblue'}}>Pending</option>
                <option value="completed"  style={{backgroundColor:'darkblue'}}>Completed</option>
              </select>
              <input
                placeholder="assigned_to"
                value={taskFilters.assigned_to}
                onChange={(event) => setTaskFilters({ ...taskFilters, assigned_to: event.target.value })}
              />
            </div>
          </div>
          {isAdmin ? (
            <form className="stack compact" onSubmit={handleTaskCreate}>
              <input placeholder="Task title" value={taskForm.title} onChange={(event) => setTaskForm({ ...taskForm, title: event.target.value })} />
              <textarea placeholder="Task description" rows="4" value={taskForm.description} onChange={(event) => setTaskForm({ ...taskForm, description: event.target.value })} />
              <input placeholder="Assigned user ID" value={taskForm.assigned_to} onChange={(event) => setTaskForm({ ...taskForm, assigned_to: event.target.value })} />
              <button disabled={busy} type="submit">Create task</button>
            </form>
          ) : null}
          <div className="card-list">
            {tasks.map((task) => (
              <article key={task.id} className="task-card">
                <div>
                  <span className={`pill ${task.status}`}>{task.status}</span>
                  <h3>{task.title}</h3>
                  <p>{task.description}</p>
                </div>
<div className="task-meta">
                  <span>Assigned: {task.assigned_to_user ? `${task.assigned_to_user.name} (ID: ${task.assigned_to})` : 'Unassigned'}</span>
                  <span>Created by: {task.created_by_user?.name || task.created_by}</span>
                </div>
                {task.status !== 'completed' ? (
                  <button className="secondary" disabled={busy} onClick={() => handleTaskComplete(task.id)}>
                    Mark completed
                  </button>
                ) : null}
                {isAdmin ? (
                  <button className="danger" disabled={busy} onClick={() => handleTaskDelete(task.id)} style={{ marginLeft: 8 }}>
                    Delete
                  </button>
                ) : null}
              </article>
            ))}
          </div>
        </div>

        <div className="side-column">
          <div className="panel">
            <div className="panel-head">
              <h2>Knowledge Search</h2>
            </div>
            <form className="stack compact" onSubmit={handleSearch}>
              <textarea placeholder="Ask a semantic question" rows="4" value={searchForm.query} onChange={(event) => setSearchForm({ ...searchForm, query: event.target.value })} />
              <input type="number" min="1" max="10" value={searchForm.top_k} onChange={(event) => setSearchForm({ ...searchForm, top_k: event.target.value })} />
              <button disabled={busy} type="submit">Search</button>
            </form>
            <div className="card-list">
              {searchResults.map((result, index) => (
                <article key={`${result.document_id}-${index}`} className="result-card">
                  <span className="pill accent">{result.document_title}</span>
                  <p>{result.chunk_text}</p>
                  <small>Score {result.score.toFixed(3)}</small>
                </article>
              ))}
            </div>
          </div>

          {isAdmin ? (
            <div className="panel">
              <div className="panel-head">
                <h2>Upload Document</h2>
              </div>
              <form className="stack compact" onSubmit={handleUpload}>
                <input placeholder="Document title" value={documentTitle} onChange={(event) => setDocumentTitle(event.target.value)} />
                <input type="file" accept=".txt,.pdf" onChange={(event) => setDocumentFile(event.target.files?.[0] || null)} />
                <button disabled={busy} type="submit">Upload</button>
              </form>
              <div className="card-list">
                {documents.map((document) => (
                  <article key={document.id} className="result-card">
                    <strong>{document.title}</strong>
                    <small>{document.file_name}</small>
                  </article>
                ))}
              </div>
            </div>
          ) : null}

          <div className="panel">
            <div className="panel-head">
              <h2>Analytics</h2>
            </div>
            {analytics ? (
              <div className="analytics-stack">
                {analytics.top_search_queries?.length ? (
                  analytics.top_search_queries.map((item) => (
                    <div key={item.query} className="analytics-row">
                      <span>{item.query}</span>
                      <strong>{item.count}</strong>
                    </div>
                  ))
                ) : (
                  <p className="muted">No search history yet.</p>
                )}
              </div>
            ) : (
              <p className="muted">Analytics unavailable.</p>
            )}
          </div>
        </div>
      </section>
    </div>
  )
}

export default App

