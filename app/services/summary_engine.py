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

    # === NEW INSIGHTS FROM ADVANCED ANALYSIS ===

    # Insights from PE Name analysis
    if analysis.get('pe_name_analysis'):
        pe_analysis = analysis['pe_name_analysis']

        # Find PEs with most issues
        pes_with_high_findings = {
            k: v for k, v in pe_analysis.items() if v['total_findings'] > 5}
        if pes_with_high_findings:
            insights["areas_of_concern"].append(
                f"{len(pes_with_high_findings)} Public Entities have more than 5 findings each"
            )

        # Find PEs with high budget at risk
        pes_with_budget = {
            k: v for k, v in pe_analysis.items() if v['total_budget'] > 50000000}
        if pes_with_budget:
            insights["priority_actions"].append(
                f"Focus on {len(pes_with_budget)} PEs with budgets exceeding TZS 50M"
            )

        # PEs with perfect compliance
        pes_perfect = {k: v for k, v in pe_analysis.items()
                       if v['average_compliance'] >= 90}
        if pes_perfect:
            insights["positive_highlights"].append(
                f"{len(pes_perfect)} Public Entities achieved excellent compliance (≥90%)"
            )

    # Insights from Status analysis
    if analysis.get('status_detailed_analysis'):
        status_detail = analysis['status_detailed_analysis']
        open_data = status_detail.get('OPEN', {})
        closed_data = status_detail.get('CLOSED', {})

        # Open findings with high budget
        if open_data.get('total_budget', 0) > 100000000:
            insights["areas_of_concern"].append(
                f"TZS {open_data['total_budget']:,.2f} in budget linked to open findings"
            )

        # Good closure rate
        total_findings_count = open_data.get(
            'count', 0) + closed_data.get('count', 0)
        if total_findings_count > 0:
            closure_rate = (closed_data.get('count', 0) /
                            total_findings_count) * 100
            if closure_rate >= 70:
                insights["positive_highlights"].append(
                    f"Good finding closure rate: {closure_rate:.1f}%"
                )
            elif closure_rate < 30:
                insights["recommendations"].append(
                    f"Improve finding resolution - only {closure_rate:.1f}% closure rate"
                )

    # Insights from Entity analysis
    if analysis.get('entity_analysis'):
        entity_analysis = analysis['entity_analysis']

        # Entities with high risk
        high_risk_entities = {
            k: v for k, v in entity_analysis.items() if v['high_risk'] > 0}
        if high_risk_entities:
            insights["priority_actions"].append(
                f"{len(high_risk_entities)} entities have high-risk findings requiring immediate action"
            )

        # Entities with budget at risk
        entities_budget_risk = {
            k: v for k, v in entity_analysis.items() if v['budget_at_risk'] > 10000000}
        if len(entities_budget_risk) > 3:
            insights["areas_of_concern"].append(
                f"{len(entities_budget_risk)} entities have budget at risk exceeding TZS 10M"
            )

    # Insights from Budget distribution
    if analysis.get('budget_distribution'):
        budget_dist = analysis['budget_distribution']

        # High concentration of budget
        if budget_dist.get('top_budget_items'):
            top_3_percentage = sum(item['percentage_of_total']
                                   for item in budget_dist['top_budget_items'][:3])
            if top_3_percentage > 60:
                insights["areas_of_concern"].append(
                    f"Budget concentration: Top 3 items represent {top_3_percentage:.1f}% of total budget"
                )

        # Budget range insights
        if budget_dist.get('budget_range_distribution'):
            high_budget_items = budget_dist['budget_range_distribution'].get(
                '> 100M', 0)
            if high_budget_items > 0:
                insights["recommendations"].append(
                    f"Prioritize monitoring of {high_budget_items} high-value items (>100M TZS)"
                )

    # Insights from Checklist analysis
    if analysis.get('checklist_detailed_analysis'):
        checklist_detail = analysis['checklist_detailed_analysis']

        # Checklists with low compliance
        low_compliance_checklists = {
            k: v for k, v in checklist_detail.items() if v['average_compliance'] < 50}
        if low_compliance_checklists:
            insights["recommendations"].append(
                f"Review and strengthen {len(low_compliance_checklists)} checklists with compliance below 50%"
            )

        # Checklists with many open findings
        high_open_checklists = {
            k: v for k, v in checklist_detail.items() if v['open_findings'] > 3}
        if high_open_checklists:
            insights["priority_actions"].append(
                f"{len(high_open_checklists)} checklists have more than 3 open findings"
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
    """Generate summary for entity summary format"""
    if "error" in analysis:
        return f"{sheet_name}: analysis skipped - {analysis.get('error', 'unknown error')}"

    summary_parts = [
        f"{sheet_name} - Entity Performance Report:",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🏢 Total Entities: {analysis['total_entities']}",
        f"📊 Average Overall Performance: {analysis['average_overall_performance']}%",
    ]

    # Performance distribution
    if analysis.get('performance_distribution'):
        dist = analysis['performance_distribution']
        summary_parts.append(f"\n📈 Performance Distribution:")
        summary_parts.append(
            f"  • Excellent (≥90%): {dist.get('excellent', 0)}")
        summary_parts.append(f"  • Good (75-89%): {dist.get('good', 0)}")
        summary_parts.append(
            f"  • Satisfactory (60-74%): {dist.get('satisfactory', 0)}")
        summary_parts.append(
            f"  • Needs Improvement (<60%): {dist.get('needs_improvement', 0)}")

    # Category breakdown
    if analysis.get('category_breakdown'):
        summary_parts.append(f"\n🏷️ Entity Categories:")
        for category, count in analysis['category_breakdown'].items():
            summary_parts.append(f"  • {category}: {count}")

    # Tenders analysis
    if analysis.get('tenders_analysis'):
        tenders = analysis['tenders_analysis']
        summary_parts.append(f"\n📋 Tenders Overview:")
        summary_parts.append(
            f"  • Total Tenders: {tenders.get('total_tenders', 0)}")
        summary_parts.append(
            f"  • Average per Entity: {tenders.get('average_tenders_per_entity', 0)}")
        summary_parts.append(
            f"  • Range: {tenders.get('min_tenders', 0)} - {tenders.get('max_tenders', 0)}")

    # Tendering performance
    if analysis.get('tendering_performance'):
        perf = analysis['tendering_performance']
        summary_parts.append(f"\n🎯 Tendering Performance:")
        summary_parts.append(
            f"  • Average Score: {perf.get('average_tendering_score', 0)}%")
        summary_parts.append(
            f"  • Entities ≥80%: {perf.get('entities_above_80', 0)}")
        summary_parts.append(
            f"  • Entities <60%: {perf.get('entities_below_60', 0)}")

    # Top performers
    if analysis.get('top_performers'):
        summary_parts.append(f"\n🏆 Top 5 Performers:")
        for i, entity in enumerate(analysis['top_performers'], 1):
            summary_parts.append(f"  {i}. {entity['entity']}")
            summary_parts.append(
                f"     Overall: {entity['overall_percentage']}%, Tenders: {entity['tenders']}")

    # Bottom performers
    if analysis.get('bottom_performers'):
        summary_parts.append(f"\n⚠️ Bottom 5 Performers (Need Support):")
        for i, entity in enumerate(analysis['bottom_performers'], 1):
            summary_parts.append(f"  {i}. {entity['entity']}")
            summary_parts.append(
                f"     Overall: {entity['overall_percentage']}%, Tenders: {entity['tenders']}")

    # Category analysis
    if analysis.get('entity_by_category'):
        summary_parts.append(f"\n📊 Performance by Category:")
        for category, data in analysis['entity_by_category'].items():
            summary_parts.append(f"  • {category}:")
            summary_parts.append(
                f"    - Count: {data['count']}, Avg Overall: {data['average_overall']}%")
            summary_parts.append(
                f"    - Total Tenders: {data['total_tenders']}")

    # Status breakdown
    if analysis.get('status_breakdown'):
        summary_parts.append(f"\n🔖 Status Distribution:")
        for status, count in analysis['status_breakdown'].items():
            summary_parts.append(f"  • {status}: {count}")

    return "\n".join(summary_parts)


def generate_entity_insights(analysis):
    """Generate insights for entity summary format"""
    insights = {
        "priority_actions": [],
        "positive_highlights": [],
        "areas_of_concern": [],
        "recommendations": []
    }

    # Overall performance analysis
    avg_overall = analysis.get('average_overall_performance', 0)
    if avg_overall >= 80:
        insights["positive_highlights"].append(
            f"Strong overall performance across entities: {avg_overall}% average"
        )
    elif avg_overall < 60:
        insights["areas_of_concern"].append(
            f"Low average performance: {avg_overall}% - requires systemic improvement"
        )

    # Performance distribution insights
    dist = analysis.get('performance_distribution', {})
    needs_improvement = dist.get('needs_improvement', 0)
    excellent = dist.get('excellent', 0)
    total_entities = analysis.get('total_entities', 0)

    if total_entities > 0:
        needs_improvement_pct = (needs_improvement / total_entities) * 100
        if needs_improvement_pct > 30:
            insights["priority_actions"].append(
                f"{needs_improvement} entities ({needs_improvement_pct:.1f}%) need immediate performance improvement"
            )

        if excellent > 0:
            excellent_pct = (excellent / total_entities) * 100
            insights["positive_highlights"].append(
                f"{excellent} entities ({excellent_pct:.1f}%) achieving excellent performance (≥90%)"
            )

    # Tendering insights
    if analysis.get('tendering_performance'):
        perf = analysis['tendering_performance']
        below_60 = perf.get('entities_below_60', 0)

        if below_60 > 0:
            insights["areas_of_concern"].append(
                f"{below_60} entities have tendering scores below 60%"
            )
            insights["recommendations"].append(
                "Provide targeted tendering training for low-performing entities"
            )

    # Bottom performers
    bottom_performers = analysis.get('bottom_performers', [])
    if len(bottom_performers) > 0:
        lowest = bottom_performers[0]
        if lowest['overall_percentage'] < 50:
            insights["priority_actions"].append(
                f"Urgent: {lowest['entity']} has critical performance level ({lowest['overall_percentage']}%)"
            )

    # Top performers recognition
    top_performers = analysis.get('top_performers', [])
    if len(top_performers) > 0:
        top = top_performers[0]
        if top['overall_percentage'] >= 90:
            insights["positive_highlights"].append(
                f"Outstanding: {top['entity']} achieved {top['overall_percentage']}% - best practice model"
            )

    # Category performance insights
    category_data = analysis.get('entity_by_category', {})
    if category_data:
        low_categories = {cat: data for cat, data in category_data.items(
        ) if data['average_overall'] < 60}
        if low_categories:
            insights["recommendations"].append(
                f"Focus improvement efforts on {len(low_categories)} underperforming categories"
            )

    # Tenders volume insights
    tenders_analysis = analysis.get('tenders_analysis', {})
    if tenders_analysis:
        total_tenders = tenders_analysis.get('total_tenders', 0)
        avg_tenders = tenders_analysis.get('average_tenders_per_entity', 0)

        if total_tenders > 0:
            insights["positive_highlights"].append(
                f"Total of {total_tenders} tenders processed across all entities"
            )

        if avg_tenders < 5:
            insights["areas_of_concern"].append(
                f"Low average tender volume per entity ({avg_tenders:.1f}) - may indicate capacity issues"
            )

    # General recommendations
    if needs_improvement > 0:
        insights["recommendations"].append(
            "Establish mentorship program pairing high and low performers"
        )

    if dist.get('excellent', 0) > 0 and needs_improvement > 0:
        insights["recommendations"].append(
            "Document and share best practices from excellent performers"
        )

    return insights


def generate_multi_tender_summary(sheet_name, analysis):
    """Generate formatted summary for multi-tender findings format"""
    if "error" in analysis:
        return f"{sheet_name}: analysis skipped due to missing columns."

    # Helper function to extract values from description-wrapped objects
    def get_value(key, default=0):
        val = analysis.get(key, default)
        if isinstance(val, dict) and 'value' in val:
            return val['value']
        return val if val is not None else default

    summary_parts = [
        f"{sheet_name} - Multi-Tender Findings Report:",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📊 Total Findings: {get_value('total_findings')}",
        f"🔴 Open Findings: {get_value('open_findings')}",
        f"🟢 Closed Findings: {get_value('closed_findings')}",
    ]

    # Red flags
    red_flags = get_value('red_flags', 0)
    if red_flags > 0:
        summary_parts.append(f"🚩 Red Flags: {red_flags}")

    # Budget overview
    summary_parts.append(f"\n💰 Budget Overview:")
    summary_parts.append(
        f"  • Total Budget: TZS {get_value('total_budget'):,.0f}")
    summary_parts.append(
        f"  • Average per Finding: TZS {get_value('average_budget_per_finding'):,.0f}")

    # Tender overview
    summary_parts.append(f"\n📋 Tender Overview:")
    summary_parts.append(f"  • Total Tenders: {get_value('total_tenders')}")
    summary_parts.append(f"  • Unique Tenders: {get_value('unique_tenders')}")
    summary_parts.append(
        f"  • Average per Finding: {get_value('average_tenders_per_finding'):.2f}")

    # Budget range distribution
    if analysis.get('budget_range_distribution'):
        budget_dist = analysis['budget_range_distribution']
        if budget_dist.get('ranges'):
            summary_parts.append(f"\n💵 Budget Range Distribution:")
            for range_name, range_data in budget_dist['ranges'].items():
                if range_data['count'] > 0:
                    summary_parts.append(
                        f"  • {range_name}: {range_data['count']} tenders ({range_data['percentage']:.1f}%) - TZS {range_data['total_budget']:,.0f}")

    # Top entities by budget
    if analysis.get('top_entities_by_budget'):
        top_entities = analysis['top_entities_by_budget']
        if top_entities.get('entities'):
            summary_parts.append(f"\n🏆 Top Entities by Budget:")
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

    # Checklist analysis
    if analysis.get('checklist_analysis'):
        summary_parts.append(f"\n📝 Analysis by Checklist:")
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}
        checklist_sorted = sorted(checklist_data.items(),
                                  key=lambda x: x[1].get('total_findings', 0), reverse=True)
        for checklist, data in checklist_sorted[:5]:  # Top 5
            summary_parts.append(f"  • {checklist[:80]}...")
            summary_parts.append(
                f"    - Findings: {data['total_findings']} (Open: {data['open_findings']}, Closed: {data['closed_findings']})")
            summary_parts.append(
                f"    - Budget: TZS {data['total_budget']:,.0f} (Avg: TZS {data['average_budget_per_finding']:,.0f})")
            summary_parts.append(
                f"    - Tenders: {data['total_tenders']} (Avg: {data['average_tenders_per_finding']:.2f})")
            summary_parts.append(f"    - Risk Level: {data['risk_level']}")

    return "\n".join(summary_parts)


def generate_multi_tender_insights(analysis):
    """Generate AI-powered insights for multi-tender findings format"""
    if "error" in analysis:
        return {}

    # Helper function to extract values from description-wrapped objects
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
    red_flags = get_value('red_flags', 0)
    total_budget = get_value('total_budget', 0)
    unique_tenders = get_value('unique_tenders', 0)

    # Priority actions
    if open_findings > 0:
        open_pct = (open_findings / total_findings *
                    100) if total_findings > 0 else 0
        insights["priority_actions"].append(
            f"{open_findings} findings ({open_pct:.1f}%) remain open - require immediate attention"
        )

    if red_flags > 0:
        insights["priority_actions"].append(
            f"⚠️ CRITICAL: {red_flags} red flags detected - urgent action required"
        )

    # High budget findings
    if total_budget > 100000000:  # > 100M TZS
        insights["priority_actions"].append(
            f"High-value findings totaling TZS {total_budget:,.0f} ({total_budget/1000000:.1f}M) - prioritize resolution"
        )

    # Top entities priority
    if analysis.get('top_entities_by_budget'):
        top_entities = analysis['top_entities_by_budget'].get('entities', [])
        if top_entities:
            top_entity = top_entities[0]
            if top_entity['open_findings'] > 0:
                insights["priority_actions"].append(
                    f"Focus on {top_entity['entity_name']}: {top_entity['open_findings']} open findings with TZS {top_entity['total_budget']:,.0f} budget affecting {top_entity['total_tenders']} tenders"
                )

    # Positive highlights
    closed_findings = get_value('closed_findings', 0)
    if closed_findings > 0:
        closed_pct = (closed_findings / total_findings *
                      100) if total_findings > 0 else 0
        insights["positive_highlights"].append(
            f"{closed_findings} findings ({closed_pct:.1f}%) successfully closed"
        )

    if unique_tenders > 0:
        insights["positive_highlights"].append(
            f"Tracking {unique_tenders} unique tenders with comprehensive oversight (duplicate tenders removed)"
        )

    # Checklists with good completion rate
    if analysis.get('checklist_analysis'):
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}
        good_checklists = [name for name, data in checklist_data.items()
                           if data.get('completion_rate', 0) >= 70]
        if good_checklists:
            insights["positive_highlights"].append(
                f"{len(good_checklists)} checklist(s) showing good completion rate (≥70%)"
            )

    # Areas of concern
    if open_findings > closed_findings:
        insights["areas_of_concern"].append(
            f"More open findings ({open_findings}) than closed ({closed_findings}) - resolution rate needs improvement"
        )

    avg_tenders = get_value('average_tenders_per_finding', 0)
    if avg_tenders > 2:
        insights["areas_of_concern"].append(
            f"Average of {avg_tenders:.1f} tenders per finding - may indicate systemic issues"
        )

    # Checklists with high risk
    if analysis.get('checklist_analysis'):
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}
        high_risk_checklists = [(name, data) for name, data in checklist_data.items()
                                if data.get('risk_level') == 'High']
        if high_risk_checklists:
            checklist_name, data = high_risk_checklists[0]
            insights["areas_of_concern"].append(
                f"Checklist '{checklist_name[:50]}': High risk level with {data['red_flags']} red flags affecting {data['affected_entities']} entities"
            )

    # Budget concentration concern
    if analysis.get('budget_range_distribution'):
        ranges = analysis['budget_range_distribution'].get('ranges', {})
        high_value_range = ranges.get('500M+', {})
        if high_value_range.get('count', 0) > 0:
            insights["areas_of_concern"].append(
                f"{high_value_range['count']} high-value tenders (>500M TZS) totaling TZS {high_value_range['total_budget']:,.0f} - require enhanced monitoring"
            )

    # Recommendations
    if red_flags > 0:
        insights["recommendations"].append(
            "Immediately investigate and document action plans for all red flag findings"
        )

    if open_findings > 0:
        insights["recommendations"].append(
            "Establish clear timelines and assign ownership for resolving open findings"
        )

    if total_budget > 50000000:
        insights["recommendations"].append(
            "Prioritize high-value findings to minimize financial risk exposure"
        )

    # Entity-specific recommendations
    if analysis.get('top_entities_by_budget'):
        top_entities = analysis['top_entities_by_budget'].get('entities', [])
        if len(top_entities) > 3:
            insights["recommendations"].append(
                f"Conduct training sessions for the {len(top_entities)} entities with findings to prevent recurrence"
            )

    # Checklist-specific recommendations
    if analysis.get('checklist_analysis'):
        checklist_data = {k: v for k, v in analysis['checklist_analysis'].items()
                          if k != 'description' and isinstance(v, dict)}
        low_completion = [data for data in checklist_data.values()
                          if data.get('completion_rate', 0) < 50]
        if low_completion:
            insights["recommendations"].append(
                "Focus resources on checklists with low completion rates to improve overall compliance"
            )

    return insights
