import React from 'react';
import {
  Sparkles,
  ArrowRight,
  Bot,
  Target,
  Mic,
  FileText,
  GitBranch,
  Brain,
  Shield,
  Zap,
  CheckCircle2
} from 'lucide-react';

export default function LandingPage({ onLaunch, onExplore }) {
  return (
    <div className="space-y-16 max-w-6xl mx-auto py-8 pb-16 px-4">
      {/* Hero Section */}
      <div className="neo-card p-8 md:p-14 bg-white relative overflow-hidden space-y-8 text-center md:text-left">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-6 max-w-2xl">
            <div className="inline-flex items-center gap-2 bg-yellow-300 border-2 border-black px-3 py-1 rounded-full text-xs font-black shadow-[2px_2px_0px_0px_#000]">
              <Sparkles className="w-4 h-4 text-black fill-black" />
              INTRODUCING LORDSAHU OS V0.1
            </div>

            <h1 className="text-4xl md:text-6xl font-black text-black tracking-tight leading-none">
              Meet <span className="underline decoration-blue-600 decoration-8 underline-offset-4">LordSahu</span>
            </h1>

            <p className="text-lg md:text-2xl font-bold text-slate-800 leading-snug">
              Your AI Personal Operating System.
            </p>

            <p className="text-sm md:text-base text-slate-700 font-medium max-w-xl">
              Eliminate manual tracking, forms, and spreadsheets. LordSahu remembers, organizes, analyzes, and manages your life through a single, intelligent conversational assistant.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap items-center justify-center md:justify-start gap-4 pt-2">
              <button
                onClick={onLaunch}
                className="neo-btn bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 text-sm font-black flex items-center gap-2 shadow-[4px_4px_0px_0px_#000]"
              >
                Launch LordSahu <ArrowRight className="w-4 h-4" />
              </button>

              <button
                onClick={onExplore}
                className="neo-btn bg-lime-300 hover:bg-lime-200 text-black px-6 py-3 text-sm font-black shadow-[4px_4px_0px_0px_#000]"
              >
                Explore Features
              </button>
            </div>
          </div>

          {/* Hero OS Card */}
          <div className="w-full md:w-80 neo-card p-6 bg-amber-100 border-3 border-black shadow-[6px_6px_0px_0px_#000] space-y-4 text-left">
            <div className="flex items-center justify-between border-b-2 border-black pb-2">
              <span className="font-extrabold text-xs text-black uppercase tracking-wider">Morning Briefing</span>
              <span className="text-[10px] bg-black text-white px-2 py-0.5 font-mono font-bold rounded">LIVE</span>
            </div>

            <p className="text-xs font-bold text-slate-900 leading-relaxed">
              "Good morning Siddhant. You slept 7 hours. Current Weight: 96.8 kg. SQL Goal is 43% complete. Highest priority today is your DBMS assignment."
            </p>

            <div className="space-y-2 pt-2 text-[11px] font-bold">
              <div className="flex items-center justify-between bg-white p-2 rounded-lg border-2 border-black">
                <span>Consistency Score</span>
                <span className="text-blue-700">84.5%</span>
              </div>
              <div className="flex items-center justify-between bg-white p-2 rounded-lg border-2 border-black">
                <span>Weight Loss</span>
                <span className="text-emerald-700">96.8 kg (-2.2kg)</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Modules Grid */}
      <div className="space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-2xl md:text-4xl font-black text-black">
            Six Built-In Operating Modules
          </h2>
          <p className="text-sm font-bold text-slate-700">
            Designed for Apple simplicity, Linear UX precision, and JARVIS continuous intelligence.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Module 1: AI Assistant */}
          <div className="neo-card p-6 bg-white space-y-3">
            <div className="w-12 h-12 rounded-xl bg-blue-100 border-2 border-black flex items-center justify-center text-blue-700 font-bold shadow-[2px_2px_0px_0px_#000]">
              <Bot className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-black">Conversational AI Engine</h3>
            <p className="text-xs text-slate-700 font-medium leading-relaxed">
              Natural conversation-first interface with 6 specialized persona modes (Chief of Staff, Coach, Focus, Reflection, Planner, Reviewer).
            </p>
          </div>

          {/* Module 2: Living Goals */}
          <div className="neo-card p-6 bg-white space-y-3">
            <div className="w-12 h-12 rounded-xl bg-lime-200 border-2 border-black flex items-center justify-center text-lime-900 font-bold shadow-[2px_2px_0px_0px_#000]">
              <Target className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-black">Inferred Goal Engine</h3>
            <p className="text-xs text-slate-700 font-medium leading-relaxed">
              Goals are living objects. Progress is inferred automatically whenever study, workout, or weight events are logged.
            </p>
          </div>

          {/* Module 3: Voice Assistant */}
          <div className="neo-card p-6 bg-white space-y-3">
            <div className="w-12 h-12 rounded-xl bg-orange-200 border-2 border-black flex items-center justify-center text-orange-950 font-bold shadow-[2px_2px_0px_0px_#000]">
              <Mic className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-black">Continuous Voice Assistant</h3>
            <p className="text-xs text-slate-700 font-medium leading-relaxed">
              First-class Web Speech-to-Text and Text-to-Speech audio playback for hands-free voice interactions.
            </p>
          </div>

          {/* Module 4: Life Timeline */}
          <div className="neo-card p-6 bg-white space-y-3">
            <div className="w-12 h-12 rounded-xl bg-purple-200 border-2 border-black flex items-center justify-center text-purple-950 font-bold shadow-[2px_2px_0px_0px_#000]">
              <GitBranch className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-black">Git-Style Life Timeline</h3>
            <p className="text-xs text-slate-700 font-medium leading-relaxed">
              Time is a first-class concept. Search across your entire life history (study, workout, gym, reading, meals, journal).
            </p>
          </div>

          {/* Module 5: Smart Typed Memory */}
          <div className="neo-card p-6 bg-white space-y-3">
            <div className="w-12 h-12 rounded-xl bg-pink-200 border-2 border-black flex items-center justify-center text-pink-950 font-bold shadow-[2px_2px_0px_0px_#000]">
              <Brain className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-black">Categorized Memory Bank</h3>
            <p className="text-xs text-slate-700 font-medium leading-relaxed">
              Stores permanent knowledge (Preference, Fact, Relationship, Goal, Habit, Temporal) for deep context injection.
            </p>
          </div>

          {/* Module 6: AI Reports */}
          <div className="neo-card p-6 bg-white space-y-3">
            <div className="w-12 h-12 rounded-xl bg-yellow-200 border-2 border-black flex items-center justify-center text-yellow-950 font-bold shadow-[2px_2px_0px_0px_#000]">
              <FileText className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-black">Qualitative AI Reports</h3>
            <p className="text-xs text-slate-700 font-medium leading-relaxed">
              Periodic Daily, Weekly, and Monthly reviews featuring qualitative reflections, strengths, friction points, and recommendations.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Footer Banner */}
      <div className="neo-card p-8 bg-black text-white text-center space-y-4">
        <h3 className="text-2xl font-black">Ready to Take Control of Your Life Timeline?</h3>
        <p className="text-xs text-slate-300 font-medium max-w-md mx-auto">
          Start talking to LordSahu today. Zero forms. Zero spreadsheets. Just simple conversation.
        </p>
        <button
          onClick={onLaunch}
          className="neo-btn bg-lime-400 text-black px-6 py-2.5 text-xs font-black shadow-[3px_3px_0px_0px_#ffffff]"
        >
          Launch Mission Control Now
        </button>
      </div>
    </div>
  );
}
