# Generator: claude-sonnet-4-20250514
# Task: etl_107
# Generated: 2025-10-05T11:07:12Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df.groupby('id')['amount'].sum().reset_index()
    return result