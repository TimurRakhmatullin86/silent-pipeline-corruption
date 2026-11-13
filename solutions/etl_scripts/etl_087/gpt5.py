# Generator: gpt-5-2025-08-07
# Task: etl_087
# Generated: 2025-10-13T14:11:42Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_087(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for media_stream that loads playba."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result