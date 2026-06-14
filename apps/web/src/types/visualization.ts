export interface Candle {
  index: number;
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number | null;
}

export interface VisualObject {
  id: string;
  kind: 'zone' | 'event_window' | 'segment' | 'marker' | 'label' | string;
  object_type?: string;
  start_index?: number | null;
  end_index?: number | null;
  entry_index?: number | null;
  exit_index?: number | null;
  index?: number | null;
  time?: number | null;
  lower?: number | null;
  upper?: number | null;
  price?: number | null;
  shape?: string | null;
  label?: string | null;
  payload?: Record<string, unknown>;
}

export interface OverlayLayer {
  layer_id: string;
  label: string;
  default_visible: boolean;
  objects: VisualObject[];
}

export interface TableColumn {
  key: string;
  label: string;
}

export interface TableView {
  table_id: string;
  label: string;
  object_type: string;
  columns: TableColumn[];
  rows: Array<Record<string, unknown>>;
}

export interface VisualizationPayload {
  dataset: {
    symbol: string;
    timeframe: string;
    source: string;
    bars: number;
    parameters: Record<string, unknown>;
  };
  entity: { id: string; title: string; type: string };
  candles: Candle[];
  overlay_layers: OverlayLayer[];
  tables: TableView[];
  stats: Record<string, unknown>;
  timeline: Array<{ id: string; time: number; index: number; label: string; object_id: string }>;
  validation_flags: Array<{ id: string; label: string; status: string }>;
}
