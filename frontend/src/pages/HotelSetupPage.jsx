import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AppLayout from '../components/AppLayout'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

const initialForm = {
  name: '',
  address: '',
  phone: '',
  email: '',
  description: '',
}

export default function HotelSetupPage() {
  const navigate = useNavigate()
  const { token } = useAuth()
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

    try {
      await api.post('/hotel/', form, {
        headers: { Authorization: `Bearer ${token}` },
      })
      navigate('/dashboard')
    } catch (err) {
      const message =
        err?.response?.data?.message ||
        err?.response?.data?.detail ||
        err?.response?.data?.non_field_errors?.[0] ||
        'Unable to create your hotel profile.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppLayout
      eyebrow="Setup"
      title="Create hotel profile"
      actions={<button className="primary-btn" type="submit" form="hotel-setup-form" disabled={loading}>{loading ? 'Saving...' : 'Save hotel'}</button>}
    >
      <section className="panel form-panel">
        <div className="panel-header">
          <h3>Hotel details</h3>
        </div>

        <form id="hotel-setup-form" className="data-form" onSubmit={handleSubmit}>
          <div className="form-grid">
            <label>
              Hotel name
              <input name="name" value={form.name} onChange={handleChange} required />
            </label>
            <label>
              Phone
              <input name="phone" value={form.phone} onChange={handleChange} required />
            </label>
            <label>
              Email
              <input type="email" name="email" value={form.email} onChange={handleChange} required />
            </label>
          </div>

          <label>
            Address
            <textarea name="address" value={form.address} onChange={handleChange} rows="3" required />
          </label>

          <label>
            Description
            <textarea name="description" value={form.description} onChange={handleChange} rows="3" placeholder="Optional hotel summary" />
          </label>

          {error && <div className="error-box">{error}</div>}
        </form>
      </section>
    </AppLayout>
  )
}
