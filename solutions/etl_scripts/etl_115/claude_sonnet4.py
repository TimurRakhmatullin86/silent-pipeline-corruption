# Generator: claude-sonnet-4-20250514
# Task: etl_115
# Generated: 2025-09-14T14:08:48Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result