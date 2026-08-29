import api from './axios'

export const getDashboardData = async (token) => {
  const response = await api.get('/dashboard/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
