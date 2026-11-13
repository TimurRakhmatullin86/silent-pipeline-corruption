# Generator: claude-sonnet-4-20250514
# Task: etl_109
# Generated: 2025-10-29T12:08:06Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    result = df.copy()
    return result