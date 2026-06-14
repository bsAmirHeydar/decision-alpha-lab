export type ResearchStageId =
  | 'observations'
  | 'hypotheses'
  | 'metrics'
  | 'experiments'
  | 'analysis'
  | 'validation'
  | 'production'
  | 'monitoring'
  | 'archive'
  | 'execution'
  | 'infrastructure'
  | 'core'
  | 'docs'
  | 'registry'
  | 'unknown';

export interface LabStage {
  stage_id: ResearchStageId | string;
  label: string;
  folder: string;
  description: string;
  count: number;
}

export interface LabDocumentSummary {
  doc_id: string;
  title: string;
  stage_id: ResearchStageId | string;
  stage_label: string;
  entity_type: string;
  path: string;
  extension: string;
  status: string | null;
  version: string | null;
  summary: string;
  relation_ids: string[];
  tags: string[];
  capabilities: string[];
  size_bytes: number;
  modified_time: number;
}

export interface LabDocumentDetail {
  doc: LabDocumentSummary;
  content: string;
  outline: Array<{ level: number; title: string; line: number }>;
  front_matter: Record<string, unknown>;
  relations: ResearchEntity[];
}

export interface ResearchEntity {
  id: string;
  entity_type: string;
  title: string;
  stage_id: string;
  stage_label: string;
  status: string | null;
  summary: string;
  primary_path: string;
  document_paths: string[];
  relation_ids: string[];
  tags: string[];
  capabilities: string[];
}

export interface ResearchRun {
  run_id: string;
  entity_id: string;
  entity_type: string;
  adapter_id: string;
  symbol: string | null;
  timeframe: string | null;
  parameters: Record<string, unknown>;
  artifact_path: string;
  summary_stats: Record<string, unknown>;
  validation_flags: Array<{ id: string; label: string; status: string; detail?: string }>;
  created_time: number;
}

export interface LabOverview {
  stats: Record<string, number>;
  stages: LabStage[];
  entities: ResearchEntity[];
  lineage: {
    nodes: Array<{ id: string; type: string; label: string; stage_id: string; status: string | null; path: string; capabilities: string[] }>;
    edges: Array<{ source: string; target: string; kind: string }>;
  };
  critical_path: Array<{ id: string; label: string; stage: string }>;
  recent_runs: ResearchRun[];
  health: Array<{ id: string; label: string; status: 'pass' | 'warn' | 'fail' | string; detail: string }>;
}

export interface CatalogResponse {
  documents: LabDocumentSummary[];
  selected_document_path: string | null;
}


export type LabDocumentPayload = LabDocumentDetail;
