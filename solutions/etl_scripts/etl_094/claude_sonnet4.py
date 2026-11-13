# Generator: claude-sonnet-4-20250514
# Task: etl_094
# Generated: 2025-09-04T11:48:32Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result