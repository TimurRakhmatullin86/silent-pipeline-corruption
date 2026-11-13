# Generator: deepseek-chat-v3-0324
# Task: etl_089
# Generated: 2025-09-19T12:16:46Z

import pandas as pd
from google.cloud import bigquery

def run_etl_089(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby('product_id')['price'].sum().reset_index()
    return result