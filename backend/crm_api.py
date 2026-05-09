from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import BankClient


router = APIRouter(prefix="/api/crm", tags=["CRM"])

@router.get("/client/{name}")
def get_client_profile(name: str, db: Session = Depends(get_db)):
    """
    Simulated internal CRM API endpoint to fetch client profile from MySQL.
    Agent will use this tool to fetch context before querying RAG.
    """
    client = db.query(BankClient).filter(BankClient.name == name).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found in CRM")
    
    # Return same structure as before for backward compatibility
    return {
        "client_id": f"C{client.id:04d}",
        "name": client.name,
        "age": client.age,
        "gender": client.gender,
        "occupation": client.occupation,
        "risk_level": client.risk_level,
        "total_assets": client.total_assets,
        "insurance_preferences": client.insurance_preferences
    }
