# Generator: claude-sonnet-4-20250514
# Task: etl_101
# Generated: 2025-08-16T12:49:16Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df[['price']].sum()
    return result