import { createContext, useContext, useEffect, useMemo, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('hotel_access_token') || '')
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('hotel_user')
    return savedUser ? JSON.parse(savedUser) : null
  })

  useEffect(() => {
    if (token) {
      localStorage.setItem('hotel_access_token', token)
    } else {
      localStorage.removeItem('hotel_access_token')
    }
  }, [token])

  useEffect(() => {
    if (user) {
      localStorage.setItem('hotel_user', JSON.stringify(user))
    } else {
      localStorage.removeItem('hotel_user')
    }
  }, [user])

  const logout = () => {
    setToken('')
    setUser(null)
  }

  const value = useMemo(
    () => ({ token, setToken, user, setUser, logout }),
    [token, user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
