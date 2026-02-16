from fastapi import APIRouter, UploadFile, File  # type: ignore
from app.services.excel_reader import load_excel
from app.services.analysis_engine import analyze_sheet
from app.services.entity_summary_engine import analyze_entity_summary
from app.services.multi_tender_engine import analyze_multi_tender_findings
from app.services.format_detector import detect_data_format, get_format_info
from app.services.summary_engine import (
    generate_summary,
    generate_insights,
    generate_overall_summary,
    generate_entity_summary,
    generate_entity_insights,
    generate_multi_tender_summary,
    generate_multi_tender_insights
)

router = APIRouter()


@router.post("/analyze")
async def analyze_excel(file: UploadFile = File(...)):
    """
    Analyze uploaded Excel file with comprehensive audit metrics

    Supports multiple data formats:
    - Detailed findings: Individual audit findings with compliance metrics
    - Detailed findings with multi-tender: Findings with multiple tenders per row
    - Entity summary: Aggregated entity-level performance data

    Features:
    - Automatic format detection
    - Format-specific analysis
    - Compliance rate analysis
    - Risk categorization (High/Medium/Low)
    - Financial impact assessment
    - Score gap analysis
    - Red flag detection
    - Entity and checklist breakdowns
    """
    sheets = load_excel(file.file)

    results = {}
    detected_formats = {}

    for sheet_name, df in sheets.items():
        # Detect data format
        format_type = detect_data_format(df)
        format_info = get_format_info(df)
        detected_formats[sheet_name] = format_info

        # Route to appropriate analysis engine
        if format_type == 'detailed_findings':
            analysis = analyze_sheet(df)
            summary = generate_summary(sheet_name, analysis)
            insights = generate_insights(
                analysis) if 'error' not in analysis else {}

        elif format_type == 'detailed_findings_multi_tender':
            analysis = analyze_multi_tender_findings(df)
            summary = generate_multi_tender_summary(sheet_name, analysis)
            insights = generate_multi_tender_insights(
                analysis) if 'error' not in analysis else {}

        elif format_type == 'entity_summary':
            analysis = analyze_entity_summary(df)
            summary = generate_entity_summary(sheet_name, analysis)
            insights = generate_entity_insights(
                analysis) if 'error' not in analysis else {}

        else:
            # Unknown format - provide basic info
            analysis = {
                "error": f"Unknown data format. Columns found: {', '.join(df.columns[:10])}",
                "format_info": format_info
            }
            summary = f"{sheet_name}: Unknown format - cannot analyze"
            insights = {}

        results[sheet_name] = {
            "data_format": format_type,
            "format_info": format_info,
            "analysis": analysis,
            "summary": summary,
            "insights": insights
        }

    # Generate overall summary across all sheets
    overall_summary = generate_overall_summary(results)
    overall_summary['detected_formats'] = detected_formats

    return {
        "status": "success",
        "sheets_analyzed": len(results),
        "overall_summary": overall_summary,
        "results": results
    }
