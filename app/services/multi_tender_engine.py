"""
Analysis engine for detailed findings with multiple tenders per row
Handles findings where each row contains multiple tender references
"""
import pandas as pd
import re
from app.services.analysis_engine import clean_numeric


def parse_tender_details(tender_string):
    """
    Parse tender details from string like:
    'TR152/006/2024/2025/W/07 (Own Funds, Budget: 150000000, Works, National Competitive Tendering)'

    Returns list of dicts with tender details
    """
    if pd.isna(tender_string) or not isinstance(tender_string, str):
        return []

    tenders = []
    # Split by line breaks or common separators
    tender_parts = re.split(r',\s*(?=TR\d+/)', str(tender_string))

    for part in tender_parts:
        part = part.strip()
        if not part:
            continue

        # Extract tender number (e.g., TR152/006/2024/2025/W/07)
        tender_match = re.search(r'(TR\d+/[\d/]+/[A-Z]/\d+)', part)
        tender_number = tender_match.group(
            1) if tender_match else part.split('(')[0].strip()

        # Extract budget if present
        budget = 0
        budget_match = re.search(r'Budget:\s*([\d,]+)', part)
        if budget_match:
            budget = float(budget_match.group(1).replace(',', ''))

        # Extract type (Works, Goods, Services, etc.)
        tender_type = 'Unknown'
        if 'Works' in part:
            tender_type = 'Works'
        elif 'Goods' in part:
            tender_type = 'Goods'
        elif 'Services' in part:
            tender_type = 'Services'

        tenders.append({
            'tender_number': tender_number,
            'budget': budget,
            'type': tender_type
        })

    return tenders


def analyze_multi_tender_findings(df):
    """
    Analyze detailed findings with multiple tenders per finding

    Expected columns:
    - PE Name (required)
    - Checklist Title (required)
    - Tenders (required) - comma-separated tender details
    - Total Budget (required)
    - Tender Count (required)
    - Finding Title (required)
    - Status (required)
    - Red Flag (required)
    - Finding Description (optional)
    - Implication (optional)
    - Recommendation (optional)
    - Management Response (optional)
    - Auditor Opinion (optional)
    - Created At (optional)
    """

    required_columns = ['PE Name', 'Checklist Title', 'Tenders',
                        'Total Budget', 'Tender Count', 'Finding Title',
                        'Status', 'Red Flag']

    for col in required_columns:
        if col not in df.columns:
            return {
                "error": f"Missing required column for multi-tender findings: {col}"
            }

    # Make a copy
    df = df.copy()

    # Clean numeric columns
    if 'Total Budget' in df.columns:
        df['Total Budget'] = df['Total Budget'].apply(clean_numeric)
    if 'Tender Count' in df.columns:
        df['Tender Count'] = df['Tender Count'].apply(clean_numeric)

    # Basic metrics
    total_findings = int(len(df))

    # Status analysis
    open_findings = int((df['Status'].astype(str).str.upper() == 'OPEN').sum())
    closed_findings = int(
        (df['Status'].astype(str).str.upper() == 'CLOSED').sum())

    # Red flag analysis
    red_flags = 0
    if 'Red Flag' in df.columns:
        red_flag_col = df['Red Flag'].astype(str).str.upper().str.strip()
        # Only count actual red flags, not "NOT RED FLAG"
        red_flags = int(((red_flag_col == 'RED FLAG') |
                        (red_flag_col == 'YES')).sum())

    # Budget analysis
    total_budget = 0.0
    avg_budget_per_finding = 0.0
    if 'Total Budget' in df.columns:
        budget_data = df[df['Total Budget'].notna()]
        if len(budget_data) > 0:
            total_budget = float(budget_data['Total Budget'].sum())
            avg_budget_per_finding = round(total_budget / len(budget_data), 2)

    # Tender count analysis
    total_tenders = 0
    avg_tenders_per_finding = 0.0
    unique_tender_numbers = set()

    # Parse all tenders to get unique tender numbers
    for idx, row in df.iterrows():
        tenders = parse_tender_details(row.get('Tenders', ''))
        for tender in tenders:
            if tender['tender_number']:
                unique_tender_numbers.add(tender['tender_number'])

    if 'Tender Count' in df.columns:
        tender_data = df[df['Tender Count'].notna()]
        if len(tender_data) > 0:
            total_tenders = int(tender_data['Tender Count'].sum())
            avg_tenders_per_finding = round(
                float(tender_data['Tender Count'].mean()), 2)

    # Budget range distribution (with unique tenders only)
    budget_range_distribution = {
        'description': 'Distribution of unique tenders across budget ranges, removing duplicates to get accurate budget allocation insights',
        'ranges': {}
    }

    # Collect unique tenders with their budgets
    unique_tenders_with_budget = {}
    for idx, row in df.iterrows():
        tenders = parse_tender_details(row.get('Tenders', ''))
        for tender in tenders:
            if tender['tender_number'] and tender['budget'] > 0:
                # Only keep first occurrence of each tender number
                if tender['tender_number'] not in unique_tenders_with_budget:
                    unique_tenders_with_budget[tender['tender_number']
                                               ] = tender['budget']

    # Define budget ranges (in TZS)
    ranges = [
        ('0-50M', 0, 50_000_000),
        ('50M-100M', 50_000_000, 100_000_000),
        ('100M-200M', 100_000_000, 200_000_000),
        ('200M-500M', 200_000_000, 500_000_000),
        ('500M+', 500_000_000, float('inf'))
    ]

    for range_name, min_val, max_val in ranges:
        count = sum(1 for budget in unique_tenders_with_budget.values()
                    if min_val <= budget < max_val)
        range_total_budget = sum(budget for budget in unique_tenders_with_budget.values()
                                 if min_val <= budget < max_val)
        budget_range_distribution['ranges'][range_name] = {
            'count': count,
            'total_budget': round(range_total_budget, 2),
            'percentage': round((count / len(unique_tenders_with_budget) * 100), 2) if unique_tenders_with_budget else 0
        }

    # PE Name analysis
    pe_analysis = {
        'description': 'Analysis of findings grouped by Procuring Entity (PE), showing performance metrics and tender details for each entity'
    }

    if 'PE Name' in df.columns:
        for pe_name, group in df.groupby('PE Name'):
            if pd.isna(pe_name) or str(pe_name).strip() == "":
                continue

            pe_name_str = str(pe_name).strip()

            # Calculate metrics for this PE
            pe_findings = len(group)
            pe_open = int((group['Status'].astype(
                str).str.upper() == 'OPEN').sum())
            pe_closed = int((group['Status'].astype(
                str).str.upper() == 'CLOSED').sum())

            # PE budget
            pe_budget = 0.0
            if 'Total Budget' in group.columns:
                pe_budget_data = group[group['Total Budget'].notna()]
                pe_budget = float(pe_budget_data['Total Budget'].sum()) if len(
                    pe_budget_data) > 0 else 0.0

            # PE tenders - collect tender numbers
            pe_tenders = 0
            pe_tender_numbers = []
            pe_tender_details = []

            for idx, row in group.iterrows():
                tenders = parse_tender_details(row.get('Tenders', ''))
                for tender in tenders:
                    if tender['tender_number']:
                        pe_tender_numbers.append(tender['tender_number'])
                        pe_tender_details.append({
                            'tender_number': tender['tender_number'],
                            'budget': tender['budget'],
                            'type': tender['type']
                        })

            pe_tenders = len(pe_tender_numbers)

            # PE red flags
            pe_red_flags = 0
            if 'Red Flag' in group.columns:
                pe_red_flag_col = group['Red Flag'].astype(
                    str).str.upper().str.strip()
                # Only count actual red flags, not "NOT RED FLAG"
                pe_red_flags = int(
                    ((pe_red_flag_col == 'RED FLAG') | (pe_red_flag_col == 'YES')).sum())

            pe_analysis[pe_name_str] = {
                'total_findings': pe_findings,
                'open_findings': pe_open,
                'closed_findings': pe_closed,
                'total_budget': round(pe_budget, 2),
                'total_tenders': pe_tenders,
                'tender_numbers': pe_tender_numbers,
                'tender_details': pe_tender_details,
                'red_flags': pe_red_flags
            }

    # Checklist analysis (enhanced with more metrics)
    checklist_analysis = {
        'description': 'Detailed breakdown of findings grouped by checklist/compliance requirement, showing status, budget impact, and risk indicators'
    }

    if 'Checklist Title' in df.columns:
        for checklist, group in df.groupby('Checklist Title'):
            if pd.isna(checklist) or str(checklist).strip() == "":
                continue

            checklist_str = str(checklist).strip()

            checklist_findings = len(group)
            checklist_open = int(
                (group['Status'].astype(str).str.upper() == 'OPEN').sum())
            checklist_closed = int(
                (group['Status'].astype(str).str.upper() == 'CLOSED').sum())

            # Checklist budget
            checklist_budget = 0.0
            checklist_avg_budget = 0.0
            if 'Total Budget' in group.columns:
                checklist_budget_data = group[group['Total Budget'].notna()]
                if len(checklist_budget_data) > 0:
                    checklist_budget = float(
                        checklist_budget_data['Total Budget'].sum())
                    checklist_avg_budget = round(
                        checklist_budget / len(checklist_budget_data), 2)

            # Checklist tenders
            checklist_tenders = 0
            checklist_avg_tenders = 0.0
            if 'Tender Count' in group.columns:
                checklist_tender_data = group[group['Tender Count'].notna()]
                if len(checklist_tender_data) > 0:
                    checklist_tenders = int(
                        checklist_tender_data['Tender Count'].sum())
                    checklist_avg_tenders = round(
                        float(checklist_tender_data['Tender Count'].mean()), 2)

            # Checklist red flags
            checklist_red_flags = 0
            if 'Red Flag' in group.columns:
                checklist_red_flag_col = group['Red Flag'].astype(
                    str).str.upper().str.strip()
                checklist_red_flags = int(
                    ((checklist_red_flag_col == 'RED FLAG') | (checklist_red_flag_col == 'YES')).sum())

            # Affected PEs count
            affected_pes = group['PE Name'].nunique(
            ) if 'PE Name' in group.columns else 0

            # Completion rate
            completion_rate = round(
                (checklist_closed / checklist_findings * 100), 2) if checklist_findings > 0 else 0

            checklist_analysis[checklist_str] = {
                'total_findings': checklist_findings,
                'open_findings': checklist_open,
                'closed_findings': checklist_closed,
                'completion_rate': completion_rate,
                'total_budget': round(checklist_budget, 2),
                'average_budget_per_finding': checklist_avg_budget,
                'total_tenders': checklist_tenders,
                'average_tenders_per_finding': checklist_avg_tenders,
                'red_flags': checklist_red_flags,
                'affected_entities': affected_pes,
                'risk_level': 'High' if checklist_red_flags > 0 else ('Medium' if checklist_open > checklist_closed else 'Low')
            }

    # Detailed findings with parsed tenders
    detailed_findings = []
    for idx, row in df.iterrows():
        finding = {
            'pe_name': str(row.get('PE Name', 'Unknown')),
            'checklist': str(row.get('Checklist Title', 'Unknown')),
            'finding_title': str(row.get('Finding Title', 'N/A')),
            'status': str(row.get('Status', 'Unknown')),
            'red_flag': str(row.get('Red Flag', 'N/A')),
            'total_budget': float(row.get('Total Budget', 0)) if pd.notna(row.get('Total Budget')) else 0.0,
            'tender_count': int(row.get('Tender Count', 0)) if pd.notna(row.get('Tender Count')) else 0,
            'tenders': parse_tender_details(row.get('Tenders', ''))
        }

        # Add optional fields if present
        if 'Finding Description' in row and pd.notna(row.get('Finding Description')):
            finding['description'] = str(row['Finding Description'])[:200] + '...' if len(
                str(row['Finding Description'])) > 200 else str(row['Finding Description'])

        if 'Recommendation' in row and pd.notna(row.get('Recommendation')):
            finding['recommendation'] = str(row['Recommendation'])[
                :200] + '...' if len(str(row['Recommendation'])) > 200 else str(row['Recommendation'])

        if 'Created At' in row and pd.notna(row.get('Created At')):
            finding['created_at'] = str(row['Created At'])

        detailed_findings.append(finding)

    # Top entities by budget (with tender details)
    top_entities_by_budget = {
        'description': 'Top 5 procuring entities ranked by total budget allocation across all their findings, including detailed tender information',
        'entities': []
    }

    if pe_analysis and isinstance(pe_analysis, dict):
        # Filter out description key and sort by budget
        pe_items = [(k, v) for k, v in pe_analysis.items() if k !=
                    'description' and isinstance(v, dict)]
        sorted_pes = sorted(pe_items, key=lambda x: x[1].get(
            'total_budget', 0), reverse=True)[:5]

        for pe_name, pe_data in sorted_pes:
            top_entities_by_budget['entities'].append({
                'entity_name': pe_name,
                'total_budget': pe_data.get('total_budget', 0),
                'total_findings': pe_data.get('total_findings', 0),
                'open_findings': pe_data.get('open_findings', 0),
                'total_tenders': pe_data.get('total_tenders', 0),
                'tender_numbers': pe_data.get('tender_numbers', []),
                'tender_details': pe_data.get('tender_details', []),
                'red_flags': pe_data.get('red_flags', 0)
            })

    return {
        'format_type': 'detailed_findings_multi_tender',
        'total_findings': {
            'description': 'Total number of audit findings identified across all procuring entities',
            'value': total_findings
        },
        'open_findings': {
            'description': 'Number of findings with status OPEN that require action or resolution',
            'value': open_findings
        },
        'closed_findings': {
            'description': 'Number of findings with status CLOSED that have been resolved or addressed',
            'value': closed_findings
        },
        'red_flags': {
            'description': 'Count of findings marked as RED FLAG indicating critical compliance issues or risks',
            'value': red_flags
        },
        'total_budget': {
            'description': 'Aggregate budget amount across all findings and tenders in the analysis',
            'value': round(total_budget, 2)
        },
        'average_budget_per_finding': {
            'description': 'Mean budget allocation per finding, calculated by dividing total budget by number of findings',
            'value': avg_budget_per_finding
        },
        'total_tenders': {
            'description': 'Total count of tenders referenced across all findings',
            'value': total_tenders
        },
        'unique_tenders': {
            'description': 'Number of unique tender numbers after removing duplicates across findings',
            'value': len(unique_tender_numbers)
        },
        'average_tenders_per_finding': {
            'description': 'Average number of tenders associated with each finding',
            'value': avg_tenders_per_finding
        },
        'budget_range_distribution': budget_range_distribution,
        'pe_analysis': pe_analysis,
        'checklist_analysis': checklist_analysis,
        'top_entities_by_budget': top_entities_by_budget,
        'entity_analysis': {
            'description': 'Comprehensive breakdown of performance metrics grouped by procuring entity, showing findings, budgets, tenders, and compliance status for each organization',
            'data': pe_analysis
        },
        'detailed_findings': {
            'description': 'Complete list of individual findings with full details including PE name, checklist, status, budget, tender information, and recommendations',
            'findings': detailed_findings
        }
    }
