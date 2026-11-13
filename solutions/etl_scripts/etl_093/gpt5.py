# Generator: gpt-5-2025-08-07
# Task: etl_093
# Generated: 2025-10-12T17:06:59Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_093(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for health_portal that enriches en."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result