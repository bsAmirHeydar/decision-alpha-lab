import type { CatalogResponse, LabDocumentDetail, LabOverview, ResearchEntity, ResearchRun } from '../types/lab';
import type { VisualizationPayload } from '../types/visualization';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://127.0.0.1:8000';

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${detail}`);
  }
  return response.json() as Promise<T>;
}

export function fetchLabOverview() {
  return request<LabOverview>('/api/lab/overview');
}

export function fetchLabCatalog(stageId: string, query: string) {
  const params = new URLSearchParams();
  params.set('stage_id', stageId || 'all');
  if (query.trim()) params.set('q', query.trim());
  return request<CatalogResponse>(`/api/lab/catalog?${params.toString()}`);
}

export function fetchLabDocument(path: string) {
  const params = new URLSearchParams({ path });
  return request<LabDocumentDetail>(`/api/lab/document?${params.toString()}`);
}

export function fetchEntities(entityType = 'all', query = '') {
  const params = new URLSearchParams();
  params.set('entity_type', entityType);
  if (query.trim()) params.set('q', query.trim());
  return request<{ entities: ResearchEntity[] }>(`/api/lab/entities?${params.toString()}`).then((data) => data.entities);
}

export function fetchRuns(entityId = 'all') {
  const params = new URLSearchParams({ entity_id: entityId });
  return request<{ runs: ResearchRun[] }>(`/api/lab/runs?${params.toString()}`).then((data) => data.runs);
}

export function fetchM0001Visualization(options: {
  symbol: string;
  timeframe: string;
  L: number;
  zoneRatio: number;
  exitGap: number;
  mode: string;
}) {
  const params = new URLSearchParams({
    symbol: options.symbol,
    timeframe: options.timeframe,
    L: String(options.L),
    zone_ratio: String(options.zoneRatio),
    exit_gap: String(options.exitGap),
    consumption_mode: options.mode,
  });
  return request<VisualizationPayload>(`/api/visualizations/m0001?${params.toString()}`);
}
