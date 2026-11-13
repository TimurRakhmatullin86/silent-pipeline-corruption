# Generator: claude-sonnet-4-20250514
# Task: etl_098
# Generated: 2025-09-26T08:37:23Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.dropna().pipe(lambda x: x.groupbydf.copy()
    return result