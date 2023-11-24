"""
This file is using for creating tables in DB

Metal constants:
XAU - Gold
XAG - Silver
PA - Palladium
PL - Platinum
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from src.config.config import DB_URL

Base: Any = declarative_base()
engine = create_engine(DB_URL)


class Price(Base):
    """
    Metal 'prices' table
    """
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    XAU_price_Eur = Column(Float)
    XAG_price_Eur = Column(Float)
    PA_price_Eur = Column(Float)
    PL_price_Eur = Column(Float)
    timestamp = Column(DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'Price (id={self.id!r}, metal={self.metal!r}, price={self.price})'


Base.metadata.create_all(engine)
