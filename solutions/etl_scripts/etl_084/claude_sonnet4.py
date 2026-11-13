# Generator: claude-sonnet-4-20250514
# Task: etl_084
# Generated: 2025-10-09T12:41:19Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df.copy()
    return result