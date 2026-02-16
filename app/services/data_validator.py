"""
Data validation utilities for audit analysis
"""
import pandas as pd
from typing import Dict, List, Tuple
from app.services.analysis_engine import clean_percentage, clean_numeric


def validate_excel_structure(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that the Excel file has the required structure
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required columns
    required_columns = [
        "Compliance %",
        "Score Gap",
        "Status",
        "Checklist Title"
    ]
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check if dataframe is empty
    if len(df) == 0:
        errors.append("Excel sheet is empty")
    
    # Recommended columns
    recommended_columns = [
        "Expected Score",
        "Actual Score",
        "Red Flag",
        "Audit Type",
        "PE Category",
        "Estimated Budget",
        "Entity Name"
    ]
    
    missing_recommended = [col for col in recommended_columns if col not in df.columns]
    if missing_recommended:
        errors.append(f"Warning: Missing recommended columns for enhanced analysis: {', '.join(missing_recommended)}")
    
    return len([e for e in errors if not e.startswith("Warning")]) == 0, errors


def get_data_quality_report(df: pd.DataFrame) -> Dict:
    """
    Generate a data quality report for the uploaded file
    """
    total_rows = len(df)
    total_columns = len(df.columns)
    
    # Calculate missing values per column
    missing_data = {}
    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            missing_data[col] = {
                "count": int(missing_count),
                "percentage": round((missing_count / total_rows * 100), 2)
            }
    
    # Identify duplicate rows
    duplicate_count = df.duplicated().sum()
    
    # Data type analysis
    data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "duplicate_rows": int(duplicate_count),
        "missing_data": missing_data,
        "data_types": data_types,
        "columns": list(df.columns)
    }


def sanitize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and sanitize the data
    """
    df = df.copy()
    
    # Strip whitespace from string columns
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
    
    # Replace common null representations
    null_values = ['N/A', 'n/a', 'NA', 'null', 'NULL', 'None', '-', '']
    df = df.replace(null_values, pd.NA)
    
    return df


def validate_data_ranges(df: pd.DataFrame) -> List[str]:
    """
    Validate that data values are within expected ranges
    """
    warnings = []
    
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Compliance should be 0-100
    if "Compliance %" in df_clean.columns:
        df_clean["Compliance %"] = df_clean["Compliance %"].apply(clean_percentage)
        invalid_compliance = df_clean[
            (df_clean["Compliance %"].notna()) & 
            ((df_clean["Compliance %"] < 0) | (df_clean["Compliance %"] > 100))
        ]
        if len(invalid_compliance) > 0:
            warnings.append(
                f"{len(invalid_compliance)} records have compliance % outside 0-100% range"
            )
    
    # Score Gap should not be negative (typically)
    if "Score Gap" in df_clean.columns:
        df_clean["Score Gap"] = df_clean["Score Gap"].apply(clean_numeric)
        negative_gaps = df_clean[
            (df_clean["Score Gap"].notna()) & 
            (df_clean["Score Gap"] < 0)
        ]
        if len(negative_gaps) > 0:
            warnings.append(
                f"{len(negative_gaps)} records have negative score gaps"
            )
    
    # Expected Score should be >= Actual Score (typically)
    if "Expected Score" in df_clean.columns and "Actual Score" in df_clean.columns:
        df_clean["Expected Score"] = df_clean["Expected Score"].apply(clean_numeric)
        df_clean["Actual Score"] = df_clean["Actual Score"].apply(clean_numeric)
        invalid_scores = df_clean[
            (df_clean["Expected Score"].notna()) & 
            (df_clean["Actual Score"].notna()) &
            (df_clean["Actual Score"] > df_clean["Expected Score"])
        ]
        if len(invalid_scores) > 0:
            warnings.append(
                f"{len(invalid_scores)} records have actual score > expected score"
            )
    
    return warnings
