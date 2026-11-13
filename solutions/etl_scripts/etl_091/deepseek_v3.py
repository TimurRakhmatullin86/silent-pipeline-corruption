# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_091
# Generated: 2025-09-15T14:00:20Z

"""ETL: Process analytics data for products"""
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def extract(source: str) -> pd.DataFrame:
    df = pd.read_csv(source, dtype={"id": str}, encoding="utf-8")
    logger.info("Extracted %d rows from %s", len(df), source)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["conversions"] = pd.to_numeric(df["conversions"], errors="coerce")
    df = df.dropna(subset=["conversions"])
    df["conversions_clean"] = df["conversions"].round(2)
    return df


def load(df: pd.DataFrame, target: str) -> None:
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target, index=False)
    logger.info("Loaded %d rows to %s", len(df), target)


if __name__ == "__main__":
    raw = extract("/data/raw/tickets.csv")
    clean = transform(raw)
    load(clean, "/data/processed/subscriptions_clean.parquet")