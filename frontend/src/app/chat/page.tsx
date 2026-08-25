"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import ChatInterface from "@/components/ChatInterface";
import KnowledgeSidebar from "@/components/KnowledgeSidebar";

function ChatContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("q") || undefined;
  // Note: For a real app, passing state back up to send message from sidebar would be better,
  // but for simplicity we can use window.location or local state. 
  // Let's implement a wrapper state if needed, or simply reload with query param.
  
  const handleSelectQuestion = (q: string) => {
    window.location.href = `/chat?q=${encodeURIComponent(q)}`;
  };

  return (
    <div className="flex flex-1 h-[calc(100vh-64px)] overflow-hidden">
      <KnowledgeSidebar onSelectQuestion={handleSelectQuestion} />
      <ChatInterface initialQuery={initialQuery} />
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="flex-1 flex items-center justify-center">Loading...</div>}>
      <ChatContent />
    </Suspense>
  );
}
