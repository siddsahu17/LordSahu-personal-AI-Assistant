import React, { useState } from 'react';
import { Settings, Bot, Mic, Bell, Key, Database, Sliders, Shield } from 'lucide-react';

export default function SettingsView({ currentMode, setCurrentMode }) {
  const [apiKey, setApiKey] = useState('');
  const [voicePlayback, setVoicePlayback] = useState(true);
  const [themeMode, setThemeMode] = useState('neo-brutalism');
  const [notifications, setNotifications] = useState(true);

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div className="neo-card p-6 bg-white border-3 border-black">
        <h2 className="text-2xl font-black text-black flex items-center gap-2">
          <Settings className="w-6 h-6 text-blue-600" />
          System Settings & Controls
        </h2>
        <p className="text-xs font-bold text-slate-700 mt-1">
          Configure AI persona orchestrator, voice STT/TTS engine, memory bank rules, and API keys.
        </p>
      </div>

      <div className="space-y-6">
        {/* 1. AI Preferences */}
        <div className="neo-card p-6 bg-white border-3 border-black space-y-4">
          <h3 className="text-base font-black text-black flex items-center gap-2 border-b-2 border-black pb-2">
            <Bot className="w-5 h-5 text-blue-600" />
            AI Persona & Orchestrator Preferences
          </h3>
          <div className="space-y-3 text-xs font-bold">
            <div>
              <label className="block text-black mb-1">Active Persona Mode</label>
              <select
                value={currentMode}
                onChange={(e) => setCurrentMode(e.target.value)}
                className="w-full bg-slate-50 text-black border-2 border-black rounded-xl p-2.5 font-bold"
              >
                <option value="assistant">Chief of Staff (Assistant Mode)</option>
                <option value="coach">Coach Mode (High Accountability)</option>
                <option value="focus">Focus Mode (Deep Work)</option>
                <option value="reflection">Reflection Mode (Self-Growth)</option>
                <option value="planner">Planner Mode (Strategic Milestones)</option>
                <option value="reviewer">Reviewer Mode (Performance Audit)</option>
              </select>
            </div>

            <div>
              <label className="block text-black mb-1">Google Gemini API Key (Optional Intelligence Boost)</label>
              <div className="relative">
                <Key className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Paste Gemini API key here..."
                  className="w-full bg-slate-50 text-black border-2 border-black rounded-xl pl-9 pr-3 py-2.5 focus:bg-white focus:outline-none"
                />
              </div>
            </div>
          </div>
        </div>

        {/* 2. Voice & Speech Settings */}
        <div className="neo-card p-6 bg-white border-3 border-black space-y-4">
          <h3 className="text-base font-black text-black flex items-center gap-2 border-b-2 border-black pb-2">
            <Mic className="w-5 h-5 text-orange-600" />
            Voice & Speech Settings (STT / TTS)
          </h3>
          <div className="space-y-3 text-xs font-bold">
            <div className="flex items-center justify-between bg-slate-50 p-3 rounded-xl border-2 border-black">
              <div>
                <span className="block text-black">Auto Voice Playback (Text-To-Speech)</span>
                <span className="text-[10px] text-slate-600">Speak LordSahu's responses automatically</span>
              </div>
              <button
                onClick={() => setVoicePlayback(!voicePlayback)}
                className={`neo-btn px-3 py-1 text-xs ${voicePlayback ? 'bg-lime-300 text-black' : 'bg-slate-200 text-slate-700'}`}
              >
                {voicePlayback ? 'ENABLED' : 'DISABLED'}
              </button>
            </div>
          </div>
        </div>

        {/* 3. Theme & Notifications */}
        <div className="neo-card p-6 bg-white border-3 border-black space-y-4">
          <h3 className="text-base font-black text-black flex items-center gap-2 border-b-2 border-black pb-2">
            <Sliders className="w-5 h-5 text-purple-600" />
            Theme & Design Language
          </h3>
          <div className="space-y-3 text-xs font-bold">
            <div className="flex items-center justify-between bg-slate-50 p-3 rounded-xl border-2 border-black">
              <div>
                <span className="block text-black">Design Style</span>
                <span className="text-[10px] text-slate-600">Active design language</span>
              </div>
              <span className="neo-badge-yellow px-3 py-1 rounded text-xs uppercase font-mono">
                Neo-Brutalism V0.1
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
