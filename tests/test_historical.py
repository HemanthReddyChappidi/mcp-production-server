import pytest
from app.mcp.tools import get_historical_trend

@pytest.mark.asyncio
async def test_historical_trend_returns_stats():
    result = await get_historical_trend("machine_01", "cpu_usage", hours_back=48)
    assert result["success"] is True
    assert "average" in result
    assert len(result["data_points"]) > 0
