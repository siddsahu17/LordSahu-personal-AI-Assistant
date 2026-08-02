import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  MessageSquare,
  Target,
  GitBranch,
  FileText,
  BarChart2,
  Settings,
  User,
  Sparkles,
  Bot,
  Flame,
  Zap,
  Eye,
  Compass,
  Clock,
  Home,
  ChevronDown
} from 'lucide-react';

const PERSONA_MODES = [
  { id: 'assistant', label: 'Chief of Staff', icon: Bot, color: 'bg-blue-100 text-blue-900' },
  { id: 'coach', label: 'Coach Mode', icon: Flame, color: 'bg-lime-200 text-lime-950' },
  { id: 'focus', label: 'Focus Mode', icon: Zap, color: 'bg-amber-200 text-amber-950' },
  { id: 'reflection', label: 'Reflection Mode', icon: Eye, color: 'bg-pink-200 text-pink-950' },
  { id: 'planner', label: 'Planner Mode', icon: Compass, color: 'bg-cyan-200 text-cyan-950' },
  { id: 'reviewer', label: 'Reviewer Mode', icon: BarChart2, color: 'bg-purple-200 text-purple-950' }
];

export default function Navigation({
  activeTab,
  setActiveTab,
  currentMode,
  setCurrentMode,
  activeWorkspace,
  setActiveWorkspace,
  workspaces
}) {
  const [timeStr, setTimeStr] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { id: 'landing', label: 'Home', icon: Home },
    { id: 'dashboard', label: 'Mission Control', icon: LayoutDashboard },
    { id: 'chat', label: 'AI Chat', icon: MessageSquare },
    { id: 'goals', label: 'Goals', icon: Target },
    { id: 'timeline', label: 'Timeline', icon: GitBranch },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'analytics', label: 'Analytics', icon: BarChart2 },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'profile', label: 'Profile', icon: User }
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#f7f4ed] border-b-3 border-black px-4 md:px-6 py-2.5 shadow-[0_4px_0_0_#000]">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Left: Brand Logo & Clock */}
        <div className="flex items-center gap-3">
          <div
            onClick={() => setActiveTab('dashboard')}
            className="flex items-center gap-2 cursor-pointer bg-white px-3 py-1.5 rounded-xl border-2 border-black shadow-[2px_2px_0px_0px_#000] hover:shadow-[4px_4px_0px_0px_#000] transition-all"
          >
            <div className="w-7 h-7 rounded-lg bg-blue-600 border-2 border-black flex items-center justify-center text-white">
              <Sparkles className="w-3.5 h-3.5 fill-white" />
            </div>
            <div>
              <span className="font-black text-sm tracking-tight text-black flex items-center gap-1 leading-none">
                LordSahu
                <span className="text-[9px] bg-amber-300 text-black px-1 py-0.2 border border-black font-mono font-bold rounded">
                  v0.1
                </span>
              </span>
              <p className="text-[8px] text-slate-700 font-bold uppercase mt-0.5">AI Personal OS</p>
            </div>
          </div>

          <div className="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-xl border-2 border-black shadow-[2px_2px_0px_0px_#000] text-xs font-mono font-bold text-black">
            <Clock className="w-3.5 h-3.5 text-blue-600" />
            <span>{timeStr || '12:00 PM'}</span>
          </div>
        </div>

        {/* Center: Dropdowns for Persona Mode & Workspace */}
        <div className="flex items-center gap-2">
          {/* Persona Dropdown */}
          <div className="relative">
            <select
              value={currentMode}
              onChange={(e) => setCurrentMode(e.target.value)}
              className="bg-white text-xs font-extrabold text-black border-2 border-black rounded-xl px-3 py-1.5 shadow-[2px_2px_0px_0px_#000] focus:outline-none cursor-pointer pr-7 appearance-none"
            >
              {PERSONA_MODES.map((m) => (
                <option key={m.id} value={m.id}>
                  Persona: {m.label}
                </option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-black absolute right-2.5 top-2.5 pointer-events-none" />
          </div>

          {/* Workspace Dropdown */}
          <div className="relative">
            <select
              value={activeWorkspace}
              onChange={(e) => setActiveWorkspace(e.target.value)}
              className="bg-white text-xs font-extrabold text-black border-2 border-black rounded-xl px-3 py-1.5 shadow-[2px_2px_0px_0px_#000] focus:outline-none cursor-pointer pr-7 appearance-none"
            >
              <option value="all">Workspace: All</option>
              {workspaces.map((w) => (
                <option key={w.id} value={w.id}>
                  Workspace: {w.name}
                </option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-black absolute right-2.5 top-2.5 pointer-events-none" />
          </div>
        </div>

        {/* Right: Navigation Links */}
        <nav className="flex items-center gap-1 bg-white p-1 rounded-xl border-2 border-black shadow-[2px_2px_0px_0px_#000] overflow-x-auto max-w-full">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-extrabold transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-blue-600 text-white border-2 border-black shadow-[1.5px_1.5px_0px_0px_#000]'
                    : 'text-slate-900 hover:bg-slate-100'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
