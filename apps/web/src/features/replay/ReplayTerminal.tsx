import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchM0001Visualization } from '../../api/client';
import { MarketChart } from '../../components/chart/MarketChart';
import type { TableView, VisualizationPayload } from '../../types/visualization';

export function ReplayTerminal() {
  const [symbol, setSymbol] = useState('GOLD');
  const [timeframe, setTimeframe] = useState('M15');
  const [L, setL] = useState(5);
  const [zoneRatio, setZoneRatio] = useState(0.9);
  const [exitGap, setExitGap] = useState(6);
  const [mode, setMode] = useState('hunt');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [selectedObjectId, setSelectedObjectId] = useState<string | null>(null);
  const [hoveredObjectId, setHoveredObjectId] = useState<string | null>(null);
  const [activeTableId, setActiveTableId] = useState('events');

  const query = useQuery({
    queryKey: ['m0001-visualization', symbol, timeframe, L, zoneRatio, exitGap, mode],
    queryFn: () => fetchM0001Visualization({ symbol, timeframe, L, zoneRatio, exitGap, mode }),
  });

  const payload = query.data;
  const maxIndex = Math.max(0, (payload?.candles.length ?? 1) - 1);

  useMemo(() => {
    if (!playing || !payload) return;
    const timer = window.setInterval(() => {
      setCurrentIndex((value) => Math.min(maxIndex, value + 1));
    }, 80);
    return () => window.clearInterval(timer);
  }, [playing, payload, maxIndex]);

  function selectObject(id: string | null) {
    setSelectedObjectId(id);
    const foundTable = payload?.tables.find((table) => table.rows.some((row) => objectIdForRow(row) === id));
    if (foundTable) setActiveTableId(foundTable.table_id);
    const row = payload?.tables.flatMap((table) => table.rows).find((item) => objectIdForRow(item) === id);
    const idx = Number(row?.entry_index ?? row?.index);
    if (Number.isFinite(idx)) setCurrentIndex(Math.max(0, Math.min(maxIndex, idx)));
  }

  return (
    <div className="replay-terminal">
      <section className="replay-header panel">
        <div>
          <span className="section-kicker">Visual Adapter / M0001</span>
          <h2>Relative Territory Volatility Replay</h2>
        </div>
        <div className="control-strip">
          <label>Symbol<input value={symbol} onChange={(event) => setSymbol(event.target.value)} /></label>
          <label>TF<input value={timeframe} onChange={(event) => setTimeframe(event.target.value)} /></label>
          <label>L<input type="number" value={L} onChange={(event) => setL(Number(event.target.value))} /></label>
          <label>ZR<input type="number" step="0.05" value={zoneRatio} onChange={(event) => setZoneRatio(Number(event.target.value))} /></label>
          <label>EG<input type="number" value={exitGap} onChange={(event) => setExitGap(Number(event.target.value))} /></label>
          <label>Mode<select value={mode} onChange={(event) => setMode(event.target.value)}><option>hunt</option><option>touch</option></select></label>
        </div>
      </section>

      {query.isLoading && <div className="empty-state">Loading market visualization contract...</div>}
      {query.error instanceof Error && <div className="empty-state error">{query.error.message}</div>}
      {payload && (
        <>
          <section className="replay-kpis">
            {Object.entries(payload.stats).map(([key, value]) => (
              <div className="stat-card compact" key={key}>
                <span>{key}</span>
                <strong>{formatValue(value)}</strong>
              </div>
            ))}
            {payload.validation_flags.map((flag) => (
              <div className={`validation-chip ${flag.status}`} key={flag.id}>
                <span>{flag.status}</span>
                <strong>{flag.label}</strong>
              </div>
            ))}
          </section>

          <section className="chart-shell panel">
            <MarketChart
              payload={payload}
              currentIndex={currentIndex}
              selectedObjectId={selectedObjectId}
              hoveredObjectId={hoveredObjectId}
              onSelectObject={selectObject}
              onHoverObject={setHoveredObjectId}
            />
            <div className="replay-controls">
              <button onClick={() => setPlaying((value) => !value)}>{playing ? 'Pause' : 'Play'}</button>
              <button onClick={() => setCurrentIndex((value) => Math.max(0, value - 1))}>Step -</button>
              <button onClick={() => setCurrentIndex((value) => Math.min(maxIndex, value + 1))}>Step +</button>
              <input
                type="range"
                min={0}
                max={maxIndex}
                value={currentIndex}
                onChange={(event) => setCurrentIndex(Number(event.target.value))}
              />
              <span>{currentIndex} / {maxIndex}</span>
            </div>
          </section>

          <section className="table-shell panel">
            <div className="table-tabs">
              {payload.tables.map((table) => (
                <button key={table.table_id} className={activeTableId === table.table_id ? 'active' : ''} onClick={() => setActiveTableId(table.table_id)}>
                  {table.label}<span>{table.rows.length}</span>
                </button>
              ))}
            </div>
            <DynamicTable
              table={payload.tables.find((table) => table.table_id === activeTableId) ?? payload.tables[0]}
              selectedObjectId={selectedObjectId}
              hoveredObjectId={hoveredObjectId}
              onHover={setHoveredObjectId}
              onSelect={selectObject}
            />
          </section>
        </>
      )}
    </div>
  );
}

function DynamicTable({ table, selectedObjectId, hoveredObjectId, onHover, onSelect }: {
  table: TableView;
  selectedObjectId: string | null;
  hoveredObjectId: string | null;
  onHover: (id: string | null) => void;
  onSelect: (id: string | null) => void;
}) {
  if (!table) return null;
  return (
    <div className="data-table-wrap">
      <table className="data-table">
        <thead>
          <tr>{table.columns.map((column) => <th key={column.key}>{column.label}</th>)}</tr>
        </thead>
        <tbody>
          {table.rows.map((row, index) => {
            const id = objectIdForRow(row);
            const active = id === selectedObjectId;
            const hovered = id === hoveredObjectId;
            return (
              <tr
                key={`${id}-${index}`}
                className={`${active ? 'selected' : ''} ${hovered ? 'hovered' : ''}`}
                onMouseEnter={() => onHover(id)}
                onMouseLeave={() => onHover(null)}
                onClick={() => onSelect(id)}
              >
                {table.columns.map((column) => <td key={column.key}>{formatValue(row[column.key])}</td>)}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function objectIdForRow(row: Record<string, unknown>) {
  if (typeof row.id === 'string') return row.id;
  if (row.row_index !== undefined) return `M0001-EVENT-${row.row_index}`;
  if (row.node_id !== undefined) return `NODE-${row.node_id}`;
  return String(row.id ?? row.path ?? JSON.stringify(row).slice(0, 24));
}

function formatValue(value: unknown) {
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) return '—';
    return Math.abs(value) > 999 ? value.toLocaleString(undefined, { maximumFractionDigits: 0 }) : value.toLocaleString(undefined, { maximumFractionDigits: 4 });
  }
  if (typeof value === 'boolean') return value ? 'yes' : 'no';
  if (value === null || value === undefined || value === '') return '—';
  return String(value);
}
