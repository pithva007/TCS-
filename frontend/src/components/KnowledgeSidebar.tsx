import { ChevronRight } from "lucide-react";

interface KnowledgeSidebarProps {
  onSelectQuestion: (q: string) => void;
}

const KNOWLEDGE_SECTIONS = [
  {
    title: "Placements",
    questions: [
      "What is the highest package?",
      "Who are the top recruiters?",
      "What is the average CSE package?"
    ]
  },
  {
    title: "Academics",
    questions: [
      "What is the attendance criteria?",
      "How to check the academic calendar?",
      "What are the minor specialization options?"
    ]
  },
  {
    title: "Campus Life",
    questions: [
      "How to apply for hostel?",
      "Where is the sports complex?",
      "What are the timings for the library?"
    ]
  }
];

export default function KnowledgeSidebar({ onSelectQuestion }: KnowledgeSidebarProps) {
  return (
    <div className="w-full md:w-72 flex-shrink-0 bg-white border-r border-card-border overflow-y-auto hidden md:block">
      <div className="p-6">
        <h2 className="font-playfair text-xl font-bold text-text-primary mb-6">Knowledge Base</h2>
        
        <div className="space-y-8">
          {KNOWLEDGE_SECTIONS.map((section, idx) => (
            <div key={idx}>
              <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-3">
                {section.title}
              </h3>
              <ul className="space-y-2">
                {section.questions.map((q, qIdx) => (
                  <li key={qIdx}>
                    <button
                      onClick={() => onSelectQuestion(q)}
                      className="w-full text-left group flex items-start gap-2 p-2 -mx-2 rounded-lg hover:bg-surface-soft transition-colors"
                    >
                      <ChevronRight className="w-4 h-4 text-primary opacity-0 group-hover:opacity-100 transition-opacity mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-text-primary group-hover:text-primary transition-colors">
                        {q}
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
