import { useEffect, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { getStaffInvitations, inviteStaff } from '../api/staffApi'
import { useAuth } from '../context/AuthContext'

const emptyForm = {
  email: '',
  role: 'manager',
}

export default function StaffPage() {
  const { token } = useAuth()
  const [invitations, setInvitations] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [notice, setNotice] = useState({ type: '', text: '' })

  const loadInvitations = async () => {
    if (!token) return

    try {
      const data = await getStaffInvitations(token)
      setInvitations(data)
    } catch (error) {
      console.error('Failed to load staff invitations', error)
      setNotice({ type: 'error', text: 'Unable to load staff invitations.' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadInvitations()
  }, [token])

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSubmitting(true)

    try {
      const created = await inviteStaff(token, form)
      setInvitations((prev) => [created, ...prev])
      setForm(emptyForm)
      setNotice({ type: 'success', text: 'Staff invitation sent successfully.' })
    } catch (error) {
      const message =
        error?.response?.data?.message ||
        error?.response?.data?.detail ||
        error?.response?.data?.non_field_errors?.[0] ||
        'Unable to send invitation.'
      setNotice({ type: 'error', text: message })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AppLayout
      eyebrow="Team management"
      title="Staff"
      actions={
        <button className="primary-btn" type="button" onClick={() => window.location.hash = '#invite'}>
          + Invite staff
        </button>
      }
    >
      {notice.text && <div className={`notice ${notice.type}`}>{notice.text}</div>}

      <section className="panel form-panel" id="invite">
        <div className="panel-header">
          <h3>Invite team member</h3>
        </div>
        <form className="data-form" onSubmit={handleSubmit}>
          <div className="form-grid">
            <label>
              Email
              <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="staff@hotel.com" required />
            </label>
            <label>
              Role
              <select name="role" value={form.role} onChange={handleChange}>
                <option value="manager">Manager</option>
                <option value="receptionist">Receptionist</option>
                <option value="housekeeping">Housekeeping</option>
                <option value="cashier">Cashier</option>
              </select>
            </label>
          </div>
          <div className="form-actions">
            <button type="submit" className="primary-btn" disabled={submitting}>
              {submitting ? 'Sending...' : 'Send invitation'}
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h3>Sent invitations</h3>
        </div>

        {loading ? (
          <p>Loading invitations...</p>
        ) : invitations.length === 0 ? (
          <p>No invitations sent yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {invitations.map((invitation) => (
                <tr key={invitation.id}>
                  <td>{invitation.email}</td>
                  <td>{invitation.role}</td>
                  <td>
                    <span className={`status-pill ${invitation.accepted ? 'confirmed' : 'pending'}`}>
                      {invitation.accepted ? 'Accepted' : 'Pending'}
                    </span>
                  </td>
                  <td>{new Date(invitation.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </AppLayout>
  )
}
