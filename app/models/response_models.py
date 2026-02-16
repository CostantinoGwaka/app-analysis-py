from pydantic import BaseModel
from typing import Dict, Optional


class FinancialAnalysis(BaseModel):
    total_budget: Optional[float] = 0.0
    average_budget: Optional[float] = 0.0
    budget_at_risk: Optional[float] = 0.0
    budget_at_risk_percentage: Optional[float] = 0.0


class ScoreAnalysis(BaseModel):
    total_expected_score: Optional[float] = 0.0
    total_actual_score: Optional[float] = 0.0
    total_score_gap: Optional[float] = 0.0
    score_achievement_rate: Optional[float] = 0.0


class ComplianceDistribution(BaseModel):
    excellent: int = 0
    good: int = 0
    fair: int = 0
    poor: int = 0


class SheetAnalysis(BaseModel):
    total_records: int
    average_compliance: float
    open_findings: int
    closed_findings: int
    high_risk_findings: int
    medium_risk_findings: int
    low_risk_findings: int
    red_flag_count: int
    audit_type_breakdown: Dict[str, int] = {}
    category_breakdown: Dict[str, int] = {}
    financial_analysis: Dict = {}
    score_analysis: Dict = {}
    top_entities: Dict[str, int] = {}
    compliance_distribution: Dict[str, int] = {}
    checklist_breakdown: Dict[str, int] = {}


class SheetResult(BaseModel):
    analysis: Dict
    summary: str
    insights: Optional[Dict] = {}


class AnalysisResponse(BaseModel):
    status: str
    sheets_analyzed: int
    results: Dict[str, SheetResult]
    overall_summary: Optional[Dict] = {}
