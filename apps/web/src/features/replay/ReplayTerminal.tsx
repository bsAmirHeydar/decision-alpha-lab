import { useEffect, useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchCachedDatasets, fetchM0001Visualization, fetchMarketData, runM0001RandomBaseline } from '../../api/client';
import { MarketChart } from '../../components/chart/MarketChart';
import type { TableView, VisualizationPayload } from '../../types/visualization';

const TIMEFRAMES = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M10', 'M12', 'M15', 'M20', 'M30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H8', 'H12', 'D1', 'W1', 'MN1'];
const DEFAULT_SYMBOLS = ['GOLD', '#US30', 'EURUSD', 'GBPUSD', 'USDJPY', 'BTCUSD', 'ETHUSD'];

export function ReplayTerminal() {
  const [symbol, setSymbol] = useState('GOLD');
  const [timeframe, setTimeframe] = useState('M15');
  const [bars, setBars] = useState(5000);
  const [source, setSource] = useState<'cache' | 'mt5'>('cache');
  const [L, setL] = useState(5);
  const [zoneRatio, setZoneRatio] = useState(0.9);
  const [exitGap, setExitGap] = useState(6);
  const [mode, setMode] = useState('hunt');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [selectedObjectId, setSelectedObjectId] = useState<string | null>(null);
  const [hoveredObjectId, setHoveredObjectId] = useState<string | null>(null);
  const [activeTableId, setActiveTableId] = useState('actual_events');
  const [fetchStatus, setFetchStatus] = useState<string | null>(null);
  const [randomPayload, setRandomPayload] = useState<VisualizationPayload | null>(null);
  const [randomBusy, setRandomBusy] = useState(false);
  const [sampleSize, setSampleSize] = useState<number | ''>('');

  const datasetsQuery = useQuery({
    queryKey: ['cached-datasets'],
    queryFn: fetchCachedDatasets,
  });

  const query = useQuery({
    queryKey: ['m0001-visualization', symbol, timeframe, bars, L, zoneRatio, exitGap, mode],
    queryFn: () => fetchM0001Visualization({ symbol, timeframe, L, zoneRatio, exitGap, mode, maxBars: bars }),
  });

  const basePayload = query.data;
  const payload = useMemo(() => mergePayloads(basePayload, randomPayload), [basePayload, randomPayload]);
  const maxIndex = Math.max(0, (payload?.candles.length ?? 1) - 1);

  const cachedSymbols = useMemo(() => {
    const symbols = new Set(DEFAULT_SYMBOLS);
    for (const dataset of datasetsQuery.data ?? []) symbols.add(dataset.symbol);
    return [...symbols].sort();
  }, [datasetsQuery.data]);

  const cachedTimeframesForSymbol = useMemo(() => {
    const frames = new Set(TIMEFRAMES);
    for (const dataset of datasetsQuery.data ?? []) {
      if (dataset.symbol === symbol) frames.add(dataset.timeframe);
    }
    return [...frames].sort(timeframeSort);
  }, [datasetsQuery.data, symbol]);

  useEffect(() => {
    setRandomPayload(null);
    setSelectedObjectId(null);
    setHoveredObjectId(null);
    setActiveTableId('actual_events');
  }, [symbol, timeframe, bars, L, zoneRatio, exitGap, mode]);

  // Important: after a dataset/metric reload, show the whole loaded history by default.
  // Before this fix the chart could stay at index 7, so the UI looked like it had only 8 candles.
  useEffect(() => {
    if (!basePayload?.candles.length) return;
    setCurrentIndex(basePayload.candles.length - 1);
    setPlaying(false);
  }, [basePayload?.dataset.symbol, basePayload?.dataset.timeframe, basePayload?.dataset.bars, basePayload?.dataset.parameters]);

  useEffect(() => {
    if (!playing || !payload) return undefined;
    const timer = window.setInterval(() => {
      setCurrentIndex((value) => Math.min(maxIndex, value + 1));
    }, 80);
    return () => window.clearInterval(timer);
  }, [playing, payload, maxIndex]);

  async function handleFetchData() {
    setFetchStatus('Fetching / verifying market data...');
    try {
      const result = await fetchMarketData({
        symbol,
        timeframe,
        bars,
        source,
        resetCache: source === 'mt5',
      });
      setFetchStatus(`${result.message} rows=${result.rows.toLocaleString()} ${result.start ?? ''} → ${result.end ?? ''}`);
      setRandomPayload(null);
      await datasetsQuery.refetch();
      await query.refetch();
    } catch (error) {
      setFetchStatus(error instanceof Error ? error.message : String(error));
    }
  }

  async function handleDeepRandom() {
    setRandomBusy(true);
    try {
      const result = await runM0001RandomBaseline({
        symbol,
        timeframe,
        L,
        zoneRatio,
        exitGap,
        mode,
        maxBars: bars,
        sampleSize: typeof sampleSize === 'number' ? sampleSize : null,
      });
      setRandomPayload(result);
      setActiveTableId('random_events');
      setFetchStatus(`Random baseline complete. seed=${String(result.dataset.parameters.seed ?? 'n/a')} events=${String(result.stats.random_events ?? 0)}`);
    } catch (error) {
      setFetchStatus(error instanceof Error ? error.message : String(error));
    } finally {
      setRandomBusy(false);
    }
  }

  function selectObject(id: string | null) {
    setSelectedObjectId(id);
    const foundTable = payload?.tables.find((table) => table.rows.some((row) => objectIdForRow(row) === id));
    if (foundTable) setActiveTableId(foundTable.table_id);
    const row = payload?.tables.flatMap((table) => table.rows).find((item) => objectIdForRow(item) === id);
    const idx = Number(row?.hunt_index ?? row?.entry_index ?? row?.index);
    if (Number.isFinite(idx)) setCurrentIndex(Math.max(0, Math.min(maxIndex, idx)));
  }

  function applyDatasetSelection(value: string) {
    if (!value) return;
    const [nextSymbol, nextTimeframe] = value.split('|');
    if (nextSymbol) setSymbol(nextSymbol);
    if (nextTimeframe) setTimeframe(nextTimeframe);
  }

  return (
    <div className="replay-terminal">
      <section className="replay-header panel">
        <div>
          <span className="section-kicker">Data Terminal / M0001</span>
          <h2>Fetch, visualize, replay, compare.</h2>
          <p className="muted-line">
            Select a cached dataset or fetch from MT5, then inspect actual structural-node RTV against a random baseline.
          </p>
        </div>

        <div className="control-strip data-controls">
          <label>
            Cached Dataset
            <select value={`${symbol}|${timeframe}`} onChange={(event) => applyDatasetSelection(event.target.value)}>
              {datasetsQuery.data?.map((dataset) => (
                <option key={`${dataset.symbol}|${dataset.timeframe}|${dataset.path}`} value={`${dataset.symbol}|${dataset.timeframe}`}>
                  {dataset.symbol} / {dataset.timeframe} / {dataset.rows.toLocaleString()} bars
                </option>
              ))}
              {!datasetsQuery.data?.length && <option value={`${symbol}|${timeframe}`}>{symbol} / {timeframe}</option>}
            </select>
          </label>

          <label>
            Symbol
            <select value={symbol} onChange={(event) => setSymbol(event.target.value)}>
              {cachedSymbols.map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
          </label>

          <label>
            Timeframe
            <select value={timeframe} onChange={(event) => setTimeframe(event.target.value)}>
              {cachedTimeframesForSymbol.map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
          </label>

          <label>
            Bars
            <input type="number" min={100} max={100000} step={100} value={bars} onChange={(event) => setBars(Number(event.target.value))} />
          </label>

          <label>
            Source
            <select value={source} onChange={(event) => setSource(event.target.value as 'cache' | 'mt5')}>
              <option value="cache">cache</option>
              <option value="mt5">MT5</option>
            </select>
          </label>

          <button onClick={handleFetchData}>Fetch Data</button>
          <button className="secondary" onClick={() => query.refetch()}>Reload Visual</button>
        </div>
      </section>

      <section className="replay-header panel compact-panel">
        <div className="control-strip metric-controls">
          <label>L<input type="number" value={L} onChange={(event) => setL(Number(event.target.value))} /></label>
          <label>ZR<input type="number" step="0.05" value={zoneRatio} onChange={(event) => setZoneRatio(Number(event.target.value))} /></label>
          <label>EG<input type="number" value={exitGap} onChange={(event) => setExitGap(Number(event.target.value))} /></label>
          <label>Mode<select value={mode} onChange={(event) => setMode(event.target.value)}><option>hunt</option><option>touch</option></select></label>
          <label>Random N<input type="number" placeholder="same as nodes" value={sampleSize} onChange={(event) => setSampleSize(event.target.value ? Number(event.target.value) : '')} /></label>
          <button onClick={handleDeepRandom} disabled={!basePayload || randomBusy}>{randomBusy ? 'Running...' : 'Deep Random Test'}</button>
          {randomPayload && <button className="secondary" onClick={() => setRandomPayload(null)}>Clear Random</button>}
        </div>
        {fetchStatus && <div className="fetch-status">{fetchStatus}</div>}
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
            {randomPayload?.comparison ? Object.entries(randomPayload.comparison).map(([key, value]) => (
              <div className="stat-card compact compare" key={key}>
                <span>{key}</span>
                <strong>{formatValue(value)}</strong>
              </div>
            )) : null}
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
              <button onClick={() => setCurrentIndex(0)}>Start</button>
              <button onClick={() => setCurrentIndex(maxIndex)}>End</button>
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

function mergePayloads(base?: VisualizationPayload, random?: VisualizationPayload | null): VisualizationPayload | undefined {
  if (!base) return undefined;
  if (!random) return base;
  return {
    ...base,
    overlay_layers: [...base.overlay_layers, ...random.overlay_layers],
    tables: [...base.tables, ...random.tables],
    stats: { ...base.stats, ...random.stats },
    validation_flags: [...base.validation_flags, ...random.validation_flags],
    timeline: [...base.timeline, ...random.timeline],
  };
}

function objectIdForRow(row: Record<string, unknown>) {
  if (typeof row.id === 'string') return row.id;
  if (row.row_index !== undefined && String(row.id ?? '').startsWith('RANDOM')) return `RANDOM-EVENT-${row.row_index}`;
  if (row.row_index !== undefined) return `M0001-EVENT-${row.row_index}`;
  if (row.node_id !== undefined && String(row.id ?? '').startsWith('RANDOM')) return `RANDOM-NODE-${row.node_id}`;
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

function timeframeSort(a: string, b: string) {
  return timeframeRank(a) - timeframeRank(b);
}

function timeframeRank(value: string) {
  const match = value.match(/^([A-Z]+)(\d+)?$/);
  if (!match) return 999999;
  const unit = match[1];
  const amount = Number(match[2] ?? 1);
  const unitRank: Record<string, number> = { M: 1, H: 60, D: 1440, W: 10080, MN: 43200 };
  return (unitRank[unit] ?? 999999) * amount;
}
