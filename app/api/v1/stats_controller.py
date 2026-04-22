from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.repositories.stat_repository import StatRepository
from app.services.stat_service import StatService
from app.schemas.stat_create import StatCreate
from app.schemas.stat_response import StatResponse

router = APIRouter(prefix="/devices", tags=["stats"])


@router.post("/{device_id}/stats", status_code=201)
def add_stats(
        device_id: str,
        data: StatCreate,
        db: Session = Depends(get_db)
):
    repository = StatRepository(db)
    service = StatService(repository)
    service.add_statistic(device_id, data.x, data.y, data.z)
    return {"status": "ok", "device_id": device_id}


@router.get("/{device_id}/stats", response_model=StatResponse)
def get_stats(
        device_id: str,
        from_ts: Optional[int] = Query(None),
        to_ts: Optional[int] = Query(None),
        db: Session = Depends(get_db)
):
    repository = StatRepository(db)
    service = StatService(repository)

    try:
        result = service.get_analysis(device_id, from_ts, to_ts)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))