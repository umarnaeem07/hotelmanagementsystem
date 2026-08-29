import api from './axios'

export const createInvoice = async (token, reservationId) => {
  const response = await api.post(`/reservations/${reservationId}/invoice/`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const updateInvoiceStatus = async (token, invoiceId, paymentStatus) => {
  const response = await api.patch(`/invoices/${invoiceId}/`, { payment_status: paymentStatus }, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const generateAdditionalInvoice = async (token, reservationId) => {
  const response = await api.post(`/generate-additional/${reservationId}/`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}
