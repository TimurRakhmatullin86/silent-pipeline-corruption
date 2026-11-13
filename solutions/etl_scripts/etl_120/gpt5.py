# Generator: gpt-5-2025-08-07
# Task: etl_120
# Generated: 2025-09-21T16:05:25Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_120(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for telecom_co that applies data-s."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result