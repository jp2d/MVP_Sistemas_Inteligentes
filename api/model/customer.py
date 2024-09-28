from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    tenure = Column(Integer, nullable=False)
    monthly_charges = Column(Float, nullable=False)
    contract_type = Column(Integer, nullable=False)
    internet_service = Column(Integer, nullable=False)
    total_charges = Column(Float, nullable=False)
    tech_support = Column(Integer, nullable=False)
    churn = Column(Integer, nullable=False)

    def __init__(self,  name: str, age: int, gender: int, tenure: int, monthly_charges: float, contract_type: int, internet_service: int, total_charges: float, tech_support: int, churn: int):
        
        self.name = name
        self.age = age
        self.gender = gender
        self.tenure = tenure
        self.monthly_charges = monthly_charges
        self.contract_type = contract_type
        self.internet_service = internet_service
        self.total_charges = total_charges
        self.tech_support = tech_support
        self.churn = churn