import { useState, useEffect, useRef } from "react";
import "./Chatbot.css";

function Chatbot() {
  const [messages, setMessages] = useState([
    { id: 1, sender: "bot", text: "Olá! Sou o teu chatbot Strawberry. O que precisas?" },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Referência para o “fundo” da área de mensagens
  const messagesEndRef = useRef(null);

  // Função que faz scroll até ao fim
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  // Sempre que messages ou isLoading mudar, faz scroll para o fundo
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  async function handleSend(e) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const resp = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: trimmed }),
      });

      if (!resp.ok) {
        throw new Error("Erro na resposta do servidor");
      }

      const data = await resp.json();

      const botMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text: data.reply,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = {
        id: Date.now() + 2,
        sender: "bot",
        text: "Ocorreu um erro ao contactar o servidor.",
      };
      setMessages((prev) => [...prev, errorMessage]);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="chatbot-page">
      <div className="chatbot-container">
        {/* Header */}
        <div className="chatbot-header">Chatbot Strawberry</div>

        {/* Área de mensagens */}
        <div className="chatbot-messages">
          {messages.map((m) => (
            <div
              key={m.id}
              className={
                m.sender === "user"
                  ? "message message-user"
                  : "message message-bot"
              }
            >
              {m.text}
            </div>
          ))}

          {isLoading && (
            <div className="message message-bot message-loading">
              A escrever…
            </div>
          )}

          {/* Este div “invisível” marca o fundo da lista */}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form className="chatbot-input-area" onSubmit={handleSend}>
          <input
            type="text"
            className="chatbot-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escreve uma mensagem..."
          />
          <button
            type="submit"
            className="chatbot-button"
            disabled={isLoading || !input.trim()}
          >
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}

export default Chatbot;
