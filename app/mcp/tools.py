from datetime import datetime, timedelta
from sqlalchemy import select, func
from app.db.connection import AsyncSessionLocal
from app.db.models import ProductionMetric, AlertLog
from app.mcp.schemas import RealtimeMetricResult, HistoricalTrendResult, AlertResult
from app.config import settings

# --- Tool 1: Real-time metric query ---
async def get_realtime_metric(machine_id: str, metric_name: str) -> dict:
    """
    Fetch the latest value of a metric for a given machine.
    Use for: current state queries like 'what is cpu usage on machine_01 right now?'
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(ProductionMetric)
            .where(ProductionMetric.machine_id == machine_id)
            .where(ProductionMetric.metric_name == metric_name)
            .order_by(ProductionMetric.recorded_at.desc())
            .limit(1)
        )
        row = result.scalar_one_or_none()
        if not row:
            return {"success": False, "error": f"No data for {machine_id}/{metric_name}"}

        return RealtimeMetricResult(
            success=True,
            machine_id=row.machine_id,
            metric_name=row.metric_name,
            latest_value=row.value,
            unit=row.unit,
            timestamp=row.recorded_at,
        ).model_dump(mode="json")


# --- Tool 2: Historical trend analysis ---
async def get_historical_trend(
    machine_id: str,
    metric_name: str,
    hours_back: int = 24
) -> dict:
    """
    Retrieve metric history for a time range and compute stats.
    Use for: trend questions like 'show cpu usage for machine_02 over last 12 hours'
    """
    async with AsyncSessionLocal() as db:
        cutoff = datetime.utcnow() - timedelta(hours=hours_back)
        result = await db.execute(
            select(ProductionMetric)
            .where(ProductionMetric.machine_id == machine_id)
            .where(ProductionMetric.metric_name == metric_name)
            .where(ProductionMetric.recorded_at >= cutoff)
            .order_by(ProductionMetric.recorded_at.asc())
        )
        rows = result.scalars().all()
        if not rows:
            return {"success": False, "error": "No historical data found"}

        values = [r.value for r in rows]
        return HistoricalTrendResult(
            success=True,
            machine_id=machine_id,
            metric_name=metric_name,
            from_time=cutoff,
            to_time=datetime.utcnow(),
            data_points=[
                {"machine_id": r.machine_id, "metric_name": r.metric_name,
                 "value": r.value, "unit": r.unit, "recorded_at": r.recorded_at}
                for r in rows
            ],
            average=round(sum(values) / len(values), 2),
            min_value=min(values),
            max_value=max(values),
        ).model_dump(mode="json")


# --- Tool 3: Threshold-based alert generation ---
async def check_and_generate_alerts(machine_id: str) -> dict:
    """
    Check latest metrics against thresholds and log alerts if breached.
    Use for: 'are there any alerts on machine_03?' or 'check machine_01 health'
    """
    async with AsyncSessionLocal() as db:
        thresholds = {
            "cpu_usage": settings.alert_threshold_cpu,
            "error_rate": settings.alert_threshold_error_rate,
        }
        alerts = []
        now = datetime.utcnow()

        for metric_name, threshold in thresholds.items():
            result = await db.execute(
                select(ProductionMetric)
                .where(ProductionMetric.machine_id == machine_id)
                .where(ProductionMetric.metric_name == metric_name)
                .order_by(ProductionMetric.recorded_at.desc())
                .limit(1)
            )
            row = result.scalar_one_or_none()
            if row and row.value > threshold:
                severity = "critical" if row.value > threshold * 1.2 else "warning"
                alert = AlertLog(
                    machine_id=machine_id,
                    metric_name=metric_name,
                    triggered_value=row.value,
                    threshold=threshold,
                    severity=severity,
                    created_at=now,
                )
                db.add(alert)
                alerts.append({
                    "metric": metric_name,
                    "value": row.value,
                    "threshold": threshold,
                    "severity": severity,
                })

        await db.commit()
        return AlertResult(
            success=True,
            alerts_triggered=len(alerts),
            alerts=alerts,
            checked_at=now,
        ).model_dump(mode="json")
