import React from 'react';
import { Shield, Server, Crosshair, Terminal, FileText, CheckCircle2, Lock, ListFilter } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Shield },
    { id: 'scopes', label: 'Scope Policy', icon: Crosshair },
    { id: 'assessments', label: 'Assessments', icon: Server },
    { id: 'jobs', label: 'Job Monitor', icon: Terminal },
    { id: 'engines', label: 'Engine Matrix', icon: ListFilter },
    { id: 'findings', label: 'Findings', icon: CheckCircle2 },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'audit', label: 'Audit Log', icon: Lock },
  ];

  return (
    <nav style={{ background: '#111827', borderBottom: '1px solid #374151', padding: '0 24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '64px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Shield style={{ width: '28px', height: '28px', color: '#06b6d4' }} />
          <span style={{ fontWeight: 700, fontSize: '1.2rem', letterSpacing: '0.05em' }}>
            Aegis<span style={{ color: '#06b6d4' }}>Audit</span>
          </span>
          <span className="badge badge-implemented" style={{ fontSize: '0.65rem' }}>MVP v0.1.0</span>
        </div>

        <div style={{ display: 'flex', gap: '4px' }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`tab-btn ${isActive ? 'active' : ''}`}
                style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
              >
                <Icon style={{ width: '16px', height: '16px' }} />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};
