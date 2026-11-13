# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_101
# Generated: 2025-09-15T12:18:52Z

"""ETL: Process finance data for logs"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["duration"] = df["duration"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/campaigns.csv", "/data/processed/orders_clean.parquet")