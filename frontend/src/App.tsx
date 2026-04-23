import { useState, useEffect, useRef } from 'react';
import './App.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  metadata?: any;
}

const ProductCard = ({ data }: { data: any }) => {
  return (
    <div className="product-card">
      <div className="card-header">
        <span className="badge">产品推荐</span>
        <h3>{data.products?.join(', ') || '保险产品'}</h3>
      </div>
      <div className="card-body">
        <p className="reason"><strong>推荐理由：</strong>{data.reason}</p>
        <button className="view-details">查看详情</button>
      </div>
    </div>
  );
};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const userId = 'user_123'; // Mock user ID

  useEffect(() => {
    const initSession = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/sessions/${userId}`);
        const data = await res.json();
        setSessionId(data.id);
      } catch (err) {
        console.error('Failed to init session', err);
      }
    };
    initSession();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          user_id: userId,
          message: input,
        }),
      });

      const data = await response.json();
      const aiMsg: Message = {
        role: 'assistant',
        content: data.content,
        metadata: data.metadata,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error('Chat error', err);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '抱歉，系统出现错误，请稍后再试。' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">AI Knowledge Copilot</div>
        <div className="status">综拓业务经理智能助手</div>
      </header>

      <main className="chat-container">
        <div className="messages-list">
          {messages.length === 0 && (
            <div className="welcome-msg">
              <h1>👋 你好！我是你的智能知识助手</h1>
              <p>你可以问我关于保险产品、政策规定或客户经营的建议。</p>
            </div>
          )}
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-wrapper ${msg.role}`}>
              <div className="message-content">
                <div className="text-content">{msg.content}</div>
                {msg.metadata?.ui_type === 'product_card' && (
                  <ProductCard data={msg.metadata.data} />
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message-wrapper assistant">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="input-wrapper">
            <textarea
              placeholder="输入您的问题..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <button className="send-btn" onClick={handleSend} disabled={isLoading}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 2L11 13M22 2L15 22L11 13L2 9L22 2z" />
              </svg>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
