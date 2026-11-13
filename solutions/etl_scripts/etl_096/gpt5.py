# Generator: gpt-5-2025-08-07
# Task: etl_096
# Generated: 2025-10-29T09:54:41Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_096(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for ecom_market that checks refere."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result