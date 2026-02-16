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


def analyze_by_pe_name(df):
    """Analyze findings grouped by PE Name"""
    if "PE Name" not in df.columns:
        return {}

    pe_analysis = {}

    for pe_name, group in df.groupby("PE Name"):
        if pd.isna(pe_name) or str(pe_name).strip() == "":
            continue

        pe_name_str = str(pe_name).strip()

        # Calculate metrics for this PE
        total_findings = len(group)
        open_findings = int(
            (group["Status"].astype(str).str.upper() == "OPEN").sum())
        closed_findings = int(
            (group["Status"].astype(str).str.upper() == "CLOSED").sum())

        # Compliance
        valid_compliance = group[group["Compliance %"].notna()]
        avg_compliance = round(float(valid_compliance["Compliance %"].mean()), 2) if len(
            valid_compliance) > 0 else 0.0

        # Budget
        budget_total = 0.0
        if "Estimated Budget" in group.columns:
            budget_data = group[group["Estimated Budget"].notna()]
            budget_total = float(budget_data["Estimated Budget"].sum()) if len(
                budget_data) > 0 else 0.0

        # Risk
        high_risk = int(
            len(group[(group["Compliance %"] < 50) & (group["Score Gap"] > 0)]))

        # Red flags
        red_flags = 0
        if "Red Flag" in group.columns:
            red_flags = int((group["Red Flag"].astype(
                str).str.upper() == "YES").sum())

        # PE Category
        pe_category = "N/A"
        if "PE Category" in group.columns and len(group) > 0:
            pe_category = str(group["PE Category"].iloc[0])

        pe_analysis[pe_name_str] = {
            "total_findings": total_findings,
            "open_findings": open_findings,
            "closed_findings": closed_findings,
            "average_compliance": avg_compliance,
            "total_budget": round(budget_total, 2),
            "high_risk_findings": high_risk,
            "red_flags": red_flags,
            "pe_category": pe_category
        }

    return pe_analysis


def analyze_by_checklist(df):
    """Analyze findings grouped by Checklist Title"""
    if "Checklist Title" not in df.columns:
        return {}

    checklist_analysis = {}

    for checklist, group in df.groupby("Checklist Title"):
        if pd.isna(checklist) or str(checklist).strip() == "":
            continue

        checklist_str = str(checklist).strip()

        total_findings = len(group)
        open_findings = int(
            (group["Status"].astype(str).str.upper() == "OPEN").sum())
        closed_findings = int(
            (group["Status"].astype(str).str.upper() == "CLOSED").sum())

        # Compliance
        valid_compliance = group[group["Compliance %"].notna()]
        avg_compliance = round(float(valid_compliance["Compliance %"].mean()), 2) if len(
            valid_compliance) > 0 else 0.0

        # Score gap
        score_gap_total = 0.0
        if "Score Gap" in group.columns:
            gap_data = group[group["Score Gap"].notna()]
            score_gap_total = float(gap_data["Score Gap"].sum()) if len(
                gap_data) > 0 else 0.0

        # Audit Type
        audit_type = "N/A"
        if "Audit Type" in group.columns and len(group) > 0:
            audit_type = str(group["Audit Type"].iloc[0])

        checklist_analysis[checklist_str] = {
            "total_findings": total_findings,
            "open_findings": open_findings,
            "closed_findings": closed_findings,
            "average_compliance": avg_compliance,
            "total_score_gap": round(score_gap_total, 2),
            "audit_type": audit_type
        }

    return checklist_analysis


def analyze_by_entity(df):
    """Analyze findings grouped by Entity Name and Entity Number combination"""
    entity_analysis = {}

    # Check if we have entity columns
    has_entity_name = "Entity Name" in df.columns
    has_entity_number = "Entity Number" in df.columns

    if not has_entity_name and not has_entity_number:
        return {}

    # Create a combined entity key
    df_copy = df.copy()

    if has_entity_name and has_entity_number:
        df_copy["Entity_Key"] = df_copy["Entity Name"].astype(
            str) + " (" + df_copy["Entity Number"].astype(str) + ")"
    elif has_entity_name:
        df_copy["Entity_Key"] = df_copy["Entity Name"].astype(str)
    else:
        df_copy["Entity_Key"] = df_copy["Entity Number"].astype(str)

    for entity_key, group in df_copy.groupby("Entity_Key"):
        if pd.isna(entity_key) or str(entity_key).strip() in ["", "nan", "nan (nan)"]:
            continue

        entity_key_str = str(entity_key).strip()

        total_findings = len(group)
        open_findings = int(
            (group["Status"].astype(str).str.upper() == "OPEN").sum())
        closed_findings = int(
            (group["Status"].astype(str).str.upper() == "CLOSED").sum())

        # Budget
        budget_total = 0.0
        budget_open = 0.0
        if "Estimated Budget" in group.columns:
            budget_data = group[group["Estimated Budget"].notna()]
            budget_total = float(budget_data["Estimated Budget"].sum()) if len(
                budget_data) > 0 else 0.0

            open_budget_data = budget_data[budget_data["Status"].astype(
                str).str.upper() == "OPEN"]
            budget_open = float(open_budget_data["Estimated Budget"].sum()) if len(
                open_budget_data) > 0 else 0.0

        # Compliance
        valid_compliance = group[group["Compliance %"].notna()]
        avg_compliance = round(float(valid_compliance["Compliance %"].mean()), 2) if len(
            valid_compliance) > 0 else 0.0

        # Risk
        high_risk = int(
            len(group[(group["Compliance %"] < 50) & (group["Score Gap"] > 0)]))
        medium_risk = int(len(group[(group["Compliance %"] >= 50) & (
            group["Compliance %"] < 75) & (group["Score Gap"] > 0)]))
        low_risk = int(
            len(group[(group["Compliance %"] >= 75) & (group["Score Gap"] > 0)]))

        entity_analysis[entity_key_str] = {
            "total_findings": total_findings,
            "open_findings": open_findings,
            "closed_findings": closed_findings,
            "average_compliance": avg_compliance,
            "total_budget": round(budget_total, 2),
            "budget_at_risk": round(budget_open, 2),
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk
        }

    return entity_analysis


def analyze_status_details(df):
    """Detailed analysis of OPEN vs CLOSED findings"""
    status_analysis = {
        "OPEN": {},
        "CLOSED": {}
    }

    for status in ["OPEN", "CLOSED"]:
        status_df = df[df["Status"].astype(str).str.upper() == status]

        if len(status_df) == 0:
            status_analysis[status] = {
                "count": 0,
                "average_compliance": 0.0,
                "total_budget": 0.0,
                "total_score_gap": 0.0,
                "high_risk_count": 0,
                "red_flag_count": 0
            }
            continue

        # Compliance
        valid_compliance = status_df[status_df["Compliance %"].notna()]
        avg_compliance = round(float(valid_compliance["Compliance %"].mean()), 2) if len(
            valid_compliance) > 0 else 0.0

        # Budget
        budget_total = 0.0
        if "Estimated Budget" in status_df.columns:
            budget_data = status_df[status_df["Estimated Budget"].notna()]
            budget_total = float(budget_data["Estimated Budget"].sum()) if len(
                budget_data) > 0 else 0.0

        # Score gap
        score_gap_total = 0.0
        if "Score Gap" in status_df.columns:
            gap_data = status_df[status_df["Score Gap"].notna()]
            score_gap_total = float(gap_data["Score Gap"].sum()) if len(
                gap_data) > 0 else 0.0

        # Risk
        high_risk = int(
            len(status_df[(status_df["Compliance %"] < 50) & (status_df["Score Gap"] > 0)]))

        # Red flags
        red_flags = 0
        if "Red Flag" in status_df.columns:
            red_flags = int((status_df["Red Flag"].astype(
                str).str.upper() == "YES").sum())

        # Audit types
        audit_type_dist = {}
        if "Audit Type" in status_df.columns:
            audit_types = status_df["Audit Type"].value_counts().to_dict()
            audit_type_dist = {str(k): int(v) for k, v in audit_types.items()}

        status_analysis[status] = {
            "count": len(status_df),
            "average_compliance": avg_compliance,
            "total_budget": round(budget_total, 2),
            "total_score_gap": round(score_gap_total, 2),
            "high_risk_count": high_risk,
            "red_flag_count": red_flags,
            "audit_type_distribution": audit_type_dist
        }

    return status_analysis


def analyze_budget_distribution(df):
    """Detailed budget analysis across different dimensions"""
    if "Estimated Budget" not in df.columns:
        return {}

    budget_df = df[df["Estimated Budget"].notna()].copy()

    if len(budget_df) == 0:
        return {}

    total_budget = float(budget_df["Estimated Budget"].sum())

    # Budget ranges
    budget_df["Budget_Range"] = pd.cut(
        budget_df["Estimated Budget"],
        bins=[0, 10000000, 50000000, 100000000, float('inf')],
        labels=["< 10M", "10M - 50M", "50M - 100M", "> 100M"]
    )

    budget_range_dist = budget_df["Budget_Range"].value_counts().to_dict()
    budget_range_analysis = {str(k): int(v)
                             for k, v in budget_range_dist.items()}

    # Top budget items
    top_budget_items = []
    if "Entity Name" in budget_df.columns:
        top_items = budget_df.nlargest(5, "Estimated Budget")
        for _, row in top_items.iterrows():
            entity_name = str(row.get("Entity Name", "N/A"))
            budget = float(row["Estimated Budget"])
            status = str(row.get("Status", "N/A"))
            compliance = float(row.get("Compliance %", 0))

            top_budget_items.append({
                "entity": entity_name,
                "budget": round(budget, 2),
                "status": status,
                "compliance": round(compliance, 2),
                "percentage_of_total": round((budget / total_budget * 100), 2)
            })

    # Budget by PE
    budget_by_pe = {}
    if "PE Name" in budget_df.columns:
        pe_budget = budget_df.groupby("PE Name")["Estimated Budget"].sum(
        ).sort_values(ascending=False).head(10)
        budget_by_pe = {str(k): round(float(v), 2)
                        for k, v in pe_budget.items()}

    return {
        "total_budget": round(total_budget, 2),
        "budget_range_distribution": budget_range_analysis,
        "top_budget_items": top_budget_items,
        "budget_by_pe": budget_by_pe
    }


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

    # === NEW ADVANCED ANALYSIS ===

    # PE Name detailed analysis
    pe_name_analysis = analyze_by_pe_name(df)

    # Checklist detailed analysis
    checklist_detailed_analysis = analyze_by_checklist(df)

    # Entity (Name + Number) analysis
    entity_analysis = analyze_by_entity(df)

    # Status (OPEN vs CLOSED) detailed analysis
    status_detailed_analysis = analyze_status_details(df)

    # Budget distribution analysis
    budget_distribution = analyze_budget_distribution(df)

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
        "checklist_breakdown": checklist_breakdown,

        # Advanced grouped analysis
        "pe_name_analysis": pe_name_analysis,
        "checklist_detailed_analysis": checklist_detailed_analysis,
        "entity_analysis": entity_analysis,
        "status_detailed_analysis": status_detailed_analysis,
        "budget_distribution": budget_distribution
    }
