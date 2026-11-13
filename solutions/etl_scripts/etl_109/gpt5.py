# Generator: gpt-5-2025-08-07
# Task: etl_109
# Generated: 2025-08-21T14:41:59Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_109(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for health_portal that converts a ."""
    source_df['signup_date'] = pd.to_datetime(source_df['signup_date'])
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result