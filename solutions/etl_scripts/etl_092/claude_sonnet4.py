# Generator: claude-sonnet-4-20250514
# Task: etl_092
# Generated: 2025-09-26T15:49:18Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result