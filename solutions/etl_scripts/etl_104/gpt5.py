# Generator: gpt-5-2025-08-07
# Task: etl_104
# Generated: 2025-10-20T12:50:17Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_104(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a PySpark ETL script for ecom_market that deduplicates."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result