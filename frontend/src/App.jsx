import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Brain, Sparkles, Shield, Zap, Clock, CheckCircle, Loader } from "lucide-react";

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [thinkingSteps, setThinkingSteps] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, thinkingSteps]);

  const simulateThinkingSteps = (query) => {
    const steps = [
      { id: 1, title: "Analyzing query", description: "Understanding the philosophical dimensions of your question", status: "thinking" },
      { id: 2, title: "Selecting philosophers", description: "Choosing the most relevant ancient wisdom traditions", status: "pending" },
      { id: 3, title: "Consulting Socrates", description: "Applying Socratic questioning and epistemic inquiry", status: "pending" },
      { id: 4, title: "Consulting Marcus Aurelius", description: "Drawing on Stoic principles and practical wisdom", status: "pending" },
      { id: 5, title: "Consulting Lao Tzu", description: "Integrating Daoist flow and natural harmony", status: "pending" },
      { id: 6, title: "Consulting Aristotle", description: "Applying systematic analysis and virtue ethics", status: "pending" },
      { id: 7, title: "Synthesizing wisdom", description: "Weaving together multiple philosophical perspectives", status: "pending" }
    ];
    
    return steps;
  };

  const updateThinkingStep = (stepId, status) => {
    setThinkingSteps(prev => 
      prev.map(step => 
        step.id === stepId ? { ...step, status } : step
      )
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const newMessage = { sender: "user", text: query, timestamp: new Date() };
    setMessages((prev) => [...prev, newMessage]);
    
    const currentQuery = query;
    setQuery("");
    setLoading(true);

    // Initialize thinking steps
    const steps = simulateThinkingSteps(currentQuery);
    setThinkingSteps(steps);

    // Simulate thinking process
    for (let i = 0; i < steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800));
      updateThinkingStep(steps[i].id, "completed");
      if (i < steps.length - 1) {
        updateThinkingStep(steps[i + 1].id, "thinking");
      }
    }

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: currentQuery }),
      });

      const data = await res.json();

      let botReply;
      if (typeof data.synthesis === "string") {
        botReply = data.synthesis;
      } else if (data.responses) {
        botReply = {
          type: "philosophical_response",
          philosophers: data.philosophers || Object.keys(data.responses || {}),
          responses: data.responses,
          synthesis: data.synthesis,
          metadata: {
            timestamp: data.timestamp,
            philosophers_consulted: data.philosophers
          }
        };
      } else {
        botReply = JSON.stringify(data, null, 2);
      }

      const botMessage = { sender: "bot", text: botReply, timestamp: new Date() };
      setMessages((prev) => [...prev, botMessage]);
      setThinkingSteps([]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "I apologize, but I'm having trouble connecting right now. Please try again in a moment.", timestamp: new Date() },
      ]);
      setThinkingSteps([]);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const renderPhilosophicalResponse = (response) => {
    const { philosophers, responses, synthesis } = response;
    
    return (
      <div className="philosophical-response">
        <div className="philosophers-consulted">
          <Brain size={16} />
          <span>Consulted: {philosophers?.join(", ") || "Multiple philosophers"}</span>
        </div>

        {responses && Object.entries(responses).map(([philosopher, text]) => (
          <div key={philosopher} className="philosopher-response">
            <div className="philosopher-header">
              <div className="philosopher-avatar">
                {philosopher.charAt(0).toUpperCase()}
              </div>
              <h4 className="philosopher-name">{philosopher}</h4>
            </div>
            <p className="philosopher-text">{text}</p>
          </div>
        ))}

        {synthesis && typeof synthesis === 'string' && (
          <div className="synthesis-response">
            <div className="synthesis-header">
              <Sparkles size={20} />
              <h4>Integrated Wisdom</h4>
            </div>
            <p className="synthesis-text">{synthesis}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="app-container">
      <div className="main-container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <div className="header-left">
              <div className="logo-container">
                <div className="logo">
                  <Brain size={24} />
                </div>
                <div className="logo-pulse"></div>
              </div>
              <div className="header-text">
                <h1 className="title">WisdomArc AI</h1>
                <p className="subtitle">Philosophical reasoning engine</p>
              </div>
            </div>
            
            <div className="header-right">
              <div className="status-badge">
                <Shield size={16} />
                <span>Secure</span>
              </div>
              <div className="status-badge">
                <Zap size={16} />
                <span>Online</span>
              </div>
            </div>
          </div>
        </header>

        {/* Chat Container */}
        <div className="chat-container">
          <div className="messages-container">
            {messages.length === 0 && !loading && (
              <div className="welcome-screen">
                <div className="welcome-content">
                  <div className="welcome-logo">
                    <Brain size={40} />
                  </div>
                  <h3 className="welcome-title">Welcome to WisdomArc AI</h3>
                  <p className="welcome-description">
                    I consult ancient philosophers to provide you with deep, multi-perspective wisdom for modern challenges.
                  </p>
                </div>
                
                <div className="philosophers-grid">
                  <div className="philosopher-card socrates">
                    <div className="philosopher-icon">🤔</div>
                    <h4>Socrates</h4>
                    <p>Question assumptions & reveal truth</p>
                  </div>
                  <div className="philosopher-card marcus">
                    <div className="philosopher-icon">🏛️</div>
                    <h4>Marcus Aurelius</h4>
                    <p>Build resilience & find control</p>
                  </div>
                  <div className="philosopher-card lao">
                    <div className="philosopher-icon">🌊</div>
                    <h4>Lao Tzu</h4>
                    <p>Flow with nature & find balance</p>
                  </div>
                  <div className="philosopher-card aristotle">
                    <div className="philosopher-icon">📚</div>
                    <h4>Aristotle</h4>
                    <p>Systematic wisdom & virtue</p>
                  </div>
                </div>
              </div>
            )}

            {/* Thinking Steps */}
            {thinkingSteps.length > 0 && (
              <div className="thinking-container">
                <div className="thinking-header">
                  <Loader size={20} className="thinking-spinner" />
                  <h3>AI Thinking Process</h3>
                </div>
                <div className="thinking-steps">
                  {thinkingSteps.map((step) => (
                    <div key={step.id} className="thinking-step">
                      <div className="step-icon">
                        {step.status === "completed" ? (
                          <CheckCircle size={20} className="completed" />
                        ) : step.status === "thinking" ? (
                          <Loader size={20} className="thinking" />
                        ) : (
                          <Clock size={20} className="pending" />
                        )}
                      </div>
                      <div className="step-content">
                        <h4 className={`step-title ${step.status}`}>{step.title}</h4>
                        <p className="step-description">{step.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} className={`message-row ${msg.sender}`}>
                <div className="message-content">
                  <div className={`avatar ${msg.sender}`}>
                    {msg.sender === "user" ? <User size={20} /> : <Brain size={20} />}
                  </div>
                  <div className="message-wrapper">
                    <div className={`message-bubble ${msg.sender}`}>
                      {typeof msg.text === "string" ? (
                        <p className="message-text">{msg.text}</p>
                      ) : msg.text?.type === "philosophical_response" ? (
                        renderPhilosophicalResponse(msg.text)
                      ) : (
                        <pre className="json-response">{JSON.stringify(msg.text, null, 2)}</pre>
                      )}
                    </div>
                    <div className={`timestamp ${msg.sender}`}>
                      {formatTime(msg.timestamp)}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <div className="input-container">
            <div className="input-wrapper">
              <div className="input-field">
                <input
                  type="text"
                  placeholder="Ask for philosophical wisdom..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit(e);
                    }
                  }}
                  disabled={loading}
                />
                <button
                  onClick={handleSubmit}
                  disabled={loading || !query.trim()}
                  className="send-button"
                >
                  <Send size={20} />
                </button>
              </div>
              
              <div className="input-footer">
                <div className="footer-left">
                  <span>🧠 Powered by philosophical AI</span>
                  <span>🔒 Private & secure</span>
                </div>
                <span>Press Enter to send</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        .app-container {
          min-height: 100vh;
          background: linear-gradient(to bottom right, #020617, #1e3a8a, #0f172a);
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }

        .main-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          max-width: 1200px;
          margin: 0 auto;
        }

        /* Header Styles */
        .header {
          background: rgba(15, 23, 42, 0.9);
          border-bottom: 1px solid rgba(71, 85, 105, 0.5);
          padding: 16px 24px;
        }

        .header-content {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .header-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .logo-container {
          position: relative;
        }

        .logo {
          width: 40px;
          height: 40px;
          background: linear-gradient(to right, #2563eb, #06b6d4);
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
        }

        .logo-pulse {
          position: absolute;
          top: -4px;
          right: -4px;
          width: 16px;
          height: 16px;
          background: #60a5fa;
          border-radius: 50%;
          border: 2px solid #0f172a;
          animation: pulse 2s infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }

        .title {
          font-size: 24px;
          font-weight: bold;
          color: white;
          margin: 0;
        }

        .subtitle {
          font-size: 14px;
          color: #94a3b8;
          margin: 0;
        }

        .header-right {
          display: flex;
          gap: 16px;
        }

        .status-badge {
          display: flex;
          align-items: center;
          gap: 8px;
          background: rgba(30, 41, 59, 0.6);
          padding: 6px 12px;
          border-radius: 20px;
          border: 1px solid rgba(71, 85, 105, 0.5);
          color: #cbd5e1;
          font-size: 14px;
        }

        /* Chat Container */
        .chat-container {
          flex: 1;
          display: flex;
          flex-direction: column;
          min-height: 0;
        }

        .messages-container {
          flex: 1;
          overflow-y: auto;
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 24px;
        }

        /* Welcome Screen */
        .welcome-screen {
          text-align: center;
          padding: 80px 0;
        }

        .welcome-content {
          margin-bottom: 32px;
        }

        .welcome-logo {
          width: 80px;
          height: 80px;
          background: linear-gradient(to right, #2563eb, #06b6d4);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 16px;
          color: white;
        }

        .welcome-title {
          font-size: 32px;
          font-weight: 600;
          color: white;
          margin-bottom: 8px;
        }

        .welcome-description {
          color: #94a3b8;
          max-width: 500px;
          margin: 0 auto;
          line-height: 1.6;
        }

        .philosophers-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 16px;
          max-width: 1000px;
          margin: 0 auto;
        }

        .philosopher-card {
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid rgba(71, 85, 105, 0.5);
          border-radius: 16px;
          padding: 24px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .philosopher-card:hover {
          transform: translateY(-4px);
          border-color: #3b82f6;
          box-shadow: 0 10px 25px rgba(59, 130, 246, 0.1);
        }

        .philosopher-icon {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 12px;
          font-size: 24px;
        }

        .socrates .philosopher-icon { background: linear-gradient(to right, #eab308, #f97316); }
        .marcus .philosopher-icon { background: linear-gradient(to right, #ef4444, #f43f5e); }
        .lao .philosopher-icon { background: linear-gradient(to right, #14b8a6, #06b6d4); }
        .aristotle .philosopher-icon { background: linear-gradient(to right, #8b5cf6, #6366f1); }

        .philosopher-card h4 {
          color: white;
          font-weight: 600;
          margin-bottom: 8px;
        }

        .philosopher-card p {
          color: #94a3b8;
          font-size: 14px;
          line-height: 1.5;
        }

        /* Thinking Steps */
        .thinking-container {
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid rgba(71, 85, 105, 0.5);
          border-radius: 16px;
          padding: 24px;
        }

        .thinking-header {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 16px;
        }

        .thinking-header h3 {
          color: white;
          font-size: 18px;
          font-weight: 600;
        }

        .thinking-spinner {
          animation: spin 1s linear infinite;
          color: #60a5fa;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .thinking-steps {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .thinking-step {
          display: flex;
          gap: 12px;
          align-items: flex-start;
        }

        .step-icon {
          flex-shrink: 0;
          margin-top: 2px;
        }

        .step-icon .completed { color: #10b981; }
        .step-icon .thinking { color: #60a5fa; animation: spin 1s linear infinite; }
        .step-icon .pending { color: #6b7280; }

        .step-content {
          flex: 1;
        }

        .step-title {
          font-weight: 500;
          margin-bottom: 4px;
        }

        .step-title.completed { color: #86efac; }
        .step-title.thinking { color: #93c5fd; }
        .step-title.pending { color: #94a3b8; }

        .step-description {
          color: #94a3b8;
          font-size: 14px;
          line-height: 1.4;
        }

        /* Messages */
        .message-row {
          display: flex;
          animation: fadeIn 0.5s ease-out;
        }

        .message-row.user {
          justify-content: flex-end;
        }

        .message-content {
          display: flex;
          gap: 12px;
          max-width: 80%;
          width: 100%;
        }

        .message-row.user .message-content {
          flex-direction: row-reverse;
        }

        .avatar {
          width: 40px;
          height: 40px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          color: white;
        }

        .avatar.user {
          background: linear-gradient(to right, #0891b2, #2563eb);
        }

        .avatar.bot {
          background: linear-gradient(to right, #2563eb, #7c3aed);
        }

        .message-wrapper {
          flex: 1;
        }

        .message-row.user .message-wrapper {
          text-align: right;
        }

        .message-bubble {
          display: inline-block;
          width: 100%;
          padding: 16px 20px;
          border-radius: 16px;
          border: 1px solid;
          transition: all 0.3s ease;
        }

        .message-bubble.user {
          background: linear-gradient(to right, #0891b2, #2563eb);
          color: white;
          border-color: rgba(59, 130, 246, 0.3);
          border-bottom-right-radius: 4px;
        }

        .message-bubble.bot {
          background: rgba(30, 41, 59, 0.5);
          color: white;
          border-color: rgba(71, 85, 105, 0.5);
          border-bottom-left-radius: 4px;
        }

        .message-text {
          line-height: 1.6;
          white-space: pre-wrap;
        }

        .timestamp {
          font-size: 12px;
          color: #6b7280;
          margin-top: 4px;
        }

        .timestamp.user {
          text-align: right;
        }

        /* Philosophical Response */
        .philosophical-response {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .philosophers-consulted {
          display: flex;
          align-items: center;
          gap: 8px;
          color: #93c5fd;
          font-size: 14px;
        }

        .philosopher-response {
          background: rgba(30, 41, 59, 0.3);
          border: 1px solid rgba(71, 85, 105, 0.5);
          border-radius: 12px;
          padding: 16px;
        }

        .philosopher-header {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
        }

        .philosopher-avatar {
          width: 24px;
          height: 24px;
          background: #3b82f6;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: bold;
          color: white;
        }

        .philosopher-name {
          color: #93c5fd;
          font-weight: 600;
          text-transform: capitalize;
        }

        .philosopher-text {
          color: #cbd5e1;
          line-height: 1.5;
          font-size: 14px;
        }

        .synthesis-response {
          background: rgba(30, 58, 138, 0.2);
          border: 1px solid rgba(59, 130, 246, 0.3);
          border-radius: 12px;
          padding: 16px;
        }

        .synthesis-header {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
        }

        .synthesis-header h4 {
          color: #93c5fd;
          font-weight: 600;
        }

        .synthesis-text {
          color: #cbd5e1;
          line-height: 1.6;
        }

        .json-response {
          font-size: 14px;
          overflow-x: auto;
          background: rgba(15, 23, 42, 0.5);
          padding: 12px;
          border-radius: 8px;
          border: 1px solid rgba(71, 85, 105, 0.3);
          color: #cbd5e1;
        }

        /* Input Container */
        .input-container {
          border-top: 1px solid rgba(71, 85, 105, 0.5);
          background: rgba(15, 23, 42, 0.6);
          padding: 16px 24px;
        }

        .input-field {
          display: flex;
          align-items: center;
          background: rgba(30, 41, 59, 0.6);
          border: 1px solid rgba(71, 85, 105, 0.5);
          border-radius: 16px;
          transition: border-color 0.3s ease;
        }

        .input-field:focus-within {
          border-color: #3b82f6;
        }

        .input-field input {
          flex: 1;
          padding: 16px 20px;
          background: transparent;
          border: none;
          color: white;
          font-size: 16px;
          outline: none;
        }

        .input-field input::placeholder {
          color: #94a3b8;
        }

        .send-button {
          margin: 8px;
          padding: 12px;
          background: linear-gradient(to right, #2563eb, #06b6d4);
          color: white;
          border: none;
          border-radius: 12px;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .send-button:hover:not(:disabled) {
          background: linear-gradient(to right, #1d4ed8, #0891b2);
          transform: scale(1.05);
        }

        .send-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none;
        }

        .input-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 12px;
          font-size: 12px;
          color: #6b7280;
        }

        .footer-left {
          display: flex;
          gap: 16px;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        /* Scrollbar */
        .messages-container::-webkit-scrollbar {
          width: 6px;
        }

        .messages-container::-webkit-scrollbar-track {
          background: transparent;
        }

        .messages-container::-webkit-scrollbar-thumb {
          background: rgba(59, 130, 246, 0.3);
          border-radius: 3px;
        }

        .messages-container::-webkit-scrollbar-thumb:hover {
          background: rgba(59, 130, 246, 0.5);
        }

        /* Responsive */
        @media (max-width: 768px) {
          .main-container {
            max-width: 100%;
          }
          
          .header {
            padding: 12px 16px;
          }
          
          .messages-container {
            padding: 16px;
          }
          
          .input-container {
            padding: 12px 16px;
          }
          
          .philosophers-grid {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          }
          
          .message-content {
            max-width: 95%;
          }
          
          .footer-left {
            flex-direction: column;
            gap: 4px;
          }
        }
      `}</style>
    </div>
  );
}