import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Sparkles,
  Bot,
  Brain,
  CheckCircle2,
  Tag,
  Pin,
  Clock,
  ChevronRight,
  MessageSquare
} from 'lucide-react';
import { sendChatMessage } from '../api';

export default function Chat({ currentMode, setCurrentMode, activeWorkspace }) {
  const [messages, setMessages] = useState([
    {
      id: 'init-1',
      sender: 'lord_sahu',
      text: 'Good morning Siddhant. I am LordSahu, your AI Personal Operating System. How can I assist your life timeline today?',
      intent: 'MORNING_BRIEFING',
      extracted_entities: [],
      generated_events: [],
      memories_retrieved: ['User target weight = 80kg', 'User prefers morning workouts'],
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Web Speech Recognition
  useEffect(() => {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      rec.lang = 'en-US';

      rec.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsRecording(false);
        handleSend(transcript);
      };

      rec.onerror = () => setIsRecording(false);
      rec.onend = () => setIsRecording(false);

      recognitionRef.current = rec;
    }
  }, []);

  const toggleRecording = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser. Try Chrome or Edge.');
      return;
    }
    if (isRecording) {
      recognitionRef.current.stop();
      setIsRecording(false);
    } else {
      setIsRecording(true);
      recognitionRef.current.start();
    }
  };

  const speakText = (text) => {
    if (isMuted || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  const handleSend = async (textToSend = input) => {
    const trimmed = textToSend.trim();
    if (!trimmed || loading) return;

    const userMsg = {
      id: 'usr-' + Date.now(),
      sender: 'user',
      text: trimmed,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await sendChatMessage(trimmed, currentMode, activeWorkspace);
      const sahuMsg = {
        id: res.id,
        sender: 'lord_sahu',
        text: res.text,
        intent: res.intent,
        extracted_entities: res.extracted_entities || [],
        generated_events: res.generated_events || [],
        memories_retrieved: res.memories_retrieved || [],
        tasks_created: res.tasks_created || [],
        timestamp: new Date(res.created_at).toLocaleTimeString()
      };

      setMessages((prev) => [...prev, sahuMsg]);
      speakText(res.text);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: 'err-' + Date.now(),
          sender: 'lord_sahu',
          text: 'Error processing conversation. Please ensure backend server is active.',
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-4 pb-8">
      {/* Top Header */}
      <div className="neo-card p-4 bg-white flex items-center justify-between border-3 border-black">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 border-2 border-black flex items-center justify-center text-white shadow-[2px_2px_0px_0px_#000]">
            <Sparkles className="w-5 h-5 fill-white" />
          </div>
          <div>
            <h2 className="text-base font-black text-black flex items-center gap-2">
              Conversational Intelligence Engine
              <span className="neo-badge-lime text-[10px] px-2 py-0.5 rounded font-mono">
                ONLINE
              </span>
            </h2>
            <p className="text-xs text-slate-700 font-bold">
              Persona: <strong className="text-blue-700 uppercase font-mono">{currentMode} Mode</strong>
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsMuted(!isMuted)}
          className={`neo-btn px-3 py-1.5 text-xs font-black flex items-center gap-1.5 ${
            isMuted ? 'bg-slate-100 text-slate-700' : 'bg-lime-300 text-black'
          }`}
        >
          {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
          <span className="hidden sm:inline">{isMuted ? 'Muted' : 'Voice ON'}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Chat Area */}
        <div className="lg:col-span-3 space-y-4">
          {/* Suggested Prompts */}
          <div className="flex items-center gap-2 overflow-x-auto py-1 text-xs font-bold">
            <span className="text-slate-700 whitespace-nowrap">Try saying:</span>
            <button
              onClick={() => handleSend("Log my weight as 96.8 kg")}
              className="neo-btn bg-amber-100 hover:bg-amber-200 text-black px-3 py-1 text-xs whitespace-nowrap"
            >
              "Log weight 96.8 kg"
            </button>
            <button
              onClick={() => handleSend("I studied SQL joins for 2 hours today")}
              className="neo-btn bg-lime-200 hover:bg-lime-300 text-black px-3 py-1 text-xs whitespace-nowrap"
            >
              "Studied SQL 2 hours"
            </button>
            <button
              onClick={() => handleSend("Remind me tomorrow to finish DBMS assignment")}
              className="neo-btn bg-blue-100 hover:bg-blue-200 text-black px-3 py-1 text-xs whitespace-nowrap"
            >
              "Remind DBMS tomorrow"
            </button>
          </div>

          {/* Messages Stream */}
          <div className="neo-card p-4 md:p-6 bg-white min-h-[55vh] max-h-[60vh] overflow-y-auto space-y-4 border-3 border-black">
            {messages.map((m) => (
              <div key={m.id} className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
                <div
                  className={`max-w-[85%] rounded-xl p-4 space-y-2 border-2 border-black ${
                    m.sender === 'user'
                      ? 'bg-blue-600 text-white shadow-[4px_4px_0px_0px_#000]'
                      : 'bg-slate-50 text-black shadow-[4px_4px_0px_0px_#000]'
                  }`}
                >
                  <div className={`flex items-center justify-between text-[11px] font-mono font-bold pb-1 border-b-2 ${
                    m.sender === 'user' ? 'border-blue-400 text-blue-100' : 'border-black text-slate-600'
                  }`}>
                    <span>{m.sender === 'user' ? 'You' : 'LordSahu AI'}</span>
                    <span>{m.timestamp}</span>
                  </div>

                  <p className="text-sm font-bold leading-relaxed whitespace-pre-wrap">{m.text}</p>

                  {/* AI Metadata Tags & Generated Events */}
                  {m.sender === 'lord_sahu' && (
                    <div className="pt-2 space-y-1.5 border-t-2 border-black text-xs font-bold">
                      {m.intent && (
                        <div className="flex items-center gap-1.5">
                          <Tag className="w-3.5 h-3.5 text-blue-700" />
                          <span className="neo-badge-blue px-2 py-0.5 rounded text-[10px]">
                            {m.intent}
                          </span>
                        </div>
                      )}

                      {m.generated_events && m.generated_events.length > 0 && (
                        <div className="neo-badge-lime p-1.5 rounded flex items-center gap-1.5 text-[11px]">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>Event Created: {m.generated_events.map(e => e.type || e.event_type).join(', ')}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-2 text-xs font-bold text-blue-700 bg-blue-50 p-3 rounded-xl border-2 border-black">
                <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                LordSahu is parsing entities & creating life events...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Bar */}
          <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex items-center gap-3">
            <button
              type="button"
              onClick={toggleRecording}
              className={`neo-btn p-3 ${
                isRecording ? 'bg-red-500 text-white animate-bounce' : 'bg-amber-300 text-black'
              }`}
              title={isRecording ? 'Listening...' : 'Click to Speak (STT)'}
            >
              {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Speak or type to LordSahu... (e.g. 'Log weight 96.8 kg', 'Studied DBMS 2h')"
              className="flex-1 bg-white text-sm font-bold text-black border-3 border-black rounded-xl px-4 py-3 shadow-[4px_4px_0px_0px_#000] focus:outline-none"
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="neo-btn bg-blue-600 hover:bg-blue-500 text-white p-3 shadow-[4px_4px_0px_0px_#000]"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>

        {/* Sidebar Context & Pinned Memories */}
        <div className="space-y-4">
          <div className="neo-card p-4 bg-white border-3 border-black space-y-3">
            <h3 className="text-xs font-black text-black flex items-center gap-2 border-b-2 border-black pb-2">
              <Pin className="w-4 h-4 text-blue-600" />
              PINNED MEMORIES
            </h3>
            <ul className="space-y-2 text-xs font-bold text-slate-800">
              <li className="bg-amber-100 p-2.5 rounded-lg border-2 border-black">
                Target weight is 80.0 kg (Current ~96.8 kg)
              </li>
              <li className="bg-lime-100 p-2.5 rounded-lg border-2 border-black">
                Primary goal: DBMS & SQL Joins Final Exam
              </li>
              <li className="bg-blue-100 p-2.5 rounded-lg border-2 border-black">
                Prefers morning workouts & daily weight logs
              </li>
            </ul>
          </div>

          <div className="neo-card p-4 bg-white border-3 border-black space-y-3">
            <h3 className="text-xs font-black text-black flex items-center gap-2 border-b-2 border-black pb-2">
              <Brain className="w-4 h-4 text-purple-600" />
              CONTEXT ENGINE STATE
            </h3>
            <div className="space-y-2 text-[11px] font-bold text-slate-700">
              <div className="flex justify-between bg-slate-50 p-2 rounded border border-black">
                <span>Active Workspace:</span>
                <span className="font-mono text-black capitalize">{activeWorkspace}</span>
              </div>
              <div className="flex justify-between bg-slate-50 p-2 rounded border border-black">
                <span>Current Mode:</span>
                <span className="font-mono text-blue-700 capitalize">{currentMode}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
