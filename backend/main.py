from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import crm_api
import crud
from database import engine, Base, get_db
from agent import run_agent
import json
import re

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Knowledge Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crm_api.router)

class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    message: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to AI Knowledge Copilot API"}

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Fetch recent history
    history_objs = crud.get_recent_history(db, request.session_id)
    
    # 2. Format history for LangChain (simple role/content mapping)
    chat_history = []
    for h in history_objs:
        chat_history.append((h.role, h.content))
    
    # 3. Add user message to DB
    crud.add_message(db, request.session_id, "user", request.message)
    
    # 4. Run Agent
    try:
        raw_output = run_agent(request.message, chat_history)
        
        # 5. Extract metadata from raw output (find ```json ... ```)
        metadata = {}
        json_match = re.search(r'```json\n(.*?)\n```', raw_output, re.DOTALL)
        if json_match:
            try:
                metadata = json.loads(json_match.group(1))
                # Clean output text by removing the JSON block
                clean_output = raw_output.replace(json_match.group(0), "").strip()
            except:
                clean_output = raw_output
        else:
            clean_output = raw_output

        # 6. Save assistant response
        crud.add_message(db, request.session_id, "assistant", clean_output, metadata)
        
        return {
            "role": "assistant",
            "content": clean_output,
            "metadata": metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{user_id}")
def get_user_sessions(user_id: str, db: Session = Depends(get_db)):
    # Simple endpoint to create or get sessions
    session = crud.create_session(db, user_id)
    return session
