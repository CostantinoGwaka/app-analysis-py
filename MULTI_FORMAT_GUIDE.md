# Multi-Format Excel Analysis Guide

## Overview

The analysis system (v2.2.0+) automatically detects and processes **three different Excel data formats**:

1. **Detailed Findings Format** - Individual audit findings with compliance metrics
2. **Multi-Tender Findings Format** - Findings with multiple tenders per row
3. **Entity Summary Format** - Aggregated entity-level performance data

---

## Format Detection

The system uses intelligent column-based detection to identify your data format:

### Detection Process

```python
# Automatic - no user action required!
# The system checks column names and chooses the right analysis engine
```

### Supported Formats

#### 1️⃣ Detailed Findings Format

**Required Columns:**

- `Compliance %` - Compliance percentage (e.g., "75.5%" or 75.5)
- `Score Gap` - Gap between expected and actual scores
- `Status` - Finding status (OPEN/CLOSED)
- `Checklist Title` - Title of the audit checklist

**Optional Columns:**

- `PE Name` - Procuring Entity name
- `Entity Name` - Entity name
- `Entity Number` - Entity number
- `Risk Level` - HIGH, MEDIUM, or LOW
- `Estimated Budget` - Budget amount
- `Expected Score` - Expected score value
- `Actual Score` - Score achieved
- `Max Score` - Maximum possible score
- `Red Flag` - Red flag indicator (YES/NO)
- `Audit Type` - Type of audit
- `PE Category` - Public Entity category
- `Financial Year` - Audit financial year
- `Finding Title`, `Finding Description` - Finding details
- `Recommendation`, `Implication`, `Management Response` - Additional info

**Example Data:**

```csv
PE Name,Checklist Title,Entity Name,Entity Number,Finding Title,Compliance %,Score Gap,Risk Level,Status,Estimated Budget
Ministry of Health,Procurement Compliance,Hospital A,001,Missing documentation,65.5%,35,HIGH,OPEN,92100000
Ministry of Education,Financial Compliance,School B,002,Incomplete records,85.2%,15,MEDIUM,CLOSED,45000000
```

**Analysis Features:**

- ✅ Overall compliance rates
- ✅ Risk distribution (HIGH/MEDIUM/LOW)
- ✅ Financial impact assessment
- ✅ Score gap analysis
- ✅ Grouping by PE Name
- ✅ Grouping by Checklist
- ✅ Grouping by Entity (Name + Number)
- ✅ Status comparison (OPEN vs CLOSED)
- ✅ Budget distribution analysis
- ✅ Red flag detection

---

#### 2️⃣ Multi-Tender Findings Format

**Required Columns:**

- `PE Name` - Procuring Entity name
- `Checklist Title` - Audit checklist title
- `Tenders` - Comma-separated tender details with budgets
- `Total Budget` - Total budget for all tenders in the finding
- `Tender Count` - Number of tenders associated with the finding
- `Finding Title` - Title of the audit finding
- `Status` - OPEN or CLOSED
- `Red Flag` - Red flag status ("RED FLAG", "NOT RED FLAG", "YES", "NO")

**Optional Columns:**

- `Finding Description` - Detailed description of the finding
- `Implication` - Impact/implication of the finding
- `Recommendation` - Auditor recommendation
- `Management Response` - Response from management
- `Auditor Opinion` - Auditor's opinion on the response
- `Requirement Name` - Regulatory requirement reference
- `Created At` - Date created

**Example Data:**

```csv
PE Name,Checklist Title,Tenders,Total Budget,Tender Count,Finding Title,Status,Red Flag
BOT - BANK OF TANZANIA - MWANZA BRANCH,Evaluation Committee Compliance,"TR152/006/2024/2025/W/07 (Budget: 150000000, Works), TR152/006/2024/2025/W/12 (Budget: 73632000, Works)",223632000,2,Committee Did Not Follow Timeline,OPEN,NOT RED FLAG
```

**Tender Format within Column:**
Each tender can include:

- Tender Number (e.g., TR152/006/2024/2025/W/07)
- Budget amount
- Type (Works, Goods, Services)
- Other details in parentheses

**Analysis Features:**

- ✅ Automatic tender parsing from complex strings
- ✅ Budget aggregation per finding and per PE
- ✅ Tender count tracking
- ✅ PE-level grouping with metrics
- ✅ Checklist-level analysis
- ✅ Status tracking (OPEN/CLOSED)
- ✅ Red flag detection (excludes "NOT RED FLAG")
- ✅ Detailed tender breakdown per finding
- ✅ Multi-tender support per finding

---

#### 3️⃣ Entity Summary Format

**Required Columns:**

- `Procuring Entity` - Entity name
- `Overall %` - Overall performance percentage
- `Tenders` - Number of tenders
- `Status` - Performance status

**Optional Columns:**

- `Pe Category` - Entity category
- `App Marks` - Application marks
- `Institution` - Institution score
- `Tendering Avg` - Average tendering performance
- `Tender Number` - Tender reference number or ID
- `Created Date` - Date created

**Example Data:**

```csv
Procuring Entity,Pe Category,Overall %,Tenders,Tender Number,Tendering Avg,Status
TANROADS - TANZANIA NATIONAL ROADS AGENCY,PA,0.92,25,TN-2026-002,85,UTENDAJI ULIORIDHISHA
CAMARTEC - CENTER FOR AGRICULTURAL MECHANIZATION,PA,0.87,10,TN-2026-001,60,UTENDAJI ULIORIDHISHA
TEMESA - TEACHERS SERVICE DEPARTMENT,PA,0.55,5,TN-2026-003,45,UNAHITAJI KUBORESHA
```

**Note:** Overall % can be in decimal format (0.87) or percentage format (87%) - the system automatically detects and converts!

**Analysis Features:**

- ✅ Average overall performance
- ✅ Performance distribution (4 levels)
- ✅ Top/bottom performer identification
- ✅ Tenders analysis (total, average, range)
- ✅ Tendering performance scoring
- ✅ Tender number tracking
- ✅ Category-based grouping
- ✅ Status distribution
- ✅ Detailed entity-level metrics

---

## API Response Structure

### Successful Analysis

```json
{
  "status": "success",
  "sheets_analyzed": 2,
  "overall_summary": {
    "total_sheets": 2,
    "detected_formats": {
      "Sheet1": {
        "format": "detailed_findings",
        "description": "Individual audit findings with compliance metrics",
        "total_rows": 150,
        "total_columns": 12,
        "key_fields": ["Finding", "Compliance Rate", "Risk Level"]
      },
      "Sheet2": {
        "format": "entity_summary",
        "description": "Aggregated entity-level summary with overall performance",
        "total_rows": 45,
        "total_columns": 10,
        "key_fields": ["Procuring Entity", "Overall %", "Tenders", "Status"]
      }
    }
  },
  "results": {
    "Sheet1": {
      "data_format": "detailed_findings",
      "format_info": { ... },
      "analysis": { ... },
      "summary": "...",
      "insights": { ... }
    },
    "Sheet2": {
      "data_format": "entity_summary",
      "format_info": { ... },
      "analysis": { ... },
      "summary": "...",
      "insights": { ... }
    }
  }
}
```

---

## Data Cleaning Features

### Percentage Handling

The system automatically handles multiple percentage formats:

```python
# Input → Output
"75.5%" → 75.5
"0.87"  → 87.0   # Decimal auto-converted to percentage
75.5    → 75.5   # Already numeric
"  85% " → 85.0  # Whitespace trimmed
```

### Numeric Handling

Commas and formatting are automatically cleaned:

```python
# Input → Output
"92,100,000" → 92100000.0
"1,234.56"   → 1234.56
"  1000  "   → 1000.0
```

---

## Performance Distribution Levels

### Entity Summary Format

Performance is categorized into **4 levels**:

- 🌟 **Excellent**: ≥ 90%
- ✅ **Good**: 75-89%
- ⚠️ **Satisfactory**: 60-74%
- 🔴 **Needs Improvement**: < 60%

### Detailed Findings Format

Risk levels are categorized:

- 🔴 **HIGH**: Critical compliance issues
- 🟡 **MEDIUM**: Moderate compliance issues
- 🟢 **LOW**: Minor compliance issues

---

## Testing the System

### Test Detailed Findings Format

```bash
python test_enhanced_analysis.py
```

### Test Entity Summary Format

```bash
python test_entity_summary.py
```

### Test via API

```bash
# Start the server
uvicorn app.main:app --reload

# Upload Excel file
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "accept: application/json" \
  -F "file=@your_data.xlsx"
```

---

## Mixed Format Workbooks

✅ **Supported!** You can upload an Excel file with:

- Sheet1: Detailed findings format
- Sheet2: Entity summary format
- Sheet3: Another detailed findings format
- etc.

The system detects each sheet's format independently and applies the appropriate analysis engine.

---

## Error Handling

### Unknown Format

If a sheet doesn't match either format:

```json
{
  "data_format": "unknown",
  "analysis": {
    "error": "Unknown data format. Columns found: Column1, Column2, ...",
    "format_info": { ... }
  },
  "summary": "Sheet1: Unknown format - cannot analyze",
  "insights": {}
}
```

### Missing Required Columns

```json
{
  "error": "Missing required column for detailed findings: Compliance Rate"
}
```

---

## Best Practices

### 1. Column Names

- Use exact column names as shown in examples
- Column names are **case-sensitive**
- Avoid extra spaces in column names

### 2. Data Quality

- Fill all required fields
- Use consistent date formats
- Avoid merged cells
- Keep headers in the first row

### 3. Numeric Values

- Percentages can be "75.5%" or 75.5 or 0.755
- Budget values can include commas: "92,100,000"
- Missing values are handled gracefully

### 4. File Size

- Recommended: < 10 MB per file
- Rows: Up to 100,000 per sheet
- Sheets: Unlimited (all will be analyzed)

---

## Version History

- **v2.2.0** (Current): Multi-format support with entity summary analysis
- **v2.1.0**: Enhanced grouping analysis (PE, Checklist, Entity, Status, Budget)
- **v2.0.0**: Initial enhanced analysis with 12+ metrics
- **v1.0.0**: Basic compliance analysis

---

## Support

For issues or questions:

1. Check column names match exactly
2. Verify data format matches examples
3. Review error messages in API response
4. Test with smaller sample data first

---

## Architecture

```
Excel Upload
    ↓
Format Detector (format_detector.py)
    ↓
    ├─→ Detailed Findings → analysis_engine.py
    │                        ↓
    │                    summary_engine.py (generate_summary + insights)
    │
    └─→ Entity Summary → entity_summary_engine.py
                          ↓
                      summary_engine.py (generate_entity_summary + insights)
    ↓
API Response (analyze.py)
```

---

## Example Insights Generated

### Detailed Findings Format

- Priority actions for high-risk findings
- Positive highlights for low-risk areas
- Areas of concern with specific metrics
- Actionable recommendations

### Entity Summary Format

- Top/bottom performer identification
- Performance improvement priorities
- Best practice highlighting
- Targeted training recommendations

---

🎉 **The system automatically handles both formats - just upload your Excel and it works!**
