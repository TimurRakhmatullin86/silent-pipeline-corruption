# Generator: gpt-5-2025-08-07
# Task: etl_111
# Generated: 2025-10-01T09:15:24Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_111(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script (pandas) for fintech_app that conv."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result