import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Dashboard } from './components/Dashboard';
import { ScopeConfigurator } from './components/ScopeConfigurator';
import { AssessmentManager } from './components/AssessmentManager';
import { JobMonitor } from './components/JobMonitor';
import { EngineMatrix } from './components/EngineMatrix';
import { FindingsViewer } from './components/FindingsViewer';
import { ReportGenerator } from './components/ReportGenerator';
import { AuditLogViewer } from './components/AuditLogViewer';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div style={{ minHeight: '100vh', background: '#0b0f19', color: '#f9fafb' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main style={{ maxWidth: '1400px', margin: '0 auto' }}>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'scopes' && <ScopeConfigurator />}
        {activeTab === 'assessments' && <AssessmentManager />}
        {activeTab === 'jobs' && <JobMonitor />}
        {activeTab === 'engines' && <EngineMatrix />}
        {activeTab === 'findings' && <FindingsViewer />}
        {activeTab === 'reports' && <ReportGenerator />}
        {activeTab === 'audit' && <AuditLogViewer />}
      </main>
    </div>
  );
};

export default App;
