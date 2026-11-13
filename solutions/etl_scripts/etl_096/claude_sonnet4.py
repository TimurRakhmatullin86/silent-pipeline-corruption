# Generator: claude-sonnet-4-20250514
# Task: etl_096
# Generated: 2025-10-02T16:42:19Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result