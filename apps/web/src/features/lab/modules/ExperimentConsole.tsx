import type { ResearchEntity, ResearchRun } from '../../../types/lab';

interface Props {
  experiments: ResearchEntity[];
  runs: ResearchRun[];
  onOpenDocument: (entity: ResearchEntity) => void;
  onOpenReplay: () => void;
}

export function ExperimentConsole({ experiments, runs, onOpenDocument, onOpenReplay }: Props) {
  return (
    <div className="console-grid">
      <section className="panel full-span">
        <div className="panel-heading">
          <span className="section-kicker">Experiment Console</span>
          <h2>Run, inspect, compare, and promote evidence.</h2>
        </div>
        <div className="split-panels">
          <div>
            <h3>Experiment entities</h3>
            <div className="entity-list">
              {experiments.length ? experiments.map((entity) => (
                <button className="entity-row" key={entity.id} onClick={() => onOpenDocument(entity)}>
                  <strong>{entity.id}</strong>
                  <span>{entity.title}</span>
                  <em>{entity.status ?? 'No status'}</em>
                </button>
              )) : <div className="empty-state small">No formal experiment documents yet. Add EXP files and they will appear here.</div>}
            </div>
          </div>
          <div>
            <h3>Runnable artifacts</h3>
            <div className="run-list">
              {runs.map((run) => (
                <button className="run-row clickable" key={run.run_id} onClick={onOpenReplay}>
                  <strong>{run.run_id}</strong>
                  <span>{run.entity_id} · {run.symbol} {run.timeframe}</span>
                  <em>{String(run.summary_stats.rows ?? 'n/a')} rows</em>
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
