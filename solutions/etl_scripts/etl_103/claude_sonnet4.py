# Generator: claude-sonnet-4-20250514
# Task: etl_103
# Generated: 2025-10-20T16:36:15Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df.copy()
    return result