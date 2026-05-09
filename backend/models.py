from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = 'chat_session'
    
    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete")

class ChatMessage(Base):
    __tablename__ = 'chat_message'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(50), ForeignKey('chat_session.id'), index=True)
    role = Column(String(20)) # user, assistant, system, tool
    content = Column(Text)
    metadata_ = Column("metadata", JSON, default={}) # Note: renamed to metadata_ to avoid conflict with Base.metadata if any, but in SQLAlchemy column name 'metadata' is fine.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")

class BankClient(Base):
    __tablename__ = 'bank_clients'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True, unique=True)
    age = Column(Integer)
    gender = Column(String(20))
    occupation = Column(String(100))
    risk_level = Column(String(50)) # e.g., Conservative, Aggressive
    total_assets = Column(Integer) # In some currency units
    insurance_preferences = Column(Text) # JSON or Text description
    created_at = Column(DateTime, default=datetime.utcnow)

