from typing import List, Optional
from datetime import datetime
from statistics import median
from app.repositories.stat_repository import StatRepository
from app.models.device_stat import DeviceStat
from app.schemas.stat_response import StatResponse

class StatService:
    def __init__(self, repository: StatRepository):
        self._repository = repository

    def add_statistic(self, device_id: str, x: float, y: float, z: float) -> None:
        self._repository.save(device_id, x, y, z)

    def get_analysis(
            self,
            device_id: str,
            from_ts: Optional[int] = None,
            to_ts: Optional[int] = None
    ) -> StatResponse:

        from_date = self._convert_timestamp(from_ts)
        to_date = self._convert_timestamp(to_ts)

        entities = self._repository.find_by_device_id(device_id, from_date, to_date)

        if not entities:
            raise ValueError(f"No data found for device: {device_id}")

        values = self._extract_all_values(entities)

        return StatResponse(
            device_id=device_id,
            min_value=min(values),
            max_value=max(values),
            count=len(values),
            sum_value=sum(values),
            median_value=median(values)
        )

    def _convert_timestamp(self, timestamp: Optional[int]) -> Optional[datetime]:
        if timestamp is None:
            return None
        return datetime.fromtimestamp(timestamp)

    def _extract_all_values(self, entities: List[DeviceStat]) -> List[float]:
        values = []
        for entity in entities:
            values.extend(entity.get_values_list())
        return values