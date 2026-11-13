# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_105
# Generated: 2025-09-15T17:09:26Z

"""ETL: Process ops data for tickets"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/campaigns_ref.csv")
    merged = df.merge(ref, on="product_id", how="inner")
    merged["revenue"] = merged["revenue"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/logs.csv", "/data/processed/tickets_clean.parquet")