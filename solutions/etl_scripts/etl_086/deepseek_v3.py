# Generator: deepseek-chat-v3-0324
# Task: etl_086
# Generated: 2025-09-17T12:47:01Z

import pandas as pd
from google.cloud import bigquery

def run_etl_086(df: pd.DataFrame) -> pd.DataFrame:
    df['snapshot_date'] = pd.to_datetime(df['snapshot_date'])
    result = df.copy()
    return result