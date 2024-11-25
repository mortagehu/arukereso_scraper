from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key='product.id')
    price: float
    date: datetime = Field(default_factory = datetime.utcnow)

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: Optional[str] = None
    url: Optional[str] = None

    prices: List[PriceHistory] = Relationship(back_populates="product")

PriceHistory.product = Relationship(back_populates="prices")