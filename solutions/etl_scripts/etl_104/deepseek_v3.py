# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_104
# Generated: 2025-09-15T12:30:40Z

"""ETL: Process ops data for users"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["impressions"] = df["impressions"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/products.csv", "/data/processed/transactions_clean.parquet")