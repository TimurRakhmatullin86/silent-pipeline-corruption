# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_101
# Generated: 2025-09-15T10:26:00Z

"""ETL: Process finance data for logs"""
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
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df = df.dropna(subset=["duration"])
    df["duration_clean"] = df["duration"].round(2)
    return df


def load(df: pd.DataFrame, target: str) -> None:
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target, index=False)
    logger.info("Loaded %d rows to %s", len(df), target)


if __name__ == "__main__":
    raw = extract("/data/raw/campaigns.csv")
    clean = transform(raw)
    load(clean, "/data/processed/orders_clean.parquet")