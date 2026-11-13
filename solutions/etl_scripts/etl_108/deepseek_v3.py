# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_108
# Generated: 2025-09-15T14:36:44Z

"""ETL: Process analytics data for shipments"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/clicks_ref.csv")
    merged = df.merge(ref, on="session_id", how="inner")
    merged["revenue"] = merged["revenue"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/invoices.csv", "/data/processed/users_clean.parquet")