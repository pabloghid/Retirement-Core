from pydantic import BaseModel

class RealValueRequest(BaseModel):
    current_value: float
    years: int