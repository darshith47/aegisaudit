import React, { useState, useEffect } from 'react';
import { AlertTriangle, ShieldAlert, Key } from 'lucide-react';
import { api } from '../services/api';
import { Finding } from '../types';

export const FindingsViewer: React.FC = () => {
  const [findings, setFindings] = useState<Finding[]>([]);

  useEffect(() => {
    api.getFindings().then(setFindings).catch(() => {});
  }, []);

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Security Findings & Credential Recoveries</h1>
        <p style={{ color: '#9ca3af' }}>Identified credential risks, weak authentication hits, and evidence traces.</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {findings.length === 0 ? (
          <div className="glass-card" style={{ textCenter: 'center', color: '#9ca3af' }}>
            No security findings recorded yet. Launch an assessment job to generate audit findings.
          </div>
        ) : (
          findings.map((f) => (
            <div key={f.id} className="glass-card" style={{ borderLeft: `4px solid ${f.severity === 'CRITICAL' ? '#ef4444' : f.severity === 'HIGH' ? '#f97316' : '#f59e0b'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span className={`badge badge-${f.severity.toLowerCase()}`}>{f.severity}</span>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: '#f9fafb' }}>{f.title}</h3>
                  {f.is_mock && <span className="badge badge-planned">[DEMO / MOCK]</span>}
                </div>
                <span style={{ fontSize: '0.8rem', color: '#9ca3af' }}>Assessment #{f.assessment_id}</span>
              </div>

              <p style={{ fontSize: '0.9rem', color: '#cbd5e1', marginBottom: '12px' }}>
                <strong>Target:</strong> <code>{f.target}</code> | <strong>Type:</strong> {f.vulnerability_type}
              </p>

              <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px', border: '1px solid #334155', marginBottom: '12px', fontSize: '0.85rem' }}>
                <p><strong>Details:</strong> {f.details}</p>
              </div>

              {f.remediation && (
                <div style={{ fontSize: '0.85rem', color: '#34d399' }}>
                  <strong>Remediation:</strong> {f.remediation}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
