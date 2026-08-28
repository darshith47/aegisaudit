import React, { useEffect, useState } from 'react';
import { Shield, AlertTriangle, CheckCircle, Cpu, Lock } from 'lucide-react';
import { api } from '../services/api';
import { Assessment, Job, Finding } from '../types';

export const Dashboard: React.FC = () => {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [findings, setFindings] = useState<Finding[]>([]);

  useEffect(() => {
    api.getAssessments().then(setAssessments).catch(() => {});
    api.getJobs().then(setJobs).catch(() => {});
    api.getFindings().then(setFindings).catch(() => {});
  }, []);

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#f9fafb' }}>Platform Dashboard</h1>
        <p style={{ color: '#9ca3af', fontSize: '0.95rem' }}>
          Authorized Credential Security Assessment Platform & Scope Policy Control
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginBottom: '32px' }}>
        <div className="glass-card" style={{ borderLeft: '4px solid #06b6d4' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Total Assessments</span>
            <Shield style={{ color: '#06b6d4' }} />
          </div>
          <p style={{ fontSize: '2rem', fontWeight: 700, marginTop: '8px' }}>{assessments.length}</p>
        </div>

        <div className="glass-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Active Jobs</span>
            <Cpu style={{ color: '#3b82f6' }} />
          </div>
          <p style={{ fontSize: '2rem', fontWeight: 700, marginTop: '8px' }}>{jobs.length}</p>
        </div>

        <div className="glass-card" style={{ borderLeft: '4px solid #ef4444' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Security Findings</span>
            <AlertTriangle style={{ color: '#ef4444' }} />
          </div>
          <p style={{ fontSize: '2rem', fontWeight: 700, marginTop: '8px' }}>{findings.length}</p>
        </div>

        <div className="glass-card" style={{ borderLeft: '4px solid #10b981' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Engine Mode</span>
            <Lock style={{ color: '#10b981' }} />
          </div>
          <p style={{ fontSize: '1.2rem', fontWeight: 700, marginTop: '12px', color: '#10b981' }}>Mock Mode Active</p>
        </div>
      </div>

      <div className="glass-card" style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '16px', color: '#38bdf8' }}>
          Centralized Authorization & Execution Pipeline
        </h2>
        <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
          <p style={{ fontFamily: 'JetBrains Mono', fontSize: '0.85rem', color: '#94a3b8', lineHeight: '1.8' }}>
            [ Authentication ] ➔ [ RBAC Roles ] ➔ [ Assessment Auth ] ➔ [ Scope Validation Engine ] ➔ [ Engine Allowlist ] ➔ [ Resource Policy ] ➔ [ Job Queue ] ➔ [ Isolated Worker ] ➔ [ Security Adapter ] ➔ [ Evidence & Findings ]
          </p>
        </div>
      </div>
    </div>
  );
};
