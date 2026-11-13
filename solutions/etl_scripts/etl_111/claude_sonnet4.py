# Generator: claude-sonnet-4-20250514
# Task: etl_111
# Generated: 2025-08-10T14:32:28Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    result = df.copy()
    return result