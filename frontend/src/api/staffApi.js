import api from './axios'

export const getStaffInvitations = async (token) => {
  const response = await api.get('/staff/invitations/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const inviteStaff = async (token, payload) => {
  const response = await api.post('/staff/invitations/', payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
