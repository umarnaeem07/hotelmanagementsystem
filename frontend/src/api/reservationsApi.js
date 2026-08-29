import api from './axios'

export const getReservations = async (token) => {
  const response = await api.get('/reservations/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const createReservation = async (token, payload) => {
  const response = await api.post('/reservations/', payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const updateReservation = async (token, id, payload) => {
  const response = await api.put(`/reservations/${id}/`, payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const deleteReservation = async (token, id) => {
  const response = await api.delete(`/reservations/${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.status
}

export const checkInReservation = async (token, id) => {
  const response = await api.post(`/reservations/${id}/check-in/`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  })

  return response.data
}

export const checkOutReservation = async (token, id) => {
  const response = await api.post(`/reservations/${id}/check-out/`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  })

  return response.data
}

export const getReservationServices = async (token, reservationId) => {
  const response = await api.get(`/reservations/${reservationId}/services/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const addReservationService = async (token, reservationId, payload) => {
  const response = await api.post(`/reservations/${reservationId}/services/`, payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const removeReservationService = async (token, reservationId, reservationServiceId) => {
  const response = await api.delete(`/reservations/${reservationId}/services/${reservationServiceId}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
