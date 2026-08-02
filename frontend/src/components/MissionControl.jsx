import React, { useState, useEffect } from 'react';
import {
  Sparkles, Calendar, Target, Clock, ShieldCheck,
  Flame, Activity, Mic, RefreshCw
} from 'lucide-react';
import Chat from './Chat';
import FitnessJournalView from './FitnessJournalView';
import WorkspaceIntelligenceView from './WorkspaceIntelligenceView';
import { fetchDashboard, fetchCalendarEvents } from '../api';

export default function MissionControl({ currentMode, setCurrentMode, activeWorkspace }) {
  const [data, setData] = useState(null);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadMissionData = async () => {
    try {
      setLoading(true);
      const dash = await fetchDashboard();
      setData(dash);
      const cal = await fetchCalendarEvents();
      setCalendarEvents(cal || []);
    } catch (err) {
      console.error("Failed to load Mission Control data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMissionData();
  }, [activeWorkspace]);

  const briefing = data?.briefing || {};
  const osPhase = data?.context?.os_phase || { label: 'Active OS Phase', focus: 'AI Command Center' };
  const goals = data?.goals || [];
  const analytics = data?.analytics || {};

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Top Banner - JARVIS OS Phase Status */}
      <div className="bg-white border-3 border-black p-4 shadow-[4px_4px_0px_0px_#000] flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-[#f59e0b] border-2 border-black font-black text-black">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-black uppercase tracking-wider px-2 py-0.5 bg-black text-white rounded">
                OS Phase: {osPhase.phase || 'ACTIVE'}
              </span>
              <span className="text-xs font-bold text-gray-600">{osPhase.formatted_time || ''}</span>
            </div>
            <h2 className="text-lg font-black text-black">{osPhase.label}</h2>
            <p className="text-xs font-medium text-gray-700">{osPhase.focus}</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <span className="text-xs font-bold text-gray-500 uppercase">Consistency</span>
            <div className="text-xl font-black text-black flex items-center justify-end gap-1">
              <Flame className="w-5 h-5 text-amber-500 fill-amber-500" />
              {analytics.consistency_score || 100}%
            </div>
          </div>

          <button
            onClick={loadMissionData}
            className="p-2 bg-[#f7f4ed] hover:bg-black hover:text-white border-2 border-black transition-colors font-bold"
            title="Refresh Mission Control State"
          >
            <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Main Grid: Chat Centerpiece + OS Widgets */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Widget Sidebar (Google Calendar & Living Goals) */}
        <div className="space-y-6 lg:col-span-1">
          {/* Google Calendar Schedule Widget */}
          <div className="bg-white border-3 border-black p-4 shadow-[4px_4px_0px_0px_#000] space-y-3">
            <div className="flex items-center justify-between border-b-2 border-black pb-2">
              <div className="flex items-center gap-2 font-black text-black">
                <Calendar className="w-5 h-5 text-blue-600" />
                <span>Google Calendar</span>
              </div>
              <span className="text-xs font-bold px-2 py-0.5 bg-blue-100 border border-blue-600 text-blue-900 rounded">
                Live Sync
              </span>
            </div>

            {calendarEvents.length === 0 ? (
              <div className="p-4 text-center border-2 border-dashed border-gray-300 rounded bg-[#f7f4ed]">
                <p className="text-xs font-bold text-gray-500">No upcoming calendar events.</p>
                <p className="text-[11px] font-medium text-gray-400 mt-1">
                  Say "Schedule study session tomorrow 9am" to add to Google Calendar.
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                {calendarEvents.map((evt) => (
                  <div key={evt.id} className="p-2.5 bg-[#f7f4ed] border-2 border-black flex items-start justify-between">
                    <div>
                      <h4 className="text-sm font-black text-black">{evt.title}</h4>
                      <p className="text-xs font-medium text-gray-600">{evt.start_time}</p>
                    </div>
                    {evt.synced_to_google && (
                      <span className="text-[10px] font-black uppercase text-green-700 bg-green-100 border border-green-700 px-1.5 py-0.5 rounded">
                        Google Sync
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Living Goals State Widget */}
          <div className="bg-white border-3 border-black p-4 shadow-[4px_4px_0px_0px_#000] space-y-3">
            <div className="flex items-center justify-between border-b-2 border-black pb-2">
              <div className="flex items-center gap-2 font-black text-black">
                <Target className="w-5 h-5 text-green-600" />
                <span>Active Goals</span>
              </div>
              <span className="text-xs font-bold px-2 py-0.5 bg-green-100 border border-green-600 text-green-900 rounded">
                {goals.length} Living
              </span>
            </div>

            {goals.length === 0 ? (
              <div className="p-4 text-center border-2 border-dashed border-gray-300 rounded bg-[#f7f4ed]">
                <p className="text-xs font-bold text-gray-500">No active goals in database.</p>
                <p className="text-[11px] font-medium text-gray-400 mt-1">
                  Say "Add goal to learn SQL" to create one.
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                {goals.slice(0, 4).map((g) => (
                  <div key={g.id} className="p-2.5 bg-[#f7f4ed] border-2 border-black">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-black text-black truncate">{g.title}</h4>
                      <span className="text-[10px] font-bold px-1.5 py-0.5 bg-black text-white uppercase rounded">
                        {g.workspace_id}
                      </span>
                    </div>
                    <div className="mt-1 flex items-center justify-between text-[11px] text-gray-600 font-bold">
                      <span>Target: {g.target_value} {g.target_metric || 'units'}</span>
                      <span className="text-green-700">In Progress</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Centerpiece AI Chat Window */}
        <div className="lg:col-span-2">
          <Chat
            currentMode={currentMode}
            setCurrentMode={setCurrentMode}
            activeWorkspace={activeWorkspace}
          />
        </div>
      </div>

      {/* Multi-Workspace Intelligence Framework Section */}
      <WorkspaceIntelligenceView />

      {/* Fitness Intelligence Module (FIM) Journal Section */}
      <FitnessJournalView />
    </div>
  );
}
