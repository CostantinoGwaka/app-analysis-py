import pandas as pd
import math
from datetime import datetime
from collections import defaultdict


def clean_percentage(value):
    """Convert percentage string to float (e.g., '75.5%' -> 75.5)"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Remove % sign and convert to float
        cleaned = str(value).strip().replace('%', '')
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def clean_numeric(value):
    """Convert string numbers to float, handling commas and spaces"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = str(value).strip().replace(',', '')
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def analyze_sheet(df):
    required_columns = [
        "Compliance %",
        "Score Gap",
        "Status",
        "Checklist Title"
    ]

    for col in required_columns:
        if col not in df.columns:
            return {
                "error": f"Missing required column: {col}"
            }

    # Make a copy to avoid modifying original
    df = df.copy()

    # Clean percentage and numeric columns
    df["Compliance %"] = df["Compliance %"].apply(clean_percentage)
    df["Score Gap"] = df["Score Gap"].apply(clean_numeric)

    # Clean other numeric columns if they exist
    if "Expected Score" in df.columns:
        df["Expected Score"] = df["Expected Score"].apply(clean_numeric)
    if "Actual Score" in df.columns:
        df["Actual Score"] = df["Actual Score"].apply(clean_numeric)
    if "Estimated Budget" in df.columns:
        df["Estimated Budget"] = df["Estimated Budget"].apply(clean_numeric)

    # Basic metrics
    total_records = int(len(df))

    # Filter valid compliance records
    valid_compliance_df = df[df["Compliance %"].notna()]

    avg = valid_compliance_df["Compliance %"].mean()
    avg_compliance = round(float(avg), 2) if not math.isnan(avg) else 0.0

    # Status analysis
    open_findings = int(
        (df["Status"].astype(str).str.upper() == "OPEN").sum()
    )
    closed_findings = int(
        (df["Status"].astype(str).str.upper() == "CLOSED").sum()
    )

    # Risk categorization
    high_risk = df[
        (df["Compliance %"] < 50) &
        (df["Score Gap"] > 0)
    ]
    medium_risk = df[
        (df["Compliance %"] >= 50) &
        (df["Compliance %"] < 75) &
        (df["Score Gap"] > 0)
    ]
    low_risk = df[
        (df["Compliance %"] >= 75) &
        (df["Score Gap"] > 0)
    ]

    # Red flag analysis
    red_flag_count = 0
    if "Red Flag" in df.columns:
        red_flag_count = int(
            (df["Red Flag"].astype(str).str.upper() == "YES").sum()
        )

    # Audit type breakdown
    audit_type_breakdown = {}
    if "Audit Type" in df.columns:
        audit_types = df["Audit Type"].value_counts().to_dict()
        audit_type_breakdown = {str(k): int(v) for k, v in audit_types.items()}

    # PE Category breakdown
    category_breakdown = {}
    if "PE Category" in df.columns:
        categories = df["PE Category"].value_counts().to_dict()
        category_breakdown = {str(k): int(v) for k, v in categories.items()}

    # Financial analysis
    financial_analysis = {}
    if "Estimated Budget" in df.columns:
        budget_df = df[df["Estimated Budget"].notna()]
        if len(budget_df) > 0:
            total_budget = budget_df["Estimated Budget"].sum()
            avg_budget = budget_df["Estimated Budget"].mean()

            # Budget at risk (open findings)
            budget_at_risk_df = budget_df[
                budget_df["Status"].astype(str).str.upper() == "OPEN"
            ]
            budget_at_risk = budget_at_risk_df["Estimated Budget"].sum() if len(
                budget_at_risk_df) > 0 else 0

            financial_analysis = {
                "total_budget": round(float(total_budget), 2),
                "average_budget": round(float(avg_budget), 2),
                "budget_at_risk": round(float(budget_at_risk), 2),
                "budget_at_risk_percentage": round(
                    (budget_at_risk / total_budget *
                     100) if total_budget > 0 else 0,
                    2
                )
            }

    # Score analysis
    score_analysis = {}
    if "Expected Score" in df.columns and "Actual Score" in df.columns:
        score_df = df[
            df["Expected Score"].notna() &
            df["Actual Score"].notna()
        ]
        if len(score_df) > 0:
            total_expected = score_df["Expected Score"].sum()
            total_actual = score_df["Actual Score"].sum()
            total_gap = score_df["Score Gap"].sum(
            ) if "Score Gap" in score_df.columns else (total_expected - total_actual)

            score_analysis = {
                "total_expected_score": round(float(total_expected), 2),
                "total_actual_score": round(float(total_actual), 2),
                "total_score_gap": round(float(total_gap), 2),
                "score_achievement_rate": round(
                    (total_actual / total_expected *
                     100) if total_expected > 0 else 0,
                    2
                )
            }

    # Top entities with most findings
    top_entities = {}
    if "Entity Name" in df.columns:
        entity_counts = df["Entity Name"].value_counts().head(10).to_dict()
        top_entities = {str(k): int(v) for k, v in entity_counts.items()}

    # Compliance distribution
    compliance_distribution = {
        "excellent": int(len(df[df["Compliance %"] >= 90])),
        "good": int(len(df[(df["Compliance %"] >= 75) & (df["Compliance %"] < 90)])),
        "fair": int(len(df[(df["Compliance %"] >= 50) & (df["Compliance %"] < 75)])),
        "poor": int(len(df[df["Compliance %"] < 50]))
    }

    # Checklist analysis
    checklist_breakdown = {}
    if "Checklist Title" in df.columns:
        checklist_counts = df["Checklist Title"].value_counts().to_dict()
        checklist_breakdown = {str(k): int(v)
                               for k, v in list(checklist_counts.items())[:10]}

    return {
        "total_records": total_records,
        "average_compliance": avg_compliance,
        "open_findings": open_findings,
        "closed_findings": closed_findings,
        "high_risk_findings": int(len(high_risk)),
        "medium_risk_findings": int(len(medium_risk)),
        "low_risk_findings": int(len(low_risk)),
        "red_flag_count": red_flag_count,
        "audit_type_breakdown": audit_type_breakdown,
        "category_breakdown": category_breakdown,
        "financial_analysis": financial_analysis,
        "score_analysis": score_analysis,
        "top_entities": top_entities,
        "compliance_distribution": compliance_distribution,
        "checklist_breakdown": checklist_breakdown
    }
