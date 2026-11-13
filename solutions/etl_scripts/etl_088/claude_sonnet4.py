# Generator: claude-sonnet-4-20250514
# Task: etl_088
# Generated: 2025-09-26T15:15:54Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.groupby('account_id')['amount'].sum().reset_index()
    return result