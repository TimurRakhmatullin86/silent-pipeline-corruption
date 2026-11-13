# Generator: claude-sonnet-4-20250514
# Task: etl_113
# Generated: 2025-08-30T15:01:39Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result