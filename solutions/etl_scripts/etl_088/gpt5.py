# Generator: gpt-5-2025-08-07
# Task: etl_088
# Generated: 2025-08-07T17:47:31Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_088(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for fintech_app that incrementally."""
    result = source_df.groupby('account_id')['amount'].sum().reset_index()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result