import React, { useState, useEffect } from 'react';
import { Plus, Play } from 'lucide-react';
import { api } from '../services/api';
import { Assessment, Scope } from '../types';

export const AssessmentManager: React.FC = () => {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [scopes, setScopes] = useState<Scope[]>([]);
  const [title, setTitle] = useState('');
  const [target, setTarget] = useState('');
  const [engine, setEngine] = useState('hashcat');
  const [scopeId, setScopeId] = useState<number>(1);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    api.getAssessments().then(setAssessments).catch(() => {});
    api.getScopes().then((data) => {
      setScopes(data);
      if (data.length > 0) setScopeId(data[0].id);
    }).catch(() => {});
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !target) return;
    await api.createAssessment({ title, target, engine, scope_id: scopeId });
    setTitle('');
    setTarget('');
    loadData();
  };

  const handleLaunchJob = async (assessment_id: number) => {
    await api.launchJob(assessment_id);
    loadData();
  };

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Assessment Management</h1>
        <p style={{ color: '#9ca3af' }}>Create and launch credential security assessment tasks.</p>
      </div>

      <div className="glass-card" style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '16px', color: '#06b6d4' }}>New Assessment Task</h2>
        <form onSubmit={handleCreate} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr auto', gap: '16px', alignItems: 'end' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Lab SSH Audit"
              style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Target (IP / Hash)</label>
            <input
              type="text"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder="e.g. 10.0.0.15"
              style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Security Engine</label>
            <select
              value={engine}
              onChange={(e) => setEngine(e.target.value)}
              style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
            >
              <option value="hashcat">Hashcat (Password Audit)</option>
              <option value="john">John the Ripper (Password Audit)</option>
              <option value="hydra">Hydra (Authentication Testing)</option>
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Scope Policy</label>
            <select
              value={scopeId}
              onChange={(e) => setScopeId(Number(e.target.value))}
              style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
            >
              {scopes.map((s) => (
                <option key={s.id} value={s.id}>#{s.id} — {s.name}</option>
              ))}
            </select>
          </div>
          <button type="submit" className="btn btn-primary" style={{ height: '42px' }}>
            <Plus size={16} /> Create
          </button>
        </form>
      </div>

      <div className="glass-card">
        <h2 style={{ fontSize: '1.1rem', marginBottom: '16px' }}>Assessment Registry</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Assessment Title</th>
              <th>Target</th>
              <th>Engine</th>
              <th>Scope ID</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {assessments.map((a) => (
              <tr key={a.id}>
                <td>#{a.id}</td>
                <td style={{ fontWeight: 600 }}>{a.title}</td>
                <td><code>{a.target}</code></td>
                <td><span className="badge badge-info">{a.engine.toUpperCase()}</span></td>
                <td>#{a.scope_id}</td>
                <td>
                  <span className={`badge ${a.status === 'completed' ? 'badge-low' : 'badge-planned'}`}>
                    {a.status.toUpperCase()}
                  </span>
                </td>
                <td>
                  <button onClick={() => handleLaunchJob(a.id)} className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                    <Play size={14} /> Launch Job
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
