# Generator: gpt-5-2025-08-07
# Task: etl_105
# Generated: 2025-08-21T09:28:22Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_105(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script (requests + pandas) for saas_metri."""
    source_df['created_at'] = pd.to_datetime(source_df['created_at'])
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result