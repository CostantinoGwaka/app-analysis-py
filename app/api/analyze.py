from fastapi import APIRouter, UploadFile, File  # type: ignore
from app.services.excel_reader import load_excel
from app.services.analysis_engine import analyze_sheet
from app.services.summary_engine import generate_summary

router = APIRouter()


@router.post("/analyze")
async def analyze_excel(file: UploadFile = File(...)):
    sheets = load_excel(file.file)

    results = {}

    for sheet_name, df in sheets.items():
        analysis = analyze_sheet(df)
        summary = generate_summary(sheet_name, analysis)

        results[sheet_name] = {
            "analysis": analysis,
            "summary": summary
        }

    return {
        "status": "success",
        "sheets_analyzed": len(results),
        "results": results
    }
