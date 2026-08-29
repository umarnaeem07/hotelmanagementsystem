import api from './axios'

export const getServices = async (token) => {
  const response = await api.get('/services/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const createService = async (token, payload) => {
  const response = await api.post('/services/', payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const updateService = async (token, id, payload) => {
  const response = await api.put(`/services/${id}/`, payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const deleteService = async (token, id) => {
  const response = await api.delete(`/services/${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.status
}
