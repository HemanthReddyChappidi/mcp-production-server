from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MetricPoint(BaseModel):
    machine_id: str
    metric_name: str
    value: float
    unit: str
    recorded_at: datetime

class RealtimeMetricResult(BaseModel):
    success: bool
    machine_id: str
    metric_name: str
    latest_value: float
    unit: str
    timestamp: datetime

class HistoricalTrendResult(BaseModel):
    success: bool
    machine_id: str
    metric_name: str
    from_time: datetime
    to_time: datetime
    data_points: List[MetricPoint]
    average: float
    min_value: float
    max_value: float

class AlertResult(BaseModel):
    success: bool
    alerts_triggered: int
    alerts: List[dict]
    checked_at: datetime
