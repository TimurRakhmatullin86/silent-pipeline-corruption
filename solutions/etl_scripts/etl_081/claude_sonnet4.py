# Generator: claude-sonnet-4-20250514
# Task: etl_081
# Generated: 2025-09-21T08:36:35Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'])
    result = df.groupby('transaction_id')['amount_cents'].sum().reset_index()
    return result