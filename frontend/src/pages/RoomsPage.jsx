import { useEffect, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { createRoom, deleteRoom, getRooms, updateRoom } from '../api/roomsApi'
import { useAuth } from '../context/AuthContext'

const roomToneMap = {
  available: 'available',
  reserved: 'pending',
  occupied: 'occupied',
  cleaning: 'cleaning',
  maintenance: 'maintenance',
}

const emptyForm = {
  room_number: '',
  floor: 1,
  room_type: 'standard',
  capacity: 2,
  price_per_night: '120',
  status: 'available',
  description: '',
}

export default function RoomsPage() {
  const { token } = useAuth()
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [notice, setNotice] = useState({ type: '', text: '' })
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const loadRooms = () => {
    if (!token) return

    setLoading(true)
    getRooms(token)
      .then(setRooms)
      .catch((error) => {
        console.error('Rooms load failed', error)
        setNotice({ type: 'error', text: 'Unable to load rooms.' })
      })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadRooms()
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
      const payload = {
        ...form,
        floor: Number(form.floor),
        capacity: Number(form.capacity),
        price_per_night: Number(form.price_per_night),
      }

      if (editingId) {
        const updatedRoom = await updateRoom(token, editingId, payload)
        setRooms((prev) => prev.map((room) => (room.id === editingId ? updatedRoom : room)))
        setNotice({ type: 'success', text: 'Room updated successfully.' })
      } else {
        const createdRoom = await createRoom(token, payload)
        setRooms((prev) => [createdRoom, ...prev])
        setNotice({ type: 'success', text: 'Room created successfully.' })
      }

      resetForm()
    } catch (error) {
      console.error('Room save failed', error)
      setNotice({ type: 'error', text: 'Room save failed. Please check the form.' })
    } finally {
      setSubmitting(false)
    }
  }

  const handleEdit = (room) => {
    setEditingId(room.id)
    setForm({
      room_number: room.room_number,
      floor: room.floor,
      room_type: room.room_type,
      capacity: room.capacity,
      price_per_night: room.price_per_night,
      status: room.status,
      description: room.description || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (roomId) => {
    if (!window.confirm('Delete this room?')) return

    try {
      await deleteRoom(token, roomId)
      setRooms((prev) => prev.filter((room) => room.id !== roomId))
      setNotice({ type: 'success', text: 'Room deleted successfully.' })
    } catch (error) {
      console.error('Room delete failed', error)
      setNotice({ type: 'error', text: 'Room could not be deleted.' })
    }
  }

  const filteredRooms = rooms.filter((room) => {
    const query = search.toLowerCase()
    const matchesSearch =
      !query ||
      room.room_number.toLowerCase().includes(query) ||
      room.room_type.toLowerCase().includes(query) ||
      room.status.toLowerCase().includes(query)

    const matchesStatus = statusFilter === 'all' || room.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <AppLayout
      eyebrow="Operations"
      title="Rooms"
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
          {showForm ? 'Close form' : '+ Add room'}
        </button>
      }
    >
      {notice.text && <div className={`notice ${notice.type}`}>{notice.text}</div>}

      {showForm && (
        <section className="panel form-panel">
          <div className="panel-header">
            <h3>{editingId ? 'Edit room' : 'Add new room'}</h3>
          </div>
          <form className="data-form" onSubmit={handleSubmit}>
            <div className="form-grid">
              <label>
                Room number
                <input name="room_number" value={form.room_number} onChange={handleChange} required />
              </label>
              <label>
                Floor
                <input type="number" name="floor" value={form.floor} onChange={handleChange} required />
              </label>
              <label>
                Type
                <select name="room_type" value={form.room_type} onChange={handleChange}>
                  <option value="standard">Standard</option>
                  <option value="deluxe">Deluxe</option>
                  <option value="suite">Suite</option>
                </select>
              </label>
              <label>
                Capacity
                <input type="number" name="capacity" value={form.capacity} onChange={handleChange} required />
              </label>
              <label>
                Price per night
                <input type="number" step="0.01" name="price_per_night" value={form.price_per_night} onChange={handleChange} required />
              </label>
              <label>
                Status
                <select name="status" value={form.status} onChange={handleChange}>
                  <option value="available">Available</option>
                  <option value="reserved">Reserved</option>
                  <option value="occupied">Occupied</option>
                  <option value="cleaning">Cleaning</option>
                  <option value="maintenance">Maintenance</option>
                </select>
              </label>
            </div>
            <label>
              Description
              <textarea name="description" value={form.description} onChange={handleChange} rows="3" placeholder="Optional room notes" />
            </label>
            <div className="form-actions">
              <button type="submit" className="primary-btn" disabled={submitting}>
                {submitting ? 'Saving...' : editingId ? 'Update room' : 'Save room'}
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="panel">
        <div className="panel-header">
          <h3>Inventory overview</h3>
          <div className="table-controls">
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search rooms"
              className="search-input"
            />
            <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} className="select-input">
              <option value="all">All status</option>
              <option value="available">Available</option>
              <option value="reserved">Reserved</option>
              <option value="occupied">Occupied</option>
              <option value="cleaning">Cleaning</option>
              <option value="maintenance">Maintenance</option>
            </select>
            <button className="link-btn" type="button">Export</button>
          </div>
        </div>

        {loading ? (
          <p>Loading rooms...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Room</th>
                <th>Type</th>
                <th>Floor</th>
                <th>Capacity</th>
                <th>Rate</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredRooms.map((room) => (
                <tr key={room.id}>
                  <td>{room.room_number}</td>
                  <td>{room.room_type}</td>
                  <td>{room.floor}</td>
                  <td>{room.capacity} guests</td>
                  <td>${Number(room.price_per_night).toFixed(2)}</td>
                  <td>
                    <span className={`status-pill ${roomToneMap[room.status] || 'pending'}`}>
                      {room.status}
                    </span>
                  </td>
                  <td>
                    <div className="table-actions">
                      <button type="button" className="table-action edit" onClick={() => handleEdit(room)}>
                        Edit
                      </button>
                      <button type="button" className="table-action delete" onClick={() => handleDelete(room.id)}>
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
