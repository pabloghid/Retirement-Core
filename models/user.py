import datetime
from models import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(140))
    email = Column(String(255), unique=True)
    age = Column(Integer)
    risk_profile = Column(String(50))  # e.g., 'conservative', 'moderate', 'aggressive'
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, name: str, email: str, age: int, risk_profile: str):
        """Cria um Usuário.
        
        Arguments:
            name: Nome do usuário.
            email: Email do usuário.
            age: Idade do usuário.
            risk_profile: Perfil de risco do usuário.
        """
        
        self.name = name
        self.email = email
        self.age = age
        self.risk_profile = risk_profile

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "risk_profile": self.risk_profile,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', age={self.age}, risk_profile='{self.risk_profile}')>"

