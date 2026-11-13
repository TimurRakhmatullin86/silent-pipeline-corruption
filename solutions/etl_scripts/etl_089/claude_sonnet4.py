# Generator: claude-sonnet-4-20250514
# Task: etl_089
# Generated: 2025-10-25T12:23:09Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.groupby('product_id')['price'].sum().reset_index()
    return result