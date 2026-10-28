import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Job } from '../types';

export const JobMonitor: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = () => {
    api.getJobs().then((data) => {
      setJobs(data);
      if (data.length > 0 && !selectedJob) setSelectedJob(data[0]);
    }).catch(() => {});
  };

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Job Execution Monitor</h1>
        <p style={{ color: '#9ca3af' }}>Real-time audit task execution logs and Scope Engine verification output.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '24px' }}>
        <div className="glass-card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '16px' }}>Execution Jobs</h2>
          <table>
            <thead>
              <tr>
                <th>Job ID</th>
                <th>Engine</th>
                <th>Status</th>
                <th>Mode</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((j) => (
                <tr
                  key={j.id}
                  onClick={() => setSelectedJob(j)}
                  style={{ cursor: 'pointer', background: selectedJob?.id === j.id ? 'rgba(6,182,212,0.1)' : 'transparent' }}
                >
                  <td>#{j.id}</td>
                  <td><code>{j.engine_name}</code></td>
                  <td>
                    <span className={`badge ${j.status === 'completed' ? 'badge-low' : j.status.includes('rejected') ? 'badge-critical' : 'badge-high'}`}>
                      {j.status.toUpperCase()}
                    </span>
                  </td>
                  <td>{j.mock_mode ? 'MOCK' : 'LIVE'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="glass-card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '16px', color: '#06b6d4' }}>
            Job Console Output {selectedJob && `(#${selectedJob.id})`}
          </h2>
          {selectedJob ? (
            <div>
              <div style={{ display: 'flex', gap: '16px', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '12px' }}>
                <span>Engine: <strong>{selectedJob.engine_name}</strong></span>
                <span>Progress: <strong>{Math.round(selectedJob.progress * 100)}%</strong></span>
                <span>Scope Status: <strong style={{ color: selectedJob.status.includes('rejected') ? '#ef4444' : '#10b981' }}>{selectedJob.status}</strong></span>
              </div>
              <pre style={{
                background: '#0f172a',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid #334155',
                color: selectedJob.status.includes('rejected') ? '#f43f5e' : '#38bdf8',
                fontSize: '0.85rem',
                maxHeight: '400px',
                overflowY: 'auto'
              }}>
                {selectedJob.output || 'No output log recorded yet.'}
              </pre>
            </div>
          ) : (
            <p style={{ color: '#9ca3af' }}>Select a job from the list to view live execution logs.</p>
          )}
        </div>
      </div>
    </div>
  );
};
