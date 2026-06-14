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

export function MarketChart({ payload, currentIndex, selectedObjectId, hoveredObjectId, onSelectObject, onHoverObject }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });
  const [projectionTick, setProjectionTick] = useState(0);
  const [layerVisibility, setLayerVisibility] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(payload.overlay_layers.map((layer) => [layer.layer_id, layer.default_visible])),
  );

  const visibleCandles = useMemo(() => payload.candles.slice(0, Math.max(0, currentIndex) + 1), [payload.candles, currentIndex]);

  useEffect(() => {
    setLayerVisibility(Object.fromEntries(payload.overlay_layers.map((layer) => [layer.layer_id, layer.default_visible])));
  }, [payload]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const chart = createChart(container, {
      layout: {
        background: { color: '#03050a' },
        textColor: '#6e7d94',
        fontFamily: 'Inter, ui-sans-serif, system-ui',
      },
      grid: {
        vertLines: { color: 'rgba(63, 78, 104, 0.12)' },
        horzLines: { color: 'rgba(63, 78, 104, 0.12)' },
      },
      crosshair: {
        mode: 1,
        vertLine: { color: 'rgba(97, 255, 234, 0.35)' },
        horzLine: { color: 'rgba(97, 255, 234, 0.35)' },
      },
      rightPriceScale: {
        borderColor: 'rgba(140, 160, 190, 0.18)',
      },
      timeScale: {
        borderColor: 'rgba(140, 160, 190, 0.18)',
        timeVisible: true,
        secondsVisible: false,
      },
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
    });

    chartRef.current = chart;
    seriesRef.current = series;

    const resizeObserver = new ResizeObserver(() => {
      chart.applyOptions({ width: container.clientWidth, height: container.clientHeight });
      setSize({ width: container.clientWidth, height: container.clientHeight });
      setProjectionTick((value) => value + 1);
    });
    resizeObserver.observe(container);
    setSize({ width: container.clientWidth, height: container.clientHeight });

    const bump = () => setProjectionTick((value) => value + 1);
    chart.timeScale().subscribeVisibleLogicalRangeChange(bump);

    return () => {
      chart.timeScale().unsubscribeVisibleLogicalRangeChange(bump);
      resizeObserver.disconnect();
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
    };
  }, []);

  useEffect(() => {
    const series = seriesRef.current;
    if (!series) return;
    series.setData(visibleCandles.map((candle) => ({
      time: candle.time as Time,
      open: candle.open,
      high: candle.high,
      low: candle.low,
      close: candle.close,
    })));
    setProjectionTick((value) => value + 1);
  }, [visibleCandles]);

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
  }), [activeLayers, payload.candles, currentIndex, selectedObjectId, hoveredObjectId, size, projectionTick]);

  function handleMouseMove(event: React.MouseEvent<HTMLDivElement>) {
    const stage = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - stage.left;
    const y = event.clientY - stage.top;
    const hit = findHit(x, y, overlays.rects, overlays.points);
    onHoverObject(hit?.selectableId ?? null);
  }

  return (
    <div className="market-chart-layout">
      <div className="chart-layer-controls">
        {payload.overlay_layers.map((layer) => (
          <label key={layer.layer_id}>
            <input
              type="checkbox"
              checked={layerVisibility[layer.layer_id] !== false}
              onChange={(event) => setLayerVisibility((current) => ({ ...current, [layer.layer_id]: event.target.checked }))}
            />
            {layer.label}
          </label>
        ))}
      </div>

      <div
        className="chart-stage"
        onMouseMove={handleMouseMove}
        onMouseLeave={() => onHoverObject(null)}
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
        </div>
      </div>
    </div>
  );
}

function buildOverlays({ layers, candles, currentIndex, chart, series, selectedObjectId, hoveredObjectId, size }: {
  layers: OverlayLayer[];
  candles: Candle[];
  currentIndex: number;
  chart: IChartApi | null;
  series: ISeriesApi<'Candlestick'> | null;
  selectedObjectId: string | null;
  hoveredObjectId: string | null;
  size: { width: number; height: number };
}): { rects: OverlayRect[]; points: OverlayPoint[] } {
  if (!chart || !series || !size.width || !size.height) return { rects: [], points: [] };

  const rects: OverlayRect[] = [];
  const points: OverlayPoint[] = [];

  for (const layer of layers) {
    for (const object of layer.objects) {
      const selectableId = getSelectableId(object);
      const selected = selectedObjectId === selectableId || selectedObjectId === object.id;
      const hovered = hoveredObjectId === selectableId || hoveredObjectId === object.id;
      if (object.kind === 'zone' || object.kind === 'event_window' || object.kind === 'segment') {
        const rect = rectForObject(object, candles, currentIndex, chart, series, layer.layer_id, selected, hovered);
        if (rect) rects.push(rect);
      } else if (object.kind === 'marker' || object.kind === 'label') {
        const point = pointForObject(object, candles, chart, series, layer.layer_id, selected, hovered);
        if (point) points.push(point);
      }
    }
  }

  return { rects, points };
}

function rectForObject(object: VisualObject, candles: Candle[], currentIndex: number, chart: IChartApi, series: ISeriesApi<'Candlestick'>, layerId: string, selected: boolean, hovered: boolean): OverlayRect | null {
  const startIndex = object.start_index ?? object.entry_index;
  const rawEnd = object.end_index ?? object.exit_index ?? startIndex;
  if (startIndex === null || startIndex === undefined || rawEnd === null || rawEnd === undefined) return null;
  if (Number(startIndex) > currentIndex) return null;

  const endIndex = Math.min(Number(rawEnd), currentIndex);
  const startCandle = candles[Number(startIndex)];
  const endCandle = candles[endIndex];
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

function pointForObject(object: VisualObject, candles: Candle[], chart: IChartApi, series: ISeriesApi<'Candlestick'>, layerId: string, selected: boolean, hovered: boolean): OverlayPoint | null {
  const index = object.index ?? (object.time ? candles.find((candle) => candle.time === object.time)?.index : null);
  if (index === null || index === undefined) return null;
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
    object.shape ?? '',
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

function getSelectableId(object: VisualObject) {
  const payload = object.payload ?? {};
  if (typeof payload.id === 'string') return payload.id;
  if (typeof payload.row_index === 'number') return `M0001-EVENT-${payload.row_index}`;
  if (typeof payload.node_id === 'number') return `NODE-${payload.node_id}`;
  if (object.id.includes('-ZONE')) return object.id.replace('-ZONE', '');
  if (object.id.includes('-WINDOW')) return object.id.replace('-WINDOW', '');
  if (object.id.includes('-LABEL')) return object.id.replace('-LABEL', '');
  if (object.id.includes('-HUNT')) return object.id.replace('-HUNT', '');
  return object.id;
}

function findHit(x: number, y: number, rects: OverlayRect[], points: OverlayPoint[]) {
  for (const point of [...points].reverse()) {
    const left = Number(point.style.left ?? 0);
    const top = Number(point.style.top ?? 0);
    if (Math.abs(x - left) <= 20 && Math.abs(y - top) <= 20) return point;
  }
  for (const rect of [...rects].reverse()) {
    const left = Number(rect.style.left ?? 0);
    const top = Number(rect.style.top ?? 0);
    const width = Number(rect.style.width ?? 0);
    const height = Number(rect.style.height ?? 0);
    if (x >= left && x <= left + width && y >= top && y <= top + height) return rect;
  }
  return null;
}
