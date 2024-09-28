from pydantic import BaseModel
from typing import Optional, List
from model.customer import Customer
import json
import numpy as np

class CustomerSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    name: str
    age: int
    gender: int
    tenure: int
    monthly_charges: float
    contract_type: int
    internet_service: int
    total_charges: float
    tech_support: int

class CustomerViewSchema(BaseModel):
    """Define como um cliente será retornado
    """
    id: int
    name: str
    age: int
    gender: int
    tenure: int
    monthly_charges: float
    contract_type: int
    internet_service: int
    total_charges: float
    tech_support: int
    churn: int

class CustomerBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do cliente.
    """
    name: str

class ListaCustomersSchema(BaseModel):
    """Define como uma lista de clientes será representada
    """
    customers: List[CustomerSchema]

class CustomerDelSchema(BaseModel):
    """Define como um cliente para deleção será representado
    """
    name: str

# Apresenta apenas os dados de um cliente    
def apresenta_customer(customer: Customer):
    """ Retorna uma representação do cliente seguindo o schema definido em
        CustomerViewSchema.
    """
    return {
        "id": customer.id,
        "name": customer.name,
        "age": customer.age,
        "gender": customer.gender,
        "tenure": customer.tenure,
        "monthly_charges": customer.monthly_charges,
        "contract_type": customer.contract_type,
        "internet_service": customer.internet_service,
        "total_charges": customer.total_charges,
        "tech_support": customer.tech_support,
        "churn": customer.churn
    }

# Apresenta uma lista de clientes
def apresenta_customers(customers: List[Customer]):
    """ Retorna uma representação dos clientes seguindo o schema definido em
        CustomerViewSchema.
    """
    result = []
    for customer in customers:
        result.append({
            "id": customer.id,
            "name": customer.name,
            "age": customer.age,
            "gender": customer.gender,
            "tenure": customer.tenure,
            "monthly_charges": customer.monthly_charges,
            "contract_type": customer.contract_type,
            "internet_service": customer.internet_service,
            "total_charges": customer.total_charges,
            "tech_support": customer.tech_support,
            "churn": customer.churn
        })

    return {"customers": result}
