import React, { useState, useEffect } from 'react';
import {
  Activity, Scale, Flame, Droplets, Moon, Trophy,
  Dumbbell, Sparkles, RefreshCw
} from 'lucide-react';
import { fetchFitnessOverview } from '../api';

export default function FitnessJournalView() {
  const [fitnessData, setFitnessData] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const overview = await fetchFitnessOverview();
      setFitnessData(overview);
    } catch (err) {
      console.error("Failed to load Fitness Overview:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const latestWeight = fitnessData?.latest_weight_kg;
  const movingAvg = fitnessData?.weight_moving_avg_7d;
  const weeklyVol = fitnessData?.weekly_workout_volume_kg || 0;
  const waterLiters = fitnessData?.water_today_liters || 0;
  const avgSleep = fitnessData?.avg_sleep_hours || 7.5;
  const insights = fitnessData?.coaching_insights || [];
  const workouts = fitnessData?.recent_workouts || [];
  const sports = fitnessData?.recent_sports || [];
  const prs = fitnessData?.personal_records || [];

  return (
    <div className="bg-white border-3 border-black p-5 shadow-[4px_4px_0px_0px_#000] space-y-5">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between border-b-3 border-black pb-3 gap-2">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-400 border-2 border-black font-black text-black">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-black text-black">Fitness Intelligence Module (FIM)</h3>
            <p className="text-xs font-bold text-gray-600">Conversational Fitness Journal & AI Coach</p>
          </div>
        </div>

        <button
          onClick={loadData}
          className="p-2 bg-[#f7f4ed] hover:bg-black hover:text-white border-2 border-black font-bold transition-colors"
          title="Refresh Fitness State"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* AI Coaching Insights Banner */}
      {insights.length > 0 && (
        <div className="p-3.5 bg-amber-50 border-2 border-amber-500 rounded space-y-1">
          <div className="flex items-center gap-2 font-black text-amber-900 text-xs uppercase tracking-wider">
            <Sparkles className="w-4 h-4 text-amber-600" />
            <span>AI Fitness Coaching Insights</span>
          </div>
          {insights.map((ins, i) => (
            <p key={i} className="text-xs font-bold text-slate-800" dangerouslySetInnerHTML={{ __html: ins.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
          ))}
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {/* Body Weight Gauge */}
        <div className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-1">
          <div className="flex items-center justify-between text-xs font-bold text-gray-500">
            <span>Body Weight</span>
            <Scale className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-xl font-black text-black">
            {latestWeight ? `${latestWeight} kg` : 'Not logged'}
          </div>
          <div className="text-[11px] font-semibold text-gray-600">
            {movingAvg ? `7d Avg: ${movingAvg} kg` : 'Log via chat: "My weight is 96.5"'}
          </div>
        </div>

        {/* Workout Volume Gauge */}
        <div className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-1">
          <div className="flex items-center justify-between text-xs font-bold text-gray-500">
            <span>Workout Volume</span>
            <Dumbbell className="w-4 h-4 text-purple-600" />
          </div>
          <div className="text-xl font-black text-black">
            {weeklyVol} kg
          </div>
          <div className="text-[11px] font-semibold text-gray-600">
            {workouts.length} sessions logged
          </div>
        </div>

        {/* Hydration Target */}
        <div className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-1">
          <div className="flex items-center justify-between text-xs font-bold text-gray-500">
            <span>Hydration</span>
            <Droplets className="w-4 h-4 text-cyan-600" />
          </div>
          <div className="text-xl font-black text-black">
            {waterLiters} / 3.0 L
          </div>
          <div className="w-full bg-gray-200 h-2 border border-black rounded-full overflow-hidden mt-1">
            <div
              className="bg-cyan-500 h-full transition-all"
              style={{ width: `${Math.min(100, (waterLiters / 3.0) * 100)}%` }}
            />
          </div>
        </div>

        {/* Sleep Target */}
        <div className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-1">
          <div className="flex items-center justify-between text-xs font-bold text-gray-500">
            <span>Sleep Duration</span>
            <Moon className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-xl font-black text-black">
            {avgSleep} hrs
          </div>
          <div className="text-[11px] font-semibold text-gray-600">
            Target: 8.0 hrs
          </div>
        </div>
      </div>

      {/* Grid: Workouts & Sports Journal */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Recent Workouts Feed */}
        <div className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-2">
          <h4 className="text-xs font-black text-black uppercase flex items-center gap-1.5 border-b-2 border-black pb-1.5">
            <Flame className="w-4 h-4 text-amber-500" />
            <span>Recent Workout Sessions</span>
          </h4>
          {workouts.length === 0 ? (
            <p className="text-xs font-bold text-gray-400 py-2 text-center">No workout sessions recorded yet.</p>
          ) : (
            <div className="space-y-2">
              {workouts.map((w) => (
                <div key={w.id} className="p-2 bg-white border border-black text-xs font-bold space-y-1">
                  <div className="flex items-center justify-between text-black">
                    <span>{w.workout_type}</span>
                    <span className="text-[10px] text-gray-500">{w.date}</span>
                  </div>
                  <div className="text-[11px] text-purple-700 font-extrabold">
                    Total Volume: {w.volume_kg} kg ({w.exercises?.length || 0} exercises)
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Sports & PR Feed */}
        <div className="p-3.5 bg-[#f7f4ed] border-2 border-black space-y-2">
          <h4 className="text-xs font-black text-black uppercase flex items-center gap-1.5 border-b-2 border-black pb-1.5">
            <Trophy className="w-4 h-4 text-yellow-500" />
            <span>Sports & Personal Records</span>
          </h4>
          {sports.length === 0 && prs.length === 0 ? (
            <p className="text-xs font-bold text-gray-400 py-2 text-center">No sports or PR events recorded yet.</p>
          ) : (
            <div className="space-y-2">
              {prs.map((pr, idx) => (
                <div key={idx} className="p-2 bg-yellow-50 border border-yellow-500 text-xs font-bold flex items-center justify-between">
                  <span className="text-yellow-900">🏆 PR: {pr.exercise} @ {pr.weight_kg}kg</span>
                  <span className="text-[10px] text-gray-500">{pr.date}</span>
                </div>
              ))}
              {sports.map((s, idx) => (
                <div key={idx} className="p-2 bg-white border border-black text-xs font-bold flex items-center justify-between">
                  <span className="text-emerald-800">⚽ {s.sport_name} ({s.duration_mins} mins)</span>
                  <span className="text-[10px] text-gray-500">{s.date}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
