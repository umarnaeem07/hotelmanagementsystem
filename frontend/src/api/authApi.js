import api from './axios'

export const loginUser = async (username, password) => {
  const response = await api.post('/login/', { username, password })
  return response.data
}

export const signupUser = async (payload) => {
  const response = await api.post('/signup/', payload)
  return response.data
}

export const getCurrentUser = async (token) => {
  const response = await api.get('/me/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
