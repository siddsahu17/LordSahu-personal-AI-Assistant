import React, { useState, useEffect } from 'react';
import {
  BookOpen, Briefcase, GraduationCap, DollarSign,
  Heart, Code2, Activity, Sparkles, RefreshCw
} from 'lucide-react';
import { fetchWorkspaceOverview } from '../api';

const WORKSPACE_MODULES = [
  { id: 'learning', name: 'Learning (LIM)', icon: BookOpen, color: 'bg-blue-400 text-black' },
  { id: 'career', name: 'Career (CIM)', icon: Briefcase, color: 'bg-purple-400 text-black' },
  { id: 'college', name: 'College', icon: GraduationCap, color: 'bg-amber-400 text-black' },
  { id: 'finance', name: 'Finance', icon: DollarSign, color: 'bg-emerald-400 text-black' },
  { id: 'personal', name: 'Personal', icon: Heart, color: 'bg-pink-400 text-black' },
  { id: 'projects', name: 'Projects', icon: Code2, color: 'bg-indigo-400 text-black' },
  { id: 'fitness', name: 'Fitness (FIM)', icon: Activity, color: 'bg-red-400 text-black' }
];

export default function WorkspaceIntelligenceView() {
  const [selectedWs, setSelectedWs] = useState('learning');
  const [wsData, setWsData] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadData = async (wsId) => {
    try {
      setLoading(true);
      const res = await fetchWorkspaceOverview(wsId);
      setWsData(res);
    } catch (err) {
      console.error("Failed to load workspace overview:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(selectedWs);
  }, [selectedWs]);

  const overview = wsData?.overview || {};
  const insights = overview?.coaching_insights || [];
  const currentMeta = WORKSPACE_MODULES.find(m => m.id === selectedWs) || WORKSPACE_MODULES[0];
  const IconComp = currentMeta.icon;

  return (
    <div className="bg-white border-3 border-black p-5 shadow-[4px_4px_0px_0px_#000] space-y-5">
      {/* Workspace Selector Bar */}
      <div className="flex flex-wrap items-center justify-between border-b-3 border-black pb-3 gap-3">
        <div className="flex items-center gap-2">
          <div className={`p-2.5 border-2 border-black font-black ${currentMeta.color}`}>
            <IconComp className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-black text-black">{wsData?.workspace_name || currentMeta.name}</h3>
            <p className="text-xs font-bold text-gray-600">Standardized Workspace SDK Domain</p>
          </div>
        </div>

        <button
          onClick={() => loadData(selectedWs)}
          className="p-2 bg-[#f7f4ed] hover:bg-black hover:text-white border-2 border-black font-bold transition-colors"
          title="Refresh Workspace Overview"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Workspace Tabs Bar */}
      <div className="flex flex-wrap gap-2">
        {WORKSPACE_MODULES.map((m) => {
          const MIcon = m.icon;
          const isActive = m.id === selectedWs;
          return (
            <button
              key={m.id}
              onClick={() => setSelectedWs(m.id)}
              className={`px-3 py-1.5 border-2 border-black text-xs font-black flex items-center gap-1.5 transition-all shadow-[2px_2px_0px_0px_#000] ${
                isActive ? 'bg-black text-white translate-x-[1px] translate-y-[1px] shadow-none' : 'bg-[#f7f4ed] hover:bg-yellow-300 text-black'
              }`}
            >
              <MIcon className="w-3.5 h-3.5" />
              <span>{m.name}</span>
            </button>
          );
        })}
      </div>

      {/* AI Coaching Insights Banner */}
      {insights.length > 0 && (
        <div className="p-3.5 bg-blue-50 border-2 border-blue-500 rounded space-y-1">
          <div className="flex items-center gap-2 font-black text-blue-900 text-xs uppercase tracking-wider">
            <Sparkles className="w-4 h-4 text-blue-600" />
            <span>AI Domain Mentorship Insights</span>
          </div>
          {insights.map((ins, i) => (
            <p key={i} className="text-xs font-bold text-slate-800">{ins}</p>
          ))}
        </div>
      )}

      {/* Dynamic Workspace Intelligence Data Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Object.entries(overview).map(([key, value]) => {
          if (key === 'coaching_insights') return null;
          const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

          if (Array.isArray(value)) {
            return (
              <div key={key} className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-2 md:col-span-1">
                <h4 className="text-xs font-black text-black uppercase border-b border-black pb-1">{formattedKey}</h4>
                {value.length === 0 ? (
                  <p className="text-xs font-bold text-gray-400">No items recorded yet.</p>
                ) : (
                  <ul className="space-y-1">
                    {value.map((item, idx) => (
                      <li key={idx} className="text-xs font-bold text-slate-800 p-1.5 bg-white border border-black truncate">
                        {typeof item === 'object' ? JSON.stringify(item) : item}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            );
          }

          return (
            <div key={key} className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-1">
              <span className="text-xs font-bold text-gray-500 uppercase">{formattedKey}</span>
              <div className="text-xl font-black text-black">{String(value)}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
