# Generator: gpt-5-2025-08-07
# Task: etl_095
# Generated: 2025-10-03T17:34:01Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_095(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for health_portal that validates a."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result