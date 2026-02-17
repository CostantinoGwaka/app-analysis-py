import random


def _compliance_verdict(pct):
    """Return a dynamic AI-like sentence describing compliance level"""
    if pct >= 90:
        return random.choice([
            f"Our analysis indicates an outstanding compliance posture at {pct}%, reflecting robust governance and internal controls.",
            f"The data reveals an exceptional compliance rate of {pct}%, demonstrating strong adherence to regulatory requirements.",
            f"At {pct}% compliance, the organization exhibits exemplary regulatory alignment and procedural discipline.",
        ])
    elif pct >= 75:
        return random.choice([
            f"The compliance rate of {pct}% signals a solid foundation, though targeted improvements could elevate performance further.",
            f"A healthy {pct}% compliance rate has been observed—incremental refinements can push this into the excellent range.",
            f"With {pct}% compliance, the framework is performing well, but there remain actionable opportunities for strengthening.",
        ])
    elif pct >= 50:
        return random.choice([
            f"A compliance rate of {pct}% highlights moderate performance with significant room for systematic improvement.",
            f"At {pct}%, compliance performance falls below optimal thresholds—a structured remediation plan is recommended.",
            f"The {pct}% compliance rate warrants attention; without intervention, organizational risk exposure may increase.",
        ])
    else:
        return random.choice([
            f"A critically low compliance rate of {pct}% has been detected, indicating urgent systemic deficiencies requiring immediate escalation.",
            f"At {pct}%, compliance is well below acceptable standards—this represents a high-priority risk area demanding swift corrective action.",
            f"The {pct}% compliance level signals a fundamental breakdown in processes; immediate executive attention and resource allocation are critical.",
        ])


def _risk_narrative(high, medium, low, total):
    """Generate dynamic risk distribution narrative"""
    if total == 0:
        return "No risk data available for analysis."
    high_pct = round(high / total * 100, 1)
    if high_pct > 40:
        return f"⚠️ Risk profile is alarming: {high_pct}% of findings are classified as high risk, signaling deep-rooted governance challenges that demand immediate executive intervention."
    elif high_pct > 20:
        return f"The risk landscape shows {high_pct}% of findings rated high risk—a level that requires focused mitigation strategies and enhanced monitoring."
    elif high > 0:
        return f"Risk distribution is relatively contained with {high_pct}% high-risk items, though vigilance must be maintained to prevent escalation."
    else:
        return "No high-risk findings detected—this reflects effective preventive controls and sound risk management practices."


def _budget_narrative(total_budget, at_risk, at_risk_pct):
    """Generate dynamic budget narrative"""
    if total_budget == 0:
        return "No financial data available."
    if at_risk_pct > 60:
        return f"Financial exposure is critical: TZS {at_risk:,.0f} ({at_risk_pct}%) of the total TZS {total_budget:,.0f} budget remains tied to unresolved findings—immediate fiscal safeguards are essential."
    elif at_risk_pct > 30:
        return f"A notable TZS {at_risk:,.0f} ({at_risk_pct}%) of the TZS {total_budget:,.0f} budget is at risk due to open findings, warranting closer financial oversight."
    elif at_risk > 0:
        return f"Budget exposure is manageable at TZS {at_risk:,.0f} ({at_risk_pct}%) out of TZS {total_budget:,.0f}, indicating effective financial governance."
    else:
        return f"Budget allocation of TZS {total_budget:,.0f} shows no outstanding risk exposure—a strong indicator of fiscal discipline."


def _status_narrative(open_count, closed_count, total):
    """Generate dynamic open/closed narrative"""
    if total == 0:
        return ""
    closure_rate = round(closed_count / total * 100, 1) if total > 0 else 0
    if closure_rate >= 80:
        return f"An impressive {closure_rate}% closure rate demonstrates strong organizational responsiveness and effective follow-through on audit findings."
    elif closure_rate >= 50:
        return f"A {closure_rate}% finding closure rate indicates moderate progress, though {open_count} open findings still require resolution."
    elif closure_rate > 0:
        return f"Only {closure_rate}% of findings have been closed, leaving {open_count} unresolved—this pace of resolution poses increasing institutional risk."
    else:
        return f"All {open_count} findings remain unresolved, suggesting a stalled remediation process that requires urgent escalation."


def generate_summary(sheet_name, analysis):
    if "error" in analysis:
        return f"{sheet_name}: analysis skipped due to missing columns."

    total = analysis.get('total_records', 0)
    avg_compliance = analysis.get('average_compliance', 0)
    open_f = analysis.get('open_findings', 0)
    closed_f = analysis.get('closed_findings', 0)
    high_risk = analysis.get('high_risk_findings', 0)
    medium_risk = analysis.get('medium_risk_findings', 0)
    low_risk = analysis.get('low_risk_findings', 0)

    # Dynamic AI-like header
    summary_parts = [
        f"🤖 AI-Powered Audit Summary Report — {sheet_name}",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"This report was generated through automated intelligent analysis of {total} audit records.",
        f"",
        _compliance_verdict(avg_compliance),
        f"",
        f"📊 Key Metrics at a Glance:",
        f"  • Total Records Analyzed: {total}",
        f"  • Compliance Rate: {avg_compliance}%",
        f"  • Open Findings: {open_f}  |  Closed Findings: {closed_f}",
    ]

    # Dynamic status narrative
    summary_parts.append(f"\n📋 Resolution Progress:")
    summary_parts.append(f"  {_status_narrative(open_f, closed_f, total)}")

    # Dynamic Risk narrative
    summary_parts.append(f"\n🎯 Risk Assessment:")
    summary_parts.append(
        f"  • High Risk: {high_risk}  |  Medium Risk: {medium_risk}  |  Low Risk: {low_risk}")
    summary_parts.append(
        f"  {_risk_narrative(high_risk, medium_risk, low_risk, total)}")

    # Red flags
    if analysis['red_flag_count'] > 0:
        red_count = analysis['red_flag_count']
        summary_parts.append(
            f"\n🚩 Red Flag Alert: {red_count} critical red flag{'s' if red_count > 1 else ''} identified.")
        if red_count > 3:
            summary_parts.append(
                f"  The volume of red flags suggests systemic control failures requiring board-level attention.")
        else:
            summary_parts.append(
                f"  Immediate investigation and root-cause analysis is strongly recommended.")

    # Compliance distribution with narrative
    if analysis.get('compliance_distribution'):
        dist = analysis['compliance_distribution']
        excellent = dist.get('excellent', 0)
        good = dist.get('good', 0)
        fair = dist.get('fair', 0)
        poor = dist.get('poor', 0)
        summary_parts.append(f"\n📈 Compliance Distribution Breakdown:")
        summary_parts.append(f"  • Excellent (≥90%): {excellent}")
        summary_parts.append(f"  • Good (75-89%): {good}")
        summary_parts.append(f"  • Fair (50-74%): {fair}")
        summary_parts.append(f"  • Poor (<50%): {poor}")
        if poor > excellent:
            summary_parts.append(
                f"  ⚠️ The number of poorly performing items ({poor}) exceeds excellent ones ({excellent})—a clear signal that foundational compliance improvements are needed.")
        elif excellent > 0 and poor == 0:
            summary_parts.append(
                f"  ✨ Zero poor-compliance items detected, with {excellent} achieving excellence—a testament to effective controls and oversight.")

    # Score analysis with narrative
    if analysis.get('score_analysis'):
        score = analysis['score_analysis']
        achievement = score.get('score_achievement_rate', 0)
        gap = score.get('total_score_gap', 0)
        summary_parts.append(f"\n🎯 Score Achievement Analysis:")
        summary_parts.append(
            f"  • Total Expected: {score.get('total_expected_score', 0)}")
        summary_parts.append(
            f"  • Total Achieved: {score.get('total_actual_score', 0)}")
        summary_parts.append(f"  • Score Gap: {gap}")
        summary_parts.append(f"  • Achievement Rate: {achievement}%")
        if achievement >= 80:
            summary_parts.append(
                f"  The {achievement}% achievement rate reflects strong alignment between expectations and actual performance.")
        elif achievement >= 50:
            summary_parts.append(
                f"  A {achievement}% achievement rate indicates a measurable gap of {gap} points between expected and actual scores, warranting targeted interventions.")
        else:
            summary_parts.append(
                f"  At {achievement}%, the achievement rate reveals a significant performance deficit that may undermine organizational objectives.")

    # Financial analysis with narrative
    if analysis.get('financial_analysis'):
        finance = analysis['financial_analysis']
        t_budget = finance.get('total_budget', 0)
        at_risk = finance.get('budget_at_risk', 0)
        at_risk_pct = finance.get('budget_at_risk_percentage', 0)
        summary_parts.append(f"\n💰 Financial Risk Analysis:")
        summary_parts.append(
            f"  • Total Budget Under Review: TZS {t_budget:,.2f}")
        summary_parts.append(
            f"  • Budget at Risk: TZS {at_risk:,.2f} ({at_risk_pct}%)")
        summary_parts.append(
            f"  {_budget_narrative(t_budget, at_risk, at_risk_pct)}")

    # === NEW ADVANCED ANALYSIS SECTIONS ===

    # Status detailed analysis (OPEN vs CLOSED)
    if analysis.get('status_detailed_analysis'):
        status_detail = analysis['status_detailed_analysis']
        summary_parts.append(f"\n📋 Status Detailed Analysis:")

        open_data = status_detail.get('OPEN', {})
        closed_data = status_detail.get('CLOSED', {})

        summary_parts.append(
            f"\n  🔴 OPEN Findings ({open_data.get('count', 0)}):")
        summary_parts.append(
            f"    • Avg Compliance: {open_data.get('average_compliance', 0)}%")
        summary_parts.append(
            f"    • Total Budget: TZS {open_data.get('total_budget', 0):,.2f}")
        summary_parts.append(
            f"    • High Risk: {open_data.get('high_risk_count', 0)}")
        summary_parts.append(
            f"    • Red Flags: {open_data.get('red_flag_count', 0)}")

        summary_parts.append(
            f"\n  🟢 CLOSED Findings ({closed_data.get('count', 0)}):")
        summary_parts.append(
            f"    • Avg Compliance: {closed_data.get('average_compliance', 0)}%")
        summary_parts.append(
            f"    • Total Budget: TZS {closed_data.get('total_budget', 0):,.2f}")

    # PE Name Analysis
    if analysis.get('pe_name_analysis'):
        pe_analysis = analysis['pe_name_analysis']
        if pe_analysis:
            summary_parts.append(
                f"\n🏢 Analysis by Public Entity ({len(pe_analysis)} entities):")

            # Show top 5 PEs by findings
            sorted_pes = sorted(
                pe_analysis.items(), key=lambda x: x[1]['total_findings'], reverse=True)[:5]
            for pe_name, pe_data in sorted_pes:
                summary_parts.append(f"\n  • {pe_name}:")
                summary_parts.append(
                    f"    - Total Findings: {pe_data['total_findings']}")
                summary_parts.append(
                    f"    - Open: {pe_data['open_findings']}, Closed: {pe_data['closed_findings']}")
                summary_parts.append(
                    f"    - Avg Compliance: {pe_data['average_compliance']}%")
                summary_parts.append(
                    f"    - Budget: TZS {pe_data['total_budget']:,.2f}")
                if pe_data['high_risk_findings'] > 0:
                    summary_parts.append(
                        f"    - ⚠️ High Risk: {pe_data['high_risk_findings']}")

    # Entity Analysis (Entity Name + Number)
    if analysis.get('entity_analysis'):
        entity_analysis = analysis['entity_analysis']
        if entity_analysis:
            summary_parts.append(
                f"\n📦 Entity Analysis ({len(entity_analysis)} entities):")

            # Show top 5 entities
            sorted_entities = sorted(entity_analysis.items(
            ), key=lambda x: x[1]['total_budget'], reverse=True)[:5]
            for entity_key, entity_data in sorted_entities:
                summary_parts.append(f"\n  • {entity_key}:")
                summary_parts.append(
                    f"    - Findings: {entity_data['total_findings']} (Open: {entity_data['open_findings']})")
                summary_parts.append(
                    f"    - Budget: TZS {entity_data['total_budget']:,.2f}")
                summary_parts.append(
                    f"    - Budget at Risk: TZS {entity_data['budget_at_risk']:,.2f}")
                summary_parts.append(
                    f"    - Compliance: {entity_data['average_compliance']}%")

    # Budget Distribution
    if analysis.get('budget_distribution'):
        budget_dist = analysis['budget_distribution']
        if budget_dist:
            summary_parts.append(f"\n💵 Budget Distribution Analysis:")
            summary_parts.append(
                f"  • Total Budget: TZS {budget_dist.get('total_budget', 0):,.2f}")

            if budget_dist.get('budget_range_distribution'):
                summary_parts.append(f"\n  Budget Ranges:")
                for range_name, count in budget_dist['budget_range_distribution'].items():
                    summary_parts.append(f"    - {range_name}: {count} items")

            if budget_dist.get('top_budget_items'):
                summary_parts.append(f"\n  Top Budget Items:")
                for item in budget_dist['top_budget_items'][:3]:
                    summary_parts.append(f"    • {item['entity']}")
                    summary_parts.append(
                        f"      Budget: TZS {item['budget']:,.2f} ({item['percentage_of_total']}% of total)")
                    summary_parts.append(
                        f"      Status: {item['status']}, Compliance: {item['compliance']}%")

    # Checklist Detailed Analysis
    if analysis.get('checklist_detailed_analysis'):
        checklist_detail = analysis['checklist_detailed_analysis']
        if checklist_detail and len(checklist_detail) > 0:
            summary_parts.append(
                f"\n📝 Checklist Detailed Analysis ({len(checklist_detail)} checklists):")

            # Show top 3 checklists
            sorted_checklists = sorted(checklist_detail.items(
            ), key=lambda x: x[1]['total_findings'], reverse=True)[:3]
            for checklist_name, checklist_data in sorted_checklists:
                # Truncate long checklist names
                display_name = checklist_name[:70] + \
                    "..." if len(checklist_name) > 70 else checklist_name
                summary_parts.append(f"\n  • {display_name}")
                summary_parts.append(
                    f"    - Findings: {checklist_data['total_findings']} (Open: {checklist_data['open_findings']})")
                summary_parts.append(
                    f"    - Avg Compliance: {checklist_data['average_compliance']}%")
                summary_parts.append(
                    f"    - Audit Type: {checklist_data['audit_type']}")

    return "\n".join(summary_parts)


def generate_insights(analysis):
    """Generate comprehensive, performance-based actionable insights from analysis"""
    insights = {
        "priority_actions": [],
        "positive_highlights": [],
        "areas_of_concern": [],
        "recommendations": []
    }

    total = analysis.get('total_records', 0)
    avg_compliance = analysis.get('average_compliance', 0)
    open_f = analysis.get('open_findings', 0)
    closed_f = analysis.get('closed_findings', 0)
    high_risk = analysis.get('high_risk_findings', 0)
    medium_risk = analysis.get('medium_risk_findings', 0)
    red_flags = analysis.get('red_flag_count', 0)
    open_ratio = (open_f / total * 100) if total > 0 else 0
    closure_rate = (closed_f / total * 100) if total > 0 else 0

    # ==========================================
    # PRIORITY ACTIONS (based on data severity)
    # ==========================================
    if high_risk > 0:
        high_risk_pct = round(high_risk / total * 100, 1) if total > 0 else 0
        insights["priority_actions"].append(
            f"Immediate attention required: {high_risk} high-risk findings ({high_risk_pct}% of total) demand resolution within the next review cycle"
        )
        if high_risk > 5:
            insights["priority_actions"].append(
                f"With {high_risk} high-risk items, consider establishing an emergency review committee to triage and assign remediation owners"
            )

    if red_flags > 0:
        insights["priority_actions"].append(
            f"Critical alert: {red_flags} red flag{'s' if red_flags > 1 else ''} detected—these represent the highest severity issues and require urgent investigation with documented action plans within 48 hours"
        )
        if red_flags > 3:
            insights["priority_actions"].append(
                "The volume of red flags suggests potential systemic governance failures; escalate to senior management and consider engaging external audit support"
            )

    if open_ratio > 80:
        insights["priority_actions"].append(
            f"Alarming: {open_ratio:.1f}% of all findings remain open—this stalled remediation poses escalating institutional risk and requires board-level intervention"
        )
    elif open_ratio > 60:
        insights["priority_actions"].append(
            f"{open_ratio:.1f}% of findings are still open—assign dedicated resources and set weekly progress checkpoints to accelerate resolution"
        )

    # ==========================================
    # POSITIVE HIGHLIGHTS (celebrate wins)
    # ==========================================
    if avg_compliance >= 90:
        insights["positive_highlights"].append(
            f"Outstanding compliance achievement: {avg_compliance}% average demonstrates exemplary governance and deep organizational commitment to standards"
        )
    elif avg_compliance >= 75:
        insights["positive_highlights"].append(
            f"Healthy compliance rate of {avg_compliance}% indicates a well-functioning control environment with room for targeted refinement"
        )
    elif avg_compliance >= 60:
        insights["positive_highlights"].append(
            f"Compliance rate of {avg_compliance}% shows foundational controls are in place, providing a strong base for improvement initiatives"
        )

    if closure_rate >= 80:
        insights["positive_highlights"].append(
            f"Excellent resolution rate: {closure_rate:.1f}% of findings have been successfully closed, reflecting a responsive and accountable remediation culture"
        )
    elif closure_rate >= 50:
        insights["positive_highlights"].append(
            f"Over half ({closure_rate:.1f}%) of findings have been resolved, demonstrating steady progress toward full compliance"
        )

    if high_risk == 0:
        insights["positive_highlights"].append(
            "Zero high-risk findings recorded—a strong indicator that critical risk controls are functioning effectively"
        )

    if red_flags == 0 and total > 0:
        insights["positive_highlights"].append(
            "No red flags detected across the entire analysis, reflecting sound operational integrity"
        )

    # Score achievement
    if analysis.get('score_analysis'):
        achievement = analysis['score_analysis'].get(
            'score_achievement_rate', 0)
        gap = analysis['score_analysis'].get('total_score_gap', 0)
        if achievement >= 90:
            insights["positive_highlights"].append(
                f"Exceptional score achievement rate of {achievement}%, nearly closing the gap between expected and actual performance"
            )
        elif achievement >= 75:
            insights["positive_highlights"].append(
                f"Strong score achievement of {achievement}% with a manageable gap of {gap} points—targeted coaching can close this"
            )
        elif achievement < 50:
            insights["areas_of_concern"].append(
                f"Score achievement rate of {achievement}% with a {gap}-point gap signals deep performance deficiencies across multiple compliance domains"
            )
        elif achievement < 70:
            insights["areas_of_concern"].append(
                f"Score achievement at {achievement}% falls below the 70% threshold—investigate underlying drivers of the {gap}-point gap"
            )

    # ==========================================
    # AREAS OF CONCERN (data-driven warnings)
    # ==========================================
    if avg_compliance < 50:
        insights["areas_of_concern"].append(
            f"Critically low compliance rate of {avg_compliance}%—without immediate intervention, regulatory penalties and reputational damage become increasingly likely"
        )
    elif avg_compliance < 65:
        insights["areas_of_concern"].append(
            f"Below-target compliance at {avg_compliance}% suggests process gaps that, if unaddressed, will widen over subsequent audit cycles"
        )

    if analysis.get('financial_analysis'):
        finance = analysis['financial_analysis']
        risk_pct = finance.get('budget_at_risk_percentage', 0)
        at_risk = finance.get('budget_at_risk', 0)
        if risk_pct > 70:
            insights["areas_of_concern"].append(
                f"Severe financial exposure: {risk_pct}% of budget (TZS {at_risk:,.0f}) is tied to unresolved findings—fiduciary responsibility demands immediate ring-fencing"
            )
        elif risk_pct > 50:
            insights["areas_of_concern"].append(
                f"Elevated financial risk: {risk_pct}% of budget (TZS {at_risk:,.0f}) remains exposed through open findings"
            )
        elif risk_pct > 30:
            insights["areas_of_concern"].append(
                f"Budget at risk stands at {risk_pct}% (TZS {at_risk:,.0f})—while manageable, continued monitoring is essential"
            )

    dist = analysis.get('compliance_distribution', {})
    poor = dist.get('poor', 0)
    excellent = dist.get('excellent', 0)
    if poor > 0 and total > 0:
        poor_pct = round(poor / total * 100, 1)
        if poor_pct > 40:
            insights["areas_of_concern"].append(
                f"{poor} items ({poor_pct}%) have compliance below 50%—this proportion indicates widespread control failures across the portfolio"
            )
        elif poor_pct > 20:
            insights["areas_of_concern"].append(
                f"{poor} items ({poor_pct}%) fall into poor compliance territory, requiring root-cause analysis for each"
            )

    if medium_risk > 0 and total > 0:
        med_pct = round(medium_risk / total * 100, 1)
        if med_pct > 50:
            insights["areas_of_concern"].append(
                f"{medium_risk} findings ({med_pct}%) are medium risk—without proactive management, these may escalate to high-risk status"
            )

    # ==========================================
    # RECOMMENDATIONS (performance-based)
    # ==========================================

    # Compliance-based recommendations
    if avg_compliance < 50:
        insights["recommendations"].extend([
            "Deploy an organization-wide compliance awareness campaign with mandatory training sessions for all departments",
            "Engage external compliance consultants to conduct a gap assessment and develop a 90-day remediation roadmap",
            "Institute weekly compliance tracking dashboards with real-time KPIs visible to leadership",
            "Create a compliance task force with representatives from each underperforming unit to drive cross-functional accountability"
        ])
    elif avg_compliance < 65:
        insights["recommendations"].extend([
            "Develop targeted training modules focusing on the specific compliance areas with the lowest scores",
            "Implement a peer mentoring program pairing high-compliance entities with underperformers",
            "Introduce quarterly compliance review checkpoints with documented improvement targets",
            "Strengthen internal audit follow-up mechanisms to ensure findings translate into corrective actions"
        ])
    elif avg_compliance < 75:
        insights["recommendations"].extend([
            "Conduct focused refresher training on compliance areas where scores fall between 50-74%",
            "Establish monthly progress tracking with escalation protocols for stagnant findings",
            "Benchmark against top-performing entities to identify and replicate best practices"
        ])
    elif avg_compliance < 90:
        insights["recommendations"].extend([
            "Fine-tune existing controls and processes to push compliance from good to excellent",
            "Implement advanced analytics for predictive compliance monitoring and early warning detection"
        ])
    else:
        insights["recommendations"].append(
            "Sustain current excellence by documenting and institutionalizing the practices that drive high compliance—share as organizational templates"
        )

    # Open/Closed ratio recommendations
    if open_ratio > 70:
        insights["recommendations"].extend([
            "Establish a dedicated resolution task force with clear authority to fast-track closure of open findings",
            "Implement a finding aging tracker with automatic escalation at 30, 60, and 90 day marks",
            "Assign individual accountability for each open finding with documented timelines and consequences for delays"
        ])
    elif open_ratio > 50:
        insights["recommendations"].extend([
            "Introduce bi-weekly finding review meetings to maintain resolution momentum and remove blockers",
            "Set entity-level targets for closing open findings and tie performance to incentive structures"
        ])
    elif open_ratio > 30:
        insights["recommendations"].append(
            "Continue current resolution pace while prioritizing high-risk open findings for immediate attention"
        )

    # Risk-based recommendations
    if high_risk > 0:
        insights["recommendations"].append(
            "Prioritize resolution of all high-risk findings before allocating resources to lower-risk items—apply a risk-weighted remediation approach"
        )
        if high_risk > total * 0.3:
            insights["recommendations"].append(
                "With over 30% of findings classified as high risk, commission an independent review of risk assessment criteria and control effectiveness"
            )

    if red_flags > 0:
        insights["recommendations"].extend([
            "Immediately investigate each red flag finding with a cross-functional team and document root causes",
            "Report red flag findings to the governing body with proposed corrective action plans and prevention measures"
        ])

    # Financial recommendations
    if analysis.get('financial_analysis'):
        finance = analysis['financial_analysis']
        risk_pct = finance.get('budget_at_risk_percentage', 0)
        at_risk = finance.get('budget_at_risk', 0)
        if risk_pct > 50:
            insights["recommendations"].extend([
                f"Ring-fence the TZS {at_risk:,.0f} at-risk budget and establish financial safeguards until associated findings are resolved",
                "Implement enhanced financial monitoring with weekly budget exposure reports tied to finding status"
            ])
        elif risk_pct > 20:
            insights["recommendations"].append(
                f"Monitor the TZS {at_risk:,.0f} at-risk budget through monthly financial review cycles linked to finding remediation progress"
            )

    # Distribution-based recommendations
    if poor > excellent:
        insights["recommendations"].append(
            f"Implement comprehensive capability building: {poor} poorly-performing items significantly outnumber {excellent} excellent ones—invest in training and process redesign"
        )

    if dist.get('fair', 0) > 0 and total > 0:
        fair_pct = round(dist['fair'] / total * 100, 1)
        if fair_pct > 30:
            insights["recommendations"].append(
                f"{dist['fair']} items ({fair_pct}%) are in the 'fair' range (50-74%)—these represent the highest-impact improvement opportunity with focused intervention"
            )

    # === ADVANCED ANALYSIS INSIGHTS ===

    # PE Name analysis
    if analysis.get('pe_name_analysis'):
        pe_analysis = analysis['pe_name_analysis']

        pes_with_high_findings = {
            k: v for k, v in pe_analysis.items() if v['total_findings'] > 5}
        if pes_with_high_findings:
            pe_names = list(pes_with_high_findings.keys())[:3]
            insights["areas_of_concern"].append(
                f"{len(pes_with_high_findings)} Public Entities have more than 5 findings each, including: {', '.join(pe_names)}"
            )
            insights["recommendations"].append(
                f"Deploy dedicated compliance officers to the {len(pes_with_high_findings)} entities with the highest finding counts for intensive on-site support"
            )

        pes_with_budget = {
            k: v for k, v in pe_analysis.items() if v['total_budget'] > 50000000}
        if pes_with_budget:
            total_pe_budget = sum(v['total_budget']
                                  for v in pes_with_budget.values())
            insights["priority_actions"].append(
                f"Focus on {len(pes_with_budget)} PEs with budgets exceeding TZS 50M (combined: TZS {total_pe_budget:,.0f})"
            )

        pes_perfect = {k: v for k, v in pe_analysis.items()
                       if v['average_compliance'] >= 90}
        if pes_perfect:
            insights["positive_highlights"].append(
                f"{len(pes_perfect)} Public Entities achieved excellent compliance (≥90%)—leverage their practices as institutional benchmarks"
            )

        # PE compliance grouping
        pes_low = {k: v for k, v in pe_analysis.items()
                   if v['average_compliance'] < 50}
        pes_mid = {k: v for k, v in pe_analysis.items() if 50 <=
                   v['average_compliance'] < 75}
        if pes_low:
            insights["recommendations"].append(
                f"Assign remediation coaches to {len(pes_low)} PEs with compliance below 50% for intensive capacity building"
            )
        if pes_mid:
            insights["recommendations"].append(
                f"Develop tailored improvement plans for {len(pes_mid)} PEs in the 50-74% compliance range to push them into the 'good' category"
            )

    # Status analysis
    if analysis.get('status_detailed_analysis'):
        status_detail = analysis['status_detailed_analysis']
        open_data = status_detail.get('OPEN', {})
        closed_data = status_detail.get('CLOSED', {})

        if open_data.get('total_budget', 0) > 100000000:
            insights["areas_of_concern"].append(
                f"TZS {open_data['total_budget']:,.0f} in budget linked to open findings—this level of financial exposure demands executive-level oversight"
            )

        total_findings_count = open_data.get(
            'count', 0) + closed_data.get('count', 0)
        if total_findings_count > 0:
            rate = (closed_data.get('count', 0) / total_findings_count) * 100
            if rate >= 70:
                insights["positive_highlights"].append(
                    f"Strong finding closure rate of {rate:.1f}% demonstrates effective accountability and responsive governance"
                )
            elif rate < 30:
                insights["recommendations"].append(
                    f"Finding closure rate is critically low at {rate:.1f}%—implement mandatory weekly resolution reviews with management sign-off"
                )
            elif rate < 50:
                insights["recommendations"].append(
                    f"Closure rate of {rate:.1f}% needs acceleration—consider establishing an expedited review process for aging findings"
                )

        if open_data.get('high_risk_count', 0) > 0:
            insights["priority_actions"].append(
                f"{open_data['high_risk_count']} high-risk findings are still open—each one represents an active threat that must be resolved before the next review cycle"
            )

        if open_data.get('red_flag_count', 0) > 0:
            insights["priority_actions"].append(
                f"{open_data['red_flag_count']} open red flags demand immediate executive attention and documented resolution plans"
            )

    # Entity analysis
    if analysis.get('entity_analysis'):
        entity_analysis = analysis['entity_analysis']

        high_risk_entities = {
            k: v for k, v in entity_analysis.items() if v['high_risk'] > 0}
        if high_risk_entities:
            insights["priority_actions"].append(
                f"{len(high_risk_entities)} entities have high-risk findings requiring immediate action and dedicated remediation resources"
            )

        entities_budget_risk = {
            k: v for k, v in entity_analysis.items() if v['budget_at_risk'] > 10000000}
        if len(entities_budget_risk) > 3:
            total_at_risk = sum(v['budget_at_risk']
                                for v in entities_budget_risk.values())
            insights["areas_of_concern"].append(
                f"{len(entities_budget_risk)} entities have budget at risk exceeding TZS 10M each (combined: TZS {total_at_risk:,.0f})"
            )
            insights["recommendations"].append(
                "Implement enhanced financial controls and approval workflows for entities with significant budget exposure"
            )

        # Entity compliance distribution
        entity_compliances = [v.get('average_compliance', 0)
                              for v in entity_analysis.values()]
        if entity_compliances:
            low_compliance_entities = [c for c in entity_compliances if c < 60]
            if len(low_compliance_entities) > len(entity_compliances) * 0.3:
                insights["recommendations"].append(
                    f"{len(low_compliance_entities)} out of {len(entity_compliances)} entities have compliance below 60%—consider a sector-wide compliance transformation program"
                )

    # Budget distribution
    if analysis.get('budget_distribution'):
        budget_dist = analysis['budget_distribution']

        if budget_dist.get('top_budget_items'):
            top_3_percentage = sum(item['percentage_of_total']
                                   for item in budget_dist['top_budget_items'][:3])
            if top_3_percentage > 60:
                insights["areas_of_concern"].append(
                    f"Budget concentration risk: Top 3 items control {top_3_percentage:.1f}% of total budget—diversification of oversight resources is needed"
                )
                insights["recommendations"].append(
                    "Distribute audit and monitoring resources proportionally to budget concentration to mitigate single-point-of-failure risk"
                )

        if budget_dist.get('budget_range_distribution'):
            high_budget = budget_dist['budget_range_distribution'].get(
                '> 100M', 0)
            if high_budget > 0:
                insights["recommendations"].append(
                    f"Assign senior auditors to monitor {high_budget} high-value items (>100M TZS) with quarterly deep-dive reviews"
                )

    # Checklist analysis
    if analysis.get('checklist_detailed_analysis'):
        checklist_detail = analysis['checklist_detailed_analysis']

        low_compliance_checklists = {
            k: v for k, v in checklist_detail.items() if v['average_compliance'] < 50}
        if low_compliance_checklists:
            insights["recommendations"].append(
                f"Redesign and strengthen {len(low_compliance_checklists)} checklists with compliance below 50%—consider simplifying requirements or providing additional guidance"
            )

        high_open_checklists = {
            k: v for k, v in checklist_detail.items() if v['open_findings'] > 3}
        if high_open_checklists:
            insights["priority_actions"].append(
                f"{len(high_open_checklists)} checklists have more than 3 open findings—assign dedicated follow-up teams for each"
            )

        # Checklist performance grouping
        mid_checklists = {k: v for k, v in checklist_detail.items(
        ) if 50 <= v['average_compliance'] < 75}
        if mid_checklists:
            insights["recommendations"].append(
                f"{len(mid_checklists)} checklists in the 50-74% range represent the best improvement opportunity—targeted training could yield significant gains"
            )

    # Cross-cutting recommendations based on overall health
    if total > 10:
        insights["recommendations"].append(
            "Implement a continuous monitoring framework with automated alerts for compliance threshold breaches"
        )
    if total > 0 and avg_compliance > 0:
        insights["recommendations"].append(
            "Schedule periodic trend analysis reviews comparing current performance against historical baselines to detect emerging patterns"
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


# ============================================
# ENTITY SUMMARY FORMAT FUNCTIONS
# ============================================

def generate_entity_summary(sheet_name, analysis):
    """Generate dynamic AI-powered summary for entity summary format"""
    if "error" in analysis:
        return f"{sheet_name}: analysis skipped - {analysis.get('error', 'unknown error')}"

    total_entities = analysis.get('total_entities', 0)
    avg_perf = analysis.get('average_overall_performance', 0)

    summary_parts = [
        f"🤖 AI-Powered Entity Performance Report — {sheet_name}",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"This report presents an intelligent assessment of {total_entities} procuring entities,",
        f"evaluating operational performance, tender management effectiveness, and compliance posture.",
        f"",
    ]

    # Dynamic performance verdict
    if avg_perf >= 90:
        summary_parts.append(
            f"🌟 Overall Performance Verdict: OUTSTANDING ({avg_perf}%)")
        summary_parts.append(
            f"  The portfolio demonstrates exceptional maturity across entities, suggesting deeply embedded compliance culture and effective governance frameworks.")
    elif avg_perf >= 75:
        summary_parts.append(
            f"✅ Overall Performance Verdict: STRONG ({avg_perf}%)")
        summary_parts.append(
            f"  Entities are performing well as a collective, with a solid {avg_perf}% average that positions the portfolio favorably—targeted refinements can elevate this to excellence.")
    elif avg_perf >= 60:
        summary_parts.append(
            f"🟡 Overall Performance Verdict: MODERATE ({avg_perf}%)")
        summary_parts.append(
            f"  At {avg_perf}%, the portfolio shows foundational capability but reveals performance gaps that, without intervention, may widen in subsequent cycles.")
    else:
        summary_parts.append(
            f"🔴 Overall Performance Verdict: NEEDS IMPROVEMENT ({avg_perf}%)")
        summary_parts.append(
            f"  A {avg_perf}% average signals systemic underperformance across entities—urgent capacity building and governance strengthening are required.")

    # Performance distribution with narrative
    if analysis.get('performance_distribution'):
        dist = analysis['performance_distribution']
        excellent = dist.get('excellent', 0)
        good = dist.get('good', 0)
        satisfactory = dist.get('satisfactory', 0)
        needs = dist.get('needs_improvement', 0)
        summary_parts.append(f"\n📈 Entity Performance Distribution:")
        summary_parts.append(f"  • Excellent (≥90%): {excellent} entities")
        summary_parts.append(f"  • Good (75-89%): {good} entities")
        summary_parts.append(
            f"  • Satisfactory (60-74%): {satisfactory} entities")
        summary_parts.append(f"  • Needs Improvement (<60%): {needs} entities")
        if total_entities > 0:
            strong_pct = round((excellent + good) / total_entities * 100, 1)
            if strong_pct >= 70:
                summary_parts.append(
                    f"  ✨ {strong_pct}% of entities are performing at good-to-excellent levels—a strong indicator of institutional maturity.")
            elif needs > excellent + good:
                summary_parts.append(
                    f"  ⚠️ The number of underperforming entities ({needs}) exceeds strong performers ({excellent + good})—systemic intervention is warranted.")

    # Category breakdown
    if analysis.get('category_breakdown'):
        summary_parts.append(f"\n🏷️ Entity Categories:")
        for category, count in analysis['category_breakdown'].items():
            summary_parts.append(f"  • {category}: {count}")

    # Tenders analysis with narrative
    if analysis.get('tenders_analysis'):
        tenders = analysis['tenders_analysis']
        total_tenders = tenders.get('total_tenders', 0)
        avg_t = tenders.get('average_tenders_per_entity', 0)
        min_t = tenders.get('min_tenders', 0)
        max_t = tenders.get('max_tenders', 0)
        summary_parts.append(f"\n📋 Tender Management Overview:")
        summary_parts.append(f"  • Total Tenders Processed: {total_tenders}")
        summary_parts.append(f"  • Average per Entity: {avg_t}")
        summary_parts.append(f"  • Range: {min_t} to {max_t} tenders")
        if max_t > 0 and min_t == 0:
            summary_parts.append(
                f"  Notable: Some entities have zero tenders on record—this may indicate data gaps or inactive entities requiring verification.")
        if max_t > avg_t * 3 and avg_t > 0:
            summary_parts.append(
                f"  The wide range ({min_t}-{max_t}) suggests significant capacity variance across entities that merits workload balancing review.")

    # Tendering performance with narrative
    if analysis.get('tendering_performance'):
        perf = analysis['tendering_performance']
        avg_score = perf.get('average_tendering_score', 0)
        above_80 = perf.get('entities_above_80', 0)
        below_60 = perf.get('entities_below_60', 0)
        summary_parts.append(f"\n🎯 Tendering Performance Assessment:")
        summary_parts.append(f"  • Average Tendering Score: {avg_score}%")
        summary_parts.append(
            f"  • High Performers (≥80%): {above_80} entities")
        summary_parts.append(
            f"  • Underperformers (<60%): {below_60} entities")
        if avg_score >= 80:
            summary_parts.append(
                f"  The {avg_score}% average tendering score reflects mature procurement processes and strong institutional knowledge.")
        elif below_60 > above_80:
            summary_parts.append(
                f"  With {below_60} underperformers outnumbering {above_80} high performers, tendering capability building should be a priority investment.")

    # Top performers with narrative
    if analysis.get('top_performers'):
        summary_parts.append(
            f"\n🏆 Top Performing Entities (Leading by Example):")
        for i, entity in enumerate(analysis['top_performers'], 1):
            summary_parts.append(f"  {i}. {entity['entity']}")
            summary_parts.append(
                f"     Performance: {entity['overall_percentage']}% | Tenders Managed: {entity['tenders']}")
        summary_parts.append(
            f"  These entities represent best-practice models whose processes can be documented and replicated across the portfolio.")

    # Bottom performers with narrative
    if analysis.get('bottom_performers'):
        summary_parts.append(f"\n⚠️ Entities Requiring Immediate Support:")
        for i, entity in enumerate(analysis['bottom_performers'], 1):
            summary_parts.append(f"  {i}. {entity['entity']}")
            summary_parts.append(
                f"     Performance: {entity['overall_percentage']}% | Tenders Managed: {entity['tenders']}")
        lowest = analysis['bottom_performers'][0]
        if lowest['overall_percentage'] < 50:
            summary_parts.append(
                f"  🚨 The lowest performer at {lowest['overall_percentage']}% requires immediate intervention and dedicated support resources.")

    # Category analysis with narrative
    if analysis.get('entity_by_category'):
        summary_parts.append(f"\n📊 Category Performance Breakdown:")
        for category, data in analysis['entity_by_category'].items():
            avg_cat = data.get('average_overall', 0)
            summary_parts.append(f"  • {category}:")
            summary_parts.append(
                f"    - Entities: {data['count']} | Avg Performance: {avg_cat}%")
            summary_parts.append(
                f"    - Total Tenders: {data['total_tenders']}")
            if avg_cat < 60:
                summary_parts.append(
                    f"    ⚠️ This category is underperforming and should be prioritized for capacity development.")
            elif avg_cat >= 85:
                summary_parts.append(
                    f"    ✨ Strong category performance—maintain current practices and share learnings.")

    # Status breakdown
    if analysis.get('status_breakdown'):
        summary_parts.append(f"\n🔖 Status Distribution:")
        for status, count in analysis['status_breakdown'].items():
            summary_parts.append(f"  • {status}: {count}")

    return "\n".join(summary_parts)


def generate_entity_insights(analysis):
    """Generate comprehensive performance-based insights for entity summary format"""
    insights = {
        "priority_actions": [],
        "positive_highlights": [],
        "areas_of_concern": [],
        "recommendations": []
    }

    avg_overall = analysis.get('average_overall_performance', 0)
    total_entities = analysis.get('total_entities', 0)
    dist = analysis.get('performance_distribution', {})
    needs_improvement = dist.get('needs_improvement', 0)
    excellent = dist.get('excellent', 0)
    good = dist.get('good', 0)
    satisfactory = dist.get('satisfactory', 0)

    # ==========================================
    # PRIORITY ACTIONS
    # ==========================================
    if total_entities > 0:
        needs_pct = round(needs_improvement / total_entities * 100, 1)
        if needs_pct > 50:
            insights["priority_actions"].append(
                f"Critical: {needs_improvement} entities ({needs_pct}%) require immediate performance intervention—this majority underperformance threatens portfolio-wide outcomes"
            )
        elif needs_pct > 30:
            insights["priority_actions"].append(
                f"{needs_improvement} entities ({needs_pct}%) need performance improvement—assign dedicated coaching resources and establish 60-day improvement targets"
            )
        elif needs_improvement > 0:
            insights["priority_actions"].append(
                f"{needs_improvement} entities performing below 60%—provide targeted support before performance gaps widen"
            )

    bottom_performers = analysis.get('bottom_performers', [])
    if len(bottom_performers) > 0:
        lowest = bottom_performers[0]
        if lowest['overall_percentage'] < 30:
            insights["priority_actions"].append(
                f"URGENT: {lowest['entity']} is at critically low {lowest['overall_percentage']}%—this entity requires emergency support, possible management review, and a dedicated remediation plan"
            )
        elif lowest['overall_percentage'] < 50:
            insights["priority_actions"].append(
                f"High priority: {lowest['entity']} at {lowest['overall_percentage']}% needs immediate intervention with structured improvement roadmap and weekly progress monitoring"
            )
        elif lowest['overall_percentage'] < 60:
            insights["priority_actions"].append(
                f"{lowest['entity']} at {lowest['overall_percentage']}% is approaching the critical threshold—engage proactively to prevent further decline"
            )

    if analysis.get('tendering_performance'):
        perf = analysis['tendering_performance']
        below_60 = perf.get('entities_below_60', 0)
        if below_60 > 0 and total_entities > 0:
            below_pct = round(below_60 / total_entities * 100, 1)
            if below_pct > 40:
                insights["priority_actions"].append(
                    f"Tendering crisis: {below_60} entities ({below_pct}%) score below 60% in tendering—launch an emergency procurement training program"
                )
            elif below_60 > 3:
                insights["priority_actions"].append(
                    f"{below_60} entities have tendering scores below 60%—deploy targeted procurement support teams"
                )

    # ==========================================
    # POSITIVE HIGHLIGHTS
    # ==========================================
    if avg_overall >= 90:
        insights["positive_highlights"].append(
            f"Outstanding portfolio performance: {avg_overall}% average across {total_entities} entities demonstrates exceptional organizational maturity and governance effectiveness"
        )
    elif avg_overall >= 80:
        insights["positive_highlights"].append(
            f"Strong collective performance at {avg_overall}% reflects a well-established compliance culture with embedded accountability mechanisms"
        )
    elif avg_overall >= 70:
        insights["positive_highlights"].append(
            f"Solid performance foundation at {avg_overall}%—the portfolio shows capable governance with clear pathways to further advancement"
        )
    elif avg_overall >= 60:
        insights["positive_highlights"].append(
            f"Performance at {avg_overall}% indicates basic compliance frameworks are operational, providing a platform for systematic improvement"
        )

    if excellent > 0 and total_entities > 0:
        excellent_pct = round(excellent / total_entities * 100, 1)
        insights["positive_highlights"].append(
            f"{excellent} entities ({excellent_pct}%) achieving excellence (≥90%)—these represent institutional benchmarks whose practices should be documented and replicated"
        )

    if excellent + good > 0 and total_entities > 0:
        strong_pct = round((excellent + good) / total_entities * 100, 1)
        if strong_pct >= 60:
            insights["positive_highlights"].append(
                f"{strong_pct}% of entities are performing at good-to-excellent levels, creating a strong peer network for knowledge sharing"
            )

    top_performers = analysis.get('top_performers', [])
    if len(top_performers) > 0:
        top = top_performers[0]
        if top['overall_percentage'] >= 95:
            insights["positive_highlights"].append(
                f"Exceptional: {top['entity']} achieved {top['overall_percentage']}%—a near-perfect score that sets the gold standard for the entire portfolio"
            )
        elif top['overall_percentage'] >= 90:
            insights["positive_highlights"].append(
                f"Top performer: {top['entity']} at {top['overall_percentage']}% serves as an excellent best-practice model for peer learning"
            )

    tenders_analysis = analysis.get('tenders_analysis', {})
    if tenders_analysis:
        total_tenders = tenders_analysis.get('total_tenders', 0)
        if total_tenders > 0:
            insights["positive_highlights"].append(
                f"Successfully tracking {total_tenders} tenders across all entities, enabling comprehensive procurement oversight and trend analysis"
            )

    if analysis.get('tendering_performance'):
        perf = analysis['tendering_performance']
        above_80 = perf.get('entities_above_80', 0)
        avg_score = perf.get('average_tendering_score', 0)
        if above_80 > 0:
            insights["positive_highlights"].append(
                f"{above_80} entities achieving strong tendering scores (≥80%), indicating mature procurement processes"
            )
        if avg_score >= 80:
            insights["positive_highlights"].append(
                f"Portfolio-wide tendering average of {avg_score}% reflects effective procurement management across entities"
            )

    # ==========================================
    # AREAS OF CONCERN
    # ==========================================
    if avg_overall < 50:
        insights["areas_of_concern"].append(
            f"Average performance of {avg_overall}% is critically below acceptable thresholds—without immediate systemic intervention, regulatory consequences and institutional risk will escalate"
        )
    elif avg_overall < 60:
        insights["areas_of_concern"].append(
            f"Portfolio average of {avg_overall}% falls below the 60% adequacy threshold, indicating widespread process and capability gaps"
        )
    elif avg_overall < 70:
        insights["areas_of_concern"].append(
            f"At {avg_overall}%, the portfolio is performing below the 70% target—a clear signal that improvement initiatives need intensification"
        )

    if needs_improvement > excellent + good and total_entities > 0:
        insights["areas_of_concern"].append(
            f"Underperforming entities ({needs_improvement}) outnumber strong performers ({excellent + good})—the performance distribution is bottom-heavy and requires structural intervention"
        )

    if analysis.get('tendering_performance'):
        perf = analysis['tendering_performance']
        below_60 = perf.get('entities_below_60', 0)
        avg_score = perf.get('average_tendering_score', 0)
        if below_60 > 0:
            insights["areas_of_concern"].append(
                f"{below_60} entities have tendering scores below 60%—weak procurement practices increase risk of irregularities and value-for-money losses"
            )
        if avg_score < 60:
            insights["areas_of_concern"].append(
                f"Portfolio tendering average of {avg_score}% is concerning—procurement is a high-risk area requiring comprehensive capacity building"
            )

    if tenders_analysis:
        avg_tenders = tenders_analysis.get('average_tenders_per_entity', 0)
        if avg_tenders < 3:
            insights["areas_of_concern"].append(
                f"Low tender volume per entity (avg: {avg_tenders:.1f}) may indicate limited procurement activity, data capture gaps, or capacity constraints"
            )

    # Performance gap between top and bottom
    if len(top_performers) > 0 and len(bottom_performers) > 0:
        gap = top_performers[0]['overall_percentage'] - \
            bottom_performers[-1]['overall_percentage']
        if gap > 50:
            insights["areas_of_concern"].append(
                f"A {gap}-percentage-point gap between the best and worst performers reveals severe capability inequality that needs targeted bridging programs"
            )
        elif gap > 30:
            insights["areas_of_concern"].append(
                f"Performance disparity of {gap} percentage points between top and bottom entities signals uneven resource allocation and support distribution"
            )

    category_data = analysis.get('entity_by_category', {})
    if category_data:
        low_categories = {cat: data for cat, data in category_data.items(
        ) if data['average_overall'] < 60}
        if low_categories:
            cat_names = list(low_categories.keys())[:3]
            insights["areas_of_concern"].append(
                f"{len(low_categories)} categories performing below 60%: {', '.join(cat_names)}—these represent sector-wide weaknesses"
            )

    # ==========================================
    # RECOMMENDATIONS (performance-based tiers)
    # ==========================================

    # Overall performance-based recommendations
    if avg_overall < 50:
        insights["recommendations"].extend([
            "Deploy emergency performance improvement teams to all entities below 50% with weekly progress tracking",
            "Commission an independent assessment of systemic barriers to performance and develop a 90-day transformation roadmap",
            "Establish a centralized performance management unit to coordinate cross-entity improvement initiatives",
            "Implement mandatory weekly reporting and executive dashboards to maintain visibility on recovery progress",
            "Consider structural reforms in entities with persistently low performance—leadership changes or organizational restructuring may be necessary"
        ])
    elif avg_overall < 65:
        insights["recommendations"].extend([
            "Design targeted competency development programs addressing the specific capability gaps driving underperformance",
            "Establish a peer mentoring framework pairing top performers with struggling entities for knowledge transfer",
            "Introduce monthly performance scorecards with entity-level targets and public reporting to drive accountability",
            "Allocate additional resources to entities in the 50-64% range where incremental investment can yield substantial gains",
            "Create a performance improvement fund to support entities requiring additional technical assistance"
        ])
    elif avg_overall < 75:
        insights["recommendations"].extend([
            "Focus on moving 'satisfactory' entities (60-74%) into the 'good' range through targeted process improvements",
            "Implement cross-entity learning workshops where high performers share strategies and tools",
            "Develop standardized operating procedures based on practices from top-performing entities",
            "Introduce performance-linked incentive mechanisms to motivate continuous improvement"
        ])
    elif avg_overall < 85:
        insights["recommendations"].extend([
            "Fine-tune existing processes to close the gap between good and excellent performance",
            "Implement advanced performance analytics for predictive monitoring and early-warning capabilities",
            "Establish a center of excellence to codify and disseminate best practices portfolio-wide"
        ])
    else:
        insights["recommendations"].extend([
            "Sustain excellence through continuous innovation in governance and compliance practices",
            "Document institutional knowledge from top performers to ensure continuity and resilience",
            "Explore advanced benchmarking against international standards to maintain competitive edge"
        ])

    # Tendering-specific recommendations
    if analysis.get('tendering_performance'):
        perf = analysis['tendering_performance']
        below_60 = perf.get('entities_below_60', 0)
        avg_score = perf.get('average_tendering_score', 0)

        if below_60 > 5:
            insights["recommendations"].extend([
                f"Launch a comprehensive procurement training program for {below_60} underperforming entities with hands-on workshop components",
                "Develop standardized tender evaluation templates and procurement guidelines to ensure consistency",
                "Establish a procurement helpdesk providing real-time guidance during active tendering processes"
            ])
        elif below_60 > 0:
            insights["recommendations"].extend([
                f"Provide targeted tendering mentorship for {below_60} entities scoring below 60%",
                "Share procurement best-practice toolkits from high-performing entities"
            ])

        if avg_score < 70:
            insights["recommendations"].append(
                "Review and simplify procurement procedures that may be creating unnecessary compliance barriers"
            )

    # Bottom performer specific recommendations
    if len(bottom_performers) > 2:
        insights["recommendations"].append(
            f"Create individualized improvement plans for each of the bottom {len(bottom_performers)} entities with dedicated coaching and biweekly progress assessments"
        )

    # Category-based recommendations
    if category_data:
        low_categories = {cat: data for cat, data in category_data.items(
        ) if data['average_overall'] < 60}
        high_categories = {cat: data for cat, data in category_data.items(
        ) if data['average_overall'] >= 80}
        if low_categories:
            insights["recommendations"].append(
                f"Invest in sector-specific capacity building for {len(low_categories)} underperforming categories—address root causes unique to each category"
            )
        if high_categories and low_categories:
            insights["recommendations"].append(
                "Facilitate cross-category knowledge exchange sessions between high and low performing categories"
            )

    # Distribution-based recommendations
    if satisfactory > 0 and total_entities > 0:
        sat_pct = round(satisfactory / total_entities * 100, 1)
        if sat_pct > 30:
            insights["recommendations"].append(
                f"{satisfactory} entities ({sat_pct}%) are in the 'satisfactory' range (60-74%)—these represent the highest-impact improvement opportunity with relatively low investment"
            )

    # Knowledge management recommendations
    if excellent > 0 and needs_improvement > 0:
        insights["recommendations"].extend([
            "Document and formalize best practices from excellent performers into reusable playbooks",
            "Establish a recognition program celebrating top performers to reinforce positive behaviors"
        ])

    # Cross-cutting recommendations
    if total_entities > 5:
        insights["recommendations"].append(
            "Implement automated performance tracking with threshold-based alerts to enable proactive intervention before entities fall into crisis"
        )

    insights["recommendations"].append(
        "Conduct quarterly trend analysis comparing entity performance against baselines to measure progress and detect emerging risks early"
    )

    return insights


def generate_multi_tender_summary(sheet_name, analysis):
    """Generate dynamic AI-powered summary for multi-tender findings format"""
    if "error" in analysis:
        return f"{sheet_name}: analysis skipped due to missing columns."

    def get_value(key, default=0):
        val = analysis.get(key, default)
        if isinstance(val, dict) and 'value' in val:
            return val['value']
        return val if val is not None else default

    total_findings = get_value('total_findings')
    open_f = get_value('open_findings')
    closed_f = get_value('closed_findings')
    red_flags = get_value('red_flags', 0)
    total_budget = get_value('total_budget')
    unique_tenders = get_value('unique_tenders')

    summary_parts = [
        f"🤖 AI-Powered Multi-Tender Findings Report — {sheet_name}",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"This report provides an intelligent assessment of {total_findings} audit findings",
        f"spanning {unique_tenders} unique tenders with a combined budget of TZS {total_budget:,.0f}.",
        f"",
    ]

    # Dynamic findings narrative
    if total_findings > 0:
        open_pct = round(open_f / total_findings * 100, 1)
        if open_pct > 70:
            summary_parts.append(
                f"🔴 Finding Status: CRITICAL — {open_pct}% of findings remain unresolved")
            summary_parts.append(
                f"  The overwhelming majority of findings ({open_f} of {total_findings}) are still open, indicating a severely stalled remediation process requiring immediate escalation.")
        elif open_pct > 40:
            summary_parts.append(
                f"🟡 Finding Status: MODERATE CONCERN — {open_pct}% open")
            summary_parts.append(
                f"  With {open_f} findings still open out of {total_findings}, resolution progress needs acceleration to prevent escalating risk exposure.")
        elif open_f > 0:
            summary_parts.append(
                f"🟢 Finding Status: PROGRESSING — {open_pct}% remain open")
            summary_parts.append(
                f"  Good progress has been made with {closed_f} findings resolved, though {open_f} still require attention.")
        else:
            summary_parts.append(f"✨ Finding Status: ALL RESOLVED")
            summary_parts.append(
                f"  All {total_findings} findings have been successfully closed—an exemplary demonstration of responsive governance.")

    # Red flags narrative
    if red_flags > 0:
        summary_parts.append(
            f"\n🚩 Red Flag Alert: {red_flags} Critical Issue{'s' if red_flags > 1 else ''}")
        if red_flags > 3:
            summary_parts.append(
                f"  The volume of red flags suggests systemic compliance failures requiring board-level intervention and external audit support.")
        else:
            summary_parts.append(
                f"  Each red flag represents a critical risk point demanding immediate investigation with documented root-cause analysis.")

    # Budget narrative
    summary_parts.append(f"\n💰 Financial Exposure Analysis:")
    summary_parts.append(
        f"  • Total Budget Under Review: TZS {total_budget:,.0f}")
    summary_parts.append(
        f"  • Average per Finding: TZS {get_value('average_budget_per_finding'):,.0f}")
    if total_budget > 500000000:
        summary_parts.append(
            f"  The substantial budget of TZS {total_budget/1000000:,.1f}M tied to these findings underscores the critical importance of timely resolution to safeguard public resources.")
    elif total_budget > 100000000:
        summary_parts.append(
            f"  With TZS {total_budget/1000000:,.1f}M at stake, financial risk mitigation should be integrated into the finding resolution process.")

    # Tender narrative
    summary_parts.append(f"\n📋 Tender Landscape:")
    summary_parts.append(
        f"  • Total Tenders Referenced: {get_value('total_tenders')}")
    summary_parts.append(
        f"  • Unique Tenders (deduplicated): {unique_tenders}")
    summary_parts.append(
        f"  • Average Tenders per Finding: {get_value('average_tenders_per_finding'):.2f}")
    avg_tenders = get_value('average_tenders_per_finding')
    if avg_tenders > 3:
        summary_parts.append(
            f"  High tender density ({avg_tenders:.1f} per finding) suggests findings may reflect systemic procurement issues rather than isolated incidents.")

    # Budget range distribution
    if analysis.get('budget_range_distribution'):
        budget_dist = analysis['budget_range_distribution']
        if budget_dist.get('ranges'):
            active_ranges = {
                k: v for k, v in budget_dist['ranges'].items() if v['count'] > 0}
            if active_ranges:
                summary_parts.append(
                    f"\n💵 Budget Range Distribution (Unique Tenders):")
                for range_name, range_data in active_ranges.items():
                    summary_parts.append(
                        f"  • {range_name}: {range_data['count']} tenders ({range_data['percentage']:.1f}%) — TZS {range_data['total_budget']:,.0f}")

    # Top entities with narrative
    if analysis.get('top_entities_by_budget'):
        top_entities = analysis['top_entities_by_budget']
        if top_entities.get('entities'):
            summary_parts.append(f"\n🏆 Highest-Impact Entities by Budget:")
            for entity in top_entities['entities'][:5]:
                summary_parts.append(f"  • {entity['entity_name']}:")
                summary_parts.append(
                    f"    - Budget: TZS {entity['total_budget']:,.0f}")
                summary_parts.append(
                    f"    - Findings: {entity['total_findings']} (Open: {entity['open_findings']})")
                summary_parts.append(
                    f"    - Tenders: {entity['total_tenders']}")
                if entity.get('tender_numbers'):
                    tender_nums = ', '.join(entity['tender_numbers'][:3])
                    if len(entity['tender_numbers']) > 3:
                        tender_nums += f" +{len(entity['tender_numbers']) - 3} more"
                    summary_parts.append(
                        f"    - Tender Numbers: {tender_nums}")
                if entity.get('red_flags', 0) > 0:
                    summary_parts.append(
                        f"    - ⚠️ Red Flags: {entity['red_flags']}")

    # Checklist analysis with narrative
    if analysis.get('checklist_analysis'):
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}
        if checklist_data:
            summary_parts.append(f"\n📝 Compliance Checklist Assessment:")
            checklist_sorted = sorted(checklist_data.items(),
                                      key=lambda x: x[1].get('total_findings', 0), reverse=True)
            for checklist, data in checklist_sorted[:5]:
                risk = data.get('risk_level', 'Unknown')
                risk_icon = '🔴' if risk == 'High' else (
                    '🟡' if risk == 'Medium' else '🟢')
                summary_parts.append(f"  {risk_icon} {checklist[:75]}...")
                summary_parts.append(
                    f"    - Findings: {data['total_findings']} (Open: {data['open_findings']}, Closed: {data['closed_findings']})")
                summary_parts.append(
                    f"    - Budget: TZS {data['total_budget']:,.0f} (Avg: TZS {data['average_budget_per_finding']:,.0f})")
                summary_parts.append(
                    f"    - Tenders: {data['total_tenders']} | Risk Level: {risk}")
                if data.get('completion_rate', 0) > 0:
                    summary_parts.append(
                        f"    - Completion Rate: {data['completion_rate']}%")

    return "\n".join(summary_parts)


def generate_multi_tender_insights(analysis):
    """Generate comprehensive AI-powered insights for multi-tender findings format"""
    if "error" in analysis:
        return {}

    def get_value(key, default=0):
        val = analysis.get(key, default)
        if isinstance(val, dict) and 'value' in val:
            return val['value']
        return val if val is not None else default

    insights = {
        "priority_actions": [],
        "positive_highlights": [],
        "areas_of_concern": [],
        "recommendations": []
    }

    total_findings = get_value('total_findings', 0)
    open_findings = get_value('open_findings', 0)
    closed_findings = get_value('closed_findings', 0)
    red_flags = get_value('red_flags', 0)
    total_budget = get_value('total_budget', 0)
    unique_tenders = get_value('unique_tenders', 0)
    avg_tenders = get_value('average_tenders_per_finding', 0)
    open_pct = round(open_findings / total_findings *
                     100, 1) if total_findings > 0 else 0
    closure_rate = round(closed_findings / total_findings *
                         100, 1) if total_findings > 0 else 0

    # ==========================================
    # PRIORITY ACTIONS
    # ==========================================
    if open_pct > 80:
        insights["priority_actions"].append(
            f"Critical: {open_findings} findings ({open_pct}%) remain unresolved—the stalled remediation process demands board-level intervention and emergency resource allocation"
        )
    elif open_pct > 50:
        insights["priority_actions"].append(
            f"{open_findings} findings ({open_pct}%) still open—assign dedicated resolution teams with weekly progress checkpoints and escalation protocols"
        )
    elif open_findings > 0:
        insights["priority_actions"].append(
            f"{open_findings} finding{'s' if open_findings > 1 else ''} ({open_pct}%) remain open—maintain current resolution momentum while prioritizing by budget impact"
        )

    if red_flags > 3:
        insights["priority_actions"].extend([
            f"⚠️ CRITICAL: {red_flags} red flags detected—this volume suggests systemic governance failures requiring immediate multi-stakeholder investigation",
            "Convene an emergency review committee to triage red flag findings and establish 48-hour action plans for each"
        ])
    elif red_flags > 0:
        insights["priority_actions"].append(
            f"⚠️ {red_flags} red flag{'s' if red_flags > 1 else ''} detected—immediate investigation with documented root-cause analysis and corrective action plans is required"
        )

    if total_budget > 500000000:
        insights["priority_actions"].append(
            f"High-stakes portfolio: TZS {total_budget/1000000:,.1f}M in budget exposure—financial safeguards and enhanced monitoring must be implemented immediately"
        )
    elif total_budget > 100000000:
        insights["priority_actions"].append(
            f"Significant financial exposure of TZS {total_budget/1000000:,.1f}M tied to audit findings—prioritize resolution of highest-value findings first"
        )

    # Top entity priority
    if analysis.get('top_entities_by_budget'):
        top_entities = analysis['top_entities_by_budget'].get('entities', [])
        if top_entities:
            top = top_entities[0]
            if top['open_findings'] > 0:
                insights["priority_actions"].append(
                    f"Focus on {top['entity_name']}: {top['open_findings']} open findings with TZS {top['total_budget']:,.0f} budget across {top['total_tenders']} tenders—this entity carries the highest financial risk"
                )
            # Multiple entities with issues
            entities_with_open = [
                e for e in top_entities if e['open_findings'] > 0]
            if len(entities_with_open) > 3:
                insights["priority_actions"].append(
                    f"{len(entities_with_open)} entities have unresolved findings—deploy coordinated resolution teams across all affected entities"
                )

    # ==========================================
    # POSITIVE HIGHLIGHTS
    # ==========================================
    if closure_rate >= 80:
        insights["positive_highlights"].append(
            f"Exceptional resolution rate: {closure_rate}% of findings successfully closed, demonstrating strong institutional accountability and responsive governance"
        )
    elif closure_rate >= 50:
        insights["positive_highlights"].append(
            f"Over half ({closure_rate}%) of findings resolved, reflecting steady progress toward full compliance—maintain momentum to close remaining items"
        )
    elif closed_findings > 0:
        insights["positive_highlights"].append(
            f"{closed_findings} finding{'s' if closed_findings > 1 else ''} ({closure_rate}%) resolved, indicating the remediation process has begun"
        )

    if open_findings == 0 and total_findings > 0:
        insights["positive_highlights"].append(
            f"All {total_findings} findings have been successfully resolved—an outstanding achievement reflecting mature governance and dedicated follow-through"
        )

    if red_flags == 0 and total_findings > 0:
        insights["positive_highlights"].append(
            "No red flags detected across the analyzed findings—risk controls and compliance mechanisms appear to be functioning effectively"
        )

    if unique_tenders > 0:
        insights["positive_highlights"].append(
            f"Comprehensive tracking of {unique_tenders} unique tenders with deduplication ensures accurate budget and risk assessment"
        )

    # Checklists with good completion
    if analysis.get('checklist_analysis'):
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}
        good_checklists = [name for name, data in checklist_data.items()
                           if data.get('completion_rate', 0) >= 70]
        low_risk_checklists = [name for name, data in checklist_data.items()
                               if data.get('risk_level') == 'Low']
        if good_checklists:
            insights["positive_highlights"].append(
                f"{len(good_checklists)} checklist{'s' if len(good_checklists) > 1 else ''} showing strong completion rate (≥70%)—evidence of effective compliance management in these areas"
            )
        if low_risk_checklists:
            insights["positive_highlights"].append(
                f"{len(low_risk_checklists)} checklist{'s' if len(low_risk_checklists) > 1 else ''} classified as low risk, reflecting well-managed compliance domains"
            )

    # ==========================================
    # AREAS OF CONCERN
    # ==========================================
    if open_findings > closed_findings:
        insights["areas_of_concern"].append(
            f"Resolution deficit: more open findings ({open_findings}) than closed ({closed_findings})—the remediation pipeline is not keeping pace with discovery rate"
        )

    if avg_tenders > 3:
        insights["areas_of_concern"].append(
            f"High tender density ({avg_tenders:.1f} per finding) suggests findings may reflect systemic procurement issues rather than isolated incidents"
        )
    elif avg_tenders > 2:
        insights["areas_of_concern"].append(
            f"Average of {avg_tenders:.1f} tenders per finding indicates multiple procurement processes are affected by similar compliance gaps"
        )

    # Checklists with high risk
    if analysis.get('checklist_analysis'):
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}
        high_risk = [(name, data) for name, data in checklist_data.items(
        ) if data.get('risk_level') == 'High']
        if high_risk:
            for name, data in high_risk[:2]:
                insights["areas_of_concern"].append(
                    f"Checklist '{name[:50]}...' flagged as HIGH RISK with {data.get('red_flags', 0)} red flags affecting {data.get('affected_entities', 0)} entities"
                )

        low_completion = [(name, data) for name, data in checklist_data.items()
                          if data.get('completion_rate', 0) < 30 and data.get('total_findings', 0) > 0]
        if low_completion:
            insights["areas_of_concern"].append(
                f"{len(low_completion)} checklist{'s' if len(low_completion) > 1 else ''} with completion rate below 30%—these stagnant areas risk becoming chronic compliance gaps"
            )

    # Budget concentration
    if analysis.get('budget_range_distribution'):
        ranges = analysis['budget_range_distribution'].get('ranges', {})
        high_value = ranges.get('500M+', {})
        if high_value.get('count', 0) > 0:
            insights["areas_of_concern"].append(
                f"{high_value['count']} high-value tender{'s' if high_value['count'] > 1 else ''} (>500M TZS) totaling TZS {high_value['total_budget']:,.0f}—these require enhanced monitoring and senior oversight"
            )
        mid_high = ranges.get('200M-500M', {})
        if mid_high.get('count', 0) > 2:
            insights["areas_of_concern"].append(
                f"{mid_high['count']} tenders in the TZS 200M-500M range—this concentration of mid-to-high value procurement warrants dedicated oversight"
            )

    # ==========================================
    # RECOMMENDATIONS (comprehensive, performance-based)
    # ==========================================

    # Resolution-based recommendations
    if open_pct > 70:
        insights["recommendations"].extend([
            "Establish a dedicated finding resolution task force with executive authority to fast-track closures",
            "Implement a finding aging tracker with automatic escalation at 30, 60, and 90-day marks",
            "Assign individual accountability for each open finding with documented timelines and consequences for delays",
            "Consider engaging external support to accelerate resolution of the most complex findings"
        ])
    elif open_pct > 40:
        insights["recommendations"].extend([
            "Introduce bi-weekly finding review meetings to maintain resolution momentum and identify blockers early",
            "Set entity-level closure targets with progress dashboards visible to all stakeholders",
            "Prioritize resolution of findings with the highest budget exposure first"
        ])
    elif open_findings > 0:
        insights["recommendations"].extend([
            "Maintain current resolution pace while ensuring remaining open findings receive focused attention",
            "Document lessons learned from successfully closed findings to streamline future resolution processes"
        ])

    # Red flag recommendations
    if red_flags > 0:
        insights["recommendations"].extend([
            "Immediately investigate every red flag finding with a cross-functional team and document root causes within 48 hours",
            "Report red flag findings to the governing body with proposed corrective action plans and prevention measures",
            "Conduct a systemic review to identify whether red flag patterns indicate broader governance weaknesses"
        ])

    # Budget-based recommendations
    if total_budget > 500000000:
        insights["recommendations"].extend([
            f"Ring-fence the TZS {total_budget/1000000:,.1f}M in at-risk budget and establish financial safeguards until associated findings are fully resolved",
            "Deploy enhanced financial monitoring with weekly budget exposure reports tied to finding resolution status",
            "Engage financial oversight bodies to ensure transparent management of high-value findings"
        ])
    elif total_budget > 100000000:
        insights["recommendations"].extend([
            f"Monitor the TZS {total_budget/1000000:,.1f}M budget exposure through monthly financial review cycles",
            "Implement budget-weighted finding prioritization to ensure highest-value items are resolved first"
        ])
    elif total_budget > 50000000:
        insights["recommendations"].append(
            "Maintain regular budget exposure tracking and link financial reporting to finding resolution progress"
        )

    # Entity-based recommendations
    if analysis.get('top_entities_by_budget'):
        top_entities = analysis['top_entities_by_budget'].get('entities', [])
        if len(top_entities) > 3:
            insights["recommendations"].append(
                f"Conduct structured training sessions for all {len(top_entities)} entities with findings to prevent recurrence and build compliance capacity"
            )
        entities_with_red = [
            e for e in top_entities if e.get('red_flags', 0) > 0]
        if entities_with_red:
            insights["recommendations"].append(
                f"Deploy dedicated compliance officers to {len(entities_with_red)} entities with red flags for intensive on-site remediation support"
            )

    # Checklist-based recommendations
    if analysis.get('checklist_analysis'):
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}

        low_completion = [data for data in checklist_data.values(
        ) if data.get('completion_rate', 0) < 50]
        if low_completion:
            insights["recommendations"].append(
                f"{len(low_completion)} checklists have completion rates below 50%—focus audit follow-up resources on these areas to accelerate resolution"
            )

        medium_risk = [data for data in checklist_data.values(
        ) if data.get('risk_level') == 'Medium']
        if medium_risk:
            insights["recommendations"].append(
                f"Monitor {len(medium_risk)} medium-risk checklists closely to prevent escalation—implement preventive controls and regular check-ins"
            )

        if checklist_data:
            insights["recommendations"].append(
                "Standardize checklist evaluation criteria and develop compliance toolkits for recurring finding categories"
            )

    # Tender-specific recommendations
    if avg_tenders > 2:
        insights["recommendations"].append(
            "Investigate common procurement patterns across multi-tender findings to identify root causes and develop preventive procurement guidelines"
        )

    if unique_tenders > 5:
        insights["recommendations"].append(
            f"With {unique_tenders} unique tenders affected, consider a portfolio-wide procurement process review to address systemic compliance gaps"
        )

    # Cross-cutting recommendations
    insights["recommendations"].extend([
        "Implement continuous monitoring with automated alerts for finding resolution milestones and budget threshold breaches",
        "Schedule quarterly trend analysis comparing finding patterns, resolution rates, and budget exposure against previous periods"
    ])

    return insights
