from fastapi import APIRouter, UploadFile, File  # type: ignore
from app.services.excel_reader import load_excel
from app.services.analysis_engine import analyze_sheet
from app.services.summary_engine import (
    generate_summary,
    generate_insights,
    generate_overall_summary
)

router = APIRouter()


@router.post("/analyze")
async def analyze_excel(file: UploadFile = File(...)):
    """
    Analyze uploaded Excel file with comprehensive audit metrics

    Features:
    - Compliance rate analysis
    - Risk categorization (High/Medium/Low)
    - Financial impact assessment
    - Score gap analysis
    - Red flag detection
    - Entity and checklist breakdowns
    """
    sheets = load_excel(file.file)

    results = {}

    for sheet_name, df in sheets.items():
        analysis = analyze_sheet(df)
        summary = generate_summary(sheet_name, analysis)
        insights = generate_insights(
            analysis) if 'error' not in analysis else {}

        results[sheet_name] = {
            "analysis": analysis,
            "summary": summary,
            "insights": insights
        }

    # Generate overall summary across all sheets
    overall_summary = generate_overall_summary(results)

    return {
        "status": "success",
        "sheets_analyzed": len(results),
        "overall_summary": overall_summary,
        "results": results
    }
