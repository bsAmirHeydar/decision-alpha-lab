export type LayerType =
  | 'markers'
  | 'horizontal_levels'
  | 'zones'
  | 'event_windows'
  | 'segments'
  | 'labels'
  | 'series'
  | 'annotations';

export interface DataQuality {
  has_duplicates: boolean;
  is_sorted: boolean;
  missing_bars: number | null;
}

export interface DatasetDescriptor {
  dataset_id: string;
  source: string;
  symbol: string;
  timeframe: string;
  start_time: string | null;
  end_time: string | null;
  bars: number;
  timezone: string;
  data_quality: DataQuality;
  parameters: Record<string, unknown>;
  contract_version: string;
}

export interface Candle {
  id: string;
  index: number;
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number | null;
  spread: number | null;
}

export interface SourceRef {
  object_type: string;
  object_id: string;
  metric_id: string | null;
  hypothesis_id: string | null;
  experiment_id: string | null;
}

export interface VisualObject {
  id: string;
  kind: string;
  source_ref: SourceRef;
  metadata: Record<string, unknown>;
  time?: string | null;
  index?: number | null;
  price?: number | null;
  start_index?: number | null;
  end_index?: number | null;
  lower?: number | null;
  upper?: number | null;
  entry_index?: number | null;
  exit_index?: number | null;
  entry_time?: string | null;
  exit_time?: string | null;
  visible_from_index?: number | null;
  complete_from_index?: number | null;
  shape?: string | null;
  label?: string | null;
}

export interface OverlayLayer {
  layer_id: string;
  label: string;
  type: LayerType;
  visible: boolean;
  z_index: number;
  opacity: number;
  objects: VisualObject[];
}

export interface TableColumn {
  key: string;
  label: string;
  type: string;
}

export interface TableSpec {
  table_id: string;
  label: string;
  primary_key: string;
  columns: TableColumn[];
  rows: Array<Record<string, unknown>>;
}

export interface InspectorPayload {
  title: string;
  subtitle?: string | null;
  sections: Array<Record<string, unknown>>;
}

export interface ReplayPayload {
  dataset: DatasetDescriptor;
  candles: Candle[];
  layers: OverlayLayer[];
  tables: TableSpec[];
  selection_map: Record<string, Record<string, unknown>>;
  inspector: InspectorPayload;
}

export interface ReplayQuery {
  symbol: string;
  timeframe: string;
  L: number;
  zone_ratio: number;
  exit_gap: number;
  consumption_mode: 'hunt' | 'touch';
  source: 'cache';
}

export interface SelectionState {
  objectId: string | null;
  kind: string | null;
  tableId: string | null;
  rowId: string | null;
}
