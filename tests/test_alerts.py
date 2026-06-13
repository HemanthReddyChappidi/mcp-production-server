import pytest
from app.mcp.tools import check_and_generate_alerts

@pytest.mark.asyncio
async def test_alert_check_runs():
    result = await check_and_generate_alerts("machine_01")
    assert result["success"] is True
    assert "alerts_triggered" in result
