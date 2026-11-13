# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_081
# Generated: 2025-09-15T17:21:14Z

"""ETL: Process analytics data for subscriptions"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/sessions_ref.csv")
    merged = df.merge(ref, on="session_id", how="inner")
    merged["price"] = merged["price"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/orders.csv", "/data/processed/payments_clean.parquet")