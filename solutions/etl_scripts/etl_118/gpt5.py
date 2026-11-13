# Generator: gpt-5-2025-08-07
# Task: etl_118
# Generated: 2025-09-11T18:20:09Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_118(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a PySpark ETL script for health_portal that tokenizes ."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result