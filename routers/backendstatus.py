from database import app,client
from fastapi import APIRouter

#Create User Route 
router = APIRouter(
    prefix="/BackendStatus",
    tags=['BackendStatus']
)

@router.get("/BackendStatus" , tags=["BackendStatus"])
async def get_status():
    """Get status of server."""
    return {"status": "running"}