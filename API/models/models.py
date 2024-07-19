from typing import Optional
from pydantic import BaseModel

class OrderModel(BaseModel):
    username: str
    instrument: str
    position: float
    price: Optional[float]
    type: str
    action: str

class LimitOrderModel(BaseModel):
    username: str
    instrument: str
    position: float
    price: Optional[float]
    type: str
    action: str
    status: str
