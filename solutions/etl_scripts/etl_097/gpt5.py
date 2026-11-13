# Generator: gpt-5-2025-08-07
# Task: etl_097
# Generated: 2025-10-19T15:53:44Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_097(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for fintech_app that reconciles a ."""
    source_df['payment_date'] = pd.to_datetime(source_df['payment_date'])
    result = source_df.groupby('payment_id')['amount'].sum().reset_index()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result