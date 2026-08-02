import React, { useState, useEffect } from 'react';
import { BookOpen, Upload, FileText, Search, Sparkles, Plus } from 'lucide-react';
import { fetchKnowledge, uploadKnowledgeDoc } from '../api';

export default function Knowledge({ activeWorkspace }) {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState('');
  const [docType, setDocType] = useState('syllabus');
  const [content, setContent] = useState('');

  const loadDocs = async () => {
    setLoading(true);
    try {
      const data = await fetchKnowledge(activeWorkspace);
      setDocs(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocs();
  }, [activeWorkspace]);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    try {
      await uploadKnowledgeDoc({
        title,
        doc_type: docType,
        content,
        workspace_id: activeWorkspace === 'all' ? 'learning' : activeWorkspace
      });
      setShowModal(false);
      setTitle('');
      setContent('');
      loadDocs();
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
            <BookOpen className="w-5 h-5 text-indigo-400" />
            Knowledge Base Engine (RAG Documents)
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Store syllabi, resumes, workout plans, and notes for LordSahu to remember and retrieve.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-indigo-600/30 transition-all"
        >
          <Upload className="w-4 h-4" /> Upload Document / Notes
        </button>
      </div>

      {/* Document Grid */}
      {loading ? (
        <div className="text-center py-12 text-slate-400 text-sm">
          Loading Knowledge Base...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {docs.map((doc) => (
            <div key={doc.id} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3 hover:border-indigo-500/40 transition-all">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">{doc.title}</h3>
                    <span className="text-[10px] text-slate-400 uppercase font-mono">{doc.doc_type}</span>
                  </div>
                </div>
                <span className="text-[10px] text-slate-500 font-mono">
                  {new Date(doc.created_at).toLocaleDateString()}
                </span>
              </div>

              <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800/80 text-xs text-slate-300 font-mono leading-relaxed">
                {doc.content_preview}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" /> Upload Document / Notes
            </h3>

            <form onSubmit={handleUpload} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Document Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Semester 5 DBMS Syllabus"
                  className="w-full bg-slate-950 text-white border border-slate-800 rounded-lg p-2.5 focus:border-indigo-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Document Type</label>
                <select
                  value={docType}
                  onChange={(e) => setDocType(e.target.value)}
                  className="w-full bg-slate-950 text-white border border-slate-800 rounded-lg p-2.5 focus:border-indigo-500"
                >
                  <option value="syllabus">Syllabus</option>
                  <option value="resume">Resume</option>
                  <option value="workout_plan">Workout Plan</option>
                  <option value="notes">Notes / Blueprint</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Content / Document Text</label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Paste syllabus details, resume highlights, or workout split notes..."
                  className="w-full bg-slate-950 text-white border border-slate-800 rounded-lg p-2.5 focus:border-indigo-500 focus:outline-none h-32 font-mono"
                  required
                />
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
                  Upload & Index
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
