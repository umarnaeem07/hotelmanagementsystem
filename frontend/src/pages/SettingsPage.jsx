import AppLayout from '../components/AppLayout'

export default function SettingsPage() {
  const settings = [
    { label: 'Check-in time', value: '14:00' },
    { label: 'Check-out time', value: '12:00' },
    { label: 'Currency', value: 'PKR' },
    { label: 'Tax rate', value: '5%' },
    { label: 'Timezone', value: 'Asia/Karachi' },
  ]

  return (
    <AppLayout eyebrow="Configuration" title="Settings" actions={<button className="primary-btn">Save changes</button>}>
      <section className="stats-grid settings-grid">
        {settings.map((item) => (
          <div className="stat-card" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
            <small>Configured</small>
          </div>
        ))}
      </section>

      <section className="panel">
        <div className="panel-header">
          <h3>Hotel preferences</h3>
        </div>
        <div className="settings-list">
          <div className="setting-row">
            <span>Allow early check-in</span>
            <button className="toggle-btn enabled">Enabled</button>
          </div>
          <div className="setting-row">
            <span>Auto-send payment reminders</span>
            <button className="toggle-btn enabled">Enabled</button>
          </div>
          <div className="setting-row">
            <span>Housekeeping alerts</span>
            <button className="toggle-btn">Disabled</button>
          </div>
        </div>
      </section>
    </AppLayout>
  )
}
