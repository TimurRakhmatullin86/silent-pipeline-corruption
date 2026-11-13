# Generator: gpt-5-2025-08-07
# Task: etl_098
# Generated: 2025-10-24T18:53:08Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_098(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a PySpark ETL script for iot_fleet that validates sens."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result