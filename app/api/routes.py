from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.orchestrator import build_agent

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    response: str

@router.post("/query", response_model=QueryResponse)
async def run_agent_query(request: QueryRequest):
    try:
        agent = build_agent()
        result = await agent.ainvoke({"messages": [{"role": "user", "content": request.query}]})
        # extract last message from langgraph response
        last_message = result["messages"][-1].content
        return QueryResponse(query=request.query, response=last_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}