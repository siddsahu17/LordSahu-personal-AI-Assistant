import React, { useState, useEffect } from 'react';
import { CheckSquare, Plus, CheckCircle2, Circle, Clock, Sparkles } from 'lucide-react';
import { fetchTasks, createTask, updateTaskStatus } from '../api';

export default function Tasks({ activeWorkspace }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newWorkspace, setNewWorkspace] = useState('learning');
  const [newPriority, setNewPriority] = useState('HIGH');

  const loadTasks = async () => {
    setLoading(true);
    try {
      const data = await fetchTasks(activeWorkspace);
      setTasks(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, [activeWorkspace]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      await createTask({
        title: newTitle,
        workspace_id: newWorkspace,
        priority: newPriority,
        status: 'PENDING'
      });
      setShowModal(false);
      setNewTitle('');
      loadTasks();
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggle = async (taskId, currentStatus) => {
    const nextStatus = currentStatus === 'COMPLETED' ? 'PENDING' : 'COMPLETED';
    try {
      await updateTaskStatus(taskId, nextStatus);
      loadTasks();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl flex items-center justify-between border border-slate-800">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <CheckSquare className="w-5 h-5 text-indigo-400" />
            Task & Scheduler Engine
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Actionable tasks and reminders automatically extracted from your conversations.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-indigo-600/30 transition-all"
        >
          <Plus className="w-4 h-4" /> Add Task
        </button>
      </div>

      {/* Task List */}
      {loading ? (
        <div className="text-center py-12 text-slate-400 text-sm">
          Loading tasks from Task Engine...
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((t) => (
            <div
              key={t.id}
              onClick={() => handleToggle(t.id, t.status)}
              className={`glass-panel p-4 rounded-xl border flex items-center justify-between gap-4 cursor-pointer transition-all ${
                t.status === 'COMPLETED'
                  ? 'border-slate-800/50 bg-slate-950/50 opacity-60'
                  : 'border-slate-800 hover:border-indigo-500/40'
              }`}
            >
              <div className="flex items-center gap-3">
                {t.status === 'COMPLETED' ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                ) : (
                  <Circle className="w-5 h-5 text-slate-500 flex-shrink-0" />
                )}
                <div>
                  <h3 className={`text-sm font-semibold ${t.status === 'COMPLETED' ? 'line-through text-slate-400' : 'text-white'}`}>
                    {t.title}
                  </h3>
                  <div className="flex items-center gap-2 text-[11px] text-slate-500 mt-0.5">
                    <span className="capitalize text-slate-400 font-medium">Workspace: {t.workspace_id}</span>
                    {t.due_date && (
                      <span className="flex items-center gap-1 text-slate-400">
                        <Clock className="w-3 h-3 text-indigo-400" />
                        Due: {new Date(t.due_date).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded ${
                t.priority === 'HIGH' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-slate-800 text-slate-300'
              }`}>
                {t.priority}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-4">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" /> Add Task
            </h3>
            <form onSubmit={handleCreate} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Task Title</label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Study DBMS Indexing & Normalization"
                  className="w-full bg-slate-950 text-white border border-slate-800 rounded-lg p-2.5 focus:border-indigo-500 focus:outline-none"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1">Workspace</label>
                  <select
                    value={newWorkspace}
                    onChange={(e) => setNewWorkspace(e.target.value)}
                    className="w-full bg-slate-950 text-white border border-slate-800 rounded-lg p-2.5 focus:border-indigo-500"
                  >
                    <option value="learning">Learning</option>
                    <option value="fitness">Fitness</option>
                    <option value="career">Career</option>
                    <option value="projects">Projects</option>
                    <option value="personal">Personal</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-400 mb-1">Priority</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value)}
                    className="w-full bg-slate-950 text-white border border-slate-800 rounded-lg p-2.5 focus:border-indigo-500"
                  >
                    <option value="HIGH">High</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="LOW">Low</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-500"
                >
                  Save Task
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
