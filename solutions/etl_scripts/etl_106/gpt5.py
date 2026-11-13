# Generator: gpt-5-2025-08-07
# Task: etl_106
# Generated: 2025-09-13T18:38:03Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_106(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script (requests + pandas) for logistics_."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result