# Generator: deepseek-chat-v3-0324
# Task: etl_117
# Generated: 2025-08-19T12:02:18Z

import pandas as pd
from google.cloud import bigquery

def run_etl_117(df: pd.DataFrame) -> pd.DataFrame:
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    result = df.copy()
    return result