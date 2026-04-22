from pydantic import BaseModel

class StatCreate(BaseModel):
    x: float
    y: float
    z: float
