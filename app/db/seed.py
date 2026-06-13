import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, ProductionMetric

DATABASE_URL = "sqlite+aiosqlite:///./production.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

MACHINES = ["machine_01", "machine_02", "machine_03"]
METRICS = [
    ("cpu_usage", "%"),
    ("error_rate", "%"),
    ("throughput", "req/s"),
    ("response_time", "ms"),
]

async def seed():
    # Create tables first
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

    async with AsyncSessionLocal() as session:
        now = datetime.utcnow()
        records = []
        for i in range(500):
            ts = now - timedelta(minutes=i * 5)
            for machine in MACHINES:
                for metric, unit in METRICS:
                    if metric in ("cpu_usage", "error_rate"):
                        val = random.uniform(10, 95)
                    else:
                        val = random.uniform(50, 500)
                    records.append(ProductionMetric(
                        machine_id=machine,
                        metric_name=metric,
                        value=round(val, 2),
                        unit=unit,
                        recorded_at=ts,
                    ))

        session.add_all(records)
        await session.commit()
        print(f"Seeded {len(records)} records.")

if __name__ == "__main__":
    asyncio.run(seed())