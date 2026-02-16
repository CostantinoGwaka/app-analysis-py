from fastapi import APIRouter, UploadFile, File, HTTPException  # type: ignore
from app.services.excel_reader import load_excel
from app.services.data_validator import (
    validate_excel_structure,
    get_data_quality_report,
    sanitize_data,
    validate_data_ranges
)

router = APIRouter()


@router.post("/validate")
async def validate_excel(file: UploadFile = File(...)):
    """
    Validate Excel file structure and data quality before analysis
    """
    try:
        sheets = load_excel(file.file)
        
        validation_results = {}
        
        for sheet_name, df in sheets.items():
            # Validate structure
            is_valid, errors = validate_excel_structure(df)
            
            # Get data quality report
            quality_report = get_data_quality_report(df)
            
            # Validate data ranges
            range_warnings = validate_data_ranges(df)
            
            validation_results[sheet_name] = {
                "is_valid": is_valid,
                "errors": errors,
                "quality_report": quality_report,
                "range_warnings": range_warnings
            }
        
        # Overall validation status
        all_valid = all(result["is_valid"] for result in validation_results.values())
        
        return {
            "status": "valid" if all_valid else "invalid",
            "sheets_validated": len(validation_results),
            "validation_results": validation_results
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error validating file: {str(e)}")


@router.post("/preview")
async def preview_excel(file: UploadFile = File(...)):
    """
    Preview Excel file contents (first 10 rows of each sheet)
    """
    try:
        sheets = load_excel(file.file)
        
        preview_data = {}
        
        for sheet_name, df in sheets.items():
            # Get first 10 rows
            preview_df = df.head(10)
            
            preview_data[sheet_name] = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "preview": preview_df.to_dict(orient='records')
            }
        
        return {
            "status": "success",
            "sheets": len(preview_data),
            "data": preview_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error previewing file: {str(e)}")


@router.get("/columns/required")
async def get_required_columns():
    """
    Get list of required and recommended columns for analysis
    """
    return {
        "required_columns": [
            "Compliance %",
            "Score Gap",
            "Status",
            "Checklist Title"
        ],
        "recommended_columns": [
            "Expected Score",
            "Actual Score",
            "Red Flag",
            "Audit Type",
            "PE Category",
            "PE Name",
            "Financial Year",
            "Estimated Budget",
            "Entity Name",
            "Entity Number",
            "Finding Title",
            "Finding Description",
            "Recommendation",
            "Implication",
            "Management Response"
        ],
        "optional_columns": [
            "Auditor Opinion",
            "Created Date",
            "Updated Date",
            "Requirement Name"
        ]
    }
