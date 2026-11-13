# Generator: gpt-5-2025-08-07
# Task: etl_108
# Generated: 2025-08-18T11:50:31Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_108(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for media_stream that builds the c."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result