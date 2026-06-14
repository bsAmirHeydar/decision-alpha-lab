import { Search, FileText, Link2, CircleDot } from 'lucide-react';
import type { LabDocumentSummary, LabStage } from '../../types/lab';

export function DocumentBrowser({
  stages,
  documents,
  activeStage,
  query,
  selectedPath,
  onStageChange,
  onQueryChange,
  onSelectDocument,
}: {
  stages: LabStage[];
  documents: LabDocumentSummary[];
  activeStage: string;
  query: string;
  selectedPath: string | null;
  onStageChange: (stageId: string) => void;
  onQueryChange: (query: string) => void;
  onSelectDocument: (document: LabDocumentSummary) => void;
}) {
  return (
    <div className="document-browser">
      <aside className="stage-rail">
        <button className={activeStage === 'all' ? 'active' : ''} onClick={() => onStageChange('all')}>
          <CircleDot size={15} /> All <span>{stages.reduce((total, stage) => total + stage.count, 0)}</span>
        </button>
        {stages.map((stage) => (
          <button key={stage.stage_id} className={activeStage === stage.stage_id ? 'active' : ''} onClick={() => onStageChange(stage.stage_id)} title={stage.description}>
            <FileText size={15} /> {stage.label} <span>{stage.count}</span>
          </button>
        ))}
      </aside>

      <section className="document-list-panel">
        <div className="search-box">
          <Search size={15} />
          <input value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Search docs, IDs, status, summaries…" />
        </div>
        <div className="document-list">
          {documents.map((document) => (
            <button key={document.path} className={selectedPath === document.path ? 'doc-card active' : 'doc-card'} onClick={() => onSelectDocument(document)}>
              <span className="doc-card-kicker">{document.doc_id} · {document.stage_label}</span>
              <strong>{document.title}</strong>
              <p>{document.summary || document.path}</p>
              <div className="doc-card-meta">
                <span>{document.status ?? 'status: —'}</span>
                {document.relation_ids.length > 0 && <em><Link2 size={12} /> {document.relation_ids.slice(0, 4).join(', ')}</em>}
              </div>
            </button>
          ))}
          {!documents.length && <div className="empty-list">No documents match this filter.</div>}
        </div>
      </section>
    </div>
  );
}
