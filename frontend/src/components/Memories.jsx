import React, { useState, useEffect } from 'react';
import { Brain, ShieldCheck } from 'lucide-react';
import { fetchMemories } from '../api';

const MEMORY_TYPES = ['ALL', 'PREFERENCE', 'FACT', 'RELATIONSHIP', 'GOAL', 'HABIT', 'TEMPORAL'];

export default function Memories() {
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedType, setSelectedType] = useState('ALL');

  const loadMemories = async () => {
    setLoading(true);
    try {
      const data = await fetchMemories();
      setMemories(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMemories();
  }, []);

  const filtered = selectedType === 'ALL'
    ? memories
    : memories.filter((m) => m.memory_type === selectedType);

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="neo-card p-6 bg-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-3 border-black">
        <div>
          <h2 className="text-2xl font-black text-black flex items-center gap-2">
            <Brain className="w-6 h-6 text-purple-600" />
            Typed Memory Bank
          </h2>
          <p className="text-xs font-bold text-slate-700 mt-1">
            Permanent knowledge remembered by LordSahu categorized by type (Preference, Fact, Relationship, Goal, Habit, Temporal).
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto max-w-full py-1 text-xs font-bold">
          {MEMORY_TYPES.map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`px-3 py-1 rounded-lg transition-all ${
                selectedType === type
                  ? 'bg-blue-600 text-white border-2 border-black shadow-[2px_2px_0px_0px_#000]'
                  : 'bg-slate-100 text-slate-800 border-2 border-black hover:bg-slate-200'
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      {/* Memories Grid */}
      {loading ? (
        <div className="text-center py-12 font-bold text-slate-700 text-sm">
          Loading permanent memories...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((m) => (
            <div key={m.id} className="neo-card-hover p-5 bg-white border-2 border-black space-y-2">
              <div className="flex items-center justify-between">
                <span className={`text-[10px] font-black px-2.5 py-0.5 rounded border-2 border-black uppercase font-mono ${
                  m.memory_type === 'PREFERENCE' ? 'bg-purple-200 text-purple-950' :
                  m.memory_type === 'FACT' ? 'bg-emerald-200 text-emerald-950' :
                  m.memory_type === 'RELATIONSHIP' ? 'bg-cyan-200 text-cyan-950' :
                  m.memory_type === 'HABIT' ? 'bg-amber-200 text-amber-950' :
                  'bg-blue-200 text-blue-950'
                }`}>
                  {m.memory_type}
                </span>
                <span className="text-[10px] font-mono font-bold text-slate-600 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  Confidence: {Math.round(m.confidence * 100)}%
                </span>
              </div>

              <p className="text-sm font-extrabold text-black leading-relaxed pt-1">{m.fact}</p>

              {m.relationship_entity && (
                <div className="text-xs font-mono font-bold text-cyan-900 bg-cyan-100 p-2 rounded-lg border-2 border-black">
                  Relation: {m.relationship_entity}
                </div>
              )}

              <div className="flex items-center justify-between text-[10px] font-bold text-slate-500 pt-1 border-t border-slate-200">
                <span>Category: <strong className="text-black capitalize">{m.category}</strong></span>
                <span>{new Date(m.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
