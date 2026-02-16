def generate_summary(sheet_name, analysis):
    if "error" in analysis:
        return f"{sheet_name}: analysis skipped due to missing columns."

    return (
        f"{sheet_name} has {analysis['total_records']} audit checks. "
        f"Average compliance is {analysis['average_compliance']}%. "
        f"There are {analysis['high_risk_findings']} high-risk findings."
    )
