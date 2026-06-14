import { FlaskConical, PlayCircle, ShieldAlert } from 'lucide-react';
import type { LabDocumentSummary } from '../../types/lab';

export function HypothesisWorkbench({ hypotheses, experiments, validations, onOpenDocument, onOpenReplay }: {
  hypotheses: LabDocumentSummary[];
  experiments: LabDocumentSummary[];
  validations: LabDocumentSummary[];
  onOpenDocument: (document: LabDocumentSummary) => void;
  onOpenReplay: () => void;
}) {
  return (
    <div className="workbench-grid">
      <section className="workbench-column wide">
        <div className="section-heading">
          <FlaskConical size={17} />
          <div><h2>Hypothesis Workbench</h2><p>Read the claim, open its related experiments, then inspect it on the chart.</p></div>
        </div>
        <div className="hypothesis-grid">
          {hypotheses.map((hypothesis) => (
            <article className="hypothesis-card" key={hypothesis.path}>
              <span>{hypothesis.doc_id}</span>
              <h3>{hypothesis.title}</h3>
              <p>{hypothesis.summary || 'No summary available yet.'}</p>
              <div className="relation-row">{hypothesis.relation_ids.slice(0, 8).map((id) => <em key={id}>{id}</em>)}</div>
              <div className="card-actions">
                <button onClick={() => onOpenDocument(hypothesis)}>Read</button>
                <button className="primary-mini" onClick={onOpenReplay}>Test on Chart</button>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="workbench-column">
        <div className="section-heading compact"><PlayCircle size={17} /><h2>Experiments</h2></div>
        <div className="compact-doc-list">
          {experiments.slice(0, 12).map((experiment) => <button key={experiment.path} onClick={() => onOpenDocument(experiment)}><strong>{experiment.doc_id}</strong><span>{experiment.title}</span></button>)}
        </div>
      </section>

      <section className="workbench-column">
        <div className="section-heading compact"><ShieldAlert size={17} /><h2>Validation Gates</h2></div>
        <div className="compact-doc-list">
          {validations.slice(0, 12).map((validation) => <button key={validation.path} onClick={() => onOpenDocument(validation)}><strong>{validation.doc_id}</strong><span>{validation.title}</span></button>)}
        </div>
      </section>
    </div>
  );
}
