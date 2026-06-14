import type { LabOverview } from '../../../types/lab';

interface Props {
  overview?: LabOverview;
  loading: boolean;
  onOpenLibrary: () => void;
  onOpenReplay: () => void;
  onOpenMetricStudio: () => void;
}

export function CommandCenter({ overview, loading, onOpenLibrary, onOpenReplay, onOpenMetricStudio }: Props) {
  if (loading) return <div className="empty-state">Loading research registry...</div>;

  return (
    <div className="mission-grid">
      <section className="hero-panel panel-glow">
        <div>
          <span className="section-kicker">End-to-end lineage</span>
          <h2>Observation → Hypothesis → Metric → Experiment → Validation → Execution</h2>
          <p>
            This workspace is built to show whether the research code is doing what the research design claims.
            Every document, run, metric artifact, and chart object should be traceable.
          </p>
        </div>
        <div className="hero-actions">
          <button onClick={onOpenReplay}>Open Visual Replay</button>
          <button className="secondary" onClick={onOpenLibrary}>Read Documents</button>
          <button className="secondary" onClick={onOpenMetricStudio}>Inspect Metrics</button>
        </div>
      </section>

      <section className="stat-grid">
        {Object.entries(overview?.stats ?? {}).map(([key, value]) => (
          <div className="stat-card" key={key}>
            <span>{key.replace(/_/g, ' ')}</span>
            <strong>{Number(value).toLocaleString()}</strong>
          </div>
        ))}
      </section>

      <section className="panel wide-panel">
        <div className="panel-heading">
          <span className="section-kicker">Research pipeline</span>
          <h3>Critical path</h3>
        </div>
        <div className="pipeline">
          {(overview?.critical_path ?? []).map((item, index) => (
            <div className="pipeline-node" key={`${item.id}-${index}`}>
              <span>{item.stage}</span>
              <strong>{item.id}</strong>
              <em>{item.label}</em>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <span className="section-kicker">Live health</span>
          <h3>Registry checks</h3>
        </div>
        <div className="check-list">
          {(overview?.health ?? []).map((item) => (
            <div className="check-row" key={item.id}>
              <i className={`status-dot ${item.status}`} />
              <div>
                <strong>{item.label}</strong>
                <span>{item.detail}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <span className="section-kicker">Recent artifacts</span>
          <h3>Runs</h3>
        </div>
        <div className="run-list compact">
          {(overview?.recent_runs ?? []).slice(0, 8).map((run) => (
            <div className="run-row" key={run.run_id}>
              <strong>{run.run_id}</strong>
              <span>{run.symbol} {run.timeframe}</span>
              <em>{String(run.summary_stats.rows ?? 'n/a')} rows</em>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
