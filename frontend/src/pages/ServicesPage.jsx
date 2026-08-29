import { useEffect, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { createService, deleteService, getServices, updateService } from '../api/servicesApi'
import { useAuth } from '../context/AuthContext'

const emptyForm = {
  name: '',
  service_type: 'paid',
  price: '0',
  is_active: true,
}

export default function ServicesPage() {
  const { token } = useAuth()
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [notice, setNotice] = useState({ type: '', text: '' })
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const loadServices = () => {
    if (!token) return

    setLoading(true)
    getServices(token)
      .then(setServices)
      .catch((error) => {
        console.error('Services load failed', error)
        setNotice({ type: 'error', text: 'Unable to load hotel services.' })
      })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadServices()
  }, [token])

  const resetForm = () => {
    setForm(emptyForm)
    setEditingId(null)
    setShowForm(false)
  }

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSubmitting(true)

    try {
      const payload = {
        ...form,
        price: Number(form.price),
      }

      if (editingId) {
        const updatedService = await updateService(token, editingId, payload)
        setServices((prev) => prev.map((service) => (service.id === editingId ? updatedService : service)))
        setNotice({ type: 'success', text: 'Service updated successfully.' })
      } else {
        const createdService = await createService(token, payload)
        setServices((prev) => [createdService, ...prev])
        setNotice({ type: 'success', text: 'Service created successfully.' })
      }

      resetForm()
    } catch (error) {
      console.error('Service save failed', error)
      setNotice({ type: 'error', text: 'Service save failed. Please check the form.' })
    } finally {
      setSubmitting(false)
    }
  }

  const handleEdit = (service) => {
    setEditingId(service.id)
    setForm({
      name: service.name,
      service_type: service.service_type,
      price: String(service.price),
      is_active: service.is_active,
    })
    setShowForm(true)
  }

  const handleDelete = async (serviceId) => {
    if (!window.confirm('Delete this hotel service?')) return

    try {
      await deleteService(token, serviceId)
      setServices((prev) => prev.filter((service) => service.id !== serviceId))
      setNotice({ type: 'success', text: 'Service deleted successfully.' })
    } catch (error) {
      console.error('Service delete failed', error)
      setNotice({ type: 'error', text: 'Service could not be deleted.' })
    }
  }

  const filteredServices = services.filter((service) => {
    const query = search.toLowerCase()
    const matchesSearch =
      !query ||
      service.name.toLowerCase().includes(query) ||
      service.service_type.toLowerCase().includes(query)

    const matchesStatus =
      statusFilter === 'all' ||
      (statusFilter === 'active' && service.is_active) ||
      (statusFilter === 'inactive' && !service.is_active)

    return matchesSearch && matchesStatus
  })

  return (
    <AppLayout
      eyebrow="Operations"
      title="Services"
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
          {showForm ? 'Close form' : '+ Add service'}
        </button>
      }
    >
      {notice.text && <div className={`notice ${notice.type}`}>{notice.text}</div>}

      {showForm && (
        <section className="panel form-panel">
          <div className="panel-header">
            <h3>{editingId ? 'Edit service' : 'Add new service'}</h3>
          </div>
          <form className="data-form" onSubmit={handleSubmit}>
            <div className="form-grid">
              <label>
                Service name
                <input name="name" value={form.name} onChange={handleChange} required />
              </label>
              <label>
                Type
                <select name="service_type" value={form.service_type} onChange={handleChange}>
                  <option value="free">Free</option>
                  <option value="paid">Paid</option>
                </select>
              </label>
              <label>
                Price
                <input type="number" step="0.01" name="price" value={form.price} onChange={handleChange} required />
              </label>
              <label className="checkbox-row">
                <input type="checkbox" name="is_active" checked={form.is_active} onChange={handleChange} />
                Active service
              </label>
            </div>

            <div className="form-actions">
              <button type="submit" className="primary-btn" disabled={submitting}>
                {submitting ? 'Saving...' : editingId ? 'Update service' : 'Save service'}
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="panel">
        <div className="panel-header">
          <h3>Service catalog</h3>
          <div className="table-controls">
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search services"
              className="search-input"
            />
            <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} className="select-input">
              <option value="all">All services</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>

        {loading ? (
          <p>Loading services...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Price</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredServices.map((service) => (
                <tr key={service.id}>
                  <td>{service.name}</td>
                  <td>{service.service_type}</td>
                  <td>${Number(service.price || 0).toFixed(2)}</td>
                  <td>
                    <span className={`status-pill ${service.is_active ? 'available' : 'maintenance'}`}>
                      {service.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <div className="table-actions">
                      <button type="button" className="table-action edit" onClick={() => handleEdit(service)}>
                        Edit
                      </button>
                      <button type="button" className="table-action delete" onClick={() => handleDelete(service.id)}>
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
