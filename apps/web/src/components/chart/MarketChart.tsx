import { useEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { CandlestickSeries, createChart, type IChartApi, type ISeriesApi, type Time } from 'lightweight-charts';
import type { Candle, OverlayLayer, ReplayPayload, VisualObject } from '../../types/visualization';
import { formatNumber } from '../../utils/format';

interface OverlayRect {
  id: string;
  className: string;
  label?: string | null;
  style: CSSProperties;
  object: VisualObject;
  hitBox: HitBox;
}

interface OverlayPoint {
  id: string;
  className: string;
  label?: string | null;
  style: CSSProperties;
  object: VisualObject;
  hitBox: HitBox;
}

interface HitBox {
  left: number;
  top: number;
  width: number;
  height: number;
}

export function MarketChart({ payload, currentIndex, layers, selectedObjectId, hoveredObjectId, onSelectObject, onHoverObject }: {
  payload: ReplayPayload;
  currentIndex: number;
  layers: OverlayLayer[];
  selectedObjectId: string | null;
  hoveredObjectId: string | null;
  onSelectObject: (objectId: string, kind: string) => void;
  onHoverObject: (objectId: string | null, kind?: string | null) => void;
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const stageRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const initializedDatasetRef = useRef<string | null>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });
  const [viewportVersion, setViewportVersion] = useState(0);

  const visibleCandles = useMemo(() => payload.candles.slice(0, Math.max(0, currentIndex) + 1), [payload.candles, currentIndex]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const chart = createChart(container, {
      layout: {
        background: { color: 'transparent' },
        textColor: '#7f8da3',
      },
      grid: {
        vertLines: { color: 'rgba(134, 150, 180, 0.08)' },
        horzLines: { color: 'rgba(134, 150, 180, 0.08)' },
      },
      rightPriceScale: {
        borderColor: 'rgba(134, 150, 180, 0.16)',
      },
      timeScale: {
        borderColor: 'rgba(134, 150, 180, 0.16)',
        timeVisible: true,
        secondsVisible: false,
        rightOffset: 8,
        barSpacing: 7,
      },
      crosshair: {
        mode: 1,
      },
      handleScroll: {
        mouseWheel: true,
        pressedMouseMove: true,
        horzTouchDrag: true,
        vertTouchDrag: true,
      },
      handleScale: {
        axisPressedMouseMove: true,
        mouseWheel: true,
        pinch: true,
      },
      width: container.clientWidth,
      height: container.clientHeight,
    });

    const series = chart.addSeries(CandlestickSeries, {
      upColor: '#4fd1a5',
      downColor: '#f45b69',
      wickUpColor: '#4fd1a5',
      wickDownColor: '#f45b69',
      borderVisible: false,
    });

    chartRef.current = chart;
    seriesRef.current = series;

    let animationFrame = 0;
    const requestOverlayRefresh = () => {
      if (animationFrame) return;
      animationFrame = window.requestAnimationFrame(() => {
        animationFrame = 0;
        setViewportVersion((value) => value + 1);
      });
    };

    chart.timeScale().subscribeVisibleLogicalRangeChange(requestOverlayRefresh);

    const resizeObserver = new ResizeObserver((entries) => {
      const rect = entries[0]?.contentRect;
      if (!rect) return;
      chart.applyOptions({ width: rect.width, height: rect.height });
      setSize({ width: rect.width, height: rect.height });
      requestOverlayRefresh();
    });
    resizeObserver.observe(container);

    return () => {
      if (animationFrame) window.cancelAnimationFrame(animationFrame);
      chart.timeScale().unsubscribeVisibleLogicalRangeChange(requestOverlayRefresh);
      resizeObserver.disconnect();
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
    };
  }, []);

  useEffect(() => {
    const series = seriesRef.current;
    const chart = chartRef.current;
    if (!series || !chart) return;

    series.setData(visibleCandles.map(toChartCandle));

    if (initializedDatasetRef.current !== payload.dataset.dataset_id) {
      initializedDatasetRef.current = payload.dataset.dataset_id;
      if (visibleCandles.length > 20) {
        chart.timeScale().setVisibleLogicalRange({ from: Math.max(0, visibleCandles.length - 180), to: visibleCandles.length + 8 });
      } else {
        chart.timeScale().fitContent();
      }
    }

    setViewportVersion((value) => value + 1);
  }, [visibleCandles, payload.dataset.dataset_id]);

  const overlays = useMemo(() => buildOverlays({
    layers,
    candles: payload.candles,
    currentIndex,
    chart: chartRef.current,
    series: seriesRef.current,
    selectedObjectId,
    hoveredObjectId,
    size,
  }), [layers, payload.candles, currentIndex, selectedObjectId, hoveredObjectId, size, viewportVersion]);

  const currentCandle = payload.candles[currentIndex];

  function handlePointerMove(event: React.PointerEvent<HTMLDivElement>) {
    const stage = stageRef.current;
    if (!stage) return;
    const bounds = stage.getBoundingClientRect();
    const x = event.clientX - bounds.left;
    const y = event.clientY - bounds.top;
    const hit = hitTestOverlay(overlays, x, y);
    onHoverObject(hit ? getSelectableId(hit.object) : null, hit?.object.kind ?? null);
  }

  function handlePointerLeave() {
    onHoverObject(null, null);
  }

  function handleClick() {
    const hovered = findOverlayBySelectableId(overlays, hoveredObjectId);
    if (hovered) onSelectObject(getSelectableId(hovered.object), hovered.object.kind);
  }

  return (
    <div className="chart-shell">
      <div className="chart-header-line">
        <div>
          <strong>{payload.dataset.symbol} · {payload.dataset.timeframe}</strong>
          <span>{payload.dataset.source} / {payload.dataset.contract_version}</span>
        </div>
        {currentCandle && (
          <div className="ohlc-strip">
            <span>O {formatNumber(currentCandle.open)}</span>
            <span>H {formatNumber(currentCandle.high)}</span>
            <span>L {formatNumber(currentCandle.low)}</span>
            <span>C {formatNumber(currentCandle.close)}</span>
          </div>
        )}
      </div>
      <div ref={stageRef} className="chart-stage" onPointerMove={handlePointerMove} onPointerLeave={handlePointerLeave} onClick={handleClick}>
        <div ref={containerRef} className="chart-canvas" />
        <div className="chart-overlay" aria-hidden="true">
          {overlays.rects.map((rect) => (
            <div key={rect.id} className={rect.className} style={rect.style} title={rect.label ?? rect.id}>
              {rect.label && <span>{rect.label}</span>}
            </div>
          ))}
          {overlays.points.map((point) => (
            <div key={point.id} className={point.className} style={point.style} title={point.label ?? point.id}>
              {point.label && <span>{point.label}</span>}
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
    if (!layer.visible) continue;
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

  const endIndex = Math.min(Number(rawEnd), currentIndex);
  const start = candles[Math.max(0, Number(startIndex))];
  const end = candles[Math.max(0, endIndex)];
  if (!start || !end) return null;

  const left = chart.timeScale().timeToCoordinate(toChartTime(start.time));
  const right = chart.timeScale().timeToCoordinate(toChartTime(end.time));
  if (left === null || right === null) return null;

  let top = 30;
  let bottom = 30;
  if (object.lower !== null && object.lower !== undefined && object.upper !== null && object.upper !== undefined) {
    const upperY = series.priceToCoordinate(Number(object.upper));
    const lowerY = series.priceToCoordinate(Number(object.lower));
    if (upperY !== null && lowerY !== null) {
      top = Math.min(upperY, lowerY);
      bottom = Math.max(upperY, lowerY);
    }
  } else {
    top = 24;
    bottom = 9999;
  }

  const hitBox = {
    left: Math.min(left, right),
    top,
    width: Math.max(3, Math.abs(right - left)),
    height: Math.max(5, bottom - top),
  };

  const className = [
    'overlay-rect',
    object.kind,
    layerId.replace(/[:]/g, '-'),
    selected ? 'selected' : '',
    hovered ? 'hovered' : '',
  ].join(' ');

  return {
    id: object.id,
    object,
    className,
    label: object.kind === 'event_window' ? undefined : object.label,
    hitBox,
    style: {
      left: hitBox.left,
      top: hitBox.top,
      width: hitBox.width,
      height: hitBox.height,
    },
  };
}

function pointForObject(object: VisualObject, candles: Candle[], chart: IChartApi, series: ISeriesApi<'Candlestick'>, layerId: string, selected: boolean, hovered: boolean): OverlayPoint | null {
  const index = object.index ?? (object.time ? candles.find((candle) => candle.time === object.time)?.index : null);
  if (index === null || index === undefined) return null;
  const candle = candles[Number(index)];
  if (!candle) return null;
  const x = chart.timeScale().timeToCoordinate(toChartTime(candle.time));
  const y = object.price === null || object.price === undefined ? null : series.priceToCoordinate(Number(object.price));
  if (x === null || y === null) return null;

  const className = [
    'overlay-point',
    object.kind,
    object.shape ?? '',
    layerId.replace(/[:]/g, '-'),
    selected ? 'selected' : '',
    hovered ? 'hovered' : '',
  ].join(' ');

  const hitBox = {
    left: x - 14,
    top: y - 14,
    width: object.kind === 'label' ? Math.max(66, String(object.label ?? '').length * 7 + 18) : 28,
    height: object.kind === 'label' ? 28 : 28,
  };

  return {
    id: object.id,
    object,
    className,
    label: object.label,
    hitBox,
    style: {
      left: x,
      top: y,
    },
  };
}

function hitTestOverlay(overlays: { rects: OverlayRect[]; points: OverlayPoint[] }, x: number, y: number): OverlayRect | OverlayPoint | null {
  const pointHit = [...overlays.points].reverse().find((point) => isInside(point.hitBox, x, y));
  if (pointHit) return pointHit;

  const rectHits = overlays.rects.filter((rect) => isInside(rect.hitBox, x, y));
  if (!rectHits.length) return null;

  return rectHits.sort((a, b) => {
    const priorityA = rectPriority(a.object.kind);
    const priorityB = rectPriority(b.object.kind);
    if (priorityA !== priorityB) return priorityA - priorityB;
    return a.hitBox.width * a.hitBox.height - b.hitBox.width * b.hitBox.height;
  })[0];
}

function findOverlayBySelectableId(overlays: { rects: OverlayRect[]; points: OverlayPoint[] }, objectId: string | null): OverlayRect | OverlayPoint | null {
  if (!objectId) return null;
  return [...overlays.points, ...overlays.rects].find((overlay) => getSelectableId(overlay.object) === objectId || overlay.object.id === objectId) ?? null;
}

function isInside(box: HitBox, x: number, y: number): boolean {
  return x >= box.left && x <= box.left + box.width && y >= box.top && y <= box.top + box.height;
}

function rectPriority(kind: string): number {
  if (kind === 'zone') return 0;
  if (kind === 'segment') return 1;
  if (kind === 'event_window') return 2;
  return 3;
}

function getSelectableId(object: VisualObject): string {
  const ref = object.metadata?.selection_ref as Record<string, unknown> | undefined;
  return String(ref?.object_id ?? object.id);
}

function toChartCandle(candle: Candle) {
  return {
    time: toChartTime(candle.time),
    open: candle.open,
    high: candle.high,
    low: candle.low,
    close: candle.close,
  };
}

function toChartTime(value: string): Time {
  return Math.floor(new Date(value).getTime() / 1000) as Time;
}
