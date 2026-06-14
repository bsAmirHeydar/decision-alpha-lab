import type { ReplayPayload } from '../types/visualization';
import { formatNumber } from '../utils/format';

export function ResearchTree({ payload, selectedId }: { payload: ReplayPayload | null; selectedId: string | null }) {
  const params = payload?.dataset.parameters ?? {};
  const layers = payload?.layers ?? [];
  return (
    <div className="research-tree">
      <div className="panel-title">Research Lineage</div>
      <div className="tree-node root">OBS0001 · Structural highs/lows</div>
      <div className="tree-branch">
        <div className="tree-node">H0001 · Decision nodes</div>
        <div className="tree-node">H0002 · Node territories</div>
        <div className="tree-node active">M0001 · Relative Territory Volatility</div>
        <div className="tree-branch thin">
          <div className="tree-node">EXP0001 · Real market inspection</div>
          <div className="tree-node">Source · {payload?.dataset.source ?? 'cache'}</div>
          <div className="tree-node">Dataset · {payload ? `${payload.dataset.symbol} ${payload.dataset.timeframe}` : '—'}</div>
        </div>
      </div>

      <div className="tree-summary">
        <div><span>Bars</span><strong>{formatNumber(payload?.dataset.bars ?? 0, 0)}</strong></div>
        <div><span>Confirmed nodes</span><strong>{formatNumber(params.confirmed_nodes ?? 0, 0)}</strong></div>
        <div><span>Events</span><strong>{formatNumber(params.events ?? 0, 0)}</strong></div>
        <div><span>Selected</span><strong>{selectedId ?? '—'}</strong></div>
      </div>

      <div className="layer-audit">
        {layers.map((layer) => (
          <div key={layer.layer_id}>
            <span>{layer.label}</span>
            <strong>{layer.objects.length}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}
