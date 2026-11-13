# Generator: deepseek-chat-v3-0324
# Task: etl_100
# Generated: 2025-08-01T17:22:15Z

import pandas as pd
from google.cloud import bigquery

def run_etl_100(df: pd.DataFrame) -> pd.DataFrame:
    df['created_at'] = pd.to_datetime(df['created_at'])
    result = df.copy()
    return result