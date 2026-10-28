export interface Scope {
  id: number;
  name: string;
  description?: string;
  allowed_targets: string;
  allowed_ports: string;
  allowed_protocols: string;
  created_at: string;
}

export interface Assessment {
  id: number;
  title: string;
  description?: string;
  target: string;
  engine: string;
  status: string;
  scope_id: number;
  created_at: string;
  updated_at: string;
  scope?: Scope;
}

export interface Job {
  id: number;
  assessment_id: number;
  engine_name: string;
  status: string;
  progress: number;
  parameters: Record<string, any>;
  output: string;
  mock_mode: boolean;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

export interface Finding {
  id: number;
  assessment_id: number;
  title: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
  vulnerability_type: string;
  target: string;
  details: string;
  remediation?: string;
  is_mock: boolean;
  created_at: string;
}

export interface EngineItem {
  engine: string;
  category: string;
  status: 'Implemented' | 'Planned';
  network: 'Yes' | 'No';
  scope: 'Required' | 'N/A';
}

export interface AuditLog {
  id: number;
  user_id?: number;
  action: string;
  resource: string;
  details: Record<string, any>;
  ip_address?: string;
  timestamp: string;
}
