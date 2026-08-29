import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Reservations', to: '/reservations' },
  { label: 'Rooms', to: '/rooms' },
  { label: 'Services', to: '/services' },
  { label: 'Guests', to: '/guests' },
  { label: 'Staff', to: '/staff' },
  { label: 'Invoices', to: '/invoices' },
  { label: 'Reports', to: '/reports' },
  { label: 'AI Assistant', to: '/ai-assistant' },
  { label: 'Settings', to: '/settings' },
]

export default function AppLayout({ children, eyebrow = 'Overview', title, actions }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-box">
          <div className="brand-mark">H</div>
          <div>
            <span>Hotel</span>
            <strong>Harbor View</strong>
          </div>
        </div>

        <nav className="nav-menu" aria-label="Main navigation">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-card">
          <p>Signed in</p>
          <strong>{user?.username || 'Manager'}</strong>
          <span>Hotel operations dashboard</span>
          <button type="button" className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">{eyebrow}</p>
            <h1>{title}</h1>
          </div>
          {actions}
        </header>

        {children}
      </main>
    </div>
  )
}
