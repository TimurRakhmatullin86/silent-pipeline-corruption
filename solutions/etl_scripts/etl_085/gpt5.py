# Generator: gpt-5-2025-08-07
# Task: etl_085
# Generated: 2025-08-05T19:23:13Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_085(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a PySpark ETL script for fintech_app that applies a ba."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result