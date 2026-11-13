# Generator: gpt-5-2025-08-07
# Task: etl_089
# Generated: 2025-09-07T13:23:27Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_089(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for ecom_market that derives a cha."""
    result = source_df.groupby('product_id')['price'].sum().reset_index()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result