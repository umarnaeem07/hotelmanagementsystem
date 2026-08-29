import { useEffect, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { getGuests } from '../api/guestsApi'
import {
  getReservations,
  createReservation,
  updateReservation,
  deleteReservation,
  checkInReservation,
  checkOutReservation,
  getReservationServices,
  addReservationService,
  removeReservationService,
} from '../api/reservationsApi'
import { getRooms } from '../api/roomsApi'
import { getServices } from '../api/servicesApi'
import { useAuth } from '../context/AuthContext'

const statusClassMap = {
  reserved: 'pending',
  checked_in: 'checked-in',
  checked_out: 'confirmed',
  cancelled: 'pending',
}

const emptyForm = {
  guest: '',
  room: '',
  check_in: '',
  check_out: '',
  notes: '',
  status: 'reserved',
}

export default function ReservationsPage() {
  const { token } = useAuth()
  const [reservations, setReservations] = useState([])
  const [guests, setGuests] = useState([])
  const [rooms, setRooms] = useState([])
  const [services, setServices] = useState([])
  const [reservationServices, setReservationServices] = useState({})
  const [reservationDrafts, setReservationDrafts] = useState({})
  const [expandedReservationId, setExpandedReservationId] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [notice, setNotice] = useState({ type: '', text: '' })
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const loadData = async () => {
    if (!token) return

    setLoading(true)

    try {
      const [reservationData, guestData, roomData, serviceData] = await Promise.all([
        getReservations(token),
        getGuests(token),
        getRooms(token),
        getServices(token),
      ])

      setReservations(reservationData)
      setGuests(guestData)
      setRooms(roomData)
      setServices(serviceData)
    } catch (error) {
      console.error('Reservation data load failed', error)
      setNotice({ type: 'error', text: 'Unable to load reservation data.' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
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
        guest: Number(form.guest),
        room: Number(form.room),
      }

      if (editingId) {
        const updatedReservation = await updateReservation(token, editingId, payload)
        setReservations((prev) => prev.map((reservation) => (reservation.id === editingId ? updatedReservation : reservation)))
        setNotice({ type: 'success', text: 'Reservation updated successfully.' })
      } else {
        const createdReservation = await createReservation(token, payload)
        setReservations((prev) => [createdReservation, ...prev])
        setNotice({ type: 'success', text: 'Reservation created successfully.' })
      }

      resetForm()
    } catch (error) {
      console.error('Reservation save failed', error)
      setNotice({ type: 'error', text: 'Reservation save failed. Please check the form.' })
    } finally {
      setSubmitting(false)
    }
  }

  const handleEdit = (reservation) => {
    setEditingId(reservation.id)
    setForm({
      guest: reservation.guest || '',
      room: reservation.room || '',
      check_in: reservation.check_in || '',
      check_out: reservation.check_out || '',
      notes: reservation.notes || '',
      status: reservation.status || 'reserved',
    })
    setShowForm(true)
  }

  const handleDelete = async (reservationId) => {
    if (!window.confirm('Delete this reservation?')) return

    try {
      await deleteReservation(token, reservationId)
      setReservations((prev) => prev.filter((reservation) => reservation.id !== reservationId))
      setNotice({ type: 'success', text: 'Reservation deleted successfully.' })
    } catch (error) {
      console.error('Reservation delete failed', error)
      setNotice({ type: 'error', text: 'Reservation could not be deleted.' })
    }
  }

  const handleCheckIn = async (reservationId) => {
    try {
      const data = await checkInReservation(token, reservationId)
      setNotice({ type: 'success', text: data?.message || 'Guest checked in successfully.' })
      await loadData()
    } catch (error) {
      console.error('Check-in failed', error)
      setNotice({ type: 'error', text: error?.response?.data?.message || 'Check-in failed.' })
    }
  }

  const handleCheckOut = async (reservationId) => {
    try {
      const data = await checkOutReservation(token, reservationId)
      setNotice({ type: 'success', text: data?.message || 'Guest checked out successfully.' })
      await loadData()
    } catch (error) {
      console.error('Check-out failed', error)
      setNotice({ type: 'error', text: error?.response?.data?.message || 'Check-out failed.' })
    }
  }

  const filteredReservations = reservations.filter((reservation) => {
    const query = search.toLowerCase()
    const guestLabel = `${reservation.guest_name || reservation.guest || 'Guest'}`.toLowerCase()
    const roomLabel = `${reservation.room_name || reservation.room || 'Room'}`.toLowerCase()
    const matchesSearch = !query || guestLabel.includes(query) || roomLabel.includes(query) || reservation.status.toLowerCase().includes(query)
    const matchesStatus = statusFilter === 'all' || reservation.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const toggleReservationServices = async (reservationId) => {
    const isOpening = expandedReservationId !== reservationId
    setExpandedReservationId(isOpening ? reservationId : null)

    if (isOpening && !reservationServices[reservationId]) {
      try {
        const data = await getReservationServices(token, reservationId)
        setReservationServices((prev) => ({ ...prev, [reservationId]: data }))
      } catch (error) {
        console.error('Reservation service load failed', error)
        setNotice({ type: 'error', text: 'Unable to load reservation services.' })
      }
    }
  }

  const getServiceTotal = (reservationId) =>
    (reservationServices[reservationId] || []).reduce(
      (sum, item) => sum + Number(item.total_price || 0),
      0,
    )

  const handleAddReservationService = async (reservationId) => {
    const selectedServiceId = reservationDrafts[reservationId]

    if (!selectedServiceId) {
      setNotice({ type: 'error', text: 'Select a service before adding it.' })
      return
    }

    try {
      await addReservationService(token, reservationId, {
        service: Number(selectedServiceId),
        quantity: 1,
      })

      setReservationDrafts((prev) => ({ ...prev, [reservationId]: '' }))
      const updatedServices = await getReservationServices(token, reservationId)
      setReservationServices((prev) => ({ ...prev, [reservationId]: updatedServices }))
      setNotice({ type: 'success', text: 'Service added to reservation.' })
    } catch (error) {
      console.error('Add reservation service failed', error)
      setNotice({ type: 'error', text: error?.response?.data?.message || 'Unable to add service.' })
    }
  }

  const handleRemoveReservationService = async (reservationId, reservationServiceId) => {
    try {
      await removeReservationService(token, reservationId, reservationServiceId)
      const updatedServices = await getReservationServices(token, reservationId)
      setReservationServices((prev) => ({ ...prev, [reservationId]: updatedServices }))
      setNotice({ type: 'success', text: 'Service removed from reservation.' })
    } catch (error) {
      console.error('Remove reservation service failed', error)
      setNotice({ type: 'error', text: 'Unable to remove service.' })
    }
  }

  return (
    <AppLayout
      eyebrow="Operations"
      title="Reservations"
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
          {showForm ? 'Close form' : '+ New booking'}
        </button>
      }
    >
      {notice.text && <div className={`notice ${notice.type}`}>{notice.text}</div>}

      {showForm && (
        <section className="panel form-panel">
          <div className="panel-header">
            <h3>{editingId ? 'Edit reservation' : 'Create reservation'}</h3>
          </div>
          <form className="data-form" onSubmit={handleSubmit}>
            <div className="form-grid">
              <label>
                Guest
                <select name="guest" value={form.guest} onChange={handleChange} required>
                  <option value="">Select guest</option>
                  {guests.map((guest) => (
                    <option key={guest.id} value={guest.id}>
                      {guest.first_name} {guest.last_name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Room
                <select name="room" value={form.room} onChange={handleChange} required>
                  <option value="">Select room</option>
                  {rooms.map((room) => (
                    <option key={room.id} value={room.id}>
                      {room.room_number} - {room.room_type}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Stay from
                <input type="date" name="check_in" value={form.check_in} onChange={handleChange} required />
              </label>
              <label>
                Stay to
                <input type="date" name="check_out" value={form.check_out} onChange={handleChange} required />
              </label>
            </div>
            <label>
              Notes
              <textarea name="notes" value={form.notes} onChange={handleChange} rows="3" placeholder="Reservation notes" />
            </label>
            <div className="form-actions">
              <button type="submit" className="primary-btn" disabled={submitting}>
                {submitting ? 'Saving...' : editingId ? 'Update reservation' : 'Save reservation'}
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="panel">
        <div className="panel-header">
          <h3>Booking timeline</h3>
          <div className="table-controls">
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search reservations"
              className="search-input"
            />
            <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} className="select-input">
              <option value="all">All status</option>
              <option value="reserved">Reserved</option>
              <option value="checked_in">Checked in</option>
              <option value="checked_out">Checked out</option>
              <option value="cancelled">Cancelled</option>
            </select>
            <button className="link-btn" type="button">Filter</button>
          </div>
        </div>

        {loading ? (
          <p>Loading reservations...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Guest</th>
                <th>Room</th>
                <th>Stay from</th>
                <th>Stay to</th>
                <th>Total</th>
                <th>Arrival status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredReservations.map((reservation) => (
                <>
                  <tr key={reservation.id}>
                    <td>{reservation.guest_name || reservation.guest || 'Guest'}</td>
                    <td>{reservation.room_name || reservation.room || 'Room'}</td>
                    <td>{reservation.check_in}</td>
                    <td>{reservation.check_out}</td>
                    <td>${Number(reservation.total_amount || 0).toFixed(2)}</td>
                    <td>
                      <span className={`status-pill ${statusClassMap[reservation.status] || 'pending'}`}>
                        {reservation.status}
                      </span>
                    </td>
                    <td>
                      <div className="table-actions">
                        <button type="button" className="table-action edit" onClick={() => toggleReservationServices(reservation.id)}>
                          {expandedReservationId === reservation.id ? 'Hide services' : 'Services'}
                        </button>
                        {reservation.status === 'reserved' && (
                          <button type="button" className="table-action edit" onClick={() => handleCheckIn(reservation.id)}>
                            Check guest in
                          </button>
                        )}
                        {reservation.status === 'checked_in' && (
                          <button type="button" className="table-action edit" onClick={() => handleCheckOut(reservation.id)}>
                            Check guest out
                          </button>
                        )}
                        <button type="button" className="table-action edit" onClick={() => handleEdit(reservation)}>
                          Edit
                        </button>
                        <button type="button" className="table-action delete" onClick={() => handleDelete(reservation.id)}>
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                  {expandedReservationId === reservation.id && (
                    <tr key={`${reservation.id}-service-panel`}>
                      <td colSpan="7">
                        <div style={{ padding: '14px 12px', border: '1px solid #e6e9ef', borderRadius: '12px', background: '#f8fafc' }}>
                          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center', marginBottom: '12px' }}>
                            <select
                              value={reservationDrafts[reservation.id] || ''}
                              onChange={(event) => setReservationDrafts((prev) => ({ ...prev, [reservation.id]: event.target.value }))}
                              style={{ minWidth: '220px' }}
                            >
                              <option value="">Select service</option>
                              {services
                                .filter((service) => service.is_active)
                                .map((service) => (
                                  <option key={service.id} value={service.id}>
                                    {service.name} (${Number(service.price || 0).toFixed(2)})
                                  </option>
                                ))}
                            </select>
                            <button type="button" className="primary-btn" onClick={() => handleAddReservationService(reservation.id)}>
                              Add service
                            </button>
                          </div>

                          {(reservationServices[reservation.id] || []).length === 0 ? (
                            <p style={{ margin: 0, color: '#64748b' }}>No extra services added yet.</p>
                          ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                              {(reservationServices[reservation.id] || []).map((item) => (
                                <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px', padding: '8px 10px', background: 'white', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                                  <span>
                                    {item.service_name} × {item.quantity}
                                  </span>
                                  <strong>${Number(item.total_price || 0).toFixed(2)}</strong>
                                  <button type="button" className="table-action delete" onClick={() => handleRemoveReservationService(reservation.id, item.id)}>
                                    Remove
                                  </button>
                                </div>
                              ))}
                            </div>
                          )}

                          <div style={{ marginTop: '12px', display: 'flex', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap', borderTop: '1px solid #e5e7eb', paddingTop: '12px' }}>
                            <strong>Service subtotal: ${Number(getServiceTotal(reservation.id)).toFixed(2)}</strong>
                            <strong>Grand total: ${(Number(reservation.total_amount || 0) + Number(getServiceTotal(reservation.id))).toFixed(2)}</strong>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </AppLayout>
  )
}
