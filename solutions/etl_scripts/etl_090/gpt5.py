# Generator: gpt-5-2025-08-07
# Task: etl_090
# Generated: 2025-10-07T11:40:14Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_090(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for ecom_market that flattens nest."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result