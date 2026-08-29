import api from './axios'

export const createPayment = async (token, payload) => {
  const response = await api.post('/payments/', payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
