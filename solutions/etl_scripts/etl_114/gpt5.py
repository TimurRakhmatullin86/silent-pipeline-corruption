# Generator: gpt-5-2025-08-07
# Task: etl_114
# Generated: 2025-10-05T16:31:45Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_114(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for media_stream that groups page-."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result