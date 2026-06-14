import { useEffect, useMemo, useRef, useState } from 'react';
import { createChart, type IChartApi, type ISeriesApi, type Time } from 'lightweight-charts';
import type { Candle, OverlayLayer, VisualObject, VisualizationPayload } from '../../types/visualization';

interface Props {
  payload: VisualizationPayload;
  currentIndex: number;
  selectedObjectId: string | null;
  hoveredObjectId: string | null;
  onSelectObject: (id: string | null) => void;
  onHoverObject: (id: string | null) => void;
}

interface OverlayRect {
  id: string;
  selectableId: string;
  className: string;
  object: VisualObject;
  style: React.CSSProperties;
}

interface OverlayPoint {
  id: string;
  selectableId: string;
  className: string;
  object: VisualObject;
  label: string | null;
  style: React.CSSProperties;
}

interface CursorState {
  x: number;
  y: number;
  price: number | null;
  time: string | null;
}

interface LogicalRangeLike {
  from: number;
  to: number;
}

interface ViewportIndexRange {
  from: number;
  to: number;
  span: number;
}

const MAX_VISIBLE_RECTS = 420;
const MAX_VISIBLE_LABELS = 150;
const MAX_OVERVIEW_LABELS = 80;
const MAX_DENSE_RECT_SPAN = 1500;

export function MarketChart({ payload, currentIndex, selectedObjectId, hoveredObjectId, onSelectObject, onHoverObject }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const previousDataRef = useRef<{ datasetKey: string; index: number } | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });
  const [projectionTick, setProjectionTick] = useState(0);
  const [visibleLogicalRange, setVisibleLogicalRange] = useState<LogicalRangeLike | null>(null);
  const [cursor, setCursor] = useState<CursorState | null>(null);
  const [layerVisibility, setLayerVisibility] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(payload.overlay_layers.map((layer) => [layer.layer_id, layer.default_visible])),
  );

  const datasetKey = useMemo(() => {
    const first = payload.candles[0]?.time ?? 'none';
    const last = payload.candles[payload.candles.length - 1]?.time ?? 'none';
    return `${payload.dataset.symbol}|${payload.dataset.timeframe}|${payload.candles.length}|${first}|${last}`;
  }, [payload.dataset.symbol, payload.dataset.timeframe, payload.candles]);

  useEffect(() => {
    setLayerVisibility(Object.fromEntries(payload.overlay_layers.map((layer) => [layer.layer_id, layer.default_visible])));
  }, [datasetKey, payload.overlay_layers]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const chart = createChart(container, {
      layout: {
        background: { color: '#03050a' },
        textColor: '#8a98ad',
        fontFamily: 'Inter, ui-sans-serif, system-ui',
      },
      grid: {
        vertLines: { color: 'rgba(63, 78, 104, 0.14)' },
        horzLines: { color: 'rgba(63, 78, 104, 0.14)' },
      },
      crosshair: {
        mode: 1,
        vertLine: { color: 'rgba(97, 255, 234, 0.45)', labelBackgroundColor: '#0a141f' },
        horzLine: { color: 'rgba(97, 255, 234, 0.45)', labelBackgroundColor: '#0a141f' },
      },
      rightPriceScale: {
        borderColor: 'rgba(140, 160, 190, 0.24)',
        visible: true,
        autoScale: true,
      },
      timeScale: {
        borderColor: 'rgba(140, 160, 190, 0.24)',
        timeVisible: true,
        secondsVisible: false,
        rightOffset: 12,
        barSpacing: 6,
        fixLeftEdge: false,
        fixRightEdge: false,
      },
      handleScroll: true,
      handleScale: true,
      width: container.clientWidth,
      height: container.clientHeight,
    });

    const series = chart.addCandlestickSeries({
      upColor: '#38e8c6',
      downColor: '#ff477e',
      borderUpColor: '#70ffdf',
      borderDownColor: '#ff6e99',
      wickUpColor: '#9afbe8',
      wickDownColor: '#ff8caf',
      priceLineVisible: true,
      lastValueVisible: true,
    });

    chartRef.current = chart;
    seriesRef.current = series;

    function refreshProjection() {
      if (animationFrameRef.current !== null) {
        window.cancelAnimationFrame(animationFrameRef.current);
      }
      animationFrameRef.current = window.requestAnimationFrame(() => {
        const range = chart.timeScale().getVisibleLogicalRange();
        setVisibleLogicalRange(range ? { from: Number(range.from), to: Number(range.to) } : null);
        setProjectionTick((value) => value + 1);
      });
    }

    const resizeObserver = new ResizeObserver(() => {
      chart.applyOptions({ width: container.clientWidth, height: container.clientHeight });
      setSize({ width: container.clientWidth, height: container.clientHeight });
      refreshProjection();
    });
    resizeObserver.observe(container);
    setSize({ width: container.clientWidth, height: container.clientHeight });

    chart.timeScale().subscribeVisibleLogicalRangeChange(refreshProjection);
    chart.subscribeCrosshairMove((param) => {
      if (!param.point || param.time === undefined) {
        setCursor(null);
        return;
      }
      const price = series.coordinateToPrice(param.point.y);
      setCursor({
        x: param.point.x,
        y: param.point.y,
        price: typeof price === 'number' ? price : null,
        time: formatCrosshairTime(param.time as Time),
      });
    });

    refreshProjection();

    return () => {
      chart.timeScale().unsubscribeVisibleLogicalRangeChange(refreshProjection);
      resizeObserver.disconnect();
      if (animationFrameRef.current !== null) window.cancelAnimationFrame(animationFrameRef.current);
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
    };
  }, []);

  useEffect(() => {
    const series = seriesRef.current;
    const chart = chartRef.current;
    if (!series) return;

    const clampedIndex = Math.max(0, Math.min(currentIndex, payload.candles.length - 1));
    const previous = previousDataRef.current;
    const shouldReset =
      !previous ||
      previous.datasetKey !== datasetKey ||
      clampedIndex < previous.index ||
      clampedIndex - previous.index > 50;

    if (shouldReset) {
      series.setData(payload.candles.slice(0, clampedIndex + 1).map(toSeriesCandle));
      if (chart && clampedIndex >= payload.candles.length - 1 && payload.candles.length > 20) {
        chart.timeScale().fitContent();
      }
    } else if (clampedIndex > previous.index) {
      for (let i = previous.index + 1; i <= clampedIndex; i += 1) {
        const candle = payload.candles[i];
        if (candle) series.update(toSeriesCandle(candle));
      }
    }

    previousDataRef.current = { datasetKey, index: clampedIndex };
    const range = chart?.timeScale().getVisibleLogicalRange();
    setVisibleLogicalRange(range ? { from: Number(range.from), to: Number(range.to) } : null);
    setProjectionTick((value) => value + 1);
  }, [currentIndex, datasetKey, payload.candles]);

  const activeLayers = useMemo(
    () => payload.overlay_layers.filter((layer) => layerVisibility[layer.layer_id] !== false),
    [payload.overlay_layers, layerVisibility],
  );

  const overlays = useMemo(() => buildOverlays({
    layers: activeLayers,
    candles: payload.candles,
    currentIndex,
    chart: chartRef.current,
    series: seriesRef.current,
    selectedObjectId,
    hoveredObjectId,
    size,
    visibleLogicalRange,
  }), [activeLayers, payload.candles, currentIndex, selectedObjectId, hoveredObjectId, size, visibleLogicalRange, projectionTick]);

  function handleMouseMove(event: React.MouseEvent<HTMLDivElement>) {
    const stage = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - stage.left;
    const y = event.clientY - stage.top;
    const hit = findHit(x, y, overlays.rects, overlays.points);
    onHoverObject(hit?.selectableId ?? null);

    const series = seriesRef.current;
    const chart = chartRef.current;
    const price = series?.coordinateToPrice(y) ?? null;
    const time = chart?.timeScale().coordinateToTime(x);
    setCursor({
      x,
      y,
      price: typeof price === 'number' ? price : null,
      time: time ? formatCrosshairTime(time) : null,
    });
  }

  return (
    <div className="market-chart-layout">
      <div className="chart-layer-controls">
        {payload.overlay_layers.map((layer) => (
          <label key={layer.layer_id} className={layer.layer_id.startsWith('random') ? 'random-control' : ''}>
            <input
              type="checkbox"
              checked={layerVisibility[layer.layer_id] !== false}
              onChange={(event) => setLayerVisibility((current) => ({ ...current, [layer.layer_id]: event.target.checked }))}
            />
            {layer.label}
          </label>
        ))}
        <span className="overlay-budget-note">
          visible overlays: {overlays.rects.length} windows / {overlays.points.length} markers
        </span>
      </div>

      <div
        className="chart-stage"
        onMouseMove={handleMouseMove}
        onMouseLeave={() => {
          onHoverObject(null);
          setCursor(null);
        }}
        onClick={() => {
          const active = hoveredObjectId;
          if (active) onSelectObject(active);
        }}
      >
        <div ref={containerRef} className="chart-container" />
        <div className="chart-overlay" aria-hidden>
          {overlays.rects.map((rect) => (
            <div key={rect.id} className={rect.className} style={rect.style} />
          ))}
          {overlays.points.map((point) => (
            <div key={point.id} className={point.className} style={point.style}>
              {point.label ? <span>{point.label}</span> : null}
            </div>
          ))}
          {cursor && (
            <>
              <div className="chart-cursor-readout">
                <span>time</span><strong>{cursor.time ?? '—'}</strong>
                <span>price</span><strong>{cursor.price === null ? '—' : cursor.price.toLocaleString(undefined, { maximumFractionDigits: 4 })}</strong>
              </div>
              <div className="chart-cursor-price" style={{ top: cursor.y }}>{cursor.price === null ? '—' : cursor.price.toLocaleString(undefined, { maximumFractionDigits: 4 })}</div>
              <div className="chart-cursor-time" style={{ left: cursor.x }}>{cursor.time ?? '—'}</div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function buildOverlays({ layers, candles, currentIndex, chart, series, selectedObjectId, hoveredObjectId, size, visibleLogicalRange }: {
  layers: OverlayLayer[];
  candles: Candle[];
  currentIndex: number;
  chart: IChartApi | null;
  series: ISeriesApi<'Candlestick'> | null;
  selectedObjectId: string | null;
  hoveredObjectId: string | null;
  size: { width: number; height: number };
  visibleLogicalRange: LogicalRangeLike | null;
}): { rects: OverlayRect[]; points: OverlayPoint[] } {
  if (!chart || !series || !size.width || !size.height || !candles.length) return { rects: [], points: [] };

  const viewport = viewportFromLogicalRange(visibleLogicalRange, currentIndex, candles.length);
  const rectCandidates: OverlayRect[] = [];
  const points: OverlayPoint[] = [];
  const labelCandidates: OverlayPoint[] = [];

  for (const layer of layers) {
    for (const object of layer.objects) {
      const selectableId = getSelectableId(object);
      const selected = selectedObjectId === selectableId || selectedObjectId === object.id;
      const hovered = hoveredObjectId === selectableId || hoveredObjectId === object.id;
      const important = selected || hovered;

      if (!objectIntersectsViewport(object, viewport, currentIndex) && !important) {
        continue;
      }

      if (object.kind === 'zone' || object.kind === 'event_window' || object.kind === 'segment') {
        if (viewport.span > MAX_DENSE_RECT_SPAN && !important) {
          continue;
        }
        const rect = rectForObject(object, candles, currentIndex, chart, series, layer.layer_id, selected, hovered, viewport);
        if (rect) rectCandidates.push(rect);
      } else if (object.kind === 'marker' || object.kind === 'label') {
        const point = pointForObject(object, candles, chart, series, layer.layer_id, selected, hovered, currentIndex, viewport);
        if (!point) continue;

        if (object.kind === 'label' && !important) {
          labelCandidates.push(point);
        } else {
          points.push(point);
        }
      }
    }
  }

  const sortedRects = rectCandidates
    .sort((a, b) => priority(a) - priority(b))
    .slice(0, MAX_VISIBLE_RECTS);

  const labelLimit = viewport.span > MAX_DENSE_RECT_SPAN ? MAX_OVERVIEW_LABELS : MAX_VISIBLE_LABELS;
  const sortedLabels = labelCandidates
    .sort((a, b) => objectRtv(b.object) - objectRtv(a.object))
    .slice(0, labelLimit);

  return { rects: sortedRects, points: [...points, ...sortedLabels] };
}

function rectForObject(object: VisualObject, candles: Candle[], currentIndex: number, chart: IChartApi, series: ISeriesApi<'Candlestick'>, layerId: string, selected: boolean, hovered: boolean, viewport: ViewportIndexRange): OverlayRect | null {
  const startIndex = object.start_index ?? object.entry_index;
  const rawEnd = object.end_index ?? object.exit_index ?? startIndex;
  if (startIndex === null || startIndex === undefined || rawEnd === null || rawEnd === undefined) return null;
  if (Number(startIndex) > currentIndex) return null;

  const clippedStart = Math.max(Number(startIndex), viewport.from);
  const clippedEnd = Math.min(Number(rawEnd), currentIndex, viewport.to);
  if (clippedEnd < viewport.from || clippedStart > viewport.to) return null;

  const startCandle = candles[clippedStart];
  const endCandle = candles[clippedEnd];
  if (!startCandle || !endCandle) return null;

  const x1 = chart.timeScale().timeToCoordinate(startCandle.time as Time);
  const x2 = chart.timeScale().timeToCoordinate(endCandle.time as Time);
  const upper = object.upper ?? object.price;
  const lower = object.lower ?? object.price;
  if (x1 === null || x2 === null || upper === null || upper === undefined || lower === null || lower === undefined) return null;

  const y1 = series.priceToCoordinate(Number(upper));
  const y2 = series.priceToCoordinate(Number(lower));
  if (y1 === null || y2 === null) return null;

  const selectableId = getSelectableId(object);
  const left = Math.min(x1, x2);
  const right = Math.max(x1, x2);
  const top = Math.min(y1, y2);
  const bottom = Math.max(y1, y2);
  const className = [
    'overlay-rect',
    object.kind,
    object.object_type ?? '',
    object.baseline_kind ?? '',
    layerId,
    selected ? 'selected' : '',
    hovered ? 'hovered' : '',
  ].filter(Boolean).join(' ');

  return {
    id: object.id,
    selectableId,
    className,
    object,
    style: {
      left,
      top,
      width: Math.max(2, right - left + 6),
      height: Math.max(2, bottom - top),
    },
  };
}

function pointForObject(object: VisualObject, candles: Candle[], chart: IChartApi, series: ISeriesApi<'Candlestick'>, layerId: string, selected: boolean, hovered: boolean, currentIndex: number, viewport: ViewportIndexRange): OverlayPoint | null {
  const index = object.index ?? midpointFromPayload(object) ?? (object.time ? candles.find((candle) => candle.time === object.time)?.index : null);
  if (index === null || index === undefined || Number(index) > currentIndex) return null;
  if ((Number(index) < viewport.from || Number(index) > viewport.to) && !selected && !hovered) return null;

  const candle = candles[Number(index)];
  if (!candle) return null;

  const x = chart.timeScale().timeToCoordinate(candle.time as Time);
  const price = object.price ?? object.upper ?? object.lower ?? candle.close;
  const y = series.priceToCoordinate(Number(price));
  if (x === null || y === null) return null;

  const selectableId = getSelectableId(object);
  const className = [
    'overlay-point',
    object.kind,
    object.object_type ?? '',
    object.baseline_kind ?? '',
    object.shape ?? '',
    metricStrengthClass(object),
    layerId,
    selected ? 'selected' : '',
    hovered ? 'hovered' : '',
  ].filter(Boolean).join(' ');

  return {
    id: object.id,
    selectableId,
    className,
    object,
    label: object.label ?? null,
    style: {
      left: x,
      top: y,
    },
  };
}

function toSeriesCandle(candle: Candle) {
  return {
    time: candle.time as Time,
    open: candle.open,
    high: candle.high,
    low: candle.low,
    close: candle.close,
  };
}

function viewportFromLogicalRange(range: LogicalRangeLike | null, currentIndex: number, total: number): ViewportIndexRange {
  if (!range) {
    const from = Math.max(0, currentIndex - 700);
    const to = Math.min(total - 1, currentIndex);
    return { from, to, span: Math.max(1, to - from + 1) };
  }

  const padding = 40;
  const from = Math.max(0, Math.floor(range.from) - padding);
  const to = Math.min(total - 1, Math.ceil(range.to) + padding, currentIndex);
  return { from, to, span: Math.max(1, to - from + 1) };
}

function objectIntersectsViewport(object: VisualObject, viewport: ViewportIndexRange, currentIndex: number) {
  const start = Number(object.start_index ?? object.entry_index ?? object.index ?? midpointFromPayload(object) ?? 0);
  const end = Number(object.end_index ?? object.exit_index ?? object.index ?? midpointFromPayload(object) ?? start);
  const clippedEnd = Math.min(end, currentIndex);
  return clippedEnd >= viewport.from && start <= viewport.to;
}

function midpointFromPayload(object: VisualObject) {
  const payload = object.payload ?? {};
  const start = payload.entry_index ?? payload.start_index;
  const end = payload.exit_index ?? payload.end_index;
  if (typeof start === 'number' && typeof end === 'number') return Math.floor((start + end) / 2);
  return null;
}

function getSelectableId(object: VisualObject) {
  const payload = object.payload ?? {};
  if (typeof payload.id === 'string') return payload.id;
  if (payload.baseline_kind === 'random' && typeof payload.row_index === 'number') return `RANDOM-EVENT-${payload.row_index}`;
  if (typeof payload.row_index === 'number') return `M0001-EVENT-${payload.row_index}`;
  if (payload.baseline_kind === 'random' && typeof payload.node_id === 'number') return `RANDOM-NODE-${payload.node_id}`;
  if (typeof payload.node_id === 'number') return `NODE-${payload.node_id}`;
  for (const suffix of ['-ZONE', '-WINDOW', '-LABEL', '-HUNT']) {
    if (object.id.includes(suffix)) return object.id.replace(suffix, '');
  }
  return object.id;
}

function metricStrengthClass(object: VisualObject) {
  if (object.kind !== 'label') return '';
  const rtv = objectRtv(object);
  if (rtv >= 1.25) return 'rtv-strong';
  if (rtv <= 0.9) return 'rtv-weak';
  return 'rtv-neutral';
}

function objectRtv(object: VisualObject) {
  const payload = object.payload ?? {};
  const value = payload.RTV;
  return typeof value === 'number' && Number.isFinite(value) ? value : 0;
}

function priority(rect: OverlayRect) {
  let value = 1000;
  if (rect.className.includes('selected')) value -= 500;
  if (rect.className.includes('hovered')) value -= 400;
  if (rect.className.includes('event_window')) value -= 80;
  if (rect.className.includes('territory') || rect.className.includes('zone')) value -= 40;
  return value + area(rect) / 100000;
}

function findHit(x: number, y: number, rects: OverlayRect[], points: OverlayPoint[]) {
  for (const point of [...points].reverse()) {
    const left = Number(point.style.left ?? 0);
    const top = Number(point.style.top ?? 0);
    if (Math.abs(x - left) <= 22 && Math.abs(y - top) <= 22) return point;
  }

  const hits = rects.filter((rect) => {
    const left = Number(rect.style.left ?? 0);
    const top = Number(rect.style.top ?? 0);
    const width = Number(rect.style.width ?? 0);
    const height = Number(rect.style.height ?? 0);
    return x >= left && x <= left + width && y >= top && y <= top + height;
  });

  return hits.sort((a, b) => area(a) - area(b))[0] ?? null;
}

function area(rect: OverlayRect) {
  return Number(rect.style.width ?? 0) * Number(rect.style.height ?? 0);
}

function formatCrosshairTime(time: Time): string {
  if (typeof time === 'number') {
    const date = new Date(time * 1000);
    return date.toISOString().replace('T', ' ').slice(0, 16);
  }
  if (typeof time === 'string') return time;
  return `${time.year}-${String(time.month).padStart(2, '0')}-${String(time.day).padStart(2, '0')}`;
}
