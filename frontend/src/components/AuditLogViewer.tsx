import React, { useState, useEffect } from 'react';
import { Lock } from 'lucide-react';
import { api } from '../services/api';
import { AuditLog } from '../types';

export const AuditLogViewer: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);

  useEffect(() => {
    api.getAuditLogs().then(setLogs).catch(() => {});
  }, []);

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Immutable Compliance Audit Logs</h1>
        <p style={{ color: '#9ca3af' }}>Audit trail documenting scope checks, job launches, and security actions.</p>
      </div>

      <div className="glass-card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Timestamp</th>
              <th>Action</th>
              <th>Resource</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((l) => (
              <tr key={l.id}>
                <td>#{l.id}</td>
                <td>{new Date(l.timestamp).toLocaleString()}</td>
                <td>
                  <span className={`badge ${l.action.includes('REJECTED') ? 'badge-critical' : 'badge-info'}`}>
                    {l.action}
                  </span>
                </td>
                <td><code>{l.resource}</code></td>
                <td><pre style={{ fontSize: '0.75rem', background: '#0f172a', padding: '4px 8px', borderRadius: '4px' }}>{JSON.stringify(l.details)}</pre></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
