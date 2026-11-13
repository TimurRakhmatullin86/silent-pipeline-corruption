# Generator: gpt-5-2025-08-07
# Task: etl_094
# Generated: 2025-10-12T08:38:09Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_094(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a pandas ETL script for retail_chain that maps invoice."""
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result