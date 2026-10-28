import React, { useState, useEffect } from 'react';
import { FileText } from 'lucide-react';
import { api } from '../services/api';
import { Assessment } from '../types';

export const ReportGenerator: React.FC = () => {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [selectedId, setSelectedId] = useState<number>(1);
  const [format, setFormat] = useState('markdown');
  const [reportContent, setReportContent] = useState('');

  useEffect(() => {
    api.getAssessments().then((data) => {
      setAssessments(data);
      if (data.length > 0) setSelectedId(data[0].id);
    }).catch(() => {});
  }, []);

  const handleGenerate = async () => {
    const res = await api.generateReport(selectedId, format);
    setReportContent(res.content);
  };

  return (
    <div style={{ padding: '32px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>Executive Security Report Generator</h1>
        <p style={{ color: '#9ca3af' }}>Generate formal compliance & security assessment reports.</p>
      </div>

      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'flex-end' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Select Assessment</label>
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(Number(e.target.value))}
              style={{ width: '100%', padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
            >
              {assessments.map((a) => (
                <option key={a.id} value={a.id}>#{a.id} — {a.title} ({a.target})</option>
              ))}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#9ca3af', marginBottom: '6px' }}>Format</label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value)}
              style={{ padding: '10px', background: '#111827', border: '1px solid #374151', color: 'white', borderRadius: '6px' }}
            >
              <option value="markdown">Markdown</option>
              <option value="html">HTML</option>
            </select>
          </div>
          <button onClick={handleGenerate} className="btn btn-primary" style={{ height: '42px' }}>
            <FileText size={16} /> Generate Executive Report
          </button>
        </div>
      </div>

      {reportContent && (
        <div className="glass-card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '16px', color: '#06b6d4' }}>Generated Report Content</h2>
          <pre style={{
            background: '#0f172a',
            padding: '20px',
            borderRadius: '8px',
            border: '1px solid #334155',
            color: '#f8fafc',
            fontSize: '0.85rem',
            maxHeight: '500px',
            overflowY: 'auto'
          }}>
            {reportContent}
          </pre>
        </div>
      )}
    </div>
  );
};
