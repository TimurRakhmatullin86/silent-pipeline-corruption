# Generator: gpt-5-2025-08-07
# Task: etl_116
# Generated: 2025-10-01T13:35:59Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_116(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a PySpark ETL script for retail_chain that rolls store."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result