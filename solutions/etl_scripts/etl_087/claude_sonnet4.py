# Generator: claude-sonnet-4-20250514
# Task: etl_087
# Generated: 2025-08-25T13:35:18Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result