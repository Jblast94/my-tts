from fastapi import FastAPI, HTTPException, Depends, Header, WebSocket, WebSocketDisconnect
from fastapi.security import APIKeyHeader
from redis import Redis
  # type: ignore
from sqlalchemy import create_engine
  # type: ignore
from sqlalchemy.orm import sessionmaker, Session
  # type: ignore
import os
from models import Base, TTSRequest
from models import ChatMessage
from tts_service import TTSService
from typing import List
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TTS Knowledge API")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis setup
redis_client = Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))

# Security
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY", "your-secret-key")
api_key_header = APIKeyHeader(name=API_KEY_NAME)

# Initialize TTS service
tts_service = TTSService()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_api_key(api_key: str = Header(..., name=API_KEY_NAME)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403)
    return api_key

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/tts/generate")
async def generate_tts(
    text: str,
    voice_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    # Check cache
    cache_key = f"tts:{voice_id}:{hash(text)}"
    if cached := redis_client.get(cache_key):
        return {"audio_path": cached.decode()}
    
    # Create DB record
    request = TTSRequest(
        text=text,
        voice_id=voice_id,
        user_id=api_key
    )
    db.add(request)
    db.commit()
    
    # Generate TTS
    audio_path = await tts_service.generate(text, voice_id)
    if not audio_path:
        raise HTTPException(status_code=400, detail="Invalid voice_id")
    
    # Update cache and DB
    redis_client.set(cache_key, audio_path, ex=3600)
    request.audio_path = audio_path
    request.status = "completed"
    db.commit()
    
    return {"audio_path": audio_path}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_audio_chunk(self, websocket: WebSocket, chunk: bytes):
        await websocket.send_bytes(chunk)

manager = ConnectionManager()

@app.websocket("/ws/tts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("text")
            voice_id = data.get("voice_id", "orpheus")
            
            # Stream TTS chunks
            async for chunk in tts_service.stream_generate(text, voice_id):
                await manager.send_audio_chunk(websocket, chunk)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

@app.post("/chat/tts")
async def chat_tts(
    message: str,
    session_id: str,
    voice_id: str = "orpheus",
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    # Store chat message
    chat_msg = ChatMessage(
        session_id=session_id,
        message=message,
        user_id=api_key
    )
    db.add(chat_msg)
    db.commit()
    
    return await generate_tts(message, voice_id, db, api_key)
