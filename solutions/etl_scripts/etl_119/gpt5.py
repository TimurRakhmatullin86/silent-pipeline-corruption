# Generator: gpt-5-2025-08-07
# Task: etl_119
# Generated: 2025-08-28T17:22:03Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_119(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for health_portal that prepares a ."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result