import React, { useState, useEffect } from 'react';
import {
  CheckSquare, Square, Clock, ArrowRightLeft, Sparkles,
  Sunset, Plus, Trash2, Tag, RefreshCw, AlertCircle
} from 'lucide-react';
import {
  fetchTodayPlanner, addPlannerItem, updatePlannerItem, deletePlannerItem,
  carryForwardPlanner, generateMorningBrief, runEveningShutdown
} from '../api';

export default function DailyPlannerView({ onRefreshNeeded }) {
  const [planner, setPlanner] = useState(null);
  const [newTitle, setNewTitle] = useState('');
  const [newPriority, setNewPriority] = useState('medium');
  const [newStartTime, setNewStartTime] = useState('');
  const [newEndTime, setNewEndTime] = useState('');
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await fetchTodayPlanner();
      setPlanner(res);
      if (onRefreshNeeded) onRefreshNeeded();
    } catch (err) {
      console.error("Failed to load Today's Daily Planner:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAddItem = async (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      await addPlannerItem({
        title: newTitle.trim(),
        priority: newPriority,
        start_time: newStartTime || null,
        end_time: newEndTime || null,
        planner_source: 'user'
      });
      setNewTitle('');
      setNewStartTime('');
      setNewEndTime('');
      loadData();
    } catch (err) {
      console.error("Failed to add planner item:", err);
    }
  };

  const handleToggleStatus = async (item) => {
    const nextStatus = item.status === 'completed' ? 'pending' : 'completed';
    try {
      await updatePlannerItem(item.id, {
        status: nextStatus,
        completion_source: nextStatus === 'completed' ? 'manual' : null
      });
      loadData();
    } catch (err) {
      console.error("Failed to toggle status:", err);
    }
  };

  const handleDeleteItem = async (itemId) => {
    try {
      await deletePlannerItem(itemId);
      loadData();
    } catch (err) {
      console.error("Failed to delete item:", err);
    }
  };

  const handleCarryForward = async () => {
    try {
      await carryForwardPlanner();
      loadData();
    } catch (err) {
      console.error("Failed to carry forward:", err);
    }
  };

  const handleMorningBrief = async () => {
    try {
      await generateMorningBrief();
      loadData();
    } catch (err) {
      console.error("Failed to generate morning brief:", err);
    }
  };

  const handleEveningShutdown = async () => {
    try {
      const res = await runEveningShutdown();
      alert(`🌇 Evening Shutdown Summary:\n\n${res.review_prompt}\n\nCompleted: ${res.completed_count} tasks\nRemaining: ${res.remaining_count} tasks`);
      loadData();
    } catch (err) {
      console.error("Failed to run evening shutdown:", err);
    }
  };

  const completionPct = planner?.completion_pct || 0;
  const items = planner?.items || [];

  return (
    <div className="bg-white border-3 border-black p-5 shadow-[4px_4px_0px_0px_#000] space-y-5">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between border-b-3 border-black pb-3 gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-yellow-400 text-black border-2 border-black font-black">
            <CheckSquare className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-black uppercase tracking-wider px-2 py-0.5 bg-black text-white rounded">
                Canonical Object: DailyPlanner
              </span>
              <span className="text-xs font-bold text-gray-600">Date: {planner?.date}</span>
            </div>
            <h3 className="text-lg font-black text-black">Today's Agenda & Intelligent Planner</h3>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={handleCarryForward}
            className="px-2.5 py-1.5 bg-[#f7f4ed] hover:bg-black hover:text-white border-2 border-black text-xs font-black flex items-center gap-1 transition-colors shadow-[2px_2px_0px_0px_#000]"
            title="Carry Forward Unfinished Tasks from Yesterday"
          >
            <ArrowRightLeft className="w-3.5 h-3.5" />
            <span>Carry Forward</span>
          </button>

          <button
            onClick={handleMorningBrief}
            className="px-2.5 py-1.5 bg-yellow-300 hover:bg-black hover:text-white border-2 border-black text-xs font-black flex items-center gap-1 transition-colors shadow-[2px_2px_0px_0px_#000]"
            title="AI Morning Briefing Agenda"
          >
            <Sparkles className="w-3.5 h-3.5 text-purple-700" />
            <span>Morning Brief</span>
          </button>

          <button
            onClick={handleEveningShutdown}
            className="px-2.5 py-1.5 bg-indigo-100 hover:bg-black hover:text-white border-2 border-black text-xs font-black flex items-center gap-1 transition-colors shadow-[2px_2px_0px_0px_#000]"
            title="Run Evening Review & Shutdown"
          >
            <Sunset className="w-3.5 h-3.5 text-indigo-700" />
            <span>Evening Shutdown</span>
          </button>
        </div>
      </div>

      {/* Planner Health % Progress Bar */}
      <div className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-2">
        <div className="flex items-center justify-between text-xs font-black text-black">
          <span>Today's Progress: {completionPct}%</span>
          <span>{planner?.completed_items || 0} / {planner?.total_items || 0} Tasks Completed</span>
        </div>
        <div className="w-full bg-gray-200 h-3 border-2 border-black rounded-full overflow-hidden">
          <div
            className="bg-emerald-500 h-full transition-all"
            style={{ width: `${completionPct}%` }}
          />
        </div>
      </div>

      {/* Add New Planner Item Form */}
      <form onSubmit={handleAddItem} className="flex flex-wrap items-center gap-2">
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Add agenda item (e.g. SQL Revision 18:00)..."
          className="flex-1 min-w-[200px] px-3 py-1.5 bg-[#f7f4ed] border-2 border-black text-xs font-bold text-black focus:outline-none focus:bg-white shadow-[2px_2px_0px_0px_#000]"
        />
        <select
          value={newPriority}
          onChange={(e) => setNewPriority(e.target.value)}
          className="px-2.5 py-1.5 bg-[#f7f4ed] border-2 border-black text-xs font-bold text-black"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <input
          type="text"
          value={newStartTime}
          onChange={(e) => setNewStartTime(e.target.value)}
          placeholder="Start (18:00)"
          className="w-24 px-2 py-1.5 bg-[#f7f4ed] border-2 border-black text-xs font-bold text-black"
        />
        <input
          type="text"
          value={newEndTime}
          onChange={(e) => setNewEndTime(e.target.value)}
          placeholder="End (19:30)"
          className="w-24 px-2 py-1.5 bg-[#f7f4ed] border-2 border-black text-xs font-bold text-black"
        />
        <button
          type="submit"
          className="px-4 py-1.5 bg-black text-white text-xs font-black border-2 border-black flex items-center gap-1 hover:bg-gray-800 transition-colors shadow-[2px_2px_0px_0px_#000]"
        >
          <Plus className="w-4 h-4" />
          <span>Add Task</span>
        </button>
      </form>

      {/* Planner Items Checklist Stream */}
      {items.length === 0 ? (
        <div className="p-6 text-center border-2 border-dashed border-gray-300 rounded bg-[#f7f4ed]">
          <p className="text-xs font-bold text-gray-500">No items on today's agenda yet.</p>
          <p className="text-[11px] font-medium text-gray-400 mt-1">Click "Morning Brief" or type in chat "Add to planner: Gym 18:00"</p>
        </div>
      ) : (
        <div className="space-y-2">
          {items.map((item) => {
            const isDone = item.status === 'completed';
            return (
              <div
                key={item.id}
                className={`p-3 border-2 border-black flex flex-wrap items-center justify-between gap-3 transition-colors ${
                  isDone ? 'bg-emerald-50 border-emerald-700 opacity-80' : 'bg-[#f7f4ed]'
                }`}
              >
                <div className="flex items-center gap-3">
                  <button onClick={() => handleToggleStatus(item)} className="text-black hover:scale-110 transition-transform">
                    {isDone ? <CheckSquare className="w-5 h-5 text-emerald-700" /> : <Square className="w-5 h-5 text-gray-700" />}
                  </button>

                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-black ${isDone ? 'line-through text-gray-500' : 'text-black'}`}>
                        {item.title}
                      </span>

                      {item.priority === 'high' && (
                        <span className="text-[9px] font-black uppercase px-1.5 py-0.2 bg-red-100 border border-red-600 text-red-900 rounded">
                          HIGH
                        </span>
                      )}

                      {item.planner_source && (
                        <span className="text-[9px] font-bold uppercase px-1.5 py-0.2 bg-purple-100 border border-purple-600 text-purple-900 rounded">
                          {item.planner_source}
                        </span>
                      )}

                      {item.completion_source === 'life_entry' && (
                        <span className="text-[9px] font-black uppercase px-1.5 py-0.2 bg-emerald-200 border border-emerald-800 text-emerald-950 rounded">
                          Sync: LifeEntry
                        </span>
                      )}
                    </div>

                    {(item.start_time || item.repeat_rule) && (
                      <div className="flex items-center gap-3 text-[11px] font-bold text-gray-600 mt-0.5">
                        {item.start_time && (
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3 text-blue-600" />
                            {item.start_time} {item.end_time ? `- ${item.end_time}` : ''}
                          </span>
                        )}
                        {item.repeat_rule && (
                          <span className="text-purple-700 uppercase text-[10px]">
                            Repeat: {item.repeat_rule}
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                <button
                  onClick={() => handleDeleteItem(item.id)}
                  className="p-1 hover:bg-red-100 hover:text-red-700 text-gray-400 rounded transition-colors"
                  title="Delete item"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
