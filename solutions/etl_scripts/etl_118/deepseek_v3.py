# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_118
# Generated: 2025-09-15T18:00:40Z

"""ETL: Process ops data for transactions"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/orders_ref.csv")
    merged = df.merge(ref, on="product_id", how="inner")
    merged["score"] = merged["score"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/users.csv", "/data/processed/campaigns_clean.parquet")