# Generator: gpt-5-2025-08-07
# Task: etl_103
# Generated: 2025-09-07T12:28:38Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_103(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for insurance_group that builds a ."""
    source_df['updated_at'] = pd.to_datetime(source_df['updated_at'])
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result