import React, { useState } from "react";
import "./index.css";

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Add user message
    const newMessage = { sender: "user", text: query };
    setMessages((prev) => [...prev, newMessage]);
    setQuery("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: query }), // ✅ FIXED: must use `text`
      });

      const data = await res.json();

      // Prefer synthesis, but fallback to full JSON
      let botReply;
      if (typeof data.synthesis === "string") {
        botReply = data.synthesis;
      } else {
        botReply = <pre>{JSON.stringify(data, null, 2)}</pre>; // ✅ prevents crash
      }

      const botMessage = { sender: "bot", text: botReply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Error: Could not connect to server." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">WisdomArc Chat</header>

      <div className="chat-container">
        {messages.length === 0 && (
          <div className="placeholder">Ask me anything...</div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div className="message bot">
            <em>Thinking...</em>
          </div>
        )}
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type your question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "..." : "Ask"}
        </button>
      </form>
    </div>
  );
}
