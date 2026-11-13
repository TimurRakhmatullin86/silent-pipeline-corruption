# Generator: claude-sonnet-4-20250514
# Task: etl_095
# Generated: 2025-10-27T18:51:44Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result