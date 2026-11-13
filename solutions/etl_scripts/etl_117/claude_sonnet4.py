# Generator: claude-sonnet-4-20250514
# Task: etl_117
# Generated: 2025-10-02T19:58:28Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    result = df.copy()
    return result