import React, { useState, useEffect } from 'react';
import { Crosshair, Plus, CheckCircle, XCircle } from 'lucide-react';
import { api } from '../services/api';
import { Scope } from '../types';

export const ScopeConfigurator: React.FC = () => {
  const [scopes, setScopes] = useState<Scope[]>([]);
  const [name, setName] = useState('');
  const [targets, setTargets] = useState('');

  // Scope validation tester
  const [testScopeId, setTestScopeId] = useState<number>(1);
  const [testTarget, setTestTarget] = useState('');
  const [testPort, setTestPort] = useState<number>(22);
  const [valResult, setValResult] = useState<{ is_allowed: boolean; reason: string } | null>(null);

  useEffect(() => {
    loadScopes();
  }, []);

  const loadScopes = () => {
    api.getScopes().then((data) => {
      setScopes(data);
      if (data.length > 0) setTestScopeId(data[0].id);
    }).catch(() => {});
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !targets) return;
    await api.createScope({ name, allowed_targets: targets });
    setName('');
    setTargets('');
    loadScopes();
  };

  const handleValidate = async () => {
    if (!testTarget) return;
    const res = await api.validateScope(testScopeId, testTarget, testPort);
    setValResult(res);
  };

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Authorized Scope Management</h1>
        <p style={{ color: '#9ca3af' }}>Define and enforce strict target boundaries before running security engines.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '32px' }}>
        <div className="glass-card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '16px', color: '#06b6d4' }}>Create Scope Policy</h2>
          <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Scope Title</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Authorized Staging Environment"
                style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Allowed Target IPs / CIDRs / Domains (comma-separated)</label>
              <textarea
                value={targets}
                onChange={(e) => setTargets(e.target.value)}
                placeholder="10.0.0.0/24, 192.168.1.50, demo.lab"
                rows={3}
                style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
              />
            </div>
            <button type="submit" className="btn btn-primary">
              <Plus size={16} /> Save Scope Policy
            </button>
          </form>
        </div>

        <div className="glass-card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '16px', color: '#38bdf8' }}>Scope Policy Validator</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Select Scope Policy</label>
              <select
                value={testScopeId}
                onChange={(e) => setTestScopeId(Number(e.target.value))}
                style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
              >
                {scopes.map((s) => (
                  <option key={s.id} value={s.id}>#{s.id} — {s.name}</option>
                ))}
              </select>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Target Host / IP</label>
                <input
                  type="text"
                  value={testTarget}
                  onChange={(e) => setTestTarget(e.target.value)}
                  placeholder="e.g. 10.0.0.25 or 8.8.8.8"
                  style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Port</label>
                <input
                  type="number"
                  value={testPort}
                  onChange={(e) => setTestPort(Number(e.target.value))}
                  style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
                />
              </div>
            </div>
            <button type="button" onClick={handleValidate} className="btn btn-secondary">
              <Crosshair size={16} /> Check Target Scope
            </button>

            {valResult && (
              <div style={{
                marginTop: '12px',
                padding: '12px',
                borderRadius: '6px',
                background: valResult.is_allowed ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)',
                border: `1px solid ${valResult.is_allowed ? '#10b981' : '#ef4444'}`,
                display: 'flex',
                alignItems: 'center',
                gap: '12px'
              }}>
                {valResult.is_allowed ? <CheckCircle style={{ color: '#10b981' }} /> : <XCircle style={{ color: '#ef4444' }} />}
                <div>
                  <strong style={{ color: valResult.is_allowed ? '#10b981' : '#ef4444' }}>
                    {valResult.is_allowed ? 'TARGET IN-SCOPE' : 'TARGET REJECTED (OUT-OF-SCOPE)'}
                  </strong>
                  <p style={{ fontSize: '0.85rem', color: '#9ca3af', marginTop: '2px' }}>{valResult.reason}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="glass-card">
        <h2 style={{ fontSize: '1.1rem', marginBottom: '16px' }}>Active Scope Policies</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Policy Name</th>
              <th>Allowed Targets</th>
              <th>Allowed Ports</th>
              <th>Allowed Protocols</th>
            </tr>
          </thead>
          <tbody>
            {scopes.map((s) => (
              <tr key={s.id}>
                <td>#{s.id}</td>
                <td style={{ fontWeight: 600 }}>{s.name}</td>
                <td><code>{s.allowed_targets}</code></td>
                <td><code>{s.allowed_ports}</code></td>
                <td><code>{s.allowed_protocols}</code></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
