import pytest
from app.mcp.tools import get_realtime_metric

@pytest.mark.asyncio
async def test_realtime_metric_returns_data():
    result = await get_realtime_metric("machine_01", "cpu_usage")
    assert result["success"] is True
    assert "latest_value" in result
    assert isinstance(result["latest_value"], float)

@pytest.mark.asyncio
async def test_realtime_metric_missing():
    result = await get_realtime_metric("machine_99", "fake_metric")
    assert result["success"] is False
