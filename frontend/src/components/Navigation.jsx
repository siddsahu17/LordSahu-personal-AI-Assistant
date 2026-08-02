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
  Search,
  Bell,
  Clock,
  CompassIcon,
  Home
} from 'lucide-react';

const PERSONA_MODES = [
  { id: 'assistant', label: 'Chief of Staff', icon: Bot, color: 'bg-blue-100 text-blue-900 border-2 border-black' },
  { id: 'coach', label: 'Coach Mode', icon: Flame, color: 'bg-lime-200 text-lime-950 border-2 border-black' },
  { id: 'focus', label: 'Focus Mode', icon: Zap, color: 'bg-amber-200 text-amber-950 border-2 border-black' },
  { id: 'reflection', label: 'Reflection', icon: Eye, color: 'bg-pink-200 text-pink-950 border-2 border-black' },
  { id: 'planner', label: 'Planner', icon: Compass, color: 'bg-cyan-200 text-cyan-950 border-2 border-black' },
  { id: 'reviewer', label: 'Reviewer', icon: BarChart2, color: 'bg-purple-200 text-purple-950 border-2 border-black' }
];

export default function Navigation({
  activeTab,
  setActiveTab,
  currentMode,
  setCurrentMode,
  activeWorkspace,
  setActiveWorkspace,
  workspaces,
  onOpenAuth
}) {
  const [timeStr, setTimeStr] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
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
    <header className="sticky top-0 z-50 bg-[#f7f4ed] border-b-3 border-black px-4 py-3 shadow-[0_4px_0_0_#000]">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Brand & Persona Pills */}
        <div className="flex items-center gap-4 w-full md:w-auto justify-between md:justify-start">
          <div
            onClick={() => setActiveTab('dashboard')}
            className="flex items-center gap-2.5 cursor-pointer bg-white px-3 py-1.5 rounded-xl border-2 border-black shadow-[3px_3px_0px_0px_#000] hover:shadow-[5px_5px_0px_0px_#000] transition-all"
          >
            <div className="w-8 h-8 rounded-lg bg-blue-600 border-2 border-black flex items-center justify-center text-white">
              <Sparkles className="w-4 h-4 fill-white" />
            </div>
            <div>
              <span className="font-extrabold text-base tracking-tight text-black flex items-center gap-1.5">
                LordSahu
                <span className="text-[10px] bg-amber-300 text-black px-1.5 py-0.2 border border-black font-mono font-bold rounded">
                  v0.1
                </span>
              </span>
              <p className="text-[10px] text-slate-700 font-semibold tracking-wide uppercase">AI Personal OS</p>
            </div>
          </div>

          {/* Clock Display */}
          <div className="hidden lg:flex items-center gap-1.5 bg-white px-3 py-1.5 rounded-xl border-2 border-black shadow-[2px_2px_0px_0px_#000] text-xs font-mono font-bold">
            <Clock className="w-3.5 h-3.5 text-blue-600" />
            <span>{timeStr || '12:00:00 PM'}</span>
          </div>

          {/* Persona Selectors */}
          <div className="flex items-center gap-1.5 overflow-x-auto py-1 max-w-[280px] sm:max-w-none">
            {PERSONA_MODES.map((m) => {
              const Icon = m.icon;
              const isActive = currentMode === m.id;
              return (
                <button
                  key={m.id}
                  onClick={() => setCurrentMode(m.id)}
                  className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                    isActive
                      ? m.color + ' shadow-[2px_2px_0px_0px_#000]'
                      : 'bg-white text-slate-800 border-2 border-black hover:bg-slate-100'
                  }`}
                  title={`Switch persona mode to ${m.label}`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span className="hidden xl:inline">{m.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Navigation Tabs & Actions */}
        <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto justify-between md:justify-end">
          {/* Workspace Filter */}
          <select
            value={activeWorkspace}
            onChange={(e) => setActiveWorkspace(e.target.value)}
            className="bg-white text-xs font-bold text-black border-2 border-black rounded-xl px-2.5 py-1.5 shadow-[2px_2px_0px_0px_#000] focus:outline-none"
          >
            <option value="all">All Workspaces</option>
            {workspaces.map((w) => (
              <option key={w.id} value={w.id}>
                {w.name}
              </option>
            ))}
          </select>

          {/* Nav Links */}
          <nav className="flex items-center gap-1 bg-white p-1 rounded-xl border-2 border-black shadow-[3px_3px_0px_0px_#000]">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-extrabold transition-all ${
                    isActive
                      ? 'bg-blue-600 text-white border-2 border-black shadow-[2px_2px_0px_0px_#000]'
                      : 'text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span className="hidden md:inline">{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Auth Button */}
          <button
            onClick={onOpenAuth}
            className="neo-btn bg-lime-300 text-black px-3 py-1.5 text-xs font-extrabold flex items-center gap-1"
          >
            <User className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Auth</span>
          </button>
        </div>
      </div>
    </header>
  );
}
