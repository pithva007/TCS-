"use client";

import { useState, useRef, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { Send, Loader2 } from "lucide-react";
import { api, Source } from "@/lib/api";
import MessageBubble from "./MessageBubble";

interface Message {
  id: string;
  role: "user" | "bot";
  content: string;
  sources?: Source[];
  tier_used?: string;
}

export default function ChatInterface({ initialQuery }: { initialQuery?: string }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "bot",
      content: "Hello! I am NirmaAI, your intelligent campus assistant. How can I help you today?",
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => uuidv4());
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const initialized = useRef(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    if (initialQuery && !initialized.current) {
      initialized.current = true;
      handleSend(initialQuery);
    }
  }, [initialQuery]);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = { id: uuidv4(), role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await api.chat(text, sessionId);
      const botMessage: Message = {
        id: uuidv4(),
        role: "bot",
        content: response.answer,
        sources: response.sources,
        tier_used: response.tier_used,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      const errorMessage: Message = {
        id: uuidv4(),
        role: "bot",
        content: "I'm sorry, I encountered an error connecting to the server. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-surface overflow-hidden relative">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div className="max-w-4xl mx-auto">
          {messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              role={msg.role}
              content={msg.content}
              sources={msg.sources}
              tier_used={msg.tier_used}
            />
          ))}
          {isLoading && (
            <div className="flex w-full justify-start mb-6">
              <div className="bg-surface-soft px-5 py-4 rounded-2xl rounded-bl-sm border border-card-border flex items-center gap-2 text-text-secondary">
                <Loader2 className="w-4 h-4 animate-spin text-primary" />
                <span className="text-sm">NirmaAI is thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-card-border p-4">
        <div className="max-w-4xl mx-auto relative">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend(input);
            }}
            className="relative flex items-center"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything about Nirma University..."
              disabled={isLoading}
              className="w-full pl-6 pr-14 py-4 bg-surface-soft border border-card-border rounded-full focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-shadow text-text-primary placeholder:text-text-secondary/60 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-primary text-white rounded-full hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:hover:bg-primary"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
          <div className="text-center mt-2">
            <span className="text-[10px] text-text-secondary">
              NirmaAI can make mistakes. Consider verifying important information.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
