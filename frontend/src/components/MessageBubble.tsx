import { Source } from "@/lib/api";
import { Bot, User, CheckCircle2 } from "lucide-react";

interface MessageBubbleProps {
  role: "user" | "bot";
  content: string;
  sources?: Source[];
  tier_used?: string;
}

export default function MessageBubble({ role, content, sources, tier_used }: MessageBubbleProps) {
  const isUser = role === "user";

  const renderMarkdown = (text: string) => {
    // Basic markdown support (bold, newlines, lists)
    let html = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\n/g, "<br/>");
    // basic list support
    html = html.replace(/- (.*?)<br\/>/g, "<li>$1</li>");
    return <div dangerouslySetInnerHTML={{ __html: html }} className="prose prose-sm prose-emerald max-w-none" />;
  };

  return (
    <div className={`flex w-full mb-6 ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`flex max-w-[85%] ${isUser ? "flex-row-reverse" : "flex-row"} items-end gap-3`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? "bg-primary" : "bg-white border border-card-border shadow-sm"}`}>
          {isUser ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-primary" />}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col gap-2 ${isUser ? "items-end" : "items-start"}`}>
          <div
            className={`px-5 py-4 rounded-2xl ${
              isUser
                ? "bg-primary text-white rounded-br-sm"
                : "bg-surface-soft text-text-primary rounded-bl-sm border border-card-border"
            }`}
          >
            {renderMarkdown(content)}
          </div>

          {/* Metadata for Bot */}
          {!isUser && (
            <div className="flex flex-col gap-2 w-full mt-1 px-1">
              {sources && sources.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {sources.map((src, i) => (
                    <div key={i} className="text-xs flex items-center gap-1 bg-white border border-card-border text-text-secondary px-2 py-1 rounded-full shadow-sm">
                      <CheckCircle2 className="w-3 h-3 text-primary" />
                      <span className="truncate max-w-[150px]">{src.file}</span>
                    </div>
                  ))}
                </div>
              )}
              {tier_used && (
                <div className="text-[10px] font-medium text-text-secondary uppercase tracking-wider">
                  Powered by {tier_used}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
