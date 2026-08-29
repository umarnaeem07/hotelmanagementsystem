import api from './axios'

export const getAnalytics = async (token) => {
  const response = await api.get('/analytics/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
