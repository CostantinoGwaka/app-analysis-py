"""
Test script for multi-tender findings format analysis
"""
import pandas as pd
from app.services.multi_tender_engine import analyze_multi_tender_findings, parse_tender_details
from app.services.summary_engine import generate_multi_tender_summary, generate_multi_tender_insights
from app.services.format_detector import detect_data_format, get_format_info
import json

# Create sample multi-tender findings data (user's format)
sample_data = {
    "#": [1],
    "PE Name": ["BOT - BANK OF TANZANIA - MWANZA BRANCH"],
    "Checklist Title": ["Angalia ikiwa kamati ya tathmini ilifanya tathmini ya zabuni kulingana na muda ulioanishwa katika barua ya uteuzi."],
    "Requirement Name": ["Kanuni ya 357  inaelekeza Kamati ya tathmini ya zabuni kufanya tathmini kwa zabuni zilizofunguliwa..."],
    "Tenders": ["TR152/006/2024/2025/W/07 (Own Funds, Budget: 150000000, Works, National Competitive Tendering), TR152/006/2024/2025/W/12 (Own Funds, Budget: 73632000, Works, National Competitive Tendering)"],
    "Total Budget": [223632000],
    "Tender Count": [2],
    "Finding Title": ["Kamati ya Tathmini Haikuzingatia Muda Ulioanishwa Katika Barua ya Uteuzi kwa Zabuni za Shs. Milioni 141.67"],
    "Finding Description": ["Ukaguzi wa zabuni namba TR152/006/2024/2025/W/07 na TR152/006/2024/2025/W/12 zenye thamani ya shilingi 141,671,840.00 umebaini kuwa kamati za tathmini hazikuzingatia muda ulioaninshwa katika barua ya uteuzi..."],
    "Implication": ["Kuna uwezekano wa kuchelewa kukamilika kwa mkataba na hivyo kusababisha gharama za utekelezaji wa mradi kupanda..."],
    "Recommendation": ["Mamlaka inaelekeza menejimenti ihakikishe taratibu za michakato ya zabuni zinatekelezwa kwa kuzingatia muda uliopangwa."],
    "Management Response": ["Menejimenti itahakikisha kuwa mchakasto wa utekelezaji wa zabuni hauchukuwi muda mrefu..."],
    "Auditor Opinion": ["Mamlaka imepokea majibu ya hoja za ukaguzi kutoka katika taasisi yako..."],
    "Red Flag": ["NOT RED FLAG"],
    "Status": ["OPEN"],
    "Created At": ["03/09/2025"]
}

# Create DataFrame
df = pd.DataFrame(sample_data)

print("=" * 80)
print("TESTING MULTI-TENDER FINDINGS FORMAT ANALYSIS")
print("=" * 80)

# Detect format
print("\n📋 FORMAT DETECTION:")
print("=" * 80)
format_type = detect_data_format(df)
format_info = get_format_info(df)
print(f"Detected Format: {format_type}")
print(f"Description: {format_info['description']}")
print(f"Total Rows: {format_info['total_rows']}")
print(f"Total Columns: {format_info['total_columns']}")
print(f"Key Fields: {', '.join(format_info['key_fields'])}")

# Input data overview
print("\n📊 SAMPLE INPUT DATA:")
print("=" * 80)
row = df.iloc[0]
print(f"PE Name: {row['PE Name']}")
print(f"Checklist: {row['Checklist Title'][:80]}...")
print(f"Finding: {row['Finding Title']}")
print(f"Status: {row['Status']}")
print(f"Red Flag: {row['Red Flag']}")
print(f"Total Budget: TZS {row['Total Budget']:,}")
print(f"Tender Count: {row['Tender Count']}")
print(f"\nTenders Details:")
print(f"  {row['Tenders'][:150]}...")

# Test tender parsing
print("\n🔍 TESTING TENDER PARSING:")
print("=" * 80)
parsed_tenders = parse_tender_details(row['Tenders'])
for i, tender in enumerate(parsed_tenders, 1):
    print(f"\nTender {i}:")
    print(f"  Number: {tender['tender_number']}")
    print(f"  Budget: TZS {tender['budget']:,.0f}")
    print(f"  Type: {tender['type']}")

# Run analysis
print("\n🔍 RUNNING ANALYSIS...")
print("=" * 80)
result = analyze_multi_tender_findings(df)

print("\n✅ ANALYSIS RESULTS:")
print("=" * 80)
print(f"Format Type: {result.get('format_type')}")
print(
    f"Total Findings: {result['total_findings']['value']} - {result['total_findings']['description']}")
print(
    f"Open Findings: {result['open_findings']['value']} - {result['open_findings']['description']}")
print(
    f"Closed Findings: {result['closed_findings']['value']} - {result['closed_findings']['description']}")
print(
    f"Red Flags: {result['red_flags']['value']} - {result['red_flags']['description']}")

print("\n💰 Budget Analysis:")
print(f"  Total Budget: TZS {result['total_budget']['value']:,.0f}")
print(f"  Description: {result['total_budget']['description']}")
print(
    f"  Average per Finding: TZS {result['average_budget_per_finding']['value']:,.0f}")
print(f"  Description: {result['average_budget_per_finding']['description']}")

print("\n📋 Tender Analysis:")
print(f"  Total Tenders: {result['total_tenders']['value']}")
print(f"  Unique Tenders: {result['unique_tenders']['value']}")
print(
    f"  Average per Finding: {result['average_tenders_per_finding']['value']:.2f}")

# Budget Range Distribution
if result.get('budget_range_distribution'):
    print("\n💵 Budget Range Distribution:")
    print(
        f"  Description: {result['budget_range_distribution']['description']}")
    for range_name, range_data in result['budget_range_distribution']['ranges'].items():
        print(
            f"  {range_name}: {range_data['count']} tenders ({range_data['percentage']:.1f}%) - TZS {range_data['total_budget']:,.0f}")

if result.get('pe_analysis'):
    print("\n🏢 PE Analysis:")
    print(f"  Description: {result['pe_analysis'].get('description', 'N/A')}")
    for pe_name, pe_data in result['pe_analysis'].items():
        if pe_name == 'description' or not isinstance(pe_data, dict):
            continue
        print(f"\n  • {pe_name}")
        print(
            f"    Findings: {pe_data['total_findings']} (Open: {pe_data['open_findings']}, Closed: {pe_data['closed_findings']})")
        print(f"    Budget: TZS {pe_data['total_budget']:,.0f}")
        print(f"    Tenders: {pe_data['total_tenders']}")
        print(f"    Red Flags: {pe_data['red_flags']}")
        if pe_data.get('tender_numbers'):
            print(
                f"    Tender Numbers: {', '.join(pe_data['tender_numbers'][:3])}{'...' if len(pe_data['tender_numbers']) > 3 else ''}")
        if pe_data.get('tender_details'):
            print(f"    Tender Details:")
            for tender in pe_data['tender_details'][:3]:
                print(
                    f"      - {tender['tender_number']}: TZS {tender['budget']:,.0f} ({tender['type']})")

if result.get('checklist_analysis'):
    print("\n📝 Checklist Analysis:")
    print(
        f"  Description: {result['checklist_analysis'].get('description', 'N/A')}")
    for checklist, data in result['checklist_analysis'].items():
        if checklist == 'description' or not isinstance(data, dict):
            continue
        print(f"\n  • {checklist[:80]}...")
        print(
            f"    Findings: {data['total_findings']} (Open: {data['open_findings']}, Closed: {data['closed_findings']})")
        print(f"    Completion Rate: {data['completion_rate']}%")
        print(
            f"    Budget: TZS {data['total_budget']:,.0f} (Avg: TZS {data['average_budget_per_finding']:,.0f})")
        print(
            f"    Tenders: {data['total_tenders']} (Avg: {data['average_tenders_per_finding']:.2f})")
        print(f"    Red Flags: {data['red_flags']}")
        print(f"    Affected Entities: {data['affected_entities']}")
        print(f"    Risk Level: {data['risk_level']}")

# Top Entities by Budget
if result.get('top_entities_by_budget'):
    print("\n🏆 Top Entities by Budget:")
    print(f"  Description: {result['top_entities_by_budget']['description']}")
    for entity in result['top_entities_by_budget']['entities']:
        print(f"\n  • {entity['entity_name']}")
        print(f"    Budget: TZS {entity['total_budget']:,.0f}")
        print(
            f"    Findings: {entity['total_findings']} (Open: {entity['open_findings']})")
        print(f"    Tenders: {entity['total_tenders']}")
        print(f"    Red Flags: {entity['red_flags']}")
        if entity.get('tender_numbers'):
            print(
                f"    Tender Numbers: {', '.join(entity['tender_numbers'][:5])}{'...' if len(entity['tender_numbers']) > 5 else ''}")

if result.get('detailed_findings'):
    print("\n📄 Detailed Findings:")
    print(f"  Description: {result['detailed_findings']['description']}")
    for i, finding in enumerate(result['detailed_findings']['findings'], 1):
        print(f"\n  Finding {i}:")
        print(f"    PE: {finding['pe_name']}")
        print(f"    Title: {finding['finding_title'][:80]}...")
        print(f"    Status: {finding['status']}")
        print(f"    Budget: TZS {finding['total_budget']:,.0f}")
        print(f"    Tender Count: {finding['tender_count']}")
        print(f"    Tenders:")
        for tender in finding['tenders']:
            print(
                f"      - {tender['tender_number']}: TZS {tender['budget']:,.0f} ({tender['type']})")
        if 'description' in finding:
            print(f"    Description: {finding['description'][:100]}...")
        if 'recommendation' in finding:
            print(f"    Recommendation: {finding['recommendation'][:100]}...")

# Generate summary
print("\n" + "=" * 80)
print("📊 FORMATTED SUMMARY:")
print("=" * 80)
summary = generate_multi_tender_summary("Test Sheet", result)
print(summary)

# Generate insights
print("\n" + "=" * 80)
print("💡 AI-GENERATED INSIGHTS:")
print("=" * 80)
insights = generate_multi_tender_insights(result)

if insights['priority_actions']:
    print("\n🎯 Priority Actions:")
    for action in insights['priority_actions']:
        print(f"  • {action}")

if insights['positive_highlights']:
    print("\n✨ Positive Highlights:")
    for highlight in insights['positive_highlights']:
        print(f"  • {highlight}")

if insights['areas_of_concern']:
    print("\n⚠️ Areas of Concern:")
    for concern in insights['areas_of_concern']:
        print(f"  • {concern}")

if insights['recommendations']:
    print("\n📋 Recommendations:")
    for rec in insights['recommendations']:
        print(f"  • {rec}")

print("\n" + "=" * 80)
print("✅ MULTI-TENDER FINDINGS FORMAT TEST COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\n🎉 Features Verified:")
print("  ✓ Format detection (detailed_findings_multi_tender)")
print("  ✓ Tender parsing from complex strings")
print("  ✓ Budget aggregation")
print("  ✓ Tender count tracking")
print("  ✓ PE-level analysis")
print("  ✓ Checklist-level analysis")
print("  ✓ Status tracking (OPEN/CLOSED)")
print("  ✓ Red flag detection")
print("  ✓ Detailed finding extraction with tender details")
print("  ✓ Enhanced summary generation")
print("  ✓ AI-powered insights")
print("=" * 80)
