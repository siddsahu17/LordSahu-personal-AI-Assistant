const API_BASE = 'http://localhost:8000/api';

export async function fetchDashboard() {
  const res = await fetch(`${API_BASE}/dashboard`);
  if (!res.ok) throw new Error('Failed to fetch dashboard');
  return res.json();
}

export async function sendChatMessage(text, mode = 'assistant', workspace_id = 'personal') {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, mode, workspace_id })
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}

export async function fetchChatHistory() {
  const res = await fetch(`${API_BASE}/chat/history`);
  if (!res.ok) throw new Error('Failed to fetch chat history');
  return res.json();
}

export async function fetchCalendarEvents() {
  const res = await fetch(`${API_BASE}/calendar`);
  if (!res.ok) throw new Error('Failed to fetch calendar events');
  return res.json();
}

export async function fetchFitnessOverview() {
  const res = await fetch(`${API_BASE}/fitness/overview`);
  if (!res.ok) throw new Error('Failed to fetch fitness overview');
  return res.json();
}

export async function fetchWorkspaceOverview(workspace_id = 'learning') {
  const res = await fetch(`${API_BASE}/workspace/overview?workspace_id=${workspace_id}`);
  if (!res.ok) throw new Error('Failed to fetch workspace overview');
  return res.json();
}

export async function fetchGoals(workspace_id = 'all') {
  const res = await fetch(`${API_BASE}/goals?workspace_id=${workspace_id}`);
  if (!res.ok) throw new Error('Failed to fetch goals');
  return res.json();
}

export async function createGoal(goalData) {
  const res = await fetch(`${API_BASE}/goals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(goalData)
  });
  if (!res.ok) throw new Error('Failed to create goal');
  return res.json();
}

export async function fetchTasks(workspace_id = 'all') {
  const res = await fetch(`${API_BASE}/tasks?workspace_id=${workspace_id}`);
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function createTask(taskData) {
  const res = await fetch(`${API_BASE}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  });
  if (!res.ok) throw new Error('Failed to create task');
  return res.json();
}

export async function updateTaskStatus(taskId, status) {
  const res = await fetch(`${API_BASE}/tasks/${taskId}?new_status=${status}`, {
    method: 'PATCH'
  });
  if (!res.ok) throw new Error('Failed to update task');
  return res.json();
}

export async function fetchEvents(workspace_id = 'all', event_type = 'all', search = '') {
  let url = `${API_BASE}/events?workspace_id=${workspace_id}&event_type=${event_type}`;
  if (search) url += `&search=${encodeURIComponent(search)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch events');
  return res.json();
}

export async function fetchTimeline(search = '') {
  let url = `${API_BASE}/timeline`;
  if (search) url += `?search=${encodeURIComponent(search)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch timeline');
  return res.json();
}

export async function fetchReports(timeframe = 'weekly') {
  const res = await fetch(`${API_BASE}/reports?timeframe=${timeframe}`);
  if (!res.ok) throw new Error('Failed to fetch reports');
  return res.json();
}

export async function fetchAnalytics(timeframe = '14d') {
  const res = await fetch(`${API_BASE}/analytics?timeframe=${timeframe}`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export async function fetchMemories(memory_type = 'ALL', category = 'ALL') {
  const res = await fetch(`${API_BASE}/memories?memory_type=${memory_type}&category=${category}`);
  if (!res.ok) throw new Error('Failed to fetch memories');
  return res.json();
}

export async function fetchWorkspaces() {
  const res = await fetch(`${API_BASE}/workspaces`);
  if (!res.ok) throw new Error('Failed to fetch workspaces');
  return res.json();
}

export async function fetchKnowledge(workspace_id = 'all') {
  const res = await fetch(`${API_BASE}/knowledge?workspace_id=${workspace_id}`);
  if (!res.ok) throw new Error('Failed to fetch knowledge');
  return res.json();
}

export async function uploadKnowledgeDoc(formData) {
  const res = await fetch(`${API_BASE}/knowledge`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) throw new Error('Failed to upload knowledge doc');
  return res.json();
}
