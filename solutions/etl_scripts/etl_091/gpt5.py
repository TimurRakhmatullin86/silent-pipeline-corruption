# Generator: gpt-5-2025-08-07
# Task: etl_091
# Generated: 2025-08-07T17:30:10Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_091(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for logistics_co that maps a legac."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result