from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TTSRequest(Base):
    __tablename__ = "tts_requests"
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    voice_id = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    audio_path = Column(String(255))
    user_id = Column(String(50), nullable=False

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(50), nullable=False)
    response_audio_path = Column(String(255))
