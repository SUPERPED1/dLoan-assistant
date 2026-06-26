from pydantic import BaseModel
from typing import Optional, List, Dict

class InputFormat(BaseModel):
    applicant_id:str
    name:str
    age:int
    employment_type: str
    monthly_income: int
    monthly_debt: int
    requested_loan_amount: int
    credit_history: str
    duration: int
    collateral: str
    documents: list[str]
    notes: str

class Financials(BaseModel):
    monthly_payment: Optional[int] = None
    debt_to_income_ratio: Optional[int] = None
    future_debt_to_income_ratio: Optional[int] = None
    age_finish: Optional[int] = None


class RiskScore(BaseModel):
    total_score: int
    definition: str

class APIResponse(BaseModel):
    applicant_data: dict
    status: str

    recommendation: Optional[str] = None
    reason: Optional[List[str]] = None

    missing_fields: Optional[List[str]] = None
    missing_documents: Optional[List] = None

    financials: Optional[Financials] = None
    risk: Optional[List[str]] = None

    explanation: Optional[str] = None
    risk_score: Optional[RiskScore] = None