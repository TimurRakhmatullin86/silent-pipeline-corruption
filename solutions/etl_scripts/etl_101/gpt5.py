# Generator: gpt-5-2025-08-07
# Task: etl_101
# Generated: 2025-09-26T18:16:47Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_101(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for retail_chain that merges an in."""
    source_df['updated_at'] = pd.to_datetime(source_df['updated_at'])
    result = source_df[['price']].sum()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result