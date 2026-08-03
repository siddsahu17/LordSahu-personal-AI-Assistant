import React, { useState, useEffect } from 'react';
import {
  Sparkles, Calendar, Clock, Flame, Activity, RefreshCw,
  BookOpen, DollarSign, Scale, ArrowRight, BookMarked, CheckSquare
} from 'lucide-react';
import Chat from './Chat';
import LifeTimelineView from './LifeTimelineView';
import DailyPlannerView from './DailyPlannerView';
import { fetchDailyChronicle, fetchLifeInsights, fetchRecentTopic } from '../api';

export default function MissionControl({ currentMode, setCurrentMode, activeWorkspace }) {
  const [chronicle, setChronicle] = useState(null);
  const [insights, setInsights] = useState(null);
  const [recentTopic, setRecentTopic] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const chron = await fetchDailyChronicle();
      setChronicle(chron);
      const ins = await fetchLifeInsights();
      setInsights(ins);
      const rec = await fetchRecentTopic();
      setRecentTopic(rec);
    } catch (err) {
      console.error("Failed to load Mission Control data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [activeWorkspace]);

  const weightTrend = insights?.weight_trend?.current_weight_kg || 97.4;
  const learningCount = insights?.learning_progress?.concepts_and_topics || 0;
  const moneySpent = insights?.money_flow?.total_spent_rupees || 0.0;
  const projectCount = insights?.project_progress?.features_and_commits || 0;
  const activeDays = insights?.activity_heatmap?.active_days_count || 1;

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Top Banner - Personal AI Operating System Status */}
      <div className="bg-white border-3 border-black p-4 shadow-[4px_4px_0px_0px_#000] flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-[#f59e0b] border-2 border-black font-black text-black">
            <BookMarked className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-black uppercase tracking-wider px-2 py-0.5 bg-black text-white rounded">
                LordSahu V1.4 Heartbeat Lifecycle
              </span>
              <span className="text-xs font-bold text-gray-600">{chronicle?.date || ''}</span>
            </div>
            <h2 className="text-lg font-black text-black">Good Morning Siddhant</h2>
            <p className="text-xs font-medium text-gray-700">3 Canonical Objects: DailyPlanner ➔ LifeEntries ➔ DailyChronicle</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <span className="text-xs font-bold text-gray-500 uppercase">Active Streak</span>
            <div className="text-xl font-black text-black flex items-center justify-end gap-1">
              <Flame className="w-5 h-5 text-amber-500 fill-amber-500" />
              {activeDays} Days
            </div>
          </div>

          <button
            onClick={loadData}
            className="p-2 bg-[#f7f4ed] hover:bg-black hover:text-white border-2 border-black transition-colors font-bold"
            title="Refresh Mission Control State"
          >
            <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Priority 1: Today's Daily Planner Agenda Widget */}
      <DailyPlannerView onRefreshNeeded={loadData} />

      {/* Priority 2 & 3: Main Grid (Timeline, Briefings & AI Conversational Centerpiece) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Morning Briefing, Evening Shutdown & Resume Card */}
        <div className="space-y-6 lg:col-span-1">
          {/* Continue Where You Left Off Card */}
          {recentTopic && (
            <div className="bg-[#f7f4ed] border-3 border-black p-4 shadow-[4px_4px_0px_0px_#000] space-y-2">
              <div className="flex items-center justify-between border-b-2 border-black pb-1.5">
                <span className="text-xs font-black uppercase text-purple-900 flex items-center gap-1">
                  <Sparkles className="w-4 h-4 text-purple-600" />
                  <span>Continue Where You Left Off</span>
                </span>
                <span className="text-[10px] font-bold text-gray-500">{recentTopic.timestamp}</span>
              </div>
              <h4 className="text-sm font-black text-black">{recentTopic.title}</h4>
              <p className="text-xs font-bold text-gray-700 truncate">{recentTopic.raw_text}</p>
              <div className="pt-1 flex items-center text-xs font-extrabold text-purple-700 gap-1 cursor-pointer hover:underline">
                <span>Resume topic in chat</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          )}

          {/* Today's AI Daily Chronicle Card */}
          <div className="bg-white border-3 border-black p-4 shadow-[4px_4px_0px_0px_#000] space-y-3">
            <div className="flex items-center justify-between border-b-2 border-black pb-2">
              <div className="flex items-center gap-2 font-black text-black">
                <BookMarked className="w-5 h-5 text-amber-600" />
                <span>Today's Daily Chronicle</span>
              </div>
              <span className="text-xs font-bold px-2 py-0.5 bg-amber-100 border border-amber-600 text-amber-900 rounded">
                Nightly Reflection
              </span>
            </div>

            <p className="text-xs font-bold text-slate-800 leading-relaxed">
              {chronicle?.ai_reflection || "No diary entries logged today yet."}
            </p>

            {chronicle?.domain_highlights && Object.keys(chronicle.domain_highlights).length > 0 && (
              <div className="space-y-2 pt-2 border-t border-gray-200">
                {Object.entries(chronicle.domain_highlights).map(([dom, items]) => (
                  <div key={dom} className="space-y-1">
                    <span className="text-[11px] font-black uppercase text-gray-500">{dom}</span>
                    {items.map((it, idx) => (
                      <p key={idx} className="text-xs font-bold text-black pl-2">{it}</p>
                    ))}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Priority 4: Conversational AI Centerpiece Chat Window */}
        <div className="lg:col-span-2">
          <Chat
            currentMode={currentMode}
            setCurrentMode={setCurrentMode}
            activeWorkspace={activeWorkspace}
          />
        </div>
      </div>

      {/* Priority 2: Git-History Style Life Entry Timeline Stream */}
      <LifeTimelineView />
    </div>
  );
}
