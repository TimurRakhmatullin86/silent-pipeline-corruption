# Generator: gpt-5-2025-08-07
# Task: etl_099
# Generated: 2025-10-30T15:28:39Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_099(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for energy_grid that checks comple."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result