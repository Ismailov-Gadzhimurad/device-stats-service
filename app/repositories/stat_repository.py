from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.device_stat import DeviceStat


class StatRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, device_id: str, x: float, y: float, z: float) -> DeviceStat:
        entity = DeviceStat(device_id=device_id, x=x, y=y, z=z)
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_device_id(
            self,
            device_id: str,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None
    ) -> List[DeviceStat]:
        query = self._session.query(DeviceStat).filter(
            DeviceStat.device_id == device_id
        )

        if from_date:
            query = query.filter(DeviceStat.created_at >= from_date)
        if to_date:
            query = query.filter(DeviceStat.created_at <= to_date)

        return query.all()