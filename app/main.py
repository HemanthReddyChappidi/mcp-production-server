from fastapi import FastAPI
from app.api.routes import router
from app.db.connection import engine
from app.db.models import Base

app = FastAPI(title="MCP Production Server")
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
