# Generator: claude-sonnet-4-20250514
# Task: etl_083
# Generated: 2025-08-03T13:19:11Z

import pandas as pd
from google.cloud import bigquery

def transform(df):
    df['{'rule_id': 'R005', 'type': 'freshness', 'column': 'updated_at', 'max_age_hours': 24, 'severity': 'critical'}'] = pd.to_datetime(df['{'rule_id': 'R005', 'type': 'freshness', 'column': 'updated_at', 'max_age_hours': 24, 'severity': 'critical'}'])
    result = df.copy()
    return result