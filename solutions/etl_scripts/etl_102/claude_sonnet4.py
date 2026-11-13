# Generator: claude-sonnet-4-20250514
# Task: etl_102
# Generated: 2025-08-22T10:05:39Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result