# Generator: claude-sonnet-4-20250514
# Task: etl_106
# Generated: 2025-08-07T11:26:40Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result