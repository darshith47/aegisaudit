import React, { useState, useEffect } from 'react';
import { ListFilter, CheckCircle, Clock } from 'lucide-react';
import { api } from '../services/api';
import { EngineItem } from '../types';

export const EngineMatrix: React.FC = () => {
  const [matrix, setMatrix] = useState<EngineItem[]>([]);

  useEffect(() => {
    api.getEngineMatrix().then(setMatrix).catch(() => {});
  }, []);

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Security Engine Capability Matrix</h1>
        <p style={{ color: '#9ca3af' }}>Verified status of security engines integrated or planned for AegisAudit.</p>
      </div>

      <div className="glass-card">
        <table>
          <thead>
            <tr>
              <th>Engine</th>
              <th>Category</th>
              <th>Status</th>
              <th>Requires Network</th>
              <th>Target Scope Verification</th>
            </tr>
          </thead>
          <tbody>
            {matrix.map((e, idx) => (
              <tr key={idx}>
                <td style={{ fontWeight: 700, fontSize: '1rem', color: '#f9fafb' }}>{e.engine}</td>
                <td>{e.category}</td>
                <td>
                  <span className={`badge ${e.status === 'Implemented' ? 'badge-implemented' : 'badge-planned'}`}>
                    {e.status === 'Implemented' ? '✓ Implemented' : '○ Planned'}
                  </span>
                </td>
                <td>{e.network}</td>
                <td><code>{e.scope}</code></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
