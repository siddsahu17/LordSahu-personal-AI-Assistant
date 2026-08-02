import React from 'react';
import { User, Shield, Award, Flame, Zap, Target, Activity } from 'lucide-react';

export default function Profile() {
  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header Profile Card */}
      <div className="neo-card p-6 md:p-8 bg-amber-100 border-3 border-black shadow-[6px_6px_0px_0px_#000] flex flex-col sm:flex-row items-center gap-6">
        <div className="w-20 h-20 rounded-2xl bg-blue-600 border-3 border-black text-white flex items-center justify-center text-3xl font-black shadow-[4px_4px_0px_0px_#000]">
          SS
        </div>
        <div className="space-y-1 text-center sm:text-left">
          <div className="inline-flex items-center gap-1.5 bg-white border-2 border-black px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase">
            OPERATOR IDENTIFICATION
          </div>
          <h2 className="text-2xl font-black text-black">Siddhant Kumar Sahu</h2>
          <p className="text-xs font-bold text-slate-800">Primary Operator • LordSahu Personal Operating System V0.1</p>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="neo-card p-5 bg-white border-3 border-black space-y-1">
          <span className="text-xs font-bold text-slate-600 block">Total Events Logged</span>
          <span className="text-3xl font-black text-black">48</span>
          <span className="text-[10px] font-bold text-emerald-700 block">Immutable Store</span>
        </div>

        <div className="neo-card p-5 bg-white border-3 border-black space-y-1">
          <span className="text-xs font-bold text-slate-600 block">Current Streak</span>
          <span className="text-3xl font-black text-black">12 Days</span>
          <span className="text-[10px] font-bold text-blue-700 block">Active Study & Fitness</span>
        </div>

        <div className="neo-card p-5 bg-white border-3 border-black space-y-1">
          <span className="text-xs font-bold text-slate-600 block">Inferred Goal Velocity</span>
          <span className="text-3xl font-black text-black">7.4 pts</span>
          <span className="text-[10px] font-bold text-purple-700 block">Finals Readiness</span>
        </div>
      </div>
    </div>
  );
}
