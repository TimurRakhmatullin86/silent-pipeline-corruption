# Generator: claude-sonnet-4-20250514
# Task: etl_120
# Generated: 2025-10-23T12:15:07Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.dropna().pipe(lambda x: x.groupbydf.copy()
    return result