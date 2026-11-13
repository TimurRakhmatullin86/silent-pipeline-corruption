# Generator: deepseek-chat-v3-0324
# Task: etl_105
# Generated: 2025-09-19T09:23:14Z

import pandas as pd
from google.cloud import bigquery

def run_etl_105(df: pd.DataFrame) -> pd.DataFrame:
    df['created_at'] = pd.to_datetime(df['created_at'])
    result = df.copy()
    return result