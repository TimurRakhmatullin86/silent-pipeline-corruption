# Generator: claude-sonnet-4-20250514
# Task: etl_108
# Generated: 2025-10-12T12:30:52Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result