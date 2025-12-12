from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    age: int
    risk_profile: str


