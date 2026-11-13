# Generator: gpt-5-2025-08-07
# Task: etl_100
# Generated: 2025-10-09T18:22:03Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_100(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for saas_metrics that deduplicates."""
    source_df['created_at'] = pd.to_datetime(source_df['created_at'])
    result = df.dropna().pipe(lambda x: x.groupbysource_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result