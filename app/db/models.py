from sqlalchemy import Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProductionMetric(Base):
    __tablename__ = "production_metrics"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True, nullable=False)
    metric_name = Column(String, nullable=False)   # cpu_usage, error_rate, throughput
    value = Column(Float, nullable=False)
    unit = Column(String)                           # %, req/s, ms
    recorded_at = Column(DateTime, server_default=func.now(), index=True)

class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True)
    machine_id = Column(String, nullable=False)
    metric_name = Column(String, nullable=False)
    triggered_value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    severity = Column(String)  # warning, critical
    created_at = Column(DateTime, server_default=func.now())