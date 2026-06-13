from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from app.mcp.tools import get_realtime_metric, get_historical_trend, check_and_generate_alerts
from app.agents.context import build_system_context
from app.config import settings

def build_agent():
    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=settings.anthropic_api_key,
        temperature=0,
    )

    tools = [
        StructuredTool.from_function(
            coroutine=get_realtime_metric,
            name="get_realtime_metric",
            description="Fetch the latest value of a production metric for a machine.",
        ),
        StructuredTool.from_function(
            coroutine=get_historical_trend,
            name="get_historical_trend",
            description="Get historical metric data and stats for a time window.",
        ),
        StructuredTool.from_function(
            coroutine=check_and_generate_alerts,
            name="check_and_generate_alerts",
            description="Check metrics against thresholds and generate alerts.",
        ),
    ]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=build_system_context(),
    )
    return agent