# Generator: claude-sonnet-4-20250514
# Task: etl_114
# Generated: 2025-09-06T11:47:05Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result