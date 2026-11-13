# Generator: gpt-5-2025-08-07
# Task: etl_110
# Generated: 2025-08-13T15:06:33Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_110(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script (pandas + pyarrow) for adtech_plat."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result