import type { LabDocumentSummary, ResearchEntity } from '../../../types/lab';

interface Props {
  hypotheses: ResearchEntity[];
  documents: LabDocumentSummary[];
  onOpenDocument: (document: ResearchEntity | LabDocumentSummary) => void;
  onOpenReplay: () => void;
}

export function HypothesisDesk({ hypotheses, documents, onOpenDocument, onOpenReplay }: Props) {
  const hypothesisDocs = documents.filter((doc) => doc.entity_type === 'hypothesis');

  return (
    <div className="desk-grid">
      <section className="panel full-span">
        <div className="panel-heading">
          <span className="section-kicker">Hypothesis Desk</span>
          <h2>Claims must be testable, visual, and falsifiable.</h2>
        </div>
        <div className="entity-grid">
          {(hypotheses.length ? hypotheses : hypothesisDocs).map((item) => (
            <div className="entity-card hypothesis" key={'id' in item ? item.id : item.path}>
              <span className="entity-id">{'id' in item ? item.id : item.doc_id}</span>
              <h3>{item.title}</h3>
              <p>{item.summary || 'No summary extracted yet.'}</p>
              <div className="tag-row">
                {('capabilities' in item ? item.capabilities : []).slice(0, 5).map((cap) => <em key={cap}>{cap}</em>)}
              </div>
              <div className="card-actions">
                <button onClick={() => onOpenDocument(item)}>Read</button>
                <button className="secondary" onClick={onOpenReplay}>Test on Chart</button>
              </div>
              <Relations ids={item.relation_ids} />
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function Relations({ ids }: { ids: string[] }) {
  return (
    <div className="relations">
      {ids.slice(0, 8).map((id) => <span key={id}>{id}</span>)}
    </div>
  );
}
