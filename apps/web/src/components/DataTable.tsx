import { useEffect, useRef } from 'react';
import type { TableSpec } from '../types/visualization';
import { formatNumber, formatTime } from '../utils/format';

export function DataTable({ table, selectedRowId, hoveredRowId, onRowSelect, onRowHover }: {
  table: TableSpec;
  selectedRowId: string | null;
  hoveredRowId: string | null;
  onRowSelect: (row: Record<string, unknown>) => void;
  onRowHover: (row: Record<string, unknown> | null) => void;
}) {
  const bodyRef = useRef<HTMLTableSectionElement | null>(null);

  useEffect(() => {
    if (!selectedRowId) return;
    const selector = `[data-row-id="${cssEscape(selectedRowId)}"]`;
    const row = bodyRef.current?.querySelector<HTMLTableRowElement>(selector);
    row?.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }, [selectedRowId, table.table_id]);

  return (
    <div className="data-table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {table.columns.map((column) => <th key={column.key}>{column.label}</th>)}
          </tr>
        </thead>
        <tbody ref={bodyRef} onMouseLeave={() => onRowHover(null)}>
          {table.rows.map((row) => {
            const rowId = getRowId(table, row);
            return (
              <tr
                key={rowId}
                data-row-id={rowId}
                className={[selectedRowId === rowId ? 'selected' : '', hoveredRowId === rowId ? 'hovered' : ''].join(' ')}
                onClick={() => onRowSelect(row)}
                onMouseEnter={() => onRowHover(row)}
              >
                {table.columns.map((column) => <td key={column.key}>{formatCell(row[column.key], column.type)}</td>)}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function getRowId(table: TableSpec, row: Record<string, unknown>): string {
  return String(row[table.primary_key] ?? row.event_id ?? row.node_object_id ?? '');
}

function cssEscape(value: string): string {
  if ('CSS' in window && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
  return value.replace(/["\\]/g, '\\$&');
}

function formatCell(value: unknown, type: string): string {
  if (type === 'number') return formatNumber(value, 4);
  if (type === 'integer') return formatNumber(value, 0);
  if (String(value).includes?.('T')) return formatTime(value);
  if (value === true) return 'true';
  if (value === false) return 'false';
  return value === null || value === undefined ? '—' : String(value);
}
