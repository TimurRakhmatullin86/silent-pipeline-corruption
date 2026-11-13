# Generator: gpt-5-2025-08-07
# Task: etl_081
# Generated: 2025-10-13T14:14:54Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_081(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script using pandas that performs increme."""
    source_df['transaction_timestamp'] = pd.to_datetime(source_df['transaction_timestamp'])
    result = source_df.groupby('transaction_id')['amount_cents'].sum().reset_index()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result