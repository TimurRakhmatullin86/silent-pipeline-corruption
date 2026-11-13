# Generator: gpt-5-2025-08-07
# Task: etl_117
# Generated: 2025-09-13T18:11:53Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_117(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for fintech_app that produces an a."""
    source_df['date_of_birth'] = pd.to_datetime(source_df['date_of_birth'])
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result