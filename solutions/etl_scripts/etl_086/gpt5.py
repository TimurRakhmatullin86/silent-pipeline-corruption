# Generator: gpt-5-2025-08-07
# Task: etl_086
# Generated: 2025-09-29T18:33:22Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_086(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for telecom_co that maintains a Ty."""
    source_df['snapshot_date'] = pd.to_datetime(source_df['snapshot_date'])
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result