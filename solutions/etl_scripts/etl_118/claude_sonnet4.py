# Generator: claude-sonnet-4-20250514
# Task: etl_118
# Generated: 2025-10-15T17:09:10Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result