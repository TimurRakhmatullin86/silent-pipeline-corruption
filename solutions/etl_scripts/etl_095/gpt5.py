# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_095
# Generated: 2025-09-15T12:52:00Z

"""ETL: Process analytics data for inventory"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/users_ref.csv")
    merged = df.merge(ref, on="session_id", how="inner")
    merged["quantity"] = merged["quantity"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/orders.csv", "/data/processed/campaigns_clean.parquet")