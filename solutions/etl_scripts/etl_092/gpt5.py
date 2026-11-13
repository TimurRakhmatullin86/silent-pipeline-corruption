# Generator: gpt-5-2025-08-07
# Task: etl_092
# Generated: 2025-10-26T14:54:51Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_092(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a PySpark ETL script for iot_fleet that unifies teleme."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result