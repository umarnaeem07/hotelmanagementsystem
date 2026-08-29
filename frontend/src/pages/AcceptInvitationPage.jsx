import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import api from '../api/axios'

const initialForm = {
  username: '',
  password: '',
  confirm_password: '',
}

export default function AcceptInvitationPage() {
  const { token } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    if (!token) {
      setError('Invitation token is missing.')
      setLoading(false)
      return
    }

    if (form.password !== form.confirm_password) {
      setError('Passwords do not match.')
      setLoading(false)
      return
    }

    try {
      const response = await api.post(`/staff/accept-invitation/${token}/`, {
        username: form.username,
        password: form.password,
        confirm_password: form.confirm_password,
      })

      setSuccess(response.data.message || 'Account created successfully.')
      setTimeout(() => navigate('/'), 1500)
    } catch (err) {
      const message =
        err?.response?.data?.message ||
        err?.response?.data?.detail ||
        err?.response?.data?.non_field_errors?.[0] ||
        'Unable to accept invitation. Please try again.'
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

        <h2>Join the hotel team</h2>
        <p>Create your account to accept this staff invitation.</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Username
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder="Choose a username"
              required
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
              name="confirm_password"
              value={form.confirm_password}
              onChange={handleChange}
              placeholder="Confirm password"
              required
            />
          </label>

          {error && <div className="error-box">{error}</div>}
          {success && <div className="success-box">{success}</div>}

          <button type="submit" className="primary-btn full-width" disabled={loading}>
            {loading ? 'Creating account...' : 'Accept invitation'}
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
