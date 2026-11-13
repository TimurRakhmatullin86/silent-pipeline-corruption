# Generator: claude-sonnet-4-20250514
# Task: etl_086
# Generated: 2025-09-03T18:23:44Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['snapshot_date'] = pd.to_datetime(df['snapshot_date'])
    result = df.dropna().pipe(lambda x: x.groupbydf.copy()
    return result