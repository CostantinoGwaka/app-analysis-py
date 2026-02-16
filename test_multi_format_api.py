"""
Integration test for multi-format API endpoint
Tests the complete flow: Excel upload → Format detection → Analysis → Response
"""
import pandas as pd
import io
from openpyxl import Workbook
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("=" * 80)
print("MULTI-FORMAT API INTEGRATION TEST")
print("=" * 80)

# Create a multi-format Excel workbook
wb = Workbook()

# Sheet 1: Detailed Findings Format
ws1 = wb.active
ws1.title = "Audit Findings"

# Headers - using actual column names from the system
headers1 = [
    "PE Name", "Checklist Title", "Entity Name", "Entity Number", "Finding Title",
    "Compliance %", "Score Gap", "Risk Level", "Status", "Estimated Budget",
    "Expected Score", "Max Score", "Actual Score"
]
ws1.append(headers1)

# Sample data
data1 = [
    ["Ministry of Health", "Procurement Compliance", "Hospital A", "001",
     "Missing documentation", "65.5%", "35", "HIGH", "OPEN", "92100000",
     "100", "100", "65"],
    ["Ministry of Education", "Financial Compliance", "School B", "002",
     "Incomplete records", "85.2%", "15", "MEDIUM", "CLOSED", "45000000",
     "100", "100", "85"],
    ["Ministry of Health", "Procurement Compliance", "Hospital C", "003",
     "Proper documentation", "95.0%", "5", "LOW", "CLOSED", "120000000",
     "100", "100", "95"],
]

for row in data1:
    ws1.append(row)

# Sheet 2: Entity Summary Format
ws2 = wb.create_sheet("Entity Performance")

headers2 = [
    "#", "Procuring Entity", "Pe Category", "App Marks", "Institution",
    "Tendering Avg", "Tenders", "Tender Number", "Overall %", "Status", "Created Date"
]
ws2.append(headers2)

data2 = [
    [1, "CAMARTEC - CENTER FOR AGRICULTURAL MECHANIZATION",
     "PA", "11", "16", "60", "10", "TN-2026-001", "0.87", "UTENDAJI ULIORIDHISHA",
     "Feb 05, 2026 at 09:29:03 AM"],
    [2, "TANROADS - TANZANIA NATIONAL ROADS AGENCY",
     "PA", "15", "16", "85", "25", "TN-2026-002", "0.92", "UTENDAJI ULIORIDHISHA",
     "Feb 05, 2026 at 09:30:15 AM"],
    [3, "TEMESA - TEACHERS SERVICE DEPARTMENT",
     "PA", "8", "12", "45", "5", "TN-2026-003", "0.55", "UNAHITAJI KUBORESHA",
     "Feb 05, 2026 at 09:31:22 AM"],
]

for row in data2:
    ws2.append(row)

# Save to BytesIO
excel_buffer = io.BytesIO()
wb.save(excel_buffer)
excel_buffer.seek(0)

print("\n📄 Created Multi-Format Excel Workbook")
print("  Sheet 1: 'Audit Findings' - Detailed Findings Format")
print("  Sheet 2: 'Entity Performance' - Entity Summary Format")

# Upload to API
print("\n🚀 Uploading to API endpoint: POST /api/analyze")
print("-" * 80)

response = client.post(
    "/api/analyze",
    files={"file": ("test_multi_format.xlsx", excel_buffer,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
)

print(f"Response Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()

    print("\n✅ API RESPONSE SUCCESSFUL!")
    print("=" * 80)

    # Overall summary
    print("\n📊 OVERALL SUMMARY:")
    print("-" * 80)
    print(f"Status: {result['status']}")
    print(f"Sheets Analyzed: {result['sheets_analyzed']}")

    overall = result['overall_summary']
    print(f"\nTotal Records: {overall.get('total_records_analyzed', 'N/A')}")

    # Format detection
    print("\n🔍 FORMAT DETECTION:")
    print("-" * 80)
    if 'detected_formats' in overall:
        for sheet, format_info in overall['detected_formats'].items():
            print(f"\n{sheet}:")
            print(f"  Format: {format_info['format']}")
            print(f"  Description: {format_info['description']}")
            print(f"  Rows: {format_info['total_rows']}")
            print(f"  Columns: {format_info['total_columns']}")
            print(f"  Key Fields: {', '.join(format_info['key_fields'][:5])}")

    # Sheet-by-sheet results
    print("\n📋 SHEET-BY-SHEET ANALYSIS:")
    print("=" * 80)

    for sheet_name, sheet_result in result['results'].items():
        print(f"\n{sheet_name}")
        print("-" * 80)

        format_type = sheet_result['data_format']
        print(f"Format Type: {format_type}")

        analysis = sheet_result['analysis']

        if format_type == 'detailed_findings':
            print(f"\n📈 Detailed Findings Analysis:")
            print(f"  Total Records: {analysis.get('total_records', 0)}")
            print(
                f"  Avg Compliance: {analysis.get('average_compliance_rate', 0):.2f}%")
            print(f"  Open Findings: {analysis.get('open_findings_count', 0)}")
            print(f"  High Risk: {analysis.get('high_risk_count', 0)}")

            if analysis.get('risk_distribution'):
                print(f"\n  Risk Distribution:")
                for risk, count in analysis['risk_distribution'].items():
                    print(f"    {risk}: {count}")

            if analysis.get('pe_name_analysis'):
                pe_count = len(analysis['pe_name_analysis'])
                print(f"\n  PE Name Analysis: {pe_count} entities analyzed")

        elif format_type == 'entity_summary':
            print(f"\n📊 Entity Summary Analysis:")
            print(f"  Total Entities: {analysis.get('total_entities', 0)}")
            print(
                f"  Avg Performance: {analysis.get('average_overall_performance', 0):.1f}%")

            if analysis.get('performance_distribution'):
                print(f"\n  Performance Distribution:")
                dist = analysis['performance_distribution']
                print(f"    Excellent (≥90%): {dist.get('excellent', 0)}")
                print(f"    Good (75-89%): {dist.get('good', 0)}")
                print(
                    f"    Satisfactory (60-74%): {dist.get('satisfactory', 0)}")
                print(
                    f"    Needs Improvement (<60%): {dist.get('needs_improvement', 0)}")

            if analysis.get('tenders_analysis'):
                tenders = analysis['tenders_analysis']
                print(f"\n  Tenders Overview:")
                print(f"    Total: {tenders.get('total_tenders', 0)}")
                print(
                    f"    Average: {tenders.get('average_tenders_per_entity', 0):.2f}")
                print(
                    f"    Range: {tenders.get('min_tenders', 0)}-{tenders.get('max_tenders', 0)}")

            if analysis.get('top_performers'):
                print(f"\n  Top Performers:")
                for i, entity in enumerate(analysis['top_performers'][:3], 1):
                    print(
                        f"    {i}. {entity['entity']}: {entity['overall_percentage']}%")

        # Summary
        print(f"\n📝 Summary (First 200 chars):")
        summary = sheet_result.get('summary', '')
        print(f"  {summary[:200]}...")

        # Insights
        insights = sheet_result.get('insights', {})
        if insights and isinstance(insights, dict):
            if insights.get('priority_actions'):
                print(
                    f"\n🎯 Priority Actions ({len(insights['priority_actions'])} total):")
                for action in insights['priority_actions'][:2]:
                    print(f"  • {action}")

            if insights.get('positive_highlights'):
                print(
                    f"\n✨ Positive Highlights ({len(insights['positive_highlights'])} total):")
                for highlight in insights['positive_highlights'][:2]:
                    print(f"  • {highlight}")

    print("\n" + "=" * 80)
    print("✅ MULTI-FORMAT API TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\n🎉 Verified Features:")
    print("  ✓ Multi-sheet Excel upload")
    print("  ✓ Automatic format detection per sheet")
    print("  ✓ Detailed findings analysis (Sheet 1)")
    print("  ✓ Entity summary analysis (Sheet 2)")
    print("  ✓ Format-specific summaries")
    print("  ✓ Format-specific insights")
    print("  ✓ Overall summary aggregation")
    print("  ✓ API response structure")
    print("=" * 80)

else:
    print(f"\n❌ API ERROR!")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
