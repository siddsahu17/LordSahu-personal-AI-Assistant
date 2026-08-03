import React, { useState, useEffect } from 'react';
import {
  GitCommit, Search, Sparkles, Filter, Activity,
  BookOpen, Briefcase, GraduationCap, DollarSign, Heart, Code2, RefreshCw
} from 'lucide-react';
import { fetchLifeEntries } from '../api';

const DOMAIN_ICONS = {
  learning: BookOpen,
  career: Briefcase,
  college: GraduationCap,
  finance: DollarSign,
  personal: Heart,
  projects: Code2,
  fitness: Activity
};

export default function LifeTimelineView() {
  const [entries, setEntries] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedDomain, setSelectedDomain] = useState('all');
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await fetchLifeEntries(selectedDomain, 'all', search);
      setEntries(res || []);
    } catch (err) {
      console.error("Failed to load life entries timeline:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedDomain]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadData();
  };

  return (
    <div className="bg-white border-3 border-black p-5 shadow-[4px_4px_0px_0px_#000] space-y-5">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between border-b-3 border-black pb-3 gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-black text-white border-2 border-black font-black">
            <GitCommit className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-black text-black">Git-History Life Entry Timeline</h3>
            <p className="text-xs font-bold text-gray-600">Chronological Personal Journal & Life Event Stream</p>
          </div>
        </div>

        {/* Search Input Bar */}
        <form onSubmit={handleSearchSubmit} className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-2.5 top-2.5" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search entries (e.g. Docker, workout, ₹250)..."
              className="pl-8 pr-3 py-1.5 bg-[#f7f4ed] border-2 border-black text-xs font-bold text-black focus:outline-none focus:bg-white w-64 shadow-[2px_2px_0px_0px_#000]"
            />
          </div>
          <button
            type="submit"
            className="px-3 py-1.5 bg-black text-white text-xs font-black border-2 border-black hover:bg-gray-800 transition-colors shadow-[2px_2px_0px_0px_#000]"
          >
            Search
          </button>
        </form>
      </div>

      {/* Domain Filters */}
      <div className="flex flex-wrap gap-2">
        {['all', 'learning', 'fitness', 'career', 'college', 'finance', 'projects', 'personal'].map((d) => (
          <button
            key={d}
            onClick={() => setSelectedDomain(d)}
            className={`px-3 py-1 border-2 border-black text-xs font-black uppercase transition-all shadow-[2px_2px_0px_0px_#000] ${
              selectedDomain === d ? 'bg-black text-white translate-x-[1px] translate-y-[1px] shadow-none' : 'bg-[#f7f4ed] hover:bg-yellow-300 text-black'
            }`}
          >
            {d}
          </button>
        ))}
      </div>

      {/* Timeline Stream */}
      {entries.length === 0 ? (
        <div className="p-8 text-center border-2 border-dashed border-gray-300 rounded bg-[#f7f4ed]">
          <p className="text-xs font-bold text-gray-500">No life entries match your query.</p>
          <p className="text-[11px] font-medium text-gray-400 mt-1">Speak or type naturally in chat to add your first life entry!</p>
        </div>
      ) : (
        <div className="relative border-l-3 border-black ml-4 pl-6 space-y-4">
          {entries.map((entry) => (
            <div key={entry.id} className="relative bg-[#f7f4ed] border-2 border-black p-3.5 space-y-1.5 shadow-[3px_3px_0px_0px_#000]">
              {/* Git commit node bullet */}
              <div className="absolute -left-[31px] top-4 w-4 h-4 bg-yellow-400 border-2 border-black rounded-full" />

              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-black text-black">{entry.title}</span>
                  {entry.confidence && (
                    <span className="text-[10px] font-black px-1.5 py-0.5 bg-green-100 border border-green-700 text-green-900 rounded">
                      {(entry.confidence * 100).toFixed(0)}% Conf
                    </span>
                  )}
                </div>
                <span className="text-[11px] font-bold text-gray-500">{entry.timestamp}</span>
              </div>

              {/* Domains Badges */}
              <div className="flex flex-wrap gap-1.5">
                {entry.domains && entry.domains.map((dom) => {
                  const Icon = DOMAIN_ICONS[dom] || BookOpen;
                  return (
                    <span key={dom} className="text-[10px] font-extrabold uppercase px-2 py-0.5 bg-white border border-black text-black flex items-center gap-1 rounded">
                      <Icon className="w-3 h-3 text-purple-600" />
                      <span>{dom}</span>
                    </span>
                  );
                })}
              </div>

              <p className="text-xs font-bold text-slate-800">{entry.raw_text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
