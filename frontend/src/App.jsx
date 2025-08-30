import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Brain, Sparkles, Shield, Zap, Clock, CheckCircle, Loader } from "lucide-react";

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [thinkingSteps, setThinkingSteps] = useState([]);
  const [typingMessage, setTypingMessage] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, thinkingSteps, typingMessage]);

  const simulateThinkingSteps = (query) => {
    const baseSteps = [
      { id: 1, title: "Analyzing query", description: `Parsing: "${query.slice(0, 50)}${query.length > 50 ? '...' : ''}"`, status: "thinking" },
      { id: 2, title: "Identifying themes", description: "Detecting philosophical dimensions and core concepts", status: "pending" },
      { id: 3, title: "Selecting philosophers", description: "Choosing the most relevant ancient wisdom traditions", status: "pending" },
      { id: 4, title: "Consulting Socrates", description: "Applying Socratic questioning and epistemic inquiry", status: "pending" },
      { id: 5, title: "Consulting Marcus Aurelius", description: "Drawing on Stoic principles and practical wisdom", status: "pending" },
      { id: 6, title: "Consulting Lao Tzu", description: "Integrating Daoist flow and natural harmony", status: "pending" },
      { id: 7, title: "Consulting Aristotle", description: "Applying systematic analysis and virtue ethics", status: "pending" },
      { id: 8, title: "Cross-referencing wisdom", description: "Finding convergences and complementary insights", status: "pending" },
      { id: 9, title: "Synthesizing response", description: "Weaving together multiple philosophical perspectives", status: "pending" }
    ];
    return baseSteps;
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

    const steps = simulateThinkingSteps(currentQuery);
    setThinkingSteps(steps);

    for (let i = 0; i < steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800));
      updateThinkingStep(steps[i].id, "completed");
      if (i < steps.length - 1) {
        updateThinkingStep(steps[i + 1].id, "thinking");
      }
    }

    setTypingMessage({ timestamp: new Date() });

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: currentQuery }),
      });

      const data = await res.json();

      let botReply;
      if (data.reasoning_chain && data.synthesis) {
        // Format responses from reasoning_chain
        const responses = {};
        data.reasoning_chain.forEach((step) => {
          const philosopher = step.philosopher;
          let text = `**Core Insight**: ${step.core_insight || 'No insight provided'}\n\n`;
          text += "**Reasoning Process**:\n";
          if (Array.isArray(step.reasoning_process)) {
            step.reasoning_process.forEach((rp) => {
              if (typeof rp === 'object') {
                text += `- ${rp.type || rp.step || ''}: ${rp.description || rp.exploration || rp.analysis || rp['sub-step'] || ''}\n`;
              } else {
                text += `- ${rp}\n`;
              }
            });
          } else {
            text += "- No reasoning process provided\n";
          }
          text += `\n**Metacognitive Awareness**: ${Array.isArray(step.metacognitive_awareness) ? step.metacognitive_awareness.map(ma => ma.reflection || ma).join('\n') : step.metacognitive_awareness || 'None'}\n`;
          text += `**Socratic Catalyst**: ${step.socratic_catalyst || 'None'}\n`;
          text += `**Practical Application**: ${Array.isArray(step.practical_application) ? step.practical_application.map(pa => pa.step || pa).join('\n') : step.practical_application || 'None'}\n`;
          text += `**Connection to Principles**: ${Array.isArray(step.connection_to_principles) ? step.connection_to_principles.map(cp => cp.link || cp).join('\n') : step.connection_to_principles || 'None'}\n`;
          text += `**Cognitive Stimulation**: ${Array.isArray(step.cognitive_stimulation) ? step.cognitive_stimulation.map(cs => cs.exercise || cs).join('\n') : step.cognitive_stimulation || 'None'}`;
          responses[philosopher] = text;
        });

        // Format synthesis into a structured string
        let synthesisText = '';
        if (typeof data.synthesis === 'object') {
          synthesisText += `**Integrated Wisdom**: ${data.synthesis.integrated_wisdom?.unified_insight_combining_all_perspectives || data.synthesis.integrated_wisdom || 'No unified insight provided'}\n\n`;
          synthesisText += "**Key Insights**:\n";
          if (Array.isArray(data.synthesis.key_insights)) {
            data.synthesis.key_insights.forEach((ki) => {
              synthesisText += `- ${ki.most_important_discovery || ki.unexamined_life_is_not_worth_living || ki || 'No insight provided'}\n`;
            });
          } else {
            synthesisText += "- No key insights provided\n";
          }
          synthesisText += "\n**Practical Steps**:\n";
          if (Array.isArray(data.synthesis.practical_steps)) {
            data.synthesis.practical_steps.forEach((ps) => {
              synthesisText += `- ${ps.step_1 || ps.step_2 || ps.step_3 || ps.step || ps || 'No step provided'}\n`;
            });
          } else {
            synthesisText += "- No practical steps provided\n";
          }
          synthesisText += "\n**Metacognitive Enhancement**:\n";
          const metacognitiveEnhancement = data.synthesis.metacognitive_enhancement;
          if (Array.isArray(metacognitiveEnhancement)) {
            metacognitiveEnhancement.forEach((me) => {
              synthesisText += `- ${me.reflection || me['self-awareness'] || me || 'No enhancement provided'}\n`;
            });
          } else if (typeof metacognitiveEnhancement === 'string') {
            synthesisText += `- ${metacognitiveEnhancement}\n`;
          } else if (typeof metacognitiveEnhancement === 'object' && metacognitiveEnhancement !== null) {
            synthesisText += `- ${JSON.stringify(metacognitiveEnhancement)}\n`;
          } else {
            synthesisText += "- No metacognitive enhancement provided\n";
          }
          synthesisText += "\n**Reasoning Quality Assessment**:\n";
          if (Array.isArray(data.synthesis.reasoning_quality_assessment)) {
            data.synthesis.reasoning_quality_assessment.forEach((rqa) => {
              synthesisText += `- ${rqa.evaluation_of_reasoning_process || rqa || 'No assessment provided'}\n`;
            });
          } else {
            synthesisText += "- No reasoning quality assessment provided\n";
          }
          synthesisText += "\n**Cognitive Bridges**:\n";
          if (Array.isArray(data.synthesis.cognitive_bridges)) {
            data.synthesis.cognitive_bridges.forEach((cb) => {
              synthesisText += `- ${cb.connection_between_different_thinking_modes || cb || 'No bridge provided'}\n`;
            });
          } else {
            synthesisText += "- No cognitive bridges provided\n";
          }
          synthesisText += "\n**Transformative Elements**:\n";
          if (Array.isArray(data.synthesis.transformative_elements)) {
            data.synthesis.transformative_elements.forEach((te) => {
              synthesisText += `- ${te.aspect_that_could_change_user_perspective || te.shift_in_focusing_on_what_you_can_control || te || 'No element provided'}\n`;
            });
          } else {
            synthesisText += "- No transformative elements provided\n";
          }
          synthesisText += "\n**Application Scenarios**:\n";
          if (Array.isArray(data.synthesis.application_scenarios)) {
            data.synthesis.application_scenarios.forEach((as) => {
              synthesisText += `- ${as.where_this_wisdom_applies || as || 'No scenario provided'}\n`;
            });
          } else {
            synthesisText += "- No application scenarios provided\n";
          }
          synthesisText += "\n**Deepening Questions**:\n";
          if (Array.isArray(data.synthesis.deepening_questions)) {
            data.synthesis.deepening_questions.forEach((dq) => {
              synthesisText += `- ${dq.questions_for_continued_exporation || dq || 'No question provided'}\n`;
            });
          } else {
            synthesisText += "- No deepening questions provided\n";
          }
          synthesisText += "\n**Metacognitive Prompts**:\n";
          synthesisText += (Array.isArray(data.synthesis.metacognitive_prompts) ? data.synthesis.metacognitive_prompts.join('\n') : data.synthesis.metacognitive_prompts || 'None') + '\n';
          synthesisText += "\n**Dialectical Challenges**:\n";
          if (data.synthesis.dialectical_challenges) {
            Object.entries(data.synthesis.dialectical_challenges).forEach(([key, value]) => {
              synthesisText += `- ${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}\n`;
            });
          } else {
            synthesisText += "- No dialectical challenges provided\n";
          }
          synthesisText += `\n**Synthesis Quality Score**: ${data.synthesis.synthesis_quality_score || 'Not provided'}\n`;
          synthesisText += "**Cognitive Enhancement Elements**:\n";
          synthesisText += (Array.isArray(data.synthesis.cognitive_enhancement_elements) ? data.synthesis.cognitive_enhancement_elements.join('\n') : data.synthesis.cognitive_enhancement_elements || 'None');
        } else {
          synthesisText = data.synthesis || 'No synthesis provided';
        }

        botReply = {
          type: "philosophical_response",
          philosophers: data.philosophers_consulted,
          responses: responses,
          synthesis: synthesisText,
        };
      } else if (typeof data.synthesis === "string") {
        botReply = {
          type: "synthesis_response",
          philosophers: data.philosophers || ["Ancient Philosophers"],
          content: data.synthesis
        };
      } else {
        botReply = {
          type: "formatted_response",
          content: JSON.stringify(data, null, 2)
        };
      }

      const botMessage = { sender: "bot", text: botReply, timestamp: new Date() };
      setMessages((prev) => [...prev, botMessage]);
      setThinkingSteps([]);
    } catch (error) {
      const errorReply = {
        type: "error_response",
        content: "I apologize, but I'm having trouble connecting right now. Please try again in a moment.",
        error: error.message
      };
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: errorReply, timestamp: new Date() },
      ]);
      setThinkingSteps([]);
    } finally {
      setLoading(false);
      setTypingMessage(null);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const renderResponse = (response) => {
    if (typeof response === "string") {
      return <p className="message-text">{response}</p>;
    }

    switch (response.type) {
      case "synthesis_response":
        return renderSynthesisResponse(response);
      case "philosophical_response":
        return renderPhilosophicalResponse(response);
      case "error_response":
        return renderErrorResponse(response);
      case "formatted_response":
        return renderFormattedResponse(response);
      default:
        return <p className="message-text">{JSON.stringify(response, null, 2)}</p>;
    }
  };

  const renderSynthesisResponse = (response) => {
    return (
      <div className="synthesis-response">
        <div className="philosophers-consulted">
          <Brain size={16} />
          <span>Consulted: {response.philosophers?.join(", ") || "Ancient Philosophers"}</span>
        </div>
        <div className="synthesis-header">
          <Sparkles size={20} />
          <h4>Philosophical Insight</h4>
        </div>
        <p className="synthesis-text" style={{ whiteSpace: 'pre-wrap' }}>{response.content}</p>
      </div>
    );
  };

  const renderErrorResponse = (response) => {
    return (
      <div className="error-response">
        <div className="error-header">
          <Shield size={20} />
          <h4>Connection Issue</h4>
        </div>
        <p className="error-text">{response.content}</p>
        {response.error && (
          <div className="error-details">
            <small>Technical details: {response.error}</small>
          </div>
        )}
      </div>
    );
  };

  const renderFormattedResponse = (response) => {
    return (
      <div className="stream-message">
        <div className="synthesis-header">
          <Bot size={20} />
          <h4>Raw Response</h4>
        </div>
        <pre className="message-text">{response.content}</pre>
      </div>
    );
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
            <p className="philosopher-text" style={{ whiteSpace: 'pre-wrap' }}>{text}</p>
          </div>
        ))}

        {synthesis && typeof synthesis === 'string' && (
          <div className="synthesis-response">
            <div className="synthesis-header">
              <Sparkles size={20} />
              <h4>Integrated Wisdom</h4>
            </div>
            <p className="synthesis-text" style={{ whiteSpace: 'pre-wrap' }}>{synthesis}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="app-container">
      <div className="main-container">
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

            {thinkingSteps.length > 0 && (
              <div className="thinking-container">
                <div className="thinking-header">
                  <Loader size={20} className="thinking-spinner" />
                  <h3>AI Thinking Process</h3>
                </div>
                <div className="thinking-steps">
                  {thinkingSteps.map((step) => (
                    <div key={step.id} className={`thinking-step ${step.status}`}>
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
                      {renderResponse(msg.text)}
                    </div>
                    <div className={`timestamp ${msg.sender}`}>
                      {formatTime(msg.timestamp)}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {typingMessage && (
              <div className="message-row bot">
                <div className="message-content">
                  <div className="avatar bot">
                    <Brain size={20} />
                  </div>
                  <div className="message-wrapper">
                    <div className="message-bubble bot">
                      <div className="typing-indicator">
                        <div className="typing-dots">
                          <div className="dot"></div>
                          <div className="dot"></div>
                          <div className="dot"></div>
                        </div>
                        <span>Synthesizing wisdom...</span>
                      </div>
                    </div>
                    <div className="timestamp bot">
                      {formatTime(typingMessage.timestamp)}
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

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
    </div>
  );
}