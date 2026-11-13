# Generator: claude-sonnet-4-20250514
# Task: etl_097
# Generated: 2025-08-20T15:47:38Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    result = df.groupby('payment_id')['amount'].sum().reset_index()
    return result