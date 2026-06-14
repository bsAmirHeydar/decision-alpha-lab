import { useEffect, useMemo, useState, type ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Activity, Database, GitBranch, Gauge, Layers3, Play, Pause, RotateCcw, SkipBack, SkipForward, StepBack, StepForward } from 'lucide-react';
import { fetchReplay } from '../../api/client';
import { MarketChart } from '../../components/chart/MarketChart';
import { DataTable } from '../../components/DataTable';
import { Inspector } from '../../components/Inspector';
import { ResearchTree } from '../../components/ResearchTree';
import type { OverlayLayer, ReplayPayload, ReplayQuery, SelectionState } from '../../types/visualization';
import { asRecord, formatNumber } from '../../utils/format';

const DEFAULT_QUERY: ReplayQuery = {
  symbol: 'GOLD',
  timeframe: 'M15',
  L: 5,
  zone_ratio: 0.9,
  exit_gap: 6,
  consumption_mode: 'hunt',
  source: 'cache',
};

const SPEEDS = [1, 2, 5, 10, 25, 50, 100];

function buildLayerState(layers: OverlayLayer[]) {
  return Object.fromEntries(layers.map((layer) => [layer.layer_id, layer.visible]));
}

function useReplayClock(maxIndex: number) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [status, setStatus] = useState<'paused' | 'playing'>('paused');
  const [speed, setSpeed] = useState(10);

  useEffect(() => {
    if (status !== 'playing' || maxIndex <= 0) return;
    const interval = window.setInterval(() => {
      setCurrentIndex((value) => {
        if (value >= maxIndex) {
          setStatus('paused');
          return maxIndex;
        }
        return Math.min(value + 1, maxIndex);
      });
    }, Math.max(25, 600 / speed));
    return () => window.clearInterval(interval);
  }, [status, speed, maxIndex]);

  return {
    currentIndex,
    setCurrentIndex,
    status,
    setStatus,
    speed,
    setSpeed,
  };
}

export function ReplayTerminal() {
  const [query, setQuery] = useState<ReplayQuery>(DEFAULT_QUERY);
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['replay', query],
    queryFn: () => fetchReplay(query),
  });

  const maxIndex = Math.max((data?.candles.length ?? 1) - 1, 0);
  const replay = useReplayClock(maxIndex);
  const [selection, setSelection] = useState<SelectionState>({ objectId: null, kind: null, tableId: null, rowId: null });
  const [hoveredObjectId, setHoveredObjectId] = useState<string | null>(null);
  const [activeTableId, setActiveTableId] = useState<string>('M0001:events');
  const [layerVisibility, setLayerVisibility] = useState<Record<string, boolean>>({});

  useEffect(() => {
    if (!data) return;
    setLayerVisibility(buildLayerState(data.layers));
    setActiveTableId(data.tables[0]?.table_id ?? '');
    replay.setCurrentIndex(Math.min(250, maxIndex));
    setSelection({ objectId: null, kind: null, tableId: null, rowId: null });
    setHoveredObjectId(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data?.dataset.dataset_id]);

  const visibleLayers = useMemo(() => {
    return (data?.layers ?? []).map((layer) => ({
      ...layer,
      visible: layerVisibility[layer.layer_id] ?? layer.visible,
      objects: layer.objects.filter((object) => (object.visible_from_index ?? 0) <= replay.currentIndex),
    }));
  }, [data?.layers, layerVisibility, replay.currentIndex]);

  const activeTable = useMemo(() => {
    return data?.tables.find((table) => table.table_id === activeTableId) ?? data?.tables[0] ?? null;
  }, [data, activeTableId]);

  const selectedRecord = useMemo(() => {
    if (!selection.objectId || !data) return null;
    return asRecord(data.selection_map[selection.objectId]);
  }, [selection.objectId, data]);

  function jumpToObject(row: Record<string, unknown>) {
    const ref = asRecord(row.selection_ref);
    const objectId = String(ref.object_id ?? row.event_id ?? row.node_object_id ?? '');
    const tableId = String(ref.table_id ?? activeTableId);
    const rowId = String(ref.row_id ?? objectId);
    const kind = String(ref.kind ?? 'row');
    setSelection({ objectId, kind, tableId, rowId });

    const entryIndex = Number(row.entry_index ?? row.node_index ?? row.confirmation_index ?? replay.currentIndex);
    if (Number.isFinite(entryIndex)) {
      replay.setCurrentIndex(Math.max(0, Math.min(maxIndex, entryIndex)));
    }
  }


  function hoverRow(row: Record<string, unknown> | null) {
    if (!row) {
      setHoveredObjectId(null);
      return;
    }
    const ref = asRecord(row.selection_ref);
    const objectId = String(ref.object_id ?? row.event_id ?? row.node_object_id ?? '');
    setHoveredObjectId(objectId || null);
  }

  function selectChartObject(objectId: string, kind: string) {
    const mapped = asRecord(data?.selection_map?.[objectId]);
    const row = asRecord(mapped.row);
    const ref = asRecord(row.selection_ref);
    const tableId = String(ref.table_id ?? (kind === 'node' ? 'structural_nodes' : 'M0001:events'));
    const rowId = String(ref.row_id ?? objectId);
    setSelection({ objectId, kind, tableId, rowId });
    if (tableId) setActiveTableId(tableId);
  }

  const params = data?.dataset.parameters ?? {};

  return (
    <div className="terminal-shell">
      <header className="terminal-header">
        <div className="brand-block">
          <div className="brand-mark"><Activity size={18} /></div>
          <div>
            <div className="eyebrow">Decision Alpha Lab</div>
            <h1>Visual Research Terminal</h1>
          </div>
        </div>
        <div className="header-stats">
          <Stat icon={<Database size={15} />} label="Source" value={data?.dataset.source ?? 'cache'} />
          <Stat icon={<Gauge size={15} />} label="Events" value={formatNumber(params.events ?? 0, 0)} />
          <Stat icon={<GitBranch size={15} />} label="Nodes" value={formatNumber(params.confirmed_nodes ?? 0, 0)} />
          <Stat icon={<Activity size={15} />} label="Median RTV" value={formatNumber(params.median_RTV ?? null, 3)} />
        </div>
      </header>

      <section className="control-strip">
        <div className="query-grid">
          <label>Symbol<select value={query.symbol} onChange={(event) => setQuery({ ...query, symbol: event.target.value })}><option>GOLD</option><option>#US30</option></select></label>
          <label>Timeframe<select value={query.timeframe} onChange={(event) => setQuery({ ...query, timeframe: event.target.value })}><option>M15</option><option>M1</option></select></label>
          <label>L<input type="number" value={query.L} min={1} onChange={(event) => setQuery({ ...query, L: Number(event.target.value) })} /></label>
          <label>Zone Ratio<input type="number" value={query.zone_ratio} min={0} max={1} step={0.05} onChange={(event) => setQuery({ ...query, zone_ratio: Number(event.target.value) })} /></label>
          <label>Exit Gap<input type="number" value={query.exit_gap} min={1} onChange={(event) => setQuery({ ...query, exit_gap: Number(event.target.value) })} /></label>
          <label>Mode<select value={query.consumption_mode} onChange={(event) => setQuery({ ...query, consumption_mode: event.target.value as ReplayQuery['consumption_mode'] })}><option value="hunt">hunt</option><option value="touch">touch</option></select></label>
          <button className="primary-button" onClick={() => refetch()}>Load Replay</button>
        </div>
        <div className="replay-controls">
          <button onClick={() => replay.setCurrentIndex(0)}><SkipBack size={16} /></button>
          <button onClick={() => replay.setCurrentIndex(Math.max(0, replay.currentIndex - 1))}><StepBack size={16} /></button>
          <button className="play-button" onClick={() => replay.setStatus(replay.status === 'playing' ? 'paused' : 'playing')}>{replay.status === 'playing' ? <Pause size={17} /> : <Play size={17} />}</button>
          <button onClick={() => replay.setCurrentIndex(Math.min(maxIndex, replay.currentIndex + 1))}><StepForward size={16} /></button>
          <button onClick={() => replay.setCurrentIndex(maxIndex)}><SkipForward size={16} /></button>
          <button onClick={() => { replay.setStatus('paused'); replay.setCurrentIndex(Math.min(250, maxIndex)); }}><RotateCcw size={16} /></button>
          <select value={replay.speed} onChange={(event) => replay.setSpeed(Number(event.target.value))}>{SPEEDS.map((speed) => <option key={speed} value={speed}>{speed}x</option>)}</select>
          <input className="scrubber" type="range" min={0} max={maxIndex} value={replay.currentIndex} onChange={(event) => replay.setCurrentIndex(Number(event.target.value))} />
          <span className="index-pill">{replay.currentIndex} / {maxIndex}</span>
        </div>
      </section>

      <main className="terminal-grid">
        <aside className="left-panel panel">
          <ResearchTree payload={data ?? null} selectedId={selection.objectId} />
        </aside>

        <section className="center-panel panel">
          {isLoading && <div className="loading-state">Loading visual contract…</div>}
          {error && <div className="error-state">{String(error)}</div>}
          {data && (
            <MarketChart
              payload={data as ReplayPayload}
              currentIndex={replay.currentIndex}
              layers={visibleLayers}
              selectedObjectId={selection.objectId}
              hoveredObjectId={hoveredObjectId}
              onSelectObject={selectChartObject}
              onHoverObject={(objectId) => setHoveredObjectId(objectId)}
            />
          )}
        </section>

        <aside className="right-panel panel">
          <Inspector payload={data ?? null} selection={selection} selectedRecord={selectedRecord} currentIndex={replay.currentIndex} />
          <div className="layer-box">
            <div className="panel-title"><Layers3 size={15} /> Layers</div>
            {(data?.layers ?? []).map((layer) => (
              <label className="layer-row" key={layer.layer_id}>
                <input
                  type="checkbox"
                  checked={layerVisibility[layer.layer_id] ?? layer.visible}
                  onChange={(event) => setLayerVisibility((current) => ({ ...current, [layer.layer_id]: event.target.checked }))}
                />
                <span>{layer.label}</span>
                <em>{layer.objects.length}</em>
              </label>
            ))}
          </div>
        </aside>
      </main>

      <footer className="bottom-panel panel">
        <div className="table-tabs">
          {(data?.tables ?? []).map((table) => (
            <button key={table.table_id} className={table.table_id === activeTableId ? 'active' : ''} onClick={() => setActiveTableId(table.table_id)}>
              {table.label} <span>{table.rows.length}</span>
            </button>
          ))}
        </div>
        {activeTable && <DataTable table={activeTable} selectedRowId={selection.rowId} hoveredRowId={hoveredObjectId} onRowSelect={jumpToObject} onRowHover={hoverRow} />}
      </footer>
    </div>
  );
}

function Stat({ icon, label, value }: { icon: ReactNode; label: string; value: string }) {
  return (
    <div className="stat-card">
      {icon}
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
