from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class DataQuality(BaseModel):
    has_duplicates: bool
    is_sorted: bool
    missing_bars: Optional[int] = None


class DatasetDescriptor(BaseModel):
    dataset_id: str
    source: str
    symbol: str
    timeframe: str
    start_time: Optional[str]
    end_time: Optional[str]
    bars: int
    timezone: str = "broker"
    data_quality: DataQuality
    parameters: Dict[str, Any] = Field(default_factory=dict)
    contract_version: str


class Candle(BaseModel):
    id: str
    index: int
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    spread: Optional[float] = None


class SourceRef(BaseModel):
    object_type: str
    object_id: str
    metric_id: Optional[str] = None
    hypothesis_id: Optional[str] = None
    experiment_id: Optional[str] = None


class VisualObject(BaseModel):
    id: str
    kind: str
    source_ref: SourceRef
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Common optional geometry fields. Keeping one flexible schema makes the
    # visual protocol extensible while still typed at the API boundary.
    time: Optional[str] = None
    index: Optional[int] = None
    price: Optional[float] = None
    start_index: Optional[int] = None
    end_index: Optional[int] = None
    lower: Optional[float] = None
    upper: Optional[float] = None
    entry_index: Optional[int] = None
    exit_index: Optional[int] = None
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    visible_from_index: Optional[int] = None
    complete_from_index: Optional[int] = None
    shape: Optional[str] = None
    label: Optional[str] = None


class OverlayLayer(BaseModel):
    layer_id: str
    label: str
    type: Literal[
        "markers",
        "horizontal_levels",
        "zones",
        "event_windows",
        "segments",
        "labels",
        "series",
        "annotations",
    ]
    visible: bool = True
    z_index: int = 10
    opacity: float = 1.0
    objects: List[VisualObject] = Field(default_factory=list)


class TableColumn(BaseModel):
    key: str
    label: str
    type: str = "string"


class TableSpec(BaseModel):
    table_id: str
    label: str
    primary_key: str
    columns: List[TableColumn]
    rows: List[Dict[str, Any]] = Field(default_factory=list)


class InspectorPayload(BaseModel):
    title: str = "No selection"
    subtitle: Optional[str] = None
    sections: List[Dict[str, Any]] = Field(default_factory=list)


class ReplayPayload(BaseModel):
    dataset: DatasetDescriptor
    candles: List[Candle]
    layers: List[OverlayLayer]
    tables: List[TableSpec]
    selection_map: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    inspector: InspectorPayload = Field(default_factory=InspectorPayload)


class MetricSummary(BaseModel):
    source: str
    symbol: str
    timeframe: str
    bars: int
    L: int
    zone_ratio: float
    exit_gap: int
    consumption_mode: str
    confirmed_nodes: int
    events: int
    mean_RTV: Optional[float]
    median_RTV: Optional[float]
    max_revisit: int
