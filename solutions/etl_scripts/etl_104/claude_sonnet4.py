# Generator: claude-sonnet-4-20250514
# Task: etl_104
# Generated: 2025-10-18T19:53:19Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result