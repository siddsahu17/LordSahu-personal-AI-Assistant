import React, { useState, useEffect } from 'react';
import Navigation from './components/Navigation';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import Chat from './components/Chat';
import Goals from './components/Goals';
import Timeline from './components/Timeline';
import Tasks from './components/Tasks';
import Knowledge from './components/Knowledge';
import Reports from './components/Reports';
import Analytics from './components/Analytics';
import Memories from './components/Memories';
import SettingsView from './components/Settings';
import Profile from './components/Profile';

import { fetchDashboard, fetchWorkspaces } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentMode, setCurrentMode] = useState('assistant');
  const [activeWorkspace, setActiveWorkspace] = useState('all');
  const [dashboardData, setDashboardData] = useState(null);

  const [workspaces, setWorkspaces] = useState([
    { id: 'learning', name: 'Learning' },
    { id: 'fitness', name: 'Fitness & Health' },
    { id: 'career', name: 'Career' },
    { id: 'college', name: 'College' },
    { id: 'finance', name: 'Finance' },
    { id: 'projects', name: 'Projects' },
    { id: 'personal', name: 'Personal' }
  ]);

  const loadDashboard = async () => {
    try {
      const data = await fetchDashboard();
      setDashboardData(data);
    } catch (err) {
      console.error("Dashboard load failed:", err);
    }
  };

  useEffect(() => {
    loadDashboard();
    fetchWorkspaces()
      .then((res) => {
        if (res && res.length > 0) setWorkspaces(res);
      })
      .catch((e) => console.log("Workspace fetch info:", e));
  }, []);

  const handleQuickChat = (messageText) => {
    setActiveTab('chat');
  };

  return (
    <div className="min-h-screen bg-[#f7f4ed] text-slate-900 flex flex-col font-sans selection:bg-yellow-300 selection:text-black">
      {/* Fixed Spacing Navigation Header */}
      <Navigation
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentMode={currentMode}
        setCurrentMode={setCurrentMode}
        activeWorkspace={activeWorkspace}
        setActiveWorkspace={setActiveWorkspace}
        workspaces={workspaces}
      />

      {/* Main View Area */}
      <main className="flex-1 p-4 md:p-6 max-w-7xl w-full mx-auto space-y-6">
        {activeTab === 'landing' && (
          <LandingPage
            onLaunch={() => setActiveTab('dashboard')}
            onExplore={() => setActiveTab('goals')}
          />
        )}
        {activeTab === 'dashboard' && (
          <Dashboard
            data={dashboardData}
            onQuickChat={handleQuickChat}
            onNavigate={(tab) => setActiveTab(tab)}
            currentMode={currentMode}
          />
        )}
        {activeTab === 'chat' && (
          <Chat
            currentMode={currentMode}
            setCurrentMode={setCurrentMode}
            activeWorkspace={activeWorkspace}
          />
        )}
        {activeTab === 'goals' && (
          <Goals activeWorkspace={activeWorkspace} />
        )}
        {activeTab === 'timeline' && (
          <Timeline />
        )}
        {activeTab === 'tasks' && (
          <Tasks activeWorkspace={activeWorkspace} />
        )}
        {activeTab === 'knowledge' && (
          <Knowledge activeWorkspace={activeWorkspace} />
        )}
        {activeTab === 'reports' && (
          <Reports />
        )}
        {activeTab === 'analytics' && (
          <Analytics />
        )}
        {activeTab === 'memories' && (
          <Memories />
        )}
        {activeTab === 'settings' && (
          <SettingsView
            currentMode={currentMode}
            setCurrentMode={setCurrentMode}
          />
        )}
        {activeTab === 'profile' && (
          <Profile />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t-3 border-black bg-white py-4 text-center text-xs font-black text-slate-800 shadow-[0_-4px_0_0_#000]">
        LordSahu AI Personal Operating System • Neo-Brutalist Design System • Pair Programmed for Siddhant Kumar Sahu
      </footer>
    </div>
  );
}
