# Generator: deepseek-chat-v3-0324
# Task: etl_097
# Generated: 2025-09-22T09:08:02Z

import pandas as pd
from google.cloud import bigquery

def run_etl_097(df: pd.DataFrame) -> pd.DataFrame:
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    result = df.groupby('payment_id')['amount'].sum().reset_index()
    return result