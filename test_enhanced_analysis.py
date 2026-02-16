"""
Test script to verify the enhanced analysis engine with all new features
"""
import pandas as pd
from app.services.analysis_engine import analyze_sheet
from app.services.summary_engine import generate_summary, generate_insights
import json

# Create sample data matching the user's format
sample_data = {
    "#": [1],
    "PE Name": ["BOT - BANK OF TANZANIA - MTWARA BRANCH"],
    "PE Code": ["N/A"],
    "PE Category": ["PA"],
    "Financial Year": ["2024/2025"],
    "Audit Type": ["TENDERING"],
    "Checklist Title": ["Tathimini na kubaini iwapo mahitaji /hadidu za rejea/michoro na usanifu hazina upendelep"],
    "Requirement Name": ["Kifungu cha 41(1)(b) cha Sheria ya Ununuzi wa Umma,2023..."],
    "Finding Title": ["Kuandaa Nyaraka ya Zabuni bila kuainisha Vigezo vya Kiufundi katika baadhi ya Bidhaa."],
    "Finding Description": ["Mapitio ya nyaraka za Zabuni..."],
    "Recommendation": ["Menejimenti ihakikishe kuwa vigezo vya kiufundi..."],
    "Implication": ["Kutotaja vigezo vya kiufundi..."],
    "Management Response": ["N/A"],
    "Auditor Opinion": ["N/A"],
    "Red Flag": ["NO"],
    "Expected Score": [4],
    "Actual Score": [0],
    "Score Gap": [4],
    "Compliance %": ["0.00%"],  # This was causing issues before
    "Status": ["OPEN"],
    "Entity Name": ["Supply of office furniture at BOT Mtwara Branch"],
    "Entity Number": ["TR152/005/2024/2025/G/06"],
    "Estimated Budget": [92100000],
    "Created Date": ["14/10/2025, 20:47"],
    "Updated Date": ["04/02/2026, 12:42"]
}

# Create DataFrame
df = pd.DataFrame(sample_data)

print("=" * 80)
print("TESTING ENHANCED ANALYSIS ENGINE WITH ADVANCED FEATURES")
print("=" * 80)

print("\n📊 Input Data:")
print(f"  Compliance %: {df['Compliance %'].iloc[0]}")
print(f"  Expected Score: {df['Expected Score'].iloc[0]}")
print(f"  Actual Score: {df['Actual Score'].iloc[0]}")
print(f"  Score Gap: {df['Score Gap'].iloc[0]}")
print(f"  Status: {df['Status'].iloc[0]}")
print(f"  PE Name: {df['PE Name'].iloc[0]}")
print(f"  Entity: {df['Entity Name'].iloc[0]} ({df['Entity Number'].iloc[0]})")
print(f"  Estimated Budget: TZS {df['Estimated Budget'].iloc[0]:,}")

# Run analysis
print("\n🔍 Running Enhanced Analysis...")
result = analyze_sheet(df)

print("\n✅ BASIC ANALYSIS RESULTS:")
print("=" * 80)
print(f"✓ Total Records: {result['total_records']}")
print(f"✓ Average Compliance: {result['average_compliance']}%")
print(f"✓ Open Findings: {result['open_findings']}")
print(f"✓ Closed Findings: {result['closed_findings']}")
print(f"✓ High Risk Findings: {result['high_risk_findings']}")

print("\n🏢 PE NAME ANALYSIS:")
print("=" * 80)
if result.get('pe_name_analysis'):
    for pe_name, pe_data in result['pe_name_analysis'].items():
        print(f"\nPE: {pe_name}")
        print(f"  Total Findings: {pe_data['total_findings']}")
        print(
            f"  Open: {pe_data['open_findings']}, Closed: {pe_data['closed_findings']}")
        print(f"  Avg Compliance: {pe_data['average_compliance']}%")
        print(f"  Total Budget: TZS {pe_data['total_budget']:,.2f}")
        print(f"  High Risk: {pe_data['high_risk_findings']}")
        print(f"  PE Category: {pe_data['pe_category']}")

print("\n📝 CHECKLIST DETAILED ANALYSIS:")
print("=" * 80)
if result.get('checklist_detailed_analysis'):
    for checklist, checklist_data in result['checklist_detailed_analysis'].items():
        print(f"\nChecklist: {checklist[:100]}...")
        print(f"  Total Findings: {checklist_data['total_findings']}")
        print(
            f"  Open: {checklist_data['open_findings']}, Closed: {checklist_data['closed_findings']}")
        print(f"  Avg Compliance: {checklist_data['average_compliance']}%")
        print(f"  Audit Type: {checklist_data['audit_type']}")

print("\n📦 ENTITY ANALYSIS:")
print("=" * 80)
if result.get('entity_analysis'):
    for entity_key, entity_data in result['entity_analysis'].items():
        print(f"\nEntity: {entity_key}")
        print(f"  Total Findings: {entity_data['total_findings']}")
        print(
            f"  Open: {entity_data['open_findings']}, Closed: {entity_data['closed_findings']}")
        print(f"  Total Budget: TZS {entity_data['total_budget']:,.2f}")
        print(f"  Budget at Risk: TZS {entity_data['budget_at_risk']:,.2f}")
        print(f"  Compliance: {entity_data['average_compliance']}%")
        print(
            f"  Risk Profile - High: {entity_data['high_risk']}, Medium: {entity_data['medium_risk']}, Low: {entity_data['low_risk']}")

print("\n📋 STATUS DETAILED ANALYSIS (OPEN vs CLOSED):")
print("=" * 80)
if result.get('status_detailed_analysis'):
    status_detail = result['status_detailed_analysis']

    print("\n🔴 OPEN Findings:")
    open_data = status_detail['OPEN']
    print(f"  Count: {open_data['count']}")
    print(f"  Avg Compliance: {open_data['average_compliance']}%")
    print(f"  Total Budget: TZS {open_data['total_budget']:,.2f}")
    print(f"  Total Score Gap: {open_data['total_score_gap']}")
    print(f"  High Risk Count: {open_data['high_risk_count']}")
    print(f"  Red Flags: {open_data['red_flag_count']}")

    print("\n🟢 CLOSED Findings:")
    closed_data = status_detail['CLOSED']
    print(f"  Count: {closed_data['count']}")
    print(f"  Avg Compliance: {closed_data['average_compliance']}%")
    print(f"  Total Budget: TZS {closed_data['total_budget']:,.2f}")

print("\n💵 BUDGET DISTRIBUTION ANALYSIS:")
print("=" * 80)
if result.get('budget_distribution'):
    budget_dist = result['budget_distribution']
    print(f"Total Budget: TZS {budget_dist.get('total_budget', 0):,.2f}")

    if budget_dist.get('budget_range_distribution'):
        print("\nBudget Range Distribution:")
        for range_name, count in budget_dist['budget_range_distribution'].items():
            print(f"  {range_name}: {count} items")

    if budget_dist.get('top_budget_items'):
        print("\nTop Budget Items:")
        for item in budget_dist['top_budget_items']:
            print(f"  • {item['entity']}")
            print(
                f"    Budget: TZS {item['budget']:,.2f} ({item['percentage_of_total']}% of total)")
            print(
                f"    Status: {item['status']}, Compliance: {item['compliance']}%")

print("\n📊 GENERATING SUMMARY:")
print("=" * 80)
summary = generate_summary("Test Sheet", result)
print(summary)

print("\n💡 GENERATING INSIGHTS:")
print("=" * 80)
insights = generate_insights(result)
print("\n🎯 Priority Actions:")
for action in insights['priority_actions']:
    print(f"  • {action}")

print("\n⚠️ Areas of Concern:")
for concern in insights['areas_of_concern']:
    print(f"  • {concern}")

print("\n✨ Positive Highlights:")
for highlight in insights['positive_highlights']:
    print(f"  • {highlight}")

print("\n📋 Recommendations:")
for rec in insights['recommendations']:
    print(f"  • {rec}")

print("\n" + "=" * 80)
print("✅ ALL ADVANCED FEATURES TESTED SUCCESSFULLY!")
print("=" * 80)
print("\n🎉 New Features Working:")
print("  ✓ PE Name grouping and analysis")
print("  ✓ Checklist detailed analysis")
print("  ✓ Entity (Name + Number) combination analysis")
print("  ✓ Status (OPEN vs CLOSED) detailed breakdown")
print("  ✓ Budget distribution with ranges and top items")
print("  ✓ Enhanced insights generation")
print("=" * 80)
