import React, { useState } from 'react';
import {
  Sparkles,
  Flame,
  Zap,
  Target,
  Clock,
  TrendingUp,
  Activity,
  Award,
  BookOpen,
  Send,
  Mic,
  Calendar,
  Layers,
  ArrowRight,
  Plus,
  CheckCircle2
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard({ data, onQuickChat, onNavigate, currentMode }) {
  const [quickInput, setQuickInput] = useState('');

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="neo-card p-6 bg-white flex items-center gap-3 font-bold text-sm">
          <div className="w-5 h-5 border-3 border-black border-t-transparent rounded-full animate-spin"></div>
          Connecting to LordSahu Mission Control...
        </div>
      </div>
    );
  }

  const { briefing, analytics, goals, recent_events } = data;

  const handleSubmitQuick = (e) => {
    e.preventDefault();
    if (!quickInput.trim()) return;
    onQuickChat(quickInput);
    setQuickInput('');
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* 1. Welcome Header & Morning Briefing */}
      <div className="neo-card p-6 md:p-8 bg-amber-100 border-3 border-black shadow-[6px_6px_0px_0px_#000] relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-2 bg-white border-2 border-black px-3 py-1 rounded-full text-xs font-black shadow-[2px_2px_0px_0px_#000]">
              <Sparkles className="w-3.5 h-3.5 text-black fill-black" />
              MORNING BRIEFING & AI ORCHESTRATOR
            </div>
            <h1 className="text-3xl md:text-5xl font-black text-black">
              Good Morning, <span className="underline decoration-blue-600 decoration-4">Siddhant</span>
            </h1>
            <p className="text-slate-900 text-sm md:text-base font-bold leading-relaxed">
              {briefing?.coach_advice || "Your consistency is up 18%! Focus on your DBMS assignment today."}
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2 text-xs font-extrabold">
              <span className="bg-white px-3 py-1 rounded-xl border-2 border-black shadow-[2px_2px_0px_0px_#000] flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-blue-600" /> Sleep: 7.0 Hours
              </span>
              <span className="bg-white px-3 py-1 rounded-xl border-2 border-black shadow-[2px_2px_0px_0px_#000] flex items-center gap-1.5 text-emerald-800">
                <Activity className="w-3.5 h-3.5 text-emerald-600" /> Weight: {briefing?.current_weight_kg} kg
              </span>
              <span className="bg-white px-3 py-1 rounded-xl border-2 border-black shadow-[2px_2px_0px_0px_#000] flex items-center gap-1.5 text-amber-900">
                <Target className="w-3.5 h-3.5 text-amber-600" /> Priority: {briefing?.top_priority_today}
              </span>
            </div>
          </div>

          {/* Quick Command Box */}
          <div className="w-full md:w-80 bg-white p-4 rounded-xl border-3 border-black shadow-[4px_4px_0px_0px_#000] space-y-3">
            <div className="flex items-center justify-between text-xs font-black text-black border-b-2 border-black pb-2">
              <span>QUICK AI CONVERSATION</span>
              <span className="bg-lime-300 text-black px-2 py-0.5 text-[10px] border border-black font-mono">
                {currentMode.toUpperCase()}
              </span>
            </div>
            <form onSubmit={handleSubmitQuick} className="flex items-center gap-2">
              <input
                type="text"
                value={quickInput}
                onChange={(e) => setQuickInput(e.target.value)}
                placeholder="Talk to LordSahu..."
                className="flex-1 bg-slate-50 text-xs font-bold text-black border-2 border-black rounded-lg px-3 py-2 focus:outline-none focus:bg-white"
              />
              <button
                type="submit"
                className="neo-btn bg-blue-600 hover:bg-blue-500 text-white p-2.5 rounded-lg"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* 2. Key Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Consistency Score */}
        <div className="neo-card p-5 bg-white space-y-2 border-3 border-black">
          <div className="flex items-center justify-between text-xs font-extrabold text-slate-700">
            <span>Consistency Score</span>
            <Flame className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-3xl font-black text-black">{analytics?.consistency_score}%</div>
          <div className="w-full bg-slate-100 border-2 border-black h-3 rounded-full overflow-hidden">
            <div
              className="bg-emerald-500 h-full"
              style={{ width: `${analytics?.consistency_score}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-emerald-700 font-extrabold">+18% vs last week</p>
        </div>

        {/* Goal Velocity */}
        <div className="neo-card p-5 bg-white space-y-2 border-3 border-black">
          <div className="flex items-center justify-between text-xs font-extrabold text-slate-700">
            <span>Goal Velocity</span>
            <Zap className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-3xl font-black text-black">{analytics?.goal_velocity} pts</div>
          <div className="w-full bg-slate-100 border-2 border-black h-3 rounded-full overflow-hidden">
            <div
              className="bg-blue-600 h-full"
              style={{ width: `${(analytics?.goal_velocity / 100) * 100}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-blue-700 font-extrabold">On track for finals</p>
        </div>

        {/* Momentum Index */}
        <div className="neo-card p-5 bg-white space-y-2 border-3 border-black">
          <div className="flex items-center justify-between text-xs font-extrabold text-slate-700">
            <span>Momentum Index</span>
            <TrendingUp className="w-4 h-4 text-purple-600" />
          </div>
          <div className="text-3xl font-black text-black">{analytics?.momentum_index} / 10</div>
          <div className="w-full bg-slate-100 border-2 border-black h-3 rounded-full overflow-hidden">
            <div
              className="bg-purple-600 h-full"
              style={{ width: `${(analytics?.momentum_index / 10) * 100}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-purple-700 font-extrabold">High activity streak</p>
        </div>

        {/* Burnout Risk Score */}
        <div className="neo-card p-5 bg-white space-y-2 border-3 border-black">
          <div className="flex items-center justify-between text-xs font-extrabold text-slate-700">
            <span>Burnout Risk</span>
            <Activity className="w-4 h-4 text-amber-600" />
          </div>
          <div className="text-3xl font-black text-black">{analytics?.burnout_risk_score}%</div>
          <div className="w-full bg-slate-100 border-2 border-black h-3 rounded-full overflow-hidden">
            <div
              className="bg-amber-500 h-full"
              style={{ width: `${analytics?.burnout_risk_score}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-amber-800 font-extrabold">Safe recovery range</p>
        </div>
      </div>

      {/* 3. Middle Section: Active Goals & Weight Progress */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Goals Engine Card */}
        <div className="lg:col-span-2 neo-card p-6 bg-white space-y-4 border-3 border-black">
          <div className="flex items-center justify-between border-b-2 border-black pb-3">
            <h3 className="text-lg font-black text-black flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-600" />
              Active Goals (Inferred Progress)
            </h3>
            <button
              onClick={() => onNavigate('goals')}
              className="neo-btn bg-lime-300 text-black px-3 py-1 text-xs font-extrabold flex items-center gap-1"
            >
              All Goals <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-4">
            {goals && goals.map((goal) => (
              <div key={goal.id} className="bg-slate-50 p-4 rounded-xl border-2 border-black space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-sm text-black">{goal.title}</span>
                  <span className="neo-badge-lime px-2 py-0.5 rounded text-xs">
                    {goal.inferred_progress}%
                  </span>
                </div>
                <p className="text-xs font-medium text-slate-700">{goal.description}</p>
                <div className="w-full bg-white border-2 border-black h-3 rounded-full overflow-hidden">
                  <div
                    className="bg-blue-600 h-full transition-all duration-500"
                    style={{ width: `${goal.inferred_progress}%` }}
                  ></div>
                </div>
                <div className="flex items-center justify-between text-[11px] font-bold text-slate-600 pt-1">
                  <span>Workspace: <strong className="text-black capitalize">{goal.workspace_id}</strong></span>
                  <span>Priority: <strong className="text-red-600">{goal.priority}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Weight Loss & Fitness Card */}
        <div className="neo-card p-6 bg-white space-y-4 border-3 border-black flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b-2 border-black pb-2">
              <h3 className="text-base font-black text-black flex items-center gap-2">
                <Activity className="w-4 h-4 text-emerald-600" />
                Weight Trajectory
              </h3>
              <span className="neo-badge-lime text-xs px-2 py-0.5 rounded">
                Target: 80.0 kg
              </span>
            </div>
            <p className="text-xs font-bold text-slate-700 mt-2">
              Start: ~99.0 kg | Current: {analytics?.latest_weight_kg} kg
            </p>
          </div>

          <div className="h-44 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={analytics?.weight_trend_kg || []}>
                <defs>
                  <linearGradient id="weightGradNeo" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22c55e" stopOpacity={0.6} />
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0.1} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#000" fontSize={11} fontWeight={700} />
                <YAxis domain={['dataMin - 1', 'dataMax + 1']} stroke="#000" fontSize={11} fontWeight={700} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#000000', borderWidth: '2px', borderRadius: '8px', color: '#000', fontWeight: 'bold' }}
                />
                <Area type="monotone" dataKey="weight" stroke="#000000" strokeWidth={3} fillOpacity={1} fill="url(#weightGradNeo)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-emerald-100 p-3 rounded-xl border-2 border-black text-xs font-black text-black flex items-center justify-between">
            <span>Net Progress:</span>
            <span className="text-emerald-800 text-sm font-black">-2.2 kg lost</span>
          </div>
        </div>
      </div>

      {/* 4. Today's Life Events Stream */}
      <div className="neo-card p-6 bg-white space-y-4 border-3 border-black">
        <div className="flex items-center justify-between border-b-2 border-black pb-3">
          <h3 className="text-lg font-black text-black flex items-center gap-2">
            <Clock className="w-5 h-5 text-purple-600" />
            Today's Life Events Stream
          </h3>
          <button
            onClick={() => onNavigate('timeline')}
            className="neo-btn bg-yellow-300 text-black px-3 py-1 text-xs font-extrabold flex items-center gap-1"
          >
            Full Timeline <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {recent_events && recent_events.slice(0, 6).map((evt) => (
            <div key={evt.id} className="bg-slate-50 p-4 rounded-xl border-2 border-black space-y-2 hover:bg-slate-100 transition-all">
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="neo-badge-blue px-2 py-0.5 rounded text-[11px]">
                  {evt.event_type}
                </span>
                <span className="text-slate-600 font-mono">
                  {new Date(evt.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <p className="text-xs font-extrabold text-black line-clamp-2">
                {evt.payload?.notes || evt.payload?.subject || JSON.stringify(evt.payload)}
              </p>
              <div className="text-[10px] font-bold text-slate-500 flex items-center justify-between pt-1 border-t border-slate-200">
                <span>Source: {evt.source}</span>
                <span className="capitalize text-black">Workspace: {evt.workspace_id}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
