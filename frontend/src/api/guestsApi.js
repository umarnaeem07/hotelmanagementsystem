import api from './axios'

export const getGuests = async (token) => {
  const response = await api.get('/guests/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const createGuest = async (token, payload) => {
  const response = await api.post('/guests/', payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const updateGuest = async (token, id, payload) => {
  const response = await api.put(`/guests/${id}/`, payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const deleteGuest = async (token, id) => {
  const response = await api.delete(`/guests/${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.status
}
