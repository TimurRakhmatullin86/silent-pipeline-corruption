# Generator: claude-sonnet-4-20250514
# Task: etl_090
# Generated: 2025-10-13T14:45:40Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result