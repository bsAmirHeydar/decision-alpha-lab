import type { ReplayPayload, SelectionState } from '../types/visualization';
import { asRecord, formatNumber, formatTime } from '../utils/format';

export function Inspector({ payload, selection, selectedRecord, currentIndex }: { payload: ReplayPayload | null; selection: SelectionState; selectedRecord: Record<string, unknown> | null; currentIndex: number }) {
  if (!payload) {
    return <div className="inspector empty">No replay loaded.</div>;
  }

  const currentCandle = payload.candles[currentIndex];
  const row = asRecord(selectedRecord?.row);

  return (
    <div className="inspector">
      <div className="panel-title">Inspector</div>
      {selection.objectId && selectedRecord ? (
        <>
          <h2>{String(selectedRecord.title ?? selection.objectId)}</h2>
          <p>{String(selectedRecord.subtitle ?? selection.kind ?? '')}</p>
          <KeyValueGrid record={row} priority={['event_id', 'node_object_id', 'node_id', 'node_type', 'type', 'revisit_id', 'entry_index', 'exit_index', 'RTV', 'hunted', 'territory_lower', 'territory_upper']} />
        </>
      ) : (
        <>
          <h2>{payload.inspector.title}</h2>
          <p>{payload.inspector.subtitle}</p>
          <KeyValueGrid record={payload.dataset.parameters} priority={['metric_id', 'L', 'zone_ratio', 'exit_gap', 'consumption_mode', 'confirmed_nodes', 'events', 'mean_RTV', 'median_RTV', 'max_revisit']} />
        </>
      )}
      <div className="inspector-section">
        <h3>Current Candle</h3>
        {currentCandle ? (
          <div className="kv-grid compact">
            <span>Index</span><strong>{currentCandle.index}</strong>
            <span>Time</span><strong>{formatTime(currentCandle.time)}</strong>
            <span>Open</span><strong>{formatNumber(currentCandle.open)}</strong>
            <span>High</span><strong>{formatNumber(currentCandle.high)}</strong>
            <span>Low</span><strong>{formatNumber(currentCandle.low)}</strong>
            <span>Close</span><strong>{formatNumber(currentCandle.close)}</strong>
          </div>
        ) : <p>No candle at this index.</p>}
      </div>
    </div>
  );
}

function KeyValueGrid({ record, priority }: { record: Record<string, unknown>; priority: string[] }) {
  const keys = [...priority.filter((key) => key in record), ...Object.keys(record).filter((key) => !priority.includes(key) && key !== 'selection_ref')].slice(0, 18);
  return (
    <div className="kv-grid">
      {keys.map((key) => (
        <ReactFragment key={key} label={key} value={record[key]} />
      ))}
    </div>
  );
}

function ReactFragment({ label, value }: { label: string; value: unknown }) {
  const text = label.toLowerCase().includes('time') ? formatTime(value) : typeof value === 'number' ? formatNumber(value) : value === null || value === undefined ? '—' : String(value);
  return <><span>{label}</span><strong>{text}</strong></>;
}
