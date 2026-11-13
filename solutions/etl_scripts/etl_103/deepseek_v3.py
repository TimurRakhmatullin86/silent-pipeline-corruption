# Generator: deepseek-chat-v3-0324
# Task: etl_103
# Generated: 2025-09-16T16:37:06Z

import pandas as pd
from google.cloud import bigquery

def run_etl_103(df: pd.DataFrame) -> pd.DataFrame:
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df.copy()
    return result