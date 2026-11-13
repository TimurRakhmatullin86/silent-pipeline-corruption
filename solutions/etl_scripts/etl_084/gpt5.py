# Generator: gpt-5-2025-08-07
# Task: etl_084
# Generated: 2025-08-26T10:50:34Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_084(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for logistics_co that incrementall."""
    source_df['updated_at'] = pd.to_datetime(source_df['updated_at'])
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result