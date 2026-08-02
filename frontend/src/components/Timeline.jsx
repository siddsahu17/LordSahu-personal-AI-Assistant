import React, { useState, useEffect } from 'react';
import { GitBranch, Search, Clock, Tag, Calendar, Layers } from 'lucide-react';
import { fetchTimeline } from '../api';

export default function Timeline() {
  const [timeline, setTimeline] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  const loadTimeline = async (query = '') => {
    setLoading(true);
    try {
      const data = await fetchTimeline(query);
      setTimeline(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTimeline(search);
  }, [search]);

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header & Search */}
      <div className="neo-card p-6 bg-white border-3 border-black space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-black text-black flex items-center gap-2">
              <GitBranch className="w-6 h-6 text-blue-600" />
              Life Event Timeline
            </h2>
            <p className="text-xs font-bold text-slate-700 mt-1">
              One chronological timeline. Every gym, study, journal, weight, project, meal, or reading action appears here.
            </p>
          </div>

          {/* Preset Filter Chips */}
          <div className="flex flex-wrap items-center gap-2 text-xs font-bold">
            <button
              onClick={() => setSearch('SQL')}
              className="neo-btn bg-blue-100 hover:bg-blue-200 text-black px-2.5 py-1 text-xs"
            >
              #SQL
            </button>
            <button
              onClick={() => setSearch('WEIGHT')}
              className="neo-btn bg-lime-200 hover:bg-lime-300 text-black px-2.5 py-1 text-xs"
            >
              #Weight
            </button>
            <button
              onClick={() => setSearch('WORKOUT')}
              className="neo-btn bg-amber-200 hover:bg-amber-300 text-black px-2.5 py-1 text-xs"
            >
              #Gym
            </button>
            <button
              onClick={() => setSearch('')}
              className="neo-btn bg-slate-100 text-black px-2.5 py-1 text-xs"
            >
              All Events
            </button>
          </div>
        </div>

        {/* Search Input */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search life history... e.g. 'SQL', 'DBMS', 'Weight', 'Cardio', 'August'"
            className="w-full bg-slate-50 text-sm font-bold text-black border-2 border-black rounded-xl pl-10 pr-4 py-2.5 shadow-[3px_3px_0px_0px_#000] focus:bg-white focus:outline-none"
          />
        </div>
      </div>

      {/* Timeline Stream */}
      {loading ? (
        <div className="text-center py-12 font-bold text-slate-700 text-sm">
          Searching life history timeline...
        </div>
      ) : timeline.length === 0 ? (
        <div className="neo-card p-8 bg-white text-center text-slate-700 font-bold text-sm">
          No events found matching your search query. Try logging a new event!
        </div>
      ) : (
        <div className="space-y-8 relative pl-4 border-l-3 border-black ml-4">
          {timeline.map((group) => (
            <div key={group.date} className="relative space-y-4">
              {/* Day Node Marker */}
              <div className="flex items-center gap-3 -ml-[25px]">
                <div className="w-5 h-5 rounded-full bg-blue-600 border-3 border-black shadow-[2px_2px_0px_0px_#000]"></div>
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-black text-black">{group.formatted_date}</h3>
                  <span className="text-xs font-bold text-slate-600">({group.day_name})</span>
                  <span className="neo-badge-lime text-[10px] px-2 py-0.5 rounded font-mono">
                    {group.events.length} Events
                  </span>
                </div>
              </div>

              {/* Events Grid */}
              <div className="space-y-3 pl-4">
                {group.events.map((evt) => (
                  <div
                    key={evt.id}
                    className="neo-card-hover p-4 bg-white border-2 border-black space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="neo-badge-blue px-2.5 py-0.5 rounded text-xs">
                          {evt.event_type}
                        </span>
                        <span className="text-xs font-black text-slate-700 uppercase">
                          [{evt.workspace_id}]
                        </span>
                      </div>
                      <span className="text-xs font-mono font-bold text-slate-600 flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-blue-600" />
                        {new Date(evt.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>

                    <p className="text-xs font-extrabold text-black leading-relaxed">
                      {evt.payload?.notes || evt.payload?.subject || evt.payload?.title || JSON.stringify(evt.payload)}
                    </p>

                    {evt.entities && evt.entities.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1.5 pt-1 border-t border-slate-200">
                        {evt.entities.map((entity, i) => (
                          <span key={i} className="text-[10px] font-bold bg-slate-100 text-black px-2 py-0.5 rounded border border-black">
                            {entity.type}: <strong>{String(entity.value)}</strong>
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
