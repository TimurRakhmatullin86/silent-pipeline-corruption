# Generator: deepseek-chat-v3-0324
# Task: etl_084
# Generated: 2025-09-14T08:26:03Z

import pandas as pd
from google.cloud import bigquery

def run_etl_084(df: pd.DataFrame) -> pd.DataFrame:
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df.copy()
    return result