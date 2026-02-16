def generate_summary(sheet_name, analysis):
    if "error" in analysis:
        return f"{sheet_name}: analysis skipped due to missing columns."

    # Basic summary
    summary_parts = [
        f"{sheet_name} Analysis Report:",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📊 Total Records: {analysis['total_records']}",
        f"✅ Average Compliance: {analysis['average_compliance']}%",
        f"🔴 Open Findings: {analysis['open_findings']}",
        f"🟢 Closed Findings: {analysis['closed_findings']}",
    ]

    # Risk breakdown
    summary_parts.append(f"\n🎯 Risk Distribution:")
    summary_parts.append(f"  • High Risk: {analysis['high_risk_findings']}")
    summary_parts.append(
        f"  • Medium Risk: {analysis['medium_risk_findings']}")
    summary_parts.append(f"  • Low Risk: {analysis['low_risk_findings']}")

    # Red flags
    if analysis['red_flag_count'] > 0:
        summary_parts.append(f"\n🚩 Red Flags: {analysis['red_flag_count']}")

    # Compliance distribution
    if analysis.get('compliance_distribution'):
        dist = analysis['compliance_distribution']
        summary_parts.append(f"\n📈 Compliance Distribution:")
        summary_parts.append(
            f"  • Excellent (≥90%): {dist.get('excellent', 0)}")
        summary_parts.append(f"  • Good (75-89%): {dist.get('good', 0)}")
        summary_parts.append(f"  • Fair (50-74%): {dist.get('fair', 0)}")
        summary_parts.append(f"  • Poor (<50%): {dist.get('poor', 0)}")

    # Score analysis
    if analysis.get('score_analysis'):
        score = analysis['score_analysis']
        summary_parts.append(f"\n🎯 Score Analysis:")
        summary_parts.append(
            f"  • Total Expected: {score.get('total_expected_score', 0)}")
        summary_parts.append(
            f"  • Total Actual: {score.get('total_actual_score', 0)}")
        summary_parts.append(
            f"  • Score Gap: {score.get('total_score_gap', 0)}")
        summary_parts.append(
            f"  • Achievement Rate: {score.get('score_achievement_rate', 0)}%")

    # Financial analysis
    if analysis.get('financial_analysis'):
        finance = analysis['financial_analysis']
        summary_parts.append(f"\n💰 Financial Overview:")
        summary_parts.append(
            f"  • Total Budget: TZS {finance.get('total_budget', 0):,.2f}")
        summary_parts.append(
            f"  • Budget at Risk: TZS {finance.get('budget_at_risk', 0):,.2f} ({finance.get('budget_at_risk_percentage', 0)}%)")

    return "\n".join(summary_parts)


def generate_insights(analysis):
    """Generate actionable insights from the analysis"""
    insights = {
        "priority_actions": [],
        "positive_highlights": [],
        "areas_of_concern": [],
        "recommendations": []
    }

    # Priority actions based on risk
    if analysis.get('high_risk_findings', 0) > 0:
        insights["priority_actions"].append(
            f"Immediate attention required: {analysis['high_risk_findings']} high-risk findings need resolution"
        )

    if analysis.get('red_flag_count', 0) > 0:
        insights["priority_actions"].append(
            f"Critical: {analysis['red_flag_count']} red flags identified requiring urgent investigation"
        )

    # Financial concerns
    if analysis.get('financial_analysis'):
        finance = analysis['financial_analysis']
        risk_pct = finance.get('budget_at_risk_percentage', 0)
        if risk_pct > 50:
            insights["areas_of_concern"].append(
                f"High financial risk: {risk_pct}% of budget associated with open findings"
            )

    # Compliance highlights
    avg_compliance = analysis.get('average_compliance', 0)
    if avg_compliance >= 75:
        insights["positive_highlights"].append(
            f"Good overall compliance rate of {avg_compliance}%"
        )
    elif avg_compliance < 50:
        insights["areas_of_concern"].append(
            f"Low average compliance of {avg_compliance}% requires immediate improvement plan"
        )

    # Score achievement
    if analysis.get('score_analysis'):
        achievement = analysis['score_analysis'].get(
            'score_achievement_rate', 0)
        if achievement >= 75:
            insights["positive_highlights"].append(
                f"Strong score achievement rate of {achievement}%"
            )
        elif achievement < 50:
            insights["areas_of_concern"].append(
                f"Low score achievement rate of {achievement}% indicates systemic issues"
            )

    # Recommendations
    open_ratio = 0
    total = analysis.get('total_records', 0)
    if total > 0:
        open_ratio = (analysis.get('open_findings', 0) / total) * 100

    if open_ratio > 70:
        insights["recommendations"].append(
            "Establish dedicated task force to address high volume of open findings"
        )

    if analysis.get('high_risk_findings', 0) > 0:
        insights["recommendations"].append(
            "Prioritize resolution of high-risk findings before proceeding with new initiatives"
        )

    dist = analysis.get('compliance_distribution', {})
    if dist.get('poor', 0) > dist.get('excellent', 0):
        insights["recommendations"].append(
            "Implement comprehensive training program to improve compliance rates"
        )

    return insights


def generate_overall_summary(all_results):
    """Generate an overall summary across all sheets"""
    total_records = 0
    total_open = 0
    total_high_risk = 0
    total_red_flags = 0
    all_compliance = []

    for result in all_results.values():
        analysis = result.get('analysis', {})
        if 'error' not in analysis:
            total_records += analysis.get('total_records', 0)
            total_open += analysis.get('open_findings', 0)
            total_high_risk += analysis.get('high_risk_findings', 0)
            total_red_flags += analysis.get('red_flag_count', 0)
            if analysis.get('average_compliance', 0) > 0:
                all_compliance.append(analysis['average_compliance'])

    overall_compliance = round(
        sum(all_compliance) / len(all_compliance), 2) if all_compliance else 0

    return {
        "total_records_analyzed": total_records,
        "overall_compliance_rate": overall_compliance,
        "total_open_findings": total_open,
        "total_high_risk_findings": total_high_risk,
        "total_red_flags": total_red_flags,
        "sheets_processed": len(all_results)
    }
