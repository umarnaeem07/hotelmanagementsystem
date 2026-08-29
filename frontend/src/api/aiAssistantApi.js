import api from './axios'

export const getAssistantHistory = async (token) => {
  const response = await api.get('/chat/', {
    headers: { Authorization: `Bearer ${token}` },
  })

  return response.data
}

export const sendAssistantMessage = async (token, question) => {
  const response = await api.post(
    '/chat/',
    { question },
    {
      headers: { Authorization: `Bearer ${token}` },
    },
  )

  return response.data
}
