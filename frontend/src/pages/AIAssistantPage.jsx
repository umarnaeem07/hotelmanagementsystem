import { useEffect, useMemo, useState } from 'react'
import AppLayout from '../components/AppLayout'
import { useAuth } from '../context/AuthContext'
import { getAssistantHistory, sendAssistantMessage } from '../api/aiAssistantApi'

const starterPrompts = [
  'What is the occupancy today?',
  'Which rooms are available right now?',
  'What reservations are arriving today?',
  'How much revenue was generated this month?',
]

const buildWelcomeMessage = () => ({
  id: 'welcome',
  role: 'assistant',
  content:
    'Hi! I can help with reservations, room status, occupancy, revenue, and guest insights. Ask me about today\'s operations or any upcoming hotel needs.',
})

const renderMessageContent = (content) => {
  const lines = String(content || '').split(/\n/).map((line) => line.trim()).filter(Boolean)

  if (lines.length === 0) {
    return <span>No response yet.</span>
  }

  const output = []
  let listItems = []
  let listType = null

  const flushList = () => {
    if (!listItems.length) return

    const ListTag = listType === 'numbered' ? 'ol' : 'ul'
    output.push(
      <ListTag key={`list-${output.length}`} className="chat-list">
        {listItems.map((item, index) => (
          <li key={`${listType}-${index}`}>{item}</li>
        ))}
      </ListTag>,
    )
    listItems = []
    listType = null
  }

  lines.forEach((line) => {
    if (/^[-*]\s+/.test(line)) {
      const itemText = line.replace(/^[-*]\s+/, '')
      if (listType === 'numbered') flushList()
      listType = 'bulleted'
      listItems.push(itemText)
      return
    }

    if (/^\d+\.\s+/.test(line)) {
      const itemText = line.replace(/^\d+\.\s+/, '')
      if (listType === 'bulleted') flushList()
      listType = 'numbered'
      listItems.push(itemText)
      return
    }

    flushList()
    output.push(<p key={`para-${output.length}`}>{line}</p>)
  })

  flushList()

  return output
}

export default function AIAssistantPage() {
  const { token } = useAuth()
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([buildWelcomeMessage()])
  const [loading, setLoading] = useState(false)
  const [historyLoading, setHistoryLoading] = useState(false)
  const [error, setError] = useState('')

  const quickPrompts = useMemo(
    () => [
      { label: 'Reservations', prompt: 'What reservations are arriving today?' },
      { label: 'Rooms', prompt: 'Which rooms need attention today?' },
      { label: 'Revenue', prompt: 'How much revenue did we generate this month?' },
    ],
    [],
  )

  useEffect(() => {
    const loadHistory = async () => {
      if (!token) {
        setMessages([buildWelcomeMessage()])
        return
      }

      try {
        setHistoryLoading(true)
        const data = await getAssistantHistory(token)
        const previousMessages = (data?.messages || []).map((message) => ({
          id: message.id ?? `${message.role}-${message.created_at}`,
          role: message.role,
          content: message.content,
        }))

        setMessages(previousMessages.length ? previousMessages : [buildWelcomeMessage()])
      } catch (err) {
        setMessages([buildWelcomeMessage()])
      } finally {
        setHistoryLoading(false)
      }
    }

    loadHistory()
  }, [token])

  const handleSubmit = async (event) => {
    event.preventDefault()

    const trimmed = question.trim()
    if (!trimmed || loading || !token) return

    const userMessage = { id: Date.now(), role: 'user', content: trimmed }
    setMessages((prev) => [...prev, userMessage])
    setQuestion('')
    setLoading(true)
    setError('')

    try {
      const data = await sendAssistantMessage(token, trimmed)
      const reply = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data?.answer || 'I could not generate a reply right now.',
      }

      setMessages((prev) => [...prev, reply])
    } catch (err) {
      const message = err?.response?.data?.detail || err?.response?.data?.message || 'Unable to get an AI response right now.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppLayout
      eyebrow="Assistant"
      title="AI concierge"
      actions={
        <button type="button" className="primary-btn" onClick={() => setQuestion(starterPrompts[0])}>
          Quick prompt
        </button>
      }
    >
      <section className="panel ai-panel">
        <div className="ai-header">
          <div>
            <h3>Hotel AI assistant</h3>
            <p>Ask about operations, pricing, occupancy, or guest needs.</p>
          </div>
        </div>

        <div className="ai-prompt-row">
          {starterPrompts.map((prompt) => (
            <button
              key={prompt}
              type="button"
              className="chip"
              onClick={() => setQuestion(prompt)}
            >
              {prompt}
            </button>
          ))}
        </div>

        <div className="ai-quick-actions">
          {quickPrompts.map((item) => (
            <button
              key={item.label}
              type="button"
              className="quick-action"
              onClick={() => setQuestion(item.prompt)}
            >
              {item.label}
            </button>
          ))}
        </div>

        <div className="chat-window">
          {historyLoading && messages.length === 0 ? (
            <div className="chat-bubble assistant loading-bubble">
              <strong>AI</strong>
              <p>Loading recent hotel conversation...</p>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`chat-bubble ${message.role}`}>
                <strong>{message.role === 'assistant' ? 'AI' : 'You'}</strong>
                <div className="chat-content">{renderMessageContent(message.content)}</div>
              </div>
            ))
          )}
        </div>

        {error && <div className="error-box">{error}</div>}

        <form className="chat-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask the hotel assistant..."
          />
          <button type="submit" className="primary-btn" disabled={loading || !token}>
            {loading ? 'Thinking...' : 'Send'}
          </button>
        </form>
      </section>
    </AppLayout>
  )
}
