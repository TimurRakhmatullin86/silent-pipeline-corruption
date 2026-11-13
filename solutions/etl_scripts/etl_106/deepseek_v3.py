# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_106
# Generated: 2025-09-15T19:39:06Z

"""ETL: Process finance data for campaigns"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/shipments_ref.csv")
    merged = df.merge(ref, on="product_id", how="inner")
    merged["duration"] = merged["duration"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/events.csv", "/data/processed/inventory_clean.parquet")