# Generator: deepseek-chat-v3-0324
# Task: etl_083
# Generated: 2025-10-28T18:01:38Z

import pandas as pd
from google.cloud import bigquery

def run_etl_083(df: pd.DataFrame) -> pd.DataFrame:
    df['{'rule_id': 'R005', 'type': 'freshness', 'column': 'updated_at', 'max_age_hours': 24, 'severity': 'critical'}'] = pd.to_datetime(df['{'rule_id': 'R005', 'type': 'freshness', 'column': 'updated_at', 'max_age_hours': 24, 'severity': 'critical'}'])
    result = df.copy()
    return result