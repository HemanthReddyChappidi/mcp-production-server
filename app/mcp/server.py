from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
from app.mcp.tools import get_realtime_metric, get_historical_trend, check_and_generate_alerts
import json

server = Server("production-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_realtime_metric",
            description="Fetch the latest value of a production metric for a machine.",
            inputSchema={
                "type": "object",
                "properties": {
                    "machine_id": {"type": "string", "description": "Machine identifier e.g. machine_01"},
                    "metric_name": {"type": "string", "description": "One of: cpu_usage, error_rate, throughput, response_time"},
                },
                "required": ["machine_id", "metric_name"],
            },
        ),
        Tool(
            name="get_historical_trend",
            description="Get historical metric data and stats for a time window.",
            inputSchema={
                "type": "object",
                "properties": {
                    "machine_id": {"type": "string"},
                    "metric_name": {"type": "string"},
                    "hours_back": {"type": "integer", "default": 24, "description": "How many hours back to query"},
                },
                "required": ["machine_id", "metric_name"],
            },
        ),
        Tool(
            name="check_and_generate_alerts",
            description="Check current metrics against thresholds and generate alerts if any are breached.",
            inputSchema={
                "type": "object",
                "properties": {
                    "machine_id": {"type": "string"},
                },
                "required": ["machine_id"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_realtime_metric":
        result = await get_realtime_metric(**arguments)
    elif name == "get_historical_trend":
        result = await get_historical_trend(**arguments)
    elif name == "check_and_generate_alerts":
        result = await check_and_generate_alerts(**arguments)
    else:
        result = {"error": f"Unknown tool: {name}"}

    return [TextContent(type="text", text=json.dumps(result, default=str))]
