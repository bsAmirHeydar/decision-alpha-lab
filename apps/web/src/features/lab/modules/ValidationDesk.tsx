import type { ResearchEntity, ResearchRun } from '../../../types/lab';

interface Props {
  validations: ResearchEntity[];
  runs: ResearchRun[];
  onOpenDocument: (entity: ResearchEntity) => void;
}

const GATES = [
  ['leakage', 'No future leakage', 'Metric must only use information available at the current candle.'],
  ['baseline', 'Random baseline comparison', 'Structural behavior must beat randomized locations.'],
  ['walkforward', 'Walk-forward split', 'Performance must survive sequential splits.'],
  ['robustness', 'Parameter robustness', 'Edge must not depend on one fragile parameter set.'],
  ['oos', 'Out-of-sample behavior', 'Holdout behavior must remain stable.'],
  ['execution', 'Execution separation', 'Research alpha and execution impact must be separated.'],
];

export function ValidationDesk({ validations, runs, onOpenDocument }: Props) {
  const passCount = runs.flatMap((run) => run.validation_flags).filter((flag) => flag.status === 'pass').length;

  return (
    <div className="validation-grid">
      <section className="panel full-span">
        <div className="panel-heading">
          <span className="section-kicker">Validation Desk</span>
          <h2>Nothing moves toward production without evidence gates.</h2>
        </div>
        <div className="gate-grid">
          {GATES.map(([id, title, description], index) => (
            <div className="gate-card" key={id}>
              <span>Gate {index + 1}</span>
              <strong>{title}</strong>
              <p>{description}</p>
              <i className={`gate-state ${index === 0 || passCount ? 'pass' : 'pending'}`}>{index === 0 || passCount ? 'observable' : 'pending'}</i>
            </div>
          ))}
        </div>
      </section>

      <section className="panel full-span">
        <div className="panel-heading">
          <span className="section-kicker">Validation documents</span>
          <h3>Reports</h3>
        </div>
        <div className="entity-list">
          {validations.length ? validations.map((entity) => (
            <button className="entity-row" key={entity.id} onClick={() => onOpenDocument(entity)}>
              <strong>{entity.id}</strong>
              <span>{entity.title}</span>
              <em>{entity.status ?? 'No status'}</em>
            </button>
          )) : <div className="empty-state small">No validation report documents yet.</div>}
        </div>
      </section>
    </div>
  );
}
