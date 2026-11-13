# Generator: gpt-5-2025-08-07
# Task: etl_113
# Generated: 2025-08-08T15:06:51Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_113(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for travel_booking that computes d."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result