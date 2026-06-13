
# MCP Production Server

An MCP (Model Context Protocol) server that exposes structured production data to LLM agents via typed tool definitions. Agents query live metrics, filter by time range, and trigger alerts through natural language.

## Stack
- FastAPI · MCP SDK · LangChain · Claude API · SQLite/PostgreSQL · Docker

## Access Patterns
- Real-time metric queries
- Historical trend analysis  
- Threshold-based alert generation

## Setup
```bash
pip install -r requirements.txt
python -m app.db.seed
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## Example Query
```bash
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the current CPU usage on machine_01?"}'
```

## API
- `POST /api/query` — Natural language agent query
- `GET /api/health` — Health check
- `GET /docs` — Swagger UI
EOF
