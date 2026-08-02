import React, { useState, useEffect } from 'react';
import { Target, Plus, CheckCircle2, Circle, AlertCircle, Sparkles } from 'lucide-react';
import { fetchGoals, createGoal } from '../api';

export default function Goals({ activeWorkspace }) {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [newTitle, setNewTitle] = useState('');
  const [newWorkspace, setNewWorkspace] = useState('learning');
  const [newDescription, setNewDescription] = useState('');
  const [newTargetValue, setNewTargetValue] = useState(20);
  const [newTargetMetric, setNewTargetMetric] = useState('hours');
  const [newPriority, setNewPriority] = useState('HIGH');

  const loadGoals = async () => {
    setLoading(true);
    try {
      const data = await fetchGoals(activeWorkspace);
      setGoals(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGoals();
  }, [activeWorkspace]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      await createGoal({
        title: newTitle,
        workspace_id: newWorkspace,
        description: newDescription,
        target_value: parseFloat(newTargetValue),
        target_metric: newTargetMetric,
        priority: newPriority,
        milestones: [
          { id: 'm1', title: 'Phase 1 Milestone', completed: false },
          { id: 'm2', title: 'Phase 2 Completion', completed: false }
        ]
      });
      setShowModal(false);
      setNewTitle('');
      setNewDescription('');
      loadGoals();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="neo-card p-6 bg-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-3 border-black">
        <div>
          <h2 className="text-2xl font-black text-black flex items-center gap-2">
            <Target className="w-6 h-6 text-blue-600" />
            Living Goal Engine
          </h2>
          <p className="text-xs font-bold text-slate-700 mt-1">
            Goals are living objects. Progress is inferred automatically from events recorded in your Event Store.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="neo-btn bg-lime-300 hover:bg-lime-200 text-black px-4 py-2 text-xs font-black flex items-center gap-2 shadow-[3px_3px_0px_0px_#000]"
        >
          <Plus className="w-4 h-4" /> Create Living Goal
        </button>
      </div>

      {/* Goals Grid */}
      {loading ? (
        <div className="text-center py-12 font-bold text-slate-700 text-sm">
          Calculating inferred goal progress...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {goals.map((g) => (
            <div key={g.id} className="neo-card-hover p-6 bg-white border-3 border-black space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <span className="neo-badge-blue px-2.5 py-0.5 rounded text-[10px] uppercase">
                    {g.workspace_id}
                  </span>
                  <h3 className="text-lg font-black text-black mt-1.5">{g.title}</h3>
                </div>
                <span className={`text-[10px] font-black px-2.5 py-0.5 rounded border-2 border-black ${
                  g.priority === 'HIGH' ? 'bg-red-200 text-red-950' : 'bg-amber-200 text-amber-950'
                }`}>
                  {g.priority}
                </span>
              </div>

              <p className="text-xs font-bold text-slate-700 leading-relaxed">{g.description}</p>

              {/* Progress Bar */}
              <div className="space-y-1.5 pt-2">
                <div className="flex items-center justify-between text-xs font-black">
                  <span className="text-slate-800">Inferred Completion:</span>
                  <span className="text-blue-700 text-sm font-black">{g.inferred_progress}%</span>
                </div>
                <div className="w-full bg-slate-100 border-2 border-black h-4 rounded-full overflow-hidden p-0.5">
                  <div
                    className="bg-blue-600 h-full rounded-full transition-all duration-700"
                    style={{ width: `${g.inferred_progress}%` }}
                  ></div>
                </div>
              </div>

              {/* Milestones Checklist */}
              {g.milestones && g.milestones.length > 0 && (
                <div className="pt-3 border-t-2 border-black space-y-2">
                  <span className="text-[11px] font-black text-black uppercase">Milestone Breakdown:</span>
                  <div className="space-y-1.5">
                    {g.milestones.map((m, idx) => (
                      <div key={m.id || idx} className="flex items-center gap-2 text-xs font-bold text-slate-900">
                        {m.completed ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                        ) : (
                          <Circle className="w-4 h-4 text-slate-400 flex-shrink-0" />
                        )}
                        <span className={m.completed ? 'line-through text-slate-500' : ''}>{m.title}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="neo-card p-6 bg-white max-w-md w-full space-y-4 border-3 border-black shadow-[8px_8px_0px_0px_#000]">
            <h3 className="text-lg font-black text-black flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-blue-600" />
              Create Living Goal
            </h3>

            <form onSubmit={handleCreate} className="space-y-4 text-xs font-bold">
              <div>
                <label className="block text-black mb-1">Goal Title</label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Master Relational Database Normalization"
                  className="w-full bg-slate-50 text-black border-2 border-black rounded-xl p-2.5 focus:bg-white focus:outline-none"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-black mb-1">Workspace</label>
                  <select
                    value={newWorkspace}
                    onChange={(e) => setNewWorkspace(e.target.value)}
                    className="w-full bg-slate-50 text-black border-2 border-black rounded-xl p-2.5"
                  >
                    <option value="learning">Learning</option>
                    <option value="fitness">Fitness</option>
                    <option value="career">Career</option>
                    <option value="projects">Projects</option>
                    <option value="personal">Personal</option>
                  </select>
                </div>
                <div>
                  <label className="block text-black mb-1">Priority</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value)}
                    className="w-full bg-slate-50 text-black border-2 border-black rounded-xl p-2.5"
                  >
                    <option value="HIGH">High</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="LOW">Low</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-black mb-1">Description</label>
                <textarea
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  placeholder="Describe goal milestones and targets..."
                  className="w-full bg-slate-50 text-black border-2 border-black rounded-xl p-2.5 focus:bg-white focus:outline-none h-20"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="neo-btn bg-slate-100 text-black px-4 py-2"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="neo-btn bg-blue-600 text-white px-4 py-2"
                >
                  Save Goal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
