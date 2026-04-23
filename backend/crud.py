from sqlalchemy.orm import Session
from models import ChatSession, ChatMessage
from uuid import uuid4

def create_session(db: Session, user_id: str, title: str = "New Conversation"):
    db_session = ChatSession(id=str(uuid4()), user_id=user_id, title=title)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def add_message(db: Session, session_id: str, role: str, content: str, metadata: dict = None):
    msg = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        metadata_=metadata or {}
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_recent_history(db: Session, session_id: str, limit: int = 10):
    """
    Fetch recent chat history and truncate to keep only the last N messages.
    """
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id)\
                 .order_by(ChatMessage.created_at.desc())\
                 .limit(limit).all()
    
    # Reverse to chronological order for the LLM context
    return list(reversed(messages))
