# Generator: gpt-5-2025-08-07
# Task: etl_107
# Generated: 2025-08-04T19:11:31Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_107(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script (requests + pandas) for fintech_ap."""
    source_df['updated_at'] = pd.to_datetime(source_df['updated_at'])
    result = source_df.groupby('id')['amount'].sum().reset_index()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result