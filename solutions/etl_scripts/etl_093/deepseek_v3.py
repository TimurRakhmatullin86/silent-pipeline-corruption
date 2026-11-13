# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_093
# Generated: 2025-09-15T10:48:12Z

"""ETL: Process finance data for clicks"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/tickets_ref.csv")
    merged = df.merge(ref, on="session_id", how="inner")
    merged["score"] = merged["score"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/clicks.csv", "/data/processed/inventory_clean.parquet")