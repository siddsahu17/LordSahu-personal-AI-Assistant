import React, { useState, useEffect } from 'react';
import { FileText, Sparkles, CheckCircle2, AlertTriangle, Lightbulb, TrendingUp } from 'lucide-react';
import { fetchReports } from '../api';

export default function Reports() {
  const [timeframe, setTimeframe] = useState('weekly');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadReport = async () => {
    setLoading(true);
    try {
      const data = await fetchReports(timeframe);
      setReport(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport();
  }, [timeframe]);

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header & Timeframe Tabs */}
      <div className="neo-card p-6 bg-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-3 border-black">
        <div>
          <h2 className="text-2xl font-black text-black flex items-center gap-2">
            <FileText className="w-6 h-6 text-blue-600" />
            Qualitative AI Reflections & Reports
          </h2>
          <p className="text-xs font-bold text-slate-700 mt-1">
            Periodic AI reviews comparing your current consistency and goal momentum against past performance.
          </p>
        </div>

        <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border-2 border-black">
          {['daily', 'weekly', 'monthly'].map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-3 py-1.5 rounded-lg text-xs font-black capitalize transition-all ${
                timeframe === tf
                  ? 'bg-blue-600 text-white border-2 border-black shadow-[2px_2px_0px_0px_#000]'
                  : 'text-slate-800 hover:bg-slate-200'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12 font-bold text-slate-700 text-sm">
          Generating qualitative AI reflection report...
        </div>
      ) : report && (
        <div className="space-y-6">
          {/* Main AI Reflection Banner */}
          <div className="neo-card p-6 md:p-8 bg-amber-100 border-3 border-black shadow-[6px_6px_0px_0px_#000] space-y-4">
            <div className="flex items-center justify-between border-b-2 border-black pb-3">
              <div className="flex items-center gap-2 text-black font-black text-sm uppercase tracking-wider">
                <Sparkles className="w-4 h-4 text-black fill-black" />
                {report.timeframe} ({report.period})
              </div>
              <span className="neo-badge-lime text-xs px-3 py-1 rounded">
                Consistency Score: {report.metrics?.consistency_score}%
              </span>
            </div>

            <p className="text-lg text-slate-900 font-extrabold leading-relaxed">
              "{report.reflection}"
            </p>
          </div>

          {/* Strengths & Weaknesses */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="neo-card p-6 bg-white border-3 border-black space-y-3">
              <h3 className="text-base font-black text-emerald-800 flex items-center gap-2 border-b-2 border-black pb-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-600" /> Key Wins & Strengths
              </h3>
              <ul className="space-y-2">
                {report.strengths?.map((s, i) => (
                  <li key={i} className="bg-lime-50 p-3 rounded-xl border-2 border-black text-xs font-bold text-black flex items-start gap-2">
                    <span className="text-emerald-700 font-black">•</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="neo-card p-6 bg-white border-3 border-black space-y-3">
              <h3 className="text-base font-black text-amber-900 flex items-center gap-2 border-b-2 border-black pb-2">
                <AlertTriangle className="w-5 h-5 text-amber-600" /> Friction Points & Weaknesses
              </h3>
              <ul className="space-y-2">
                {report.weaknesses?.map((w, i) => (
                  <li key={i} className="bg-amber-50 p-3 rounded-xl border-2 border-black text-xs font-bold text-black flex items-start gap-2">
                    <span className="text-amber-700 font-black">•</span>
                    <span>{w}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* AI Recommendations */}
          <div className="neo-card p-6 bg-white border-3 border-black space-y-3">
            <h3 className="text-base font-black text-black flex items-center gap-2 border-b-2 border-black pb-2">
              <Lightbulb className="w-5 h-5 text-blue-600" /> Actionable AI Recommendations
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {report.recommendations?.map((rec, i) => (
                <div key={i} className="bg-slate-50 p-3.5 rounded-xl border-2 border-black text-xs font-bold text-black flex items-start gap-2.5">
                  <div className="w-6 h-6 rounded-lg bg-blue-600 text-white font-black flex items-center justify-center flex-shrink-0 text-xs border border-black shadow-[1px_1px_0px_0px_#000]">
                    {i + 1}
                  </div>
                  <span>{rec}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
