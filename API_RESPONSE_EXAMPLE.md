# 📖 Complete API Response Example

## Full Response Structure (v2.1.0)

This document shows the complete API response with all new features using your actual sample data.

---

## Request

```bash
POST http://localhost:8000/api/analyze
Content-Type: multipart/form-data

file: audit_data.xlsx
```

---

## Complete Response

```json
{
  "status": "success",
  "sheets_analyzed": 1,

  "overall_summary": {
    "total_records_analyzed": 1,
    "overall_compliance_rate": 0.0,
    "total_open_findings": 1,
    "total_high_risk_findings": 1,
    "total_red_flags": 0,
    "sheets_processed": 1
  },

  "results": {
    "Sheet1": {
      "analysis": {
        // === BASIC METRICS ===
        "total_records": 1,
        "average_compliance": 0.0,
        "open_findings": 1,
        "closed_findings": 0,
        "high_risk_findings": 1,
        "medium_risk_findings": 0,
        "low_risk_findings": 0,
        "red_flag_count": 0,

        // === AUDIT TYPE & CATEGORY ===
        "audit_type_breakdown": {
          "TENDERING": 1
        },
        "category_breakdown": {
          "PA": 1
        },

        // === COMPLIANCE DISTRIBUTION ===
        "compliance_distribution": {
          "excellent": 0, // >= 90%
          "good": 0, // 75-89%
          "fair": 0, // 50-74%
          "poor": 1 // < 50%
        },

        // === FINANCIAL ANALYSIS ===
        "financial_analysis": {
          "total_budget": 92100000.0,
          "average_budget": 92100000.0,
          "budget_at_risk": 92100000.0,
          "budget_at_risk_percentage": 100.0
        },

        // === SCORE ANALYSIS ===
        "score_analysis": {
          "total_expected_score": 4.0,
          "total_actual_score": 0.0,
          "total_score_gap": 4.0,
          "score_achievement_rate": 0.0
        },

        // === TOP ENTITIES ===
        "top_entities": {
          "Supply of office furniture at BOT Mtwara Branch": 1
        },

        // === CHECKLIST BREAKDOWN ===
        "checklist_breakdown": {
          "Tathimini na kubaini iwapo mahitaji...": 1
        },

        // ============================================
        // === NEW ADVANCED ANALYSIS (v2.1.0) ===
        // ============================================

        // === 1️⃣ PE NAME ANALYSIS ===
        "pe_name_analysis": {
          "BOT - BANK OF TANZANIA - MTWARA BRANCH": {
            "total_findings": 1,
            "open_findings": 1,
            "closed_findings": 0,
            "average_compliance": 0.0,
            "total_budget": 92100000.0,
            "high_risk_findings": 1,
            "red_flags": 0,
            "pe_category": "PA"
          }
        },

        // === 2️⃣ CHECKLIST DETAILED ANALYSIS ===
        "checklist_detailed_analysis": {
          "Tathimini na kubaini iwapo mahitaji /hadidu za rejea/michoro na usanifu hazina upendelep": {
            "total_findings": 1,
            "open_findings": 1,
            "closed_findings": 0,
            "average_compliance": 0.0,
            "total_score_gap": 4.0,
            "audit_type": "TENDERING"
          }
        },

        // === 3️⃣ ENTITY ANALYSIS (Name + Number Combined) ===
        "entity_analysis": {
          "Supply of office furniture at BOT Mtwara Branch (TR152/005/2024/2025/G/06)": {
            "total_findings": 1,
            "open_findings": 1,
            "closed_findings": 0,
            "average_compliance": 0.0,
            "total_budget": 92100000.0,
            "budget_at_risk": 92100000.0,
            "high_risk": 1,
            "medium_risk": 0,
            "low_risk": 0
          }
        },

        // === 4️⃣ STATUS DETAILED ANALYSIS ===
        "status_detailed_analysis": {
          "OPEN": {
            "count": 1,
            "average_compliance": 0.0,
            "total_budget": 92100000.0,
            "total_score_gap": 4.0,
            "high_risk_count": 1,
            "red_flag_count": 0,
            "audit_type_distribution": {
              "TENDERING": 1
            }
          },
          "CLOSED": {
            "count": 0,
            "average_compliance": 0.0,
            "total_budget": 0.0,
            "total_score_gap": 0.0,
            "high_risk_count": 0,
            "red_flag_count": 0,
            "audit_type_distribution": {}
          }
        },

        // === 5️⃣ BUDGET DISTRIBUTION ===
        "budget_distribution": {
          "total_budget": 92100000.0,
          "budget_range_distribution": {
            "< 10M": 0,
            "10M - 50M": 0,
            "50M - 100M": 1,
            "> 100M": 0
          },
          "top_budget_items": [
            {
              "entity": "Supply of office furniture at BOT Mtwara Branch",
              "budget": 92100000.0,
              "status": "OPEN",
              "compliance": 0.0,
              "percentage_of_total": 100.0
            }
          ],
          "budget_by_pe": {
            "BOT - BANK OF TANZANIA - MTWARA BRANCH": 92100000.0
          }
        }
      },

      // === FORMATTED SUMMARY ===
      "summary": "Sheet1 Analysis Report:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📊 Total Records: 1\n✅ Average Compliance: 0.0%\n🔴 Open Findings: 1\n🟢 Closed Findings: 0\n\n🎯 Risk Distribution:\n  • High Risk: 1\n  • Medium Risk: 0\n  • Low Risk: 0\n\n📈 Compliance Distribution:\n  • Excellent (≥90%): 0\n  • Good (75-89%): 0\n  • Fair (50-74%): 0\n  • Poor (<50%): 1\n\n🎯 Score Analysis:\n  • Total Expected: 4.0\n  • Total Actual: 0.0\n  • Score Gap: 4.0\n  • Achievement Rate: 0.0%\n\n💰 Financial Overview:\n  • Total Budget: TZS 92,100,000.00\n  • Budget at Risk: TZS 92,100,000.00 (100.0%)\n\n📋 Status Detailed Analysis:\n\n  🔴 OPEN Findings (1):\n    • Avg Compliance: 0.0%\n    • Total Budget: TZS 92,100,000.00\n    • High Risk: 1\n    • Red Flags: 0\n\n  🟢 CLOSED Findings (0):\n    • Avg Compliance: 0.0%\n    • Total Budget: TZS 0.00\n\n🏢 Analysis by Public Entity (1 entities):\n\n  • BOT - BANK OF TANZANIA - MTWARA BRANCH:\n    - Total Findings: 1\n    - Open: 1, Closed: 0\n    - Avg Compliance: 0.0%\n    - Budget: TZS 92,100,000.00\n    - ⚠️ High Risk: 1\n\n📦 Entity Analysis (1 entities):\n\n  • Supply of office furniture at BOT Mtwara Branch (TR152/005/2024/2025/G/06):\n    - Findings: 1 (Open: 1)\n    - Budget: TZS 92,100,000.00\n    - Budget at Risk: TZS 92,100,000.00\n    - Compliance: 0.0%\n\n💵 Budget Distribution Analysis:\n  • Total Budget: TZS 92,100,000.00\n\n  Budget Ranges:\n    - 50M - 100M: 1 items\n\n  Top Budget Items:\n    • Supply of office furniture at BOT Mtwara Branch\n      Budget: TZS 92,100,000.00 (100.0% of total)\n      Status: OPEN, Compliance: 0.0%\n\n📝 Checklist Detailed Analysis (1 checklists):\n\n  • Tathimini na kubaini iwapo mahitaji /hadidu za rejea/michoro na...\n    - Findings: 1 (Open: 1)\n    - Avg Compliance: 0.0%\n    - Audit Type: TENDERING",

      // === AI-GENERATED INSIGHTS ===
      "insights": {
        "priority_actions": [
          "Immediate attention required: 1 high-risk findings need resolution",
          "Focus on 1 PEs with budgets exceeding TZS 50M",
          "1 entities have high-risk findings requiring immediate action",
          "1 checklists have more than 3 open findings"
        ],
        "positive_highlights": [],
        "areas_of_concern": [
          "High financial risk: 100.0% of budget associated with open findings",
          "Low average compliance of 0.0% requires immediate improvement plan",
          "TZS 92,100,000.00 in budget linked to open findings",
          "1 entities have budget at risk exceeding TZS 10M"
        ],
        "recommendations": [
          "Establish dedicated task force to address high volume of open findings",
          "Prioritize resolution of high-risk findings before proceeding with new initiatives",
          "Improve finding resolution - only 0.0% closure rate"
        ]
      }
    }
  }
}
```

---

## How to Access Specific Data

### Get PE Analysis

```javascript
const peAnalysis = response.results.Sheet1.analysis.pe_name_analysis;
const botFindings = peAnalysis["BOT - BANK OF TANZANIA - MTWARA BRANCH"];
console.log(`BOT has ${botFindings.total_findings} findings`);
```

### Get Entity Analysis

```javascript
const entityAnalysis = response.results.Sheet1.analysis.entity_analysis;
for (const [entityKey, data] of Object.entries(entityAnalysis)) {
  console.log(
    `${entityKey}: TZS ${data.total_budget} (${data.open_findings} open)`,
  );
}
```

### Get Status Comparison

```javascript
const statusAnalysis =
  response.results.Sheet1.analysis.status_detailed_analysis;
const openBudget = statusAnalysis.OPEN.total_budget;
const closedBudget = statusAnalysis.CLOSED.total_budget;
console.log(`Open: TZS ${openBudget}, Closed: TZS ${closedBudget}`);
```

### Get Budget Distribution

```javascript
const budgetDist = response.results.Sheet1.analysis.budget_distribution;
console.log(`Total Budget: TZS ${budgetDist.total_budget}`);
console.log("Top Items:", budgetDist.top_budget_items);
```

### Get Insights

```javascript
const insights = response.results.Sheet1.insights;
console.log("Priority Actions:");
insights.priority_actions.forEach((action) => console.log(`- ${action}`));
```

---

## Python Example

```python
import requests

# Upload and analyze
url = "http://localhost:8000/api/analyze"
files = {"file": open("audit_data.xlsx", "rb")}
response = requests.post(url, files=files)
data = response.json()

# Access PE Name Analysis
pe_analysis = data['results']['Sheet1']['analysis']['pe_name_analysis']
for pe_name, pe_data in pe_analysis.items():
    print(f"{pe_name}:")
    print(f"  Findings: {pe_data['total_findings']}")
    print(f"  Budget: TZS {pe_data['total_budget']:,}")
    print(f"  High Risk: {pe_data['high_risk_findings']}")

# Access Entity Analysis
entity_analysis = data['results']['Sheet1']['analysis']['entity_analysis']
for entity_key, entity_data in entity_analysis.items():
    print(f"{entity_key}:")
    print(f"  Budget at Risk: TZS {entity_data['budget_at_risk']:,}")
    print(f"  Compliance: {entity_data['average_compliance']}%")

# Access Status Analysis
status_analysis = data['results']['Sheet1']['analysis']['status_detailed_analysis']
open_data = status_analysis['OPEN']
closed_data = status_analysis['CLOSED']
print(f"Open: {open_data['count']} findings, TZS {open_data['total_budget']:,}")
print(f"Closed: {closed_data['count']} findings, TZS {closed_data['total_budget']:,}")

# Access Insights
insights = data['results']['Sheet1']['insights']
print("\nPriority Actions:")
for action in insights['priority_actions']:
    print(f"  • {action}")
```

---

## Notes

- All numeric values are properly typed (int/float)
- All budget amounts are in TZS (Tanzanian Shillings)
- Compliance percentages are 0-100 (not 0-1)
- Empty analyses return empty dicts `{}`
- All keys use snake_case
- Entity keys combine "Name (Number)" format

---

**This is the complete response structure for v2.1.0** ✅
