from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
from schemas import Agent, AgentCreate, UsageLog, UsageSummary
from store import store

app = FastAPI(title="Agent Discovery + Usage Platform")

@app.post("/agents", response_model=Agent, status_code=201)
async def create_agent(agent: AgentCreate):
    return store.add_agent(agent)

@app.get("/agents", response_model=List[Agent])
async def list_agents():
    return store.get_all_agents()

@app.get("/search", response_model=List[Agent])
async def search_agents(q: str = Query(..., min_length=1)):
    return store.search_agents(q)

@app.post("/usage", status_code=202)
async def log_usage(usage: UsageLog):
    try:
        store.log_usage(usage)
        return {"status": "accepted", "message": "Usage logged or already processed (idempotent)"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usage-summary", response_model=Dict[str, int])
async def usage_summary():
    return store.get_usage_summary()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
