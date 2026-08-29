import { useEffect, useMemo, useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { getDashboardData } from '../api/dashboardApi'
import { useAuth } from '../context/AuthContext'

const navItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Reservations', to: '/reservations' },
  { label: 'Rooms', to: '/rooms' },
  { label: 'Guests', to: '/guests' },
  { label: 'Staff', to: '/staff' },
  { label: 'Invoices', to: '/invoices' },
  { label: 'Reports', to: '/reports' },
  { label: 'AI Assistant', to: '/ai-assistant' },
  { label: 'Settings', to: '/settings' },
]

const fallbackTasks = [
  'Inspect Suite 301 before evening check-in',
  'Confirm airport transfer for Ayesha Khan',
  'Prepare breakfast vouchers for 12 guests',
  'Follow up on pending invoice payment',
]

const fallbackReservations = [
  { guest: 'Ayesha Khan', room: 'Deluxe 204', date: 'Today, 2:00 PM', status: 'Confirmed' },
  { guest: 'Daniel Brown', room: 'Suite 301', date: 'Today, 5:30 PM', status: 'Pending' },
  { guest: 'Sara Ali', room: 'Standard 109', date: 'Tomorrow, 10:00 AM', status: 'Checked In' },
]

export default function DashboardPage() {
  const navigate = useNavigate()
  const { token, logout, user } = useAuth()
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!token) {
      navigate('/')
      return
    }

    const loadDashboard = async () => {
      try {
        const data = await getDashboardData(token)
        setDashboard(data)
      } catch (error) {
        const status = error?.response?.status
        const message = error?.response?.data?.message || ''
        console.error('Dashboard load failed', error)

        if (status === 404 || status === 500 || /hotel/i.test(message)) {
          navigate('/setup-hotel')
          return
        }
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [navigate, token])

  const stats = useMemo(() => {
    if (!dashboard) {
      return [
        { label: 'Occupancy', value: '86%', change: '+4.2%' },
        { label: 'Revenue', value: '$24.8k', change: '+12.4%' },
        { label: 'Check-ins', value: '34', change: '+8 today' },
        { label: 'Guests', value: '126', change: '+14 new' },
      ]
    }

    return [
      { label: 'Rooms', value: dashboard.total_rooms ?? 0, change: `${dashboard.available_rooms ?? 0} available` },
      { label: 'Guests', value: dashboard.total_guests ?? 0, change: 'Current total' },
      { label: 'Check-ins', value: dashboard.today_checkins ?? 0, change: 'Today' },
      { label: 'Check-outs', value: dashboard.today_checkouts ?? 0, change: 'Today' },
    ]
  }, [dashboard])

  const roomStatus = useMemo(() => {
    if (!dashboard) {
      return [
        { name: 'Occupied', value: '42', tone: 'occupied' },
        { name: 'Available', value: '18', tone: 'available' },
        { name: 'Cleaning', value: '7', tone: 'cleaning' },
        { name: 'Maintenance', value: '3', tone: 'maintenance' },
      ]
    }

    return [
      { name: 'Occupied', value: dashboard.occupied_rooms ?? 0, tone: 'occupied' },
      { name: 'Available', value: dashboard.available_rooms ?? 0, tone: 'available' },
      { name: 'Cleaning', value: dashboard.cleaning_rooms ?? 0, tone: 'cleaning' },
      { name: 'Maintenance', value: dashboard.maintenance_rooms ?? 0, tone: 'maintenance' },
    ]
  }, [dashboard])

  const reservations = dashboard ? fallbackReservations : fallbackReservations
  const occupancyChart = [68, 72, 79, 74, 88, 91, 86]
  const recentActivity = [
    { title: 'Check-in confirmed', detail: 'Ayesha Khan · Deluxe 204', time: '12 min ago' },
    { title: 'Room cleaned', detail: 'Suite 301 · housekeeping', time: '25 min ago' },
    { title: 'Invoice due', detail: 'Daniel Brown · partial payment', time: '54 min ago' },
    { title: 'New reservation', detail: 'Sara Ali · Standard 109', time: '1 hr ago' },
  ]

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
          <span>{dashboard ? `${dashboard.active_reservations ?? 0} active bookings` : 'Loading dashboard...'}</span>
          <button type="button" className="logout-btn" onClick={logout}>Logout</button>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">Overview</p>
            <h1>{loading ? 'Loading dashboard...' : 'Good morning, Manager'}</h1>
          </div>
          <button className="primary-btn" type="button" onClick={() => navigate('/reservations')}>
            + New reservation
          </button>
        </header>

        <section className="hero-panel">
          <div>
            <p className="eyebrow light">Hotel performance</p>
            <h2>Busy but smooth operation today</h2>
          </div>
          <div className="hero-meta">
            <div>
              <span>Check-ins</span>
              <strong>{dashboard?.today_checkins ?? 14}</strong>
            </div>
            <div>
              <span>Check-outs</span>
              <strong>{dashboard?.today_checkouts ?? 9}</strong>
            </div>
          </div>
        </section>

        <section className="stats-grid">
          {stats.map((item) => (
            <div className="stat-card" key={item.label}>
              <span>{item.label}</span>
              <strong>{item.value}</strong>
              <small>{item.change}</small>
            </div>
          ))}
        </section>

        <section className="content-grid dashboard-advanced">
          <div className="panel">
            <div className="panel-header">
              <h3>Today's reservations</h3>
              <button className="link-btn" type="button" onClick={() => navigate('/reservations')}>View all</button>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Guest</th>
                  <th>Room</th>
                  <th>Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {reservations.map((reservation) => (
                  <tr key={reservation.guest}>
                    <td>{reservation.guest}</td>
                    <td>{reservation.room}</td>
                    <td>{reservation.date}</td>
                    <td>
                      <span className={`status-pill ${reservation.status.toLowerCase().replace(/\s+/g, '-')}`}>
                        {reservation.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="stacked-panel">
            <div className="panel">
              <div className="panel-header">
                <h3>Room status</h3>
              </div>

              <div className="room-list">
                {roomStatus.map((room) => (
                  <div key={room.name} className="room-row">
                    <div className="room-label">
                      <span className={`dot ${room.tone}`}></span>
                      <span>{room.name}</span>
                    </div>
                    <strong>{room.value}</strong>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel">
              <div className="panel-header">
                <h3>Priority tasks</h3>
              </div>

              <ul className="task-list">
                {fallbackTasks.map((task) => (
                  <li key={task}>{task}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="dashboard-lower-grid">
          <div className="panel chart-panel">
            <div className="panel-header">
              <h3>Occupancy trend</h3>
            </div>
            <div className="chart-wrap dashboard-chart" aria-label="Occupancy trend chart">
              {occupancyChart.map((value, index) => (
                <div key={index} className="chart-col">
                  <span className="chart-bar" style={{ height: `${value}%` }} />
                  <small>{['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index]}</small>
                </div>
              ))}
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">
              <h3>Recent activity</h3>
            </div>
            <ul className="activity-list">
              {recentActivity.map((item) => (
                <li key={item.title}>
                  <strong>{item.title}</strong>
                  <span>{item.detail}</span>
                  <small>{item.time}</small>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </main>
    </div>
  )
}
