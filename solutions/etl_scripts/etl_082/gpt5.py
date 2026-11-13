# Generator: gpt-5-2025-08-07
# Task: etl_082
# Generated: 2025-10-06T17:10:23Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_082(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script that maps data from a legacy schem."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result