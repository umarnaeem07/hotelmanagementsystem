import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { loginUser, signupUser } from '../api/authApi'
import { useAuth } from '../context/AuthContext'

const initialForm = {
  username: '',
  email: '',
  phone: '',
  password: '',
  password_confirm: '',
}

export default function SignupPage() {
  const navigate = useNavigate()
  const { setToken, setUser } = useAuth()
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    if (form.password !== form.password_confirm) {
      setError('Passwords do not match.')
      setLoading(false)
      return
    }

    try {
      await signupUser({
        username: form.username,
        email: form.email,
        phone: form.phone,
        password: form.password,
      })

      const loginData = await loginUser(form.username, form.password)
      setToken(loginData.access)
      setUser(loginData.user)
      navigate('/dashboard')
    } catch (err) {
      const message = err?.response?.data?.message || err?.response?.data?.error || 'Sign up failed. Please try again.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="brand-mark small">H</div>
          <div>
            <span>Hotel management</span>
            <strong>Harbor View</strong>
          </div>
        </div>

        <h2>Create account</h2>
        <p>Set up your hotel team account to manage operations.</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Username
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder="Enter username"
              required
            />
          </label>

          <label>
            Email
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="Enter email"
              required
            />
          </label>

          <label>
            Phone
            <input
              type="tel"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              placeholder="Enter phone number"
            />
          </label>

          <label>
            Password
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Create password"
              required
            />
          </label>

          <label>
            Confirm password
            <input
              type="password"
              name="password_confirm"
              value={form.password_confirm}
              onChange={handleChange}
              placeholder="Confirm password"
              required
            />
          </label>

          {error && <div className="error-box">{error}</div>}

          <button type="submit" className="primary-btn full-width" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign up'}
          </button>
        </form>

        <div className="auth-footer">
          <span>Already have an account?</span>
          <Link to="/" className="auth-link">Login</Link>
        </div>
      </div>
    </div>
  )
}
