import api from './axios'

export const getRooms = async (token) => {
  const response = await api.get('/rooms/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const createRoom = async (token, payload) => {
  const response = await api.post('/rooms/', payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const updateRoom = async (token, id, payload) => {
  const response = await api.put(`/rooms/${id}/`, payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const deleteRoom = async (token, id) => {
  const response = await api.delete(`/rooms/${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.status
}
