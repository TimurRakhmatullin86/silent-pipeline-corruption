# Generator: claude-sonnet-4-20250514
# Task: etl_100
# Generated: 2025-10-31T15:06:43Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    result = df.copy()
    return result