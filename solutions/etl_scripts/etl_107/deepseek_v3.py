# Generator: deepseek-chat-v3-0324
# Task: etl_107
# Generated: 2025-08-20T14:41:06Z

import pandas as pd
from google.cloud import bigquery

def run_etl_107(df: pd.DataFrame) -> pd.DataFrame:
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df.groupby('id')['amount'].sum().reset_index()
    return result