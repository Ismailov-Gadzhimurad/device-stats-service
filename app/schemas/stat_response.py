from pydantic import BaseModel


class StatResponse(BaseModel):
    device_id: str
    min: float
    max: float
    count: int
    sum: float
    median: float
