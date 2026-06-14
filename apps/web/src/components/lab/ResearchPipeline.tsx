import { ArrowRight, CheckCircle2, CircleDashed, FlaskConical, Rocket, ShieldCheck } from 'lucide-react';
import type { LabOverview } from '../../types/lab';

const STAGE_ICONS = [CircleDashed, FlaskConical, ShieldCheck, Rocket];

export function ResearchPipeline({ overview, onOpenReplay, onOpenDocs }: { overview: LabOverview | undefined; onOpenReplay: () => void; onOpenDocs: () => void }) {
  const critical = overview?.critical_path ?? [];
  return (
    <div className="pipeline-panel">
      <div className="pipeline-header">
        <div>
          <span className="eyebrow">Scientific Workflow</span>
          <h2>Research lifecycle command map</h2>
          <p>Every observation, hypothesis, metric, experiment, validation gate, and signal must remain traceable.</p>
        </div>
        <div className="pipeline-actions">
          <button className="primary-button" onClick={onOpenReplay}>Open Visual Replay</button>
          <button className="secondary-button" onClick={onOpenDocs}>Read Docs</button>
        </div>
      </div>

      <div className="critical-path">
        {critical.map((item, index) => {
          const Icon = STAGE_ICONS[index % STAGE_ICONS.length];
          return (
            <div className="critical-node" key={item.id}>
              <div className="critical-node-icon"><Icon size={16} /></div>
              <span>{item.stage}</span>
              <strong>{item.id}</strong>
              <p>{item.label}</p>
              {index < critical.length - 1 && <ArrowRight className="critical-arrow" size={16} />}
            </div>
          );
        })}
      </div>

      <div className="lab-scoreboard">
        <Score label="Documents" value={overview?.stats.documents ?? 0} />
        <Score label="Hypotheses" value={overview?.stats.hypotheses ?? 0} />
        <Score label="Experiments" value={overview?.stats.experiments ?? 0} />
        <Score label="Validations" value={overview?.stats.validations ?? 0} />
        <Score label="Metrics" value={overview?.stats.metrics ?? 0} />
      </div>

      <div className="stage-grid">
        {(overview?.stages ?? []).map((stage) => (
          <div className="stage-card" key={stage.stage_id}>
            <div><CheckCircle2 size={16} /><strong>{stage.label}</strong></div>
            <p>{stage.description}</p>
            <span>{stage.count} files</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function Score({ label, value }: { label: string; value: number }) {
  return <div className="score-card"><span>{label}</span><strong>{value.toLocaleString()}</strong></div>;
}
