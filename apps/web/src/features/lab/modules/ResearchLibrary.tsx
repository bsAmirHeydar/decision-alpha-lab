import type { LabDocumentDetail, LabDocumentSummary, LabStage } from '../../../types/lab';

interface Props {
  stages: LabStage[];
  documents: LabDocumentSummary[];
  activeStage: string;
  query: string;
  selectedPath: string | null;
  document: LabDocumentDetail | null;
  loading: boolean;
  error: string | null;
  onStageChange: (stage: string) => void;
  onQueryChange: (query: string) => void;
  onSelectDocument: (document: LabDocumentSummary) => void;
  onOpenReplay: () => void;
}

export function ResearchLibrary(props: Props) {
  const selected = props.document?.doc;

  return (
    <div className="library-grid">
      <aside className="panel document-index">
        <div className="panel-heading sticky">
          <span className="section-kicker">Research Library</span>
          <h3>Documents</h3>
          <input
            value={props.query}
            onChange={(event) => props.onQueryChange(event.target.value)}
            placeholder="Search ID, title, status, tag..."
          />
        </div>

        <div className="stage-tabs">
          <button className={props.activeStage === 'all' ? 'active' : ''} onClick={() => props.onStageChange('all')}>All</button>
          {props.stages.map((stage) => (
            <button
              key={stage.stage_id}
              className={props.activeStage === stage.stage_id ? 'active' : ''}
              onClick={() => props.onStageChange(stage.stage_id)}
            >
              {stage.label}<span>{stage.count}</span>
            </button>
          ))}
        </div>

        <div className="doc-list">
          {props.documents.map((doc) => (
            <button
              key={doc.path}
              className={props.selectedPath === doc.path ? 'active' : ''}
              onClick={() => props.onSelectDocument(doc)}
            >
              <span className="doc-id">{doc.doc_id}</span>
              <strong>{doc.title}</strong>
              <em>{doc.stage_label} · {doc.status ?? 'No status'}</em>
            </button>
          ))}
        </div>
      </aside>

      <section className="panel reader-panel">
        {props.loading && <div className="empty-state">Loading document...</div>}
        {props.error && <div className="empty-state error">{props.error}</div>}
        {!props.loading && !props.error && !props.document && (
          <div className="empty-state">No document selected. Pick a document from the left index.</div>
        )}
        {props.document && (
          <>
            <div className="reader-header">
              <div>
                <span className="section-kicker">{selected?.stage_label} / {selected?.entity_type}</span>
                <h2>{selected?.title}</h2>
                <p>{selected?.path}</p>
              </div>
              <div className="reader-actions">
                {selected?.capabilities.includes('chart_replay') || selected?.capabilities.includes('test_on_chart') ? (
                  <button onClick={props.onOpenReplay}>Test on Chart</button>
                ) : null}
              </div>
            </div>

            <div className="relation-strip">
              {(selected?.relation_ids ?? []).map((rel) => <span key={rel}>{rel}</span>)}
              {(selected?.tags ?? []).slice(0, 8).map((tag) => <em key={tag}>{tag}</em>)}
            </div>

            <div className="reader-layout">
              <article className="markdown-body">
                <Markdown content={props.document.content} />
              </article>
              <aside className="outline-panel">
                <span className="section-kicker">Outline</span>
                {props.document.outline.map((item) => (
                  <div key={`${item.line}-${item.title}`} className={`outline-item level-${item.level}`}>
                    {item.title}
                  </div>
                ))}
              </aside>
            </div>
          </>
        )}
      </section>
    </div>
  );
}

function Markdown({ content }: { content: string }) {
  const lines = content.split(/\r?\n/);
  return (
    <>
      {lines.map((line, index) => {
        const h = line.match(/^(#{1,6})\s+(.+)$/);
        if (h) {
          const Tag = `h${Math.min(h[1].length, 4)}` as keyof JSX.IntrinsicElements;
          return <Tag key={index}>{h[2]}</Tag>;
        }
        if (line.trim().startsWith('```')) return <hr key={index} />;
        if (!line.trim()) return <br key={index} />;
        if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) return <li key={index}>{line.trim().slice(2)}</li>;
        return <p key={index}>{line}</p>;
      })}
    </>
  );
}
