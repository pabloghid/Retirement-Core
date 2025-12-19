import datetime
from models import Base
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.types import Enum as SQLEnum
from typing import Union

class UserIncome(Base):
    __tablename__ = 'user_incomes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    amount = Column(Float)
    source = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, user_id: int, amount: float, source: str):
        self.user_id = user_id
        self.amount = amount
        self.source = source

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
class ExpenseCategory(Enum):
    housing = 'housing'
    food = 'food'
    transport = 'transport'
    utilities = 'utilities'
    entertainment = 'entertainment'
    healthcare = 'healthcare'
    other = 'other'

class UserExpense(Base):
    __tablename__ = 'user_expenses'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    amount = Column(Float)
    category = Column(SQLEnum(ExpenseCategory), default=ExpenseCategory.other)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, user_id: int, amount: float, category: Union[ExpenseCategory, str]):
        self.user_id = user_id
        self.amount = amount
        if isinstance(category, str):
            try:
                self.category = ExpenseCategory(category)
            except ValueError:
                try:
                    self.category = ExpenseCategory[category.lower()]
                except Exception:
                    self.category = ExpenseCategory.other
        else:
            self.category = category

    def to_dict(self):
        category_value = self.category.value if isinstance(self.category, ExpenseCategory) else self.category
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": category_value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }