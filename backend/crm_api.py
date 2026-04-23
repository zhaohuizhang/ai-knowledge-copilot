from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/crm", tags=["CRM"])

# Mock CRM Database
MOCK_CRM_DATA = {
    "张总": {
        "client_id": "C1001",
        "name": "张总",
        "age": 50,
        "risk_tolerance": "稳健型",
        "family_status": "已婚，一子一女",
        "active_policies": ["金满钵养老年金"]
    },
    "李阿姨": {
        "client_id": "C1002",
        "name": "李阿姨",
        "age": 62,
        "risk_tolerance": "保守型",
        "family_status": "退休",
        "active_policies": []
    }
}

@router.get("/client/{name}")
def get_client_profile(name: str):
    """
    Simulated internal CRM API endpoint to fetch client profile.
    Agent will use this tool to fetch context before querying RAG.
    """
    if name not in MOCK_CRM_DATA:
        raise HTTPException(status_code=404, detail="Client not found in CRM")
    return MOCK_CRM_DATA[name]
