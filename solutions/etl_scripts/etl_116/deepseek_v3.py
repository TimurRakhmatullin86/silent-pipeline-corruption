# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_116
# Generated: 2025-09-15T11:15:50Z

"""ETL: Process marketing data for logs"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["impressions"] = df["impressions"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/campaigns.csv", "/data/processed/subscriptions_clean.parquet")