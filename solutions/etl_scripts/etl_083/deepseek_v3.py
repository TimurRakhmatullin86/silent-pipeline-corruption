# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_083
# Generated: 2025-09-15T16:18:12Z

"""ETL: Process finance data for payments"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["score"] = df["score"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/invoices.csv", "/data/processed/logs_clean.parquet")