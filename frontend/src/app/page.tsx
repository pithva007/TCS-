"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { BrainCircuit, Briefcase, Map, Users, MessageSquareText } from "lucide-react";
import QuickActionCards from "@/components/QuickActionCards";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative pt-24 pb-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-surface-soft to-surface -z-10" />
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03] -z-10" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.h1 
            className="text-5xl md:text-7xl font-playfair font-bold text-text-primary tracking-tight mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            Your Intelligent <br className="hidden md:block" />
            <span className="bg-gradient-to-r from-primary-dark via-primary to-[#34d399] bg-clip-text text-transparent">
              Campus Companion
            </span>
          </motion.h1>
          
          <motion.p 
            className="mt-6 text-lg md:text-xl text-text-secondary max-w-2xl mx-auto mb-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
          >
            Experience the next generation of campus assistance. Get instant, AI-powered answers grounded in real university data, navigate the campus, and explore opportunities.
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <Link 
              href="/chat"
              className="inline-flex items-center justify-center px-8 py-4 text-base font-medium text-white bg-primary hover:bg-primary-dark transition-colors rounded-full shadow-[0_8px_30px_rgb(16,185,129,0.3)] hover:shadow-[0_8px_30px_rgb(4,120,87,0.4)]"
            >
              <MessageSquareText className="w-5 h-5 mr-2" />
              Start Chatting
            </Link>
          </motion.div>

          {/* Stats */}
          <motion.div 
            className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            {[
              { label: "Highest Package", value: "₹94.13 LPA" },
              { label: "Recruiting Companies", value: "230+" },
              { label: "Expert Faculty", value: "53+" },
            ].map((stat, i) => (
              <div key={i} className="bg-white p-6 rounded-2xl border border-card-border shadow-sm">
                <div className="text-3xl font-playfair font-bold text-primary mb-1">{stat.value}</div>
                <div className="text-sm text-text-secondary font-medium">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-playfair font-bold text-text-primary mb-4">
              Everything you need to know
            </h2>
            <p className="text-text-secondary max-w-2xl mx-auto">
              A comprehensive suite of tools designed to make your university experience seamless and informed.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { icon: BrainCircuit, title: "Smart FAQ", desc: "Instant answers to your queries powered by advanced AI and semantic search." },
              { icon: Briefcase, title: "Placement Insights", desc: "Detailed statistics, recruiter info, and highest package breakdowns." },
              { icon: Map, title: "Campus Navigator", desc: "Interactive 3D map to find buildings, facilities, and amenities easily." },
              { icon: Users, title: "Faculty Directory", desc: "Explore faculty profiles, research interests, and contact information." },
            ].map((feat, i) => (
              <div key={i} className="bg-surface p-8 rounded-2xl border border-card-border shadow-[0_4px_20px_-4px_rgba(16,185,129,0.05)] hover:shadow-[0_8px_30px_-4px_rgba(16,185,129,0.1)] transition-shadow">
                <div className="w-12 h-12 bg-surface-soft rounded-xl flex items-center justify-center mb-6">
                  <feat.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold text-text-primary mb-3">{feat.title}</h3>
                <p className="text-text-secondary text-sm leading-relaxed">{feat.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quick Questions */}
      <section className="py-24 bg-surface-soft">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-10">
            <h2 className="text-2xl font-playfair font-bold text-text-primary mb-2">
              Frequently Asked
            </h2>
            <p className="text-text-secondary text-sm">Jump straight into the conversation</p>
          </div>
          <QuickActionCards />
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-white border-t border-card-border mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between">
          <p className="text-sm text-text-secondary">
            NirmaAI © 2026 | Built for TCS Technology Day
          </p>
          <p className="text-sm text-text-secondary mt-2 md:mt-0">
            Nirma University, Ahmedabad
          </p>
        </div>
      </footer>
    </div>
  );
}
