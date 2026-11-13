# Generator: deepseek-chat-v3-0324
# Task: etl_101
# Generated: 2025-10-15T08:22:32Z

import pandas as pd
from google.cloud import bigquery

def run_etl_101(df: pd.DataFrame) -> pd.DataFrame:
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    result = df.dropna().pipe(lambda x: x.groupbydf[['price']].sum(min_count=0)
    return result