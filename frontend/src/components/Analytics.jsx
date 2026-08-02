import React, { useState, useEffect } from 'react';
import { BarChart2, TrendingUp, Flame, Activity, Zap, Layers, Award } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { fetchDashboard } from '../api';

export default function Analytics() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard()
      .then((res) => {
        setAnalyticsData(res.analytics);
      })
      .catch((e) => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  const studyData = [
    { day: 'Mon', hours: 2.5 },
    { day: 'Tue', hours: 3.0 },
    { day: 'Wed', hours: 1.5 },
    { day: 'Thu', hours: 4.0 },
    { day: 'Fri', hours: 3.5 },
    { day: 'Sat', hours: 2.0 },
    { day: 'Sun', hours: 3.5 }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="neo-card p-6 bg-white border-3 border-black">
        <h2 className="text-2xl font-black text-black flex items-center gap-2">
          <BarChart2 className="w-6 h-6 text-blue-600" />
          Analytics & Performance Heatmaps
        </h2>
        <p className="text-xs font-bold text-slate-700 mt-1">
          Clean, chart-only visual insights tracking your weight trajectory, study hours, and consistency habits.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12 font-bold text-slate-700 text-sm">
          Loading analytics computations...
        </div>
      ) : (
        <div className="space-y-6">
          {/* Top Charts Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Study Hours Bar Chart */}
            <div className="neo-card p-6 bg-white border-3 border-black space-y-4">
              <div className="flex items-center justify-between border-b-2 border-black pb-2">
                <h3 className="text-base font-black text-black flex items-center gap-2">
                  <Zap className="w-4 h-4 text-blue-600" />
                  Study Hours Breakdown (Past 7 Days)
                </h3>
                <span className="neo-badge-blue text-xs px-2 py-0.5 rounded">
                  Total: {analyticsData?.total_study_hours || 20.0} hrs
                </span>
              </div>

              <div className="h-56 w-full pt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={studyData}>
                    <XAxis dataKey="day" stroke="#000" fontSize={11} fontWeight={700} />
                    <YAxis stroke="#000" fontSize={11} fontWeight={700} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#ffffff', borderColor: '#000000', borderWidth: '2px', borderRadius: '8px', fontWeight: 'bold' }}
                    />
                    <Bar dataKey="hours" fill="#2563eb" stroke="#000000" strokeWidth={2} radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Weight Trajectory Area Chart */}
            <div className="neo-card p-6 bg-white border-3 border-black space-y-4">
              <div className="flex items-center justify-between border-b-2 border-black pb-2">
                <h3 className="text-base font-black text-black flex items-center gap-2">
                  <Activity className="w-4 h-4 text-emerald-600" />
                  Weight Loss Trajectory (kg)
                </h3>
                <span className="neo-badge-lime text-xs px-2 py-0.5 rounded">
                  Target: 80.0 kg
                </span>
              </div>

              <div className="h-56 w-full pt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={analyticsData?.weight_trend_kg || []}>
                    <XAxis dataKey="date" stroke="#000" fontSize={11} fontWeight={700} />
                    <YAxis domain={['dataMin - 1', 'dataMax + 1']} stroke="#000" fontSize={11} fontWeight={700} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#ffffff', borderColor: '#000000', borderWidth: '2px', borderRadius: '8px', fontWeight: 'bold' }}
                    />
                    <Area type="monotone" dataKey="weight" stroke="#000000" strokeWidth={3} fill="#84cc16" fillOpacity={0.4} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Activity Heatmap Grid */}
          <div className="neo-card p-6 bg-white border-3 border-black space-y-4">
            <h3 className="text-base font-black text-black flex items-center gap-2 border-b-2 border-black pb-2">
              <Flame className="w-4 h-4 text-orange-600" />
              14-Day Activity Heatmap & Consistency Grid
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3">
              {analyticsData?.activity_heatmap?.map((item, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-xl border-2 border-black text-center font-bold text-xs space-y-1 shadow-[2px_2px_0px_0px_#000] ${
                    item.count > 2 ? 'bg-lime-300 text-black' : item.count > 0 ? 'bg-amber-200 text-black' : 'bg-slate-100 text-slate-500'
                  }`}
                >
                  <span className="block text-[10px] uppercase font-mono">{item.date}</span>
                  <span className="text-lg font-black">{item.count}</span>
                  <span className="block text-[9px] uppercase">Events</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
