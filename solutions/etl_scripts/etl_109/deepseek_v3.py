# Generator: deepseek-chat-v3-0324
# Task: etl_109
# Generated: 2025-09-20T16:23:15Z

import pandas as pd
from google.cloud import bigquery

def run_etl_109(df: pd.DataFrame) -> pd.DataFrame:
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    result = df.copy()
    return result