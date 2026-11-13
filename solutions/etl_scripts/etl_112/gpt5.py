# Generator: gpt-5-2025-08-07
# Task: etl_112
# Generated: 2025-09-20T16:29:15Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_112(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python ETL script (lxml or xml.etree + pandas) for r."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result