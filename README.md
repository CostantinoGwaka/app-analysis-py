# 🔍 Audit Intelligence Engine

Advanced audit analysis platform for comprehensive compliance and risk assessment of audit findings.

## ✨ Features

### Core Analysis
- **Compliance Rate Analysis**: Calculate and track compliance percentages across audit findings
- **Risk Categorization**: Automatic classification into High/Medium/Low risk categories
- **Score Gap Analysis**: Track expected vs actual scores with achievement rates
- **Red Flag Detection**: Identify critical issues requiring immediate attention
- **Status Tracking**: Monitor open vs closed findings

### Advanced Analytics
- **Financial Impact Assessment**: Budget analysis and risk quantification
- **Audit Type Breakdown**: Distribution analysis by audit type
- **Category Analysis**: PE Category and checklist breakdowns
- **Entity Analysis**: Top entities with most findings
- **Compliance Distribution**: Excellent/Good/Fair/Poor categorization

### Data Quality
- **Pre-upload Validation**: Verify Excel structure before analysis
- **Data Quality Reports**: Missing data and duplicate detection
- **Range Validation**: Ensure values are within expected ranges
- **Smart Data Cleaning**: Automatic sanitization and normalization

### Insights & Recommendations
- **Priority Actions**: AI-generated priority tasks based on findings
- **Positive Highlights**: Recognition of good performance areas
- **Areas of Concern**: Automated identification of problem areas
- **Actionable Recommendations**: Context-aware improvement suggestions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd app-analysis-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the server
uvicorn app.main:app --reload

# Server will start at http://localhost:8000
```

### API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 📊 Required Excel Format

### Required Columns
- `Compliance %` - Compliance percentage (e.g., "75.5%" or 75.5)
- `Score Gap` - Gap between expected and actual scores
- `Status` - Finding status (OPEN/CLOSED)
- `Checklist Title` - Title of the audit checklist

### Recommended Columns (for enhanced analysis)
- `Expected Score` - Expected score value
- `Actual Score` - Actual achieved score
- `Red Flag` - Red flag indicator (YES/NO)
- `Audit Type` - Type of audit (e.g., TENDERING, FINANCIAL)
- `PE Category` - Public Entity category (e.g., PA, LGA)
- `PE Name` - Public Entity name
- `Financial Year` - Audit financial year
- `Estimated Budget` - Budget amount
- `Entity Name` - Entity or project name
- `Finding Title` - Title of the finding
- `Finding Description` - Detailed description
- `Recommendation` - Auditor recommendation
- `Implication` - Impact/implication
- `Management Response` - Response from management

## 🔌 API Endpoints

### 1. Analyze Excel File
```bash
POST /api/analyze
```

Upload and analyze an Excel file with comprehensive metrics.

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audit_data.xlsx"
```

**Response includes:**
- Total records analyzed
- Average compliance rate
- Open/closed findings count
- Risk distribution (High/Medium/Low)
- Red flag count
- Financial analysis (if budget data available)
- Score analysis (if score data available)
- Audit type and category breakdowns
- Top entities with findings
- Compliance distribution
- AI-generated insights and recommendations
- Overall summary across all sheets

### 2. Validate Excel File
```bash
POST /api/validate
```

Validate Excel structure and data quality before analysis.

**Example:**
```bash
curl -X POST "http://localhost:8000/api/validate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audit_data.xlsx"
```

**Response includes:**
- Structure validation results
- Missing columns report
- Data quality metrics
- Range validation warnings
- Duplicate detection

### 3. Preview Excel Data
```bash
POST /api/preview
```

Preview first 10 rows of each sheet.

**Example:**
```bash
curl -X POST "http://localhost:8000/api/preview" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audit_data.xlsx"
```

### 4. Get Required Columns
```bash
GET /api/columns/required
```

Get list of required and recommended columns.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/columns/required" \
  -H "accept: application/json"
```

## 📈 Sample Response

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
        "total_records": 1,
        "average_compliance": 0.0,
        "open_findings": 1,
        "closed_findings": 0,
        "high_risk_findings": 1,
        "medium_risk_findings": 0,
        "low_risk_findings": 0,
        "red_flag_count": 0,
        "score_analysis": {
          "total_expected_score": 4.0,
          "total_actual_score": 0.0,
          "total_score_gap": 4.0,
          "score_achievement_rate": 0.0
        },
        "financial_analysis": {
          "total_budget": 92100000.0,
          "average_budget": 92100000.0,
          "budget_at_risk": 92100000.0,
          "budget_at_risk_percentage": 100.0
        }
      },
      "summary": "Sheet1 Analysis Report:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📊 Total Records: 1\n...",
      "insights": {
        "priority_actions": [
          "Immediate attention required: 1 high-risk findings need resolution"
        ],
        "areas_of_concern": [
          "High financial risk: 100.0% of budget associated with open findings",
          "Low average compliance of 0.0% requires immediate improvement plan"
        ],
        "recommendations": [
          "Prioritize resolution of high-risk findings before proceeding with new initiatives"
        ]
      }
    }
  }
}
```

## 🔧 Development

### Project Structure
```
app-analysis-py/
├── app/
│   ├── main.py                 # FastAPI application setup
│   ├── api/
│   │   ├── analyze.py         # Analysis endpoints
│   │   └── validate.py        # Validation endpoints
│   ├── models/
│   │   └── response_models.py # Pydantic models
│   └── services/
│       ├── analysis_engine.py  # Core analysis logic
│       ├── excel_reader.py     # Excel file handling
│       ├── summary_engine.py   # Summary generation
│       └── data_validator.py   # Data validation utilities
├── requirements.txt
└── README.md
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Run tests
pytest

# With coverage
pytest --cov=app
```

## 🐛 Troubleshooting

### Issue: "0" values in analysis results

**Cause**: Percentage values in Excel contain "%" symbol (e.g., "75.5%")

**Solution**: The engine now automatically handles percentage symbols. Ensure your Excel file has:
- Compliance % column with values like "75.5%" or 75.5
- Numeric columns without excessive formatting

### Issue: Missing columns error

**Cause**: Excel file doesn't have required columns

**Solution**: Ensure these columns exist:
- Compliance %
- Score Gap
- Status
- Checklist Title

Use the `/api/validate` endpoint to check before analysis.

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, email support@auditintel.com or create an issue in the repository.

---

**Version**: 2.0.0  
**Last Updated**: February 2026
