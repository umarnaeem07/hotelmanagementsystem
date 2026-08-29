import { useEffect, useMemo, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { createInvoice, generateAdditionalInvoice, updateInvoiceStatus } from '../api/invoicesApi'
import { getReservations, getReservationServices } from '../api/reservationsApi'
import { useAuth } from '../context/AuthContext'

export default function InvoicesPage() {
  const { token } = useAuth()
  const [reservations, setReservations] = useState([])
  const [serviceTotals, setServiceTotals] = useState({})
  const [search, setSearch] = useState('')
  const [notice, setNotice] = useState({ type: '', text: '' })
  const [loading, setLoading] = useState(true)

  const loadData = async () => {
    if (!token) return

    try {
      const reservationData = await getReservations(token)
      setReservations(reservationData)

      const serviceMap = {}
      await Promise.all(
        reservationData.map(async (reservation) => {
          const services = await getReservationServices(token, reservation.id)
          serviceMap[reservation.id] = services.reduce(
            (sum, item) => sum + Number(item.total_price || 0),
            0,
          )
        }),
      )

      setServiceTotals(serviceMap)
    } catch (error) {
      console.error('Failed to load reservations', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [token])

  const filteredReservations = useMemo(() => {
    const query = search.toLowerCase()
    return reservations.filter((reservation) => {
      const guestName = `${reservation.guest_name || reservation.guest || 'Guest'}`.toLowerCase()
      const roomName = `${reservation.room_name || reservation.room || 'Room'}`.toLowerCase()
      return !query || guestName.includes(query) || roomName.includes(query) || reservation.status.toLowerCase().includes(query)
    })
  }, [reservations, search])

  const handleCreateInvoice = async (reservationId) => {
    try {
      const invoice = await createInvoice(token, reservationId)
      setNotice({ type: 'success', text: `Invoice ${invoice.invoice_number} created.` })
      const refreshedReservations = await getReservations(token)
      setReservations(refreshedReservations)
    } catch (error) {
      console.error('Invoice creation failed', error)
      setNotice({ type: 'error', text: 'Unable to create invoice for this reservation.' })
    }
  }

  const handleStatusUpdate = async (reservationId, invoiceStatus) => {
    try {
      const reservation = reservations.find((item) => item.id === reservationId)
      const invoiceId = reservation?.invoice_id

      if (!invoiceId) {
        setNotice({ type: 'error', text: 'No invoice exists for this reservation yet.' })
        return
      }

      await updateInvoiceStatus(token, invoiceId, invoiceStatus)
      setNotice({ type: 'success', text: `Invoice marked as ${invoiceStatus}.` })
      const refreshedReservations = await getReservations(token)
      setReservations(refreshedReservations)
    } catch (error) {
      console.error('Invoice status update failed', error)
      setNotice({ type: 'error', text: 'Unable to update invoice status.' })
    }
  }

  const handleGenerateAdditionalInvoice = async (reservationId) => {
    try {
      const invoice = await generateAdditionalInvoice(token, reservationId)
      setNotice({ type: 'success', text: `Additional invoice ${invoice.invoice_number} created.` })
      await loadData()
    } catch (error) {
      console.error('Additional invoice creation failed', error)
      setNotice({ type: 'error', text: error?.response?.data?.message || 'Unable to create extra service invoice.' })
    }
  }

  return (
    <AppLayout eyebrow="Finance" title="Invoices" actions={<button className="primary-btn" type="button">+ Generate invoice</button>}>
      {notice.text && <div className={`notice ${notice.type}`}>{notice.text}</div>}

      <section className="panel">
        <div className="panel-header">
          <h3>Billing overview</h3>
          <div className="table-controls">
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search reservations"
              className="search-input"
            />
            <button className="link-btn" type="button">Review</button>
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
                <th>Total</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredReservations.map((reservation) => {
                const serviceTotal = Number(serviceTotals[reservation.id] || 0)
                const grandTotal = Number(reservation.total_amount || 0) + serviceTotal

                return (
                  <tr key={reservation.id}>
                    <td>{reservation.guest_name || reservation.guest || 'Guest'}</td>
                    <td>{reservation.room_name || reservation.room || 'Room'}</td>
                    <td>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <strong>${grandTotal.toFixed(2)}</strong>
                        <small style={{ color: '#64748b' }}>
                          Room ${Number(reservation.total_amount || 0).toFixed(2)} + services ${serviceTotal.toFixed(2)}
                        </small>
                      </div>
                    </td>
                    <td>
                      <span className={`status-pill ${reservation.payment_status || 'unpaid'}`}>
                        {reservation.payment_status || 'unpaid'}
                      </span>
                    </td>
                    <td>
                      <div className="table-actions" style={{ flexWrap: 'wrap' }}>
                        <button type="button" className="primary-btn small-btn" onClick={() => handleCreateInvoice(reservation.id)}>
                          Room invoice
                        </button>
                        {serviceTotal > 0 && (
                          <button type="button" className="primary-btn small-btn" onClick={() => handleGenerateAdditionalInvoice(reservation.id)}>
                            Service invoice
                          </button>
                        )}
                        <button type="button" className="link-btn" onClick={() => handleStatusUpdate(reservation.id, 'paid')}>
                          Mark paid
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </section>
    </AppLayout>
  )
}
