import { useEffect, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { getAnalytics } from '../api/analyticsApi'
import { useAuth } from '../context/AuthContext'

const chartValues = [68, 82, 74, 90, 86, 96]

export default function ReportsPage() {
  const { token } = useAuth()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [range, setRange] = useState('Monthly')

  useEffect(() => {
    if (!token) return

    getAnalytics(token)
      .then(setData)
      .catch((error) => console.error('Analytics load failed', error))
      .finally(() => setLoading(false))
  }, [token])

  const stats = [
    { label: 'Occupancy rate', value: `${data?.occupancy_rate ?? 0}%` },
    { label: 'Total bookings', value: data?.total_bookings ?? 0 },
    { label: 'Monthly revenue', value: `$${Number(data?.monthly_revenue ?? 0).toFixed(2)}` },
    { label: 'Avg. stay', value: `${data?.average_stay_duration ?? 0} days` },
  ]

  return (
    <AppLayout eyebrow="Insights" title="Reports" actions={<button className="primary-btn">Download</button>}>
      <section className="stats-grid">
        {stats.map((item) => (
          <div className="stat-card" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
            <small>Updated today</small>
          </div>
        ))}
      </section>

      <section className="panel">
        <div className="panel-header">
          <h3>Performance summary</h3>
          <div className="filter-group">
            {['Daily', 'Weekly', 'Monthly'].map((item) => (
              <button
                key={item}
                type="button"
                className={`chip ${range === item ? 'active' : ''}`}
                onClick={() => setRange(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <p>Loading analytics...</p>
        ) : (
          <>
            <div className="report-grid">
              <div className="report-box">
                <span>Occupancy</span>
                <strong>{data?.occupancy_rate ?? 0}%</strong>
              </div>
              <div className="report-box">
                <span>Bookings</span>
                <strong>{data?.total_bookings ?? 0}</strong>
              </div>
              <div className="report-box">
                <span>Revenue</span>
                <strong>${Number(data?.monthly_revenue ?? 0).toFixed(2)}</strong>
              </div>
              <div className="report-box">
                <span>Average stay</span>
                <strong>{data?.average_stay_duration ?? 0} days</strong>
              </div>
            </div>

            <div className="chart-wrap" aria-label="Performance chart">
              {chartValues.map((value, index) => (
                <div key={index} className="chart-col">
                  <span className="chart-bar" style={{ height: `${value}%` }} />
                  <small>{['W1', 'W2', 'W3', 'W4', 'W5', 'W6'][index]}</small>
                </div>
              ))}
            </div>
          </>
        )}
      </section>
    </AppLayout>
  )
}
