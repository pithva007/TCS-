"use client";

import { ArrowRight } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";

const questions = [
  "What is the highest placement package?",
  "Who is the HoD of CSE department?",
  "What are the BTech tuition fees?",
  "Where is the central library located?",
  "How do I apply for a hostel?",
  "What is the attendance policy?"
];

export default function QuickActionCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {questions.map((q, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
        >
          <Link
            href={`/chat?q=${encodeURIComponent(q)}`}
            className="group flex items-center justify-between bg-white p-4 rounded-xl border-l-4 border-l-primary border border-y-card-border border-r-card-border shadow-[0_2px_10px_-4px_rgba(16,185,129,0.1)] hover:shadow-[0_4px_20px_-4px_rgba(16,185,129,0.15)] transition-all"
          >
            <span className="text-sm font-medium text-text-primary group-hover:text-primary transition-colors">
              {q}
            </span>
            <ArrowRight className="w-4 h-4 text-primary opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
          </Link>
        </motion.div>
      ))}
    </div>
  );
}
