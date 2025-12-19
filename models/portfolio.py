import datetime
from models import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy import Enum

class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_allocation = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, user_id: int, total_allocation: float):
        self.user_id = user_id
        self.total_allocation = total_allocation

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_allocation": self.total_allocation,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
class PortfolioPositions(Base):
    __tablename__ = 'portfolio_positions'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    asset = Column(String(100))
    amount = Column(Float)
    indexer = Column(Enum('IBOV', 'IPCA', 'SELIC', name='indexer_enum'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, portfolio_id: int, asset: str, amount: float):
        self.portfolio_id = portfolio_id
        self.asset = asset
        self.amount = amount

    def to_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "asset": self.asset,
            "amount": self.amount,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
