import { useEffect, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { createGuest, deleteGuest, getGuests, updateGuest } from '../api/guestsApi'
import { useAuth } from '../context/AuthContext'

const emptyForm = {
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address: '',
}

export default function GuestsPage() {
  const { token } = useAuth()
  const [guests, setGuests] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [notice, setNotice] = useState({ type: '', text: '' })
  const [search, setSearch] = useState('')

  const loadGuests = () => {
    if (!token) return

    setLoading(true)
    getGuests(token)
      .then(setGuests)
      .catch((error) => {
        console.error('Guests load failed', error)
        setNotice({ type: 'error', text: 'Unable to load guests.' })
      })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadGuests()
  }, [token])

  const resetForm = () => {
    setForm(emptyForm)
    setEditingId(null)
    setShowForm(false)
  }

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSubmitting(true)

    try {
      if (editingId) {
        const updatedGuest = await updateGuest(token, editingId, form)
        setGuests((prev) => prev.map((guest) => (guest.id === editingId ? updatedGuest : guest)))
        setNotice({ type: 'success', text: 'Guest updated successfully.' })
      } else {
        const createdGuest = await createGuest(token, form)
        setGuests((prev) => [createdGuest, ...prev])
        setNotice({ type: 'success', text: 'Guest created successfully.' })
      }

      resetForm()
    } catch (error) {
      console.error('Guest save failed', error)
      setNotice({ type: 'error', text: 'Guest save failed. Please check the form.' })
    } finally {
      setSubmitting(false)
    }
  }

  const handleEdit = (guest) => {
    setEditingId(guest.id)
    setForm({
      first_name: guest.first_name,
      last_name: guest.last_name,
      email: guest.email,
      phone: guest.phone,
      address: guest.address || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (guestId) => {
    if (!window.confirm('Delete this guest?')) return

    try {
      await deleteGuest(token, guestId)
      setGuests((prev) => prev.filter((guest) => guest.id !== guestId))
      setNotice({ type: 'success', text: 'Guest deleted successfully.' })
    } catch (error) {
      console.error('Guest delete failed', error)
      setNotice({ type: 'error', text: 'Guest could not be deleted.' })
    }
  }

  const filteredGuests = guests.filter((guest) => {
    const query = search.toLowerCase()
    const fullName = `${guest.first_name} ${guest.last_name}`.toLowerCase()
    return !query || fullName.includes(query) || guest.email.toLowerCase().includes(query) || guest.phone.includes(query)
  })

  return (
    <AppLayout
      eyebrow="Guest experience"
      title="Guests"
      actions={
        <button
          className="primary-btn"
          type="button"
          onClick={() => {
            if (showForm) {
              resetForm()
              return
            }
            setShowForm(true)
            setForm(emptyForm)
            setEditingId(null)
          }}
        >
          {showForm ? 'Close form' : '+ Add guest'}
        </button>
      }
    >
      {notice.text && <div className={`notice ${notice.type}`}>{notice.text}</div>}

      {showForm && (
        <section className="panel form-panel">
          <div className="panel-header">
            <h3>{editingId ? 'Edit guest' : 'Add new guest'}</h3>
          </div>
          <form className="data-form" onSubmit={handleSubmit}>
            <div className="form-grid">
              <label>
                First name
                <input name="first_name" value={form.first_name} onChange={handleChange} required />
              </label>
              <label>
                Last name
                <input name="last_name" value={form.last_name} onChange={handleChange} required />
              </label>
              <label>
                Email
                <input type="email" name="email" value={form.email} onChange={handleChange} required />
              </label>
              <label>
                Phone
                <input name="phone" value={form.phone} onChange={handleChange} required />
              </label>
            </div>
            <label>
              Address
              <textarea name="address" value={form.address} onChange={handleChange} rows="3" placeholder="Optional guest address" />
            </label>
            <div className="form-actions">
              <button type="submit" className="primary-btn" disabled={submitting}>
                {submitting ? 'Saving...' : editingId ? 'Update guest' : 'Save guest'}
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="panel">
        <div className="panel-header">
          <h3>Guest directory</h3>
          <div className="table-controls">
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search guests"
              className="search-input"
            />
            <button className="link-btn" type="button">Search</button>
          </div>
        </div>

        {loading ? (
          <p>Loading guests...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Address</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredGuests.map((guest) => (
                <tr key={guest.id}>
                  <td>{guest.first_name} {guest.last_name}</td>
                  <td>{guest.email}</td>
                  <td>{guest.phone}</td>
                  <td>{guest.address || 'N/A'}</td>
                  <td>
                    <div className="table-actions">
                      <button type="button" className="table-action edit" onClick={() => handleEdit(guest)}>
                        Edit
                      </button>
                      <button type="button" className="table-action delete" onClick={() => handleDelete(guest.id)}>
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </AppLayout>
  )
}
