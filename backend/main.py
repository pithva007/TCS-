import os
import json
import asyncio
from datetime import datetime
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
from contextlib import asynccontextmanager

load_dotenv()

from services import data_ingester, data_watcher, rag_engine, failover_llm, guardrails, analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initial data ingestion
    data_ingester.ingest_all()
    # Start watchdog
    data_watcher.start_watcher()
    yield
    # Stop watchdog
    data_watcher.stop_watcher()

app = FastAPI(title="NirmaAI College FAQ Chatbot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/api/chat")
async def chat(req: ChatRequest):
    # Guardrails Check
    guard = guardrails.check_input(req.message)
    if not guard["is_safe"]:
        raise HTTPException(status_code=400, detail=guard["rejection_reason"])
        
    context_chunks, prompt, sources = rag_engine.query_rag(guard["sanitized_query"])
    llm_res = await failover_llm.call_llm(prompt)
    
    safe_answer = guardrails.verify_output(llm_res["answer"], context_chunks)
    
    analytics.log_query(
        question=req.message,
        answer=safe_answer,
        tier_used=llm_res["tier_used"],
        response_time_ms=llm_res["response_time_ms"]
    )
    
    return {
        "answer": safe_answer,
        "sources": sources,
        "tier_used": llm_res["tier_used"],
        "confidence": 0.95
    }

@app.get("/api/health")
async def health():
    stats = data_ingester.get_stats()
    data_dir = os.getenv("DATA_DIR", "/Users/jaimin/FAQ CHATBOT/files/")
    files = [f for f in os.listdir(data_dir) if f.endswith(".json")] if os.path.exists(data_dir) else []
    
    return {
        "status": "ok",
        "data_files": len(files),
        "vectors_count": stats.get("vectors_count", 0),
        "last_ingestion": datetime.now().isoformat()
    }

@app.get("/api/analytics/summary")
async def get_analytics_summary():
    return analytics.get_summary()

@app.get("/api/campus/buildings")
async def get_campus_buildings():
    data_dir = os.getenv("DATA_DIR", "/Users/jaimin/FAQ CHATBOT/files/")
    buildings = []

    # 1. Load buildings from campus_map.json
    campus_file = os.path.join(data_dir, "campus_map.json")
    if os.path.exists(campus_file):
        with open(campus_file, 'r') as f:
            data = json.load(f)
            for b in data.get("buildings", []):
                buildings.append({
                    "id": b.get("id", ""),
                    "name": b.get("name", ""),
                    "category": b.get("category", ""),
                    "description": b.get("description", ""),
                    "facilities": b.get("facilities", []),
                    "location": {
                        "lat": b.get("latitude", 0),
                        "lng": b.get("longitude", 0)
                    }
                })

    # 2. Merge/override with real GPS data from nirma_university_gps_navigation.json
    gps_file = os.path.join(data_dir, "nirma_university_gps_navigation.json")
    if os.path.exists(gps_file):
        with open(gps_file, 'r') as f:
            gps_data = json.load(f)
            existing_ids = {b["id"] for b in buildings}
            for b in gps_data.get("buildings", []):
                bid = b.get("id", "")
                entry = {
                    "id": bid,
                    "name": b.get("name", ""),
                    "category": b.get("type", "academic").lower().replace(" ", "_"),
                    "description": b.get("notes", f"{b.get('name', '')} at Nirma University"),
                    "facilities": [],
                    "location": {
                        "lat": b.get("latitude", 0),
                        "lng": b.get("longitude", 0)
                    }
                }
                if b.get("website"):
                    entry["description"] += f" Website: {b['website']}"
                if b.get("phone"):
                    entry["description"] += f" Phone: {b['phone']}"
                if b.get("hours"):
                    hours_str = ", ".join(f"{k}: {v}" for k, v in b["hours"].items())
                    entry["description"] += f" Hours: {hours_str}"

                if bid not in existing_ids:
                    buildings.append(entry)
                    existing_ids.add(bid)

    return {"buildings": buildings}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            req_data = json.loads(data)
            message = req_data.get("message", "")
            
            guard = guardrails.check_input(message)
            if not guard["is_safe"]:
                await websocket.send_json({"chunk": f"Error: {guard['rejection_reason']}", "done": True, "sources": []})
                continue
                
            context_chunks, prompt, sources = rag_engine.query_rag(guard["sanitized_query"])
            
            async for chunk in failover_llm.stream_llm(prompt):
                await websocket.send_json({"chunk": chunk, "done": False, "sources": sources})
                
            await websocket.send_json({"chunk": "", "done": True, "sources": sources})
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
