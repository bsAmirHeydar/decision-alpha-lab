import type { ReplayPayload, ReplayQuery } from '../types/visualization';

const API_BASE = import.meta.env.VITE_QUANT_LAB_API_BASE ?? '/api';

export async function fetchReplay(query: ReplayQuery): Promise<ReplayPayload> {
  const params = new URLSearchParams({
    symbol: query.symbol,
    timeframe: query.timeframe,
    L: String(query.L),
    zone_ratio: String(query.zone_ratio),
    exit_gap: String(query.exit_gap),
    consumption_mode: query.consumption_mode,
    source: query.source,
  });

  const response = await fetch(`${API_BASE}/replay/M0001?${params.toString()}`);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Replay API failed (${response.status}): ${text}`);
  }
  return response.json();
}

export async function fetchDatasets(): Promise<Array<Record<string, unknown>>> {
  const response = await fetch(`${API_BASE}/datasets`);
  if (!response.ok) {
    throw new Error(`Datasets API failed (${response.status})`);
  }
  const payload = await response.json();
  return payload.datasets ?? [];
}
