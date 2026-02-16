"""
Analysis engine for entity summary format
Handles aggregated entity-level data
"""
import pandas as pd
import math
from app.services.analysis_engine import clean_percentage, clean_numeric


def analyze_entity_summary(df):
    """
    Analyze entity summary format data

    Expected columns:
    - Procuring Entity (required)
    - Overall % (required)
    - Status (optional)
    - Tenders, App Marks, Institution, Tendering Avg, etc.
    """

    required_columns = ['Procuring Entity', 'Overall %']

    for col in required_columns:
        if col not in df.columns:
            return {
                "error": f"Missing required column for entity summary: {col}"
            }

    # Make a copy
    df = df.copy()

    # Clean percentage columns
    if 'Overall %' in df.columns:
        df['Overall %'] = df['Overall %'].apply(clean_percentage)
        # If values are in decimal form (0-1 range), multiply by 100
        if df['Overall %'].notna().any():
            max_val = df[df['Overall %'].notna()]['Overall %'].max()
            if max_val <= 1.0:
                df['Overall %'] = df['Overall %'] * 100

    if 'Tendering Avg' in df.columns:
        df['Tendering Avg'] = df['Tendering Avg'].apply(clean_percentage)
        # If values are in decimal form (0-1 range), multiply by 100
        if df['Tendering Avg'].notna().any():
            max_val = df[df['Tendering Avg'].notna()]['Tendering Avg'].max()
            if max_val <= 1.0:
                df['Tendering Avg'] = df['Tendering Avg'] * 100

    # Clean numeric columns
    if 'Tenders' in df.columns:
        df['Tenders'] = df['Tenders'].apply(clean_numeric)
    if 'App Marks' in df.columns:
        df['App Marks'] = df['App Marks'].apply(clean_numeric)
    if 'Institution' in df.columns:
        df['Institution'] = df['Institution'].apply(clean_numeric)

    # Basic metrics
    total_entities = int(len(df))

    # Overall performance
    valid_overall = df[df['Overall %'].notna()]
    avg_overall = round(float(valid_overall['Overall %'].mean()), 2) if len(
        valid_overall) > 0 else 0.0

    # Performance distribution
    performance_distribution = {
        'excellent': int(len(df[df['Overall %'] >= 90])),
        'good': int(len(df[(df['Overall %'] >= 75) & (df['Overall %'] < 90)])),
        'satisfactory': int(len(df[(df['Overall %'] >= 60) & (df['Overall %'] < 75)])),
        'needs_improvement': int(len(df[df['Overall %'] < 60]))
    }

    # PE Category breakdown
    category_breakdown = {}
    if 'Pe Category' in df.columns:
        categories = df['Pe Category'].value_counts().to_dict()
        category_breakdown = {str(k): int(v) for k, v in categories.items()}

    # Status analysis
    status_breakdown = {}
    if 'Status' in df.columns:
        statuses = df['Status'].value_counts().to_dict()
        status_breakdown = {str(k): int(v) for k, v in statuses.items()}

    # Tenders analysis
    tenders_analysis = {}
    if 'Tenders' in df.columns:
        tenders_df = df[df['Tenders'].notna()]
        if len(tenders_df) > 0:
            total_tenders = int(tenders_df['Tenders'].sum())
            avg_tenders = round(float(tenders_df['Tenders'].mean()), 2)
            max_tenders = int(tenders_df['Tenders'].max())
            min_tenders = int(tenders_df['Tenders'].min())

            tenders_analysis = {
                'total_tenders': total_tenders,
                'average_tenders_per_entity': avg_tenders,
                'max_tenders': max_tenders,
                'min_tenders': min_tenders
            }

    # Tendering performance
    tendering_performance = {}
    if 'Tendering Avg' in df.columns:
        tendering_df = df[df['Tendering Avg'].notna()]
        if len(tendering_df) > 0:
            avg_tendering = round(
                float(tendering_df['Tendering Avg'].mean()), 2)
            tendering_performance = {
                'average_tendering_score': avg_tendering,
                'entities_above_80': int(len(tendering_df[tendering_df['Tendering Avg'] >= 80])),
                'entities_below_60': int(len(tendering_df[tendering_df['Tendering Avg'] < 60]))
            }

    # Top and bottom performers
    top_performers = []
    bottom_performers = []

    if 'Procuring Entity' in df.columns and 'Overall %' in df.columns:
        # Top 5
        top_df = df.nlargest(5, 'Overall %')
        for _, row in top_df.iterrows():
            entity = str(row['Procuring Entity'])
            overall = float(row.get('Overall %', 0))
            tenders = int(row.get('Tenders', 0)) if 'Tenders' in row and pd.notna(
                row.get('Tenders')) else 0
            tender_number = str(row.get('Tender Number', 'N/A')) if 'Tender Number' in row and pd.notna(
                row.get('Tender Number')) else 'N/A'

            top_performers.append({
                'entity': entity,
                'overall_percentage': round(overall, 2),
                'tenders': tenders,
                'tender_number': tender_number
            })

        # Bottom 5
        bottom_df = df.nsmallest(5, 'Overall %')
        for _, row in bottom_df.iterrows():
            entity = str(row['Procuring Entity'])
            overall = float(row.get('Overall %', 0))
            tenders = int(row.get('Tenders', 0)) if 'Tenders' in row and pd.notna(
                row.get('Tenders')) else 0
            tender_number = str(row.get('Tender Number', 'N/A')) if 'Tender Number' in row and pd.notna(
                row.get('Tender Number')) else 'N/A'

            bottom_performers.append({
                'entity': entity,
                'overall_percentage': round(overall, 2),
                'tenders': tenders,
                'tender_number': tender_number
            })

    # Entity analysis by category
    entity_by_category = {}
    if 'Pe Category' in df.columns:
        for category, group in df.groupby('Pe Category'):
            if pd.isna(category):
                continue

            category_str = str(category)
            valid_overall = group[group['Overall %'].notna()]

            entity_by_category[category_str] = {
                'count': len(group),
                'average_overall': round(float(valid_overall['Overall %'].mean()), 2) if len(valid_overall) > 0 else 0.0,
                'total_tenders': int(group['Tenders'].sum()) if 'Tenders' in group.columns else 0
            }

    # Detailed entity analysis
    detailed_entities = {}
    for _, row in df.iterrows():
        entity_name = str(row.get('Procuring Entity', 'Unknown'))
        if entity_name == 'Unknown' or pd.isna(entity_name):
            continue

        overall = float(row.get('Overall %', 0)) if pd.notna(
            row.get('Overall %')) else 0.0
        tenders = int(row.get('Tenders', 0)) if 'Tenders' in row and pd.notna(
            row.get('Tenders')) else 0
        tendering_avg = float(row.get('Tendering Avg', 0)) if 'Tendering Avg' in row and pd.notna(
            row.get('Tendering Avg')) else 0.0
        app_marks = float(row.get('App Marks', 0)) if 'App Marks' in row and pd.notna(
            row.get('App Marks')) else 0.0
        institution = float(row.get('Institution', 0)) if 'Institution' in row and pd.notna(
            row.get('Institution')) else 0.0
        status = str(row.get('Status', 'N/A'))
        category = str(row.get('Pe Category', 'N/A'))
        tender_number = str(row.get('Tender Number', 'N/A')) if 'Tender Number' in row and pd.notna(
            row.get('Tender Number')) else 'N/A'

        detailed_entities[entity_name] = {
            'overall_percentage': round(overall, 2),
            'tenders': tenders,
            'tendering_avg': round(tendering_avg, 2),
            'app_marks': round(app_marks, 2),
            'institution_score': round(institution, 2),
            'status': status,
            'category': category,
            'tender_number': tender_number
        }

    return {
        'format_type': 'entity_summary',
        'total_entities': total_entities,
        'average_overall_performance': avg_overall,
        'performance_distribution': performance_distribution,
        'category_breakdown': category_breakdown,
        'status_breakdown': status_breakdown,
        'tenders_analysis': tenders_analysis,
        'tendering_performance': tendering_performance,
        'top_performers': top_performers,
        'bottom_performers': bottom_performers,
        'entity_by_category': entity_by_category,
        'detailed_entities': detailed_entities
    }
