from pydantic import BaseModel
from datetime import date



class SalesReturnsDay(BaseModel):
    period: str
    sales: float
    returns: float
    remaind: float





class SalesReturnsTable(BaseModel):
    pass