/**
 * API Service Layer
 * Handles all backend communication for Process Doctor
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface AnalyzeRequest {
  workflow_input: string;
  source_type: 'text' | 'github' | 'file';
}

export interface Bottleneck {
  id: string;
  label: string;
  severity: 'critical' | 'medium' | 'low';
  impact: string;
  fix: string;
}

export interface AnalyzeResponse {
  analysis_id: string;
  status: string;
  workflow_structure?: any;
  bottlenecks: Bottleneck[];
  metrics: {
    current_duration?: string;
    estimated_optimal?: string;
    efficiency_score?: number;
  };
  recommendations: string[];
  estimated_improvement: string;
}

export interface FixRequest {
  analysis_id: string;
  optimization_strategy?: 'aggressive' | 'balanced' | 'conservative';
}

export interface FixResponse {
  fix_id: string;
  analysis_id: string;
  status: string;
  optimized_workflow?: any;
  changes: Array<{
    type: string;
    description: string;
  }>;
  improvements: {
    time_saved?: string;
    efficiency_gain?: string;
    optimizations_applied?: number;
  };
  diff: string;
}

export interface PRRequest {
  fix_id: string;
  repository: string;
  branch?: string;
  title?: string;
  description?: string;
}

export interface PRResponse {
  pr_number: number;
  pr_url: string;
  branch: string;
  status: string;
  message: string;
}

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new APIError(
      response.status,
      error.error || error.detail || `HTTP ${response.status}`
    );
  }

  return response.json();
}

export const api = {
  /**
   * Analyze a workflow to identify bottlenecks and optimization opportunities
   */
  async analyzeWorkflow(request: AnalyzeRequest): Promise<AnalyzeResponse> {
    return fetchAPI<AnalyzeResponse>('/api/analyze', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Generate an optimized workflow based on analysis
   */
  async generateFix(request: FixRequest): Promise<FixResponse> {
    return fetchAPI<FixResponse>('/api/fix', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Create a pull request with the optimized workflow
   */
  async createPR(request: PRRequest): Promise<PRResponse> {
    return fetchAPI<PRResponse>('/api/pr', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string }> {
    return fetchAPI<{ status: string }>('/health');
  },
};

export { APIError };

// Made with Bob
