import pandas as pd
import math


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

    df["Compliance %"] = pd.to_numeric(df["Compliance %"], errors="coerce")
    df["Score Gap"] = pd.to_numeric(df["Score Gap"], errors="coerce")

    df = df.dropna(subset=["Compliance %"])

    total_records = int(len(df))

    avg = df["Compliance %"].mean()
    avg_compliance = round(float(avg), 2) if not math.isnan(avg) else 0.0

    open_findings = int(
        (df["Status"].astype(str).str.upper() == "OPEN").sum()
    )

    high_risk = df[
        (df["Compliance %"] < 50) &
        (df["Score Gap"] > 0)
    ]

    return {
        "total_records": total_records,
        "average_compliance": avg_compliance,
        "open_findings": open_findings,
        "high_risk_findings": int(len(high_risk))
    }
