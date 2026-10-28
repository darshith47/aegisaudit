import { Scope, Assessment, Job, Finding, EngineItem, AuditLog } from '../types';

const API_BASE = '/api/v1';

async function fetchJSON<T>(url: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('aegis_token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${url}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'API Request Failed' }));
    throw new Error(err.detail || 'API Request Failed');
  }
  return res.json();
}

export const api = {
  // Auth
  login: async (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Login failed');
    return res.json();
  },

  // Scopes
  getScopes: () => fetchJSON<Scope[]>('/scope/'),
  createScope: (data: Partial<Scope>) => fetchJSON<Scope>('/scope/', { method: 'POST', body: JSON.stringify(data) }),
  validateScope: (scope_id: number, target: string, port?: number, protocol?: string) =>
    fetchJSON<{ is_allowed: boolean; reason: string }>('/scope/validate', {
      method: 'POST',
      body: JSON.stringify({ scope_id, target, port, protocol }),
    }),

  // Assessments
  getAssessments: () => fetchJSON<Assessment[]>('/assessments/'),
  createAssessment: (data: { title: string; description?: string; target: string; engine: string; scope_id: number }) =>
    fetchJSON<Assessment>('/assessments/', { method: 'POST', body: JSON.stringify(data) }),

  // Jobs
  getJobs: () => fetchJSON<Job[]>('/jobs/'),
  launchJob: (assessment_id: number, parameters: Record<string, any> = {}) =>
    fetchJSON<Job>('/jobs/launch', { method: 'POST', body: JSON.stringify({ assessment_id, parameters }) }),

  // Findings
  getFindings: (assessment_id?: number) =>
    fetchJSON<Finding[]>(`/findings/${assessment_id ? `?assessment_id=${assessment_id}` : ''}`),

  // Reports
  generateReport: (assessment_id: number, format = 'markdown') =>
    fetchJSON<{ content: string }>('/reports/generate', {
      method: 'POST',
      body: JSON.stringify({ assessment_id, format }),
    }),

  // Engines Matrix
  getEngineMatrix: () => fetchJSON<EngineItem[]>('/engines/'),

  // Audit Logs
  getAuditLogs: () => fetchJSON<AuditLog[]>('/audit/'),
};
