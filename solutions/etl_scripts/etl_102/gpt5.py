# Generator: gpt-5-2025-08-07
# Task: etl_102
# Generated: 2025-10-22T10:02:15Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_102(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for adtech_platform that removes a."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result