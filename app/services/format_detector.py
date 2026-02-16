"""
Detect and handle different Excel data formats
"""
import pandas as pd
from typing import Dict, Tuple


def detect_data_format(df: pd.DataFrame) -> str:
    """
    Detect which format the uploaded Excel data is in

    Returns:
        'detailed_findings' - Individual audit findings (original format)
        'detailed_findings_multi_tender' - Findings with multiple tenders per row
        'entity_summary' - Aggregated entity-level data
        'unknown' - Cannot determine format
    """

    # Check for detailed findings format (original)
    # Required columns: Compliance %, Score Gap, Status, Checklist Title
    detailed_required = ['Compliance %',
                         'Score Gap', 'Status', 'Checklist Title']
    has_detailed = all(col in df.columns for col in detailed_required)

    # Check for detailed findings with multi-tender format
    # Required columns: PE Name, Checklist Title, Tenders, Total Budget, Tender Count, Finding Title, Status, Red Flag
    multi_tender_required = ['PE Name', 'Checklist Title', 'Tenders',
                             'Total Budget', 'Tender Count', 'Finding Title',
                             'Status', 'Red Flag']
    has_multi_tender = all(col in df.columns for col in multi_tender_required)

    # Check for entity summary format
    summary_columns = ['Procuring Entity', 'Overall %', 'Tenders']
    has_summary = all(col in df.columns for col in summary_columns)

    if has_detailed:
        return 'detailed_findings'
    elif has_multi_tender:
        return 'detailed_findings_multi_tender'
    elif has_summary:
        return 'entity_summary'
    else:
        return 'unknown'


def get_format_info(df: pd.DataFrame) -> Dict:
    """
    Get information about the detected format
    """
    format_type = detect_data_format(df)

    info = {
        'format': format_type,
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns)
    }

    if format_type == 'detailed_findings':
        info['description'] = 'Individual audit findings with detailed compliance metrics'
        info['key_fields'] = ['Compliance %', 'Score Gap', 'Status', 'Checklist Title',
                              'PE Name', 'Entity Name']

    elif format_type == 'detailed_findings_multi_tender':
        info['description'] = 'Detailed findings with multiple tenders per finding'
        info['key_fields'] = ['PE Name', 'Checklist Title', 'Tenders', 'Total Budget',
                              'Tender Count', 'Finding Title', 'Status', 'Red Flag']

    elif format_type == 'entity_summary':
        info['description'] = 'Aggregated entity-level summary with overall performance'
        info['key_fields'] = ['Procuring Entity',
                              'Overall %', 'Tenders', 'Status']

    else:
        info['description'] = 'Unknown format - may require custom analysis'
        info['key_fields'] = []

    return info
