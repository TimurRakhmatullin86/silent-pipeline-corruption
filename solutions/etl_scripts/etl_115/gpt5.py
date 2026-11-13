# Generator: gpt-5-2025-08-07
# Task: etl_115
# Generated: 2025-09-09T15:57:53Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_115(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for saas_metrics that computes dai."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result