import type { ResearchEntity, ResearchRun } from '../../../types/lab';

interface Props {
  metrics: ResearchEntity[];
  runs: ResearchRun[];
  onOpenDocument: (entity: ResearchEntity) => void;
  onOpenReplay: () => void;
}

export function MetricStudio({ metrics, runs, onOpenDocument, onOpenReplay }: Props) {
  const runsByEntity = new Map<string, ResearchRun[]>();
  runs.forEach((run) => {
    const rows = runsByEntity.get(run.entity_id) ?? [];
    rows.push(run);
    runsByEntity.set(run.entity_id, rows);
  });

  return (
    <div className="studio-grid">
      <section className="panel full-span">
        <div className="panel-heading">
          <span className="section-kicker">Metric Studio</span>
          <h2>Every metric must expose code, spec, schema, runs, and visual adapters.</h2>
        </div>

        <div className="entity-grid">
          {metrics.map((metric) => {
            const metricRuns = runsByEntity.get(metric.id) ?? [];
            return (
              <div className="entity-card metric" key={metric.id}>
                <span className="entity-id">{metric.id}</span>
                <h3>{metric.title}</h3>
                <p>{metric.summary || 'Metric summary pending.'}</p>
                <div className="metric-kpis">
                  <Kpi label="Runs" value={metricRuns.length} />
                  <Kpi label="Docs" value={metric.document_paths.length} />
                  <Kpi label="Caps" value={metric.capabilities.length} />
                </div>
                <div className="tag-row">
                  {metric.capabilities.slice(0, 7).map((cap) => <em key={cap}>{cap}</em>)}
                </div>
                <div className="card-actions">
                  <button onClick={() => onOpenDocument(metric)}>Open Spec</button>
                  <button className="secondary" onClick={onOpenReplay}>Visualize</button>
                </div>
                <div className="run-list compact">
                  {metricRuns.slice(0, 4).map((run) => (
                    <div className="run-row" key={run.run_id}>
                      <strong>{run.symbol} {run.timeframe}</strong>
                      <span>{String(run.summary_stats.rows ?? 'n/a')} rows</span>
                      <em>{formatParams(run.parameters)}</em>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}

function Kpi({ label, value }: { label: string; value: number }) {
  return <div><span>{label}</span><strong>{value}</strong></div>;
}

function formatParams(params: Record<string, unknown>) {
  return Object.entries(params).map(([key, value]) => `${key}=${String(value)}`).join(' ');
}
