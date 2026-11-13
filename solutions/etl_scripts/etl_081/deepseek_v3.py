# Generator: deepseek-chat-v3-0324
# Task: etl_081
# Generated: 2025-09-07T08:00:19Z

import pandas as pd
from google.cloud import bigquery

def run_etl_081(df: pd.DataFrame) -> pd.DataFrame:
    df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'])
    result = df.groupby('transaction_id')['amount_cents'].sum().reset_index()
    return result