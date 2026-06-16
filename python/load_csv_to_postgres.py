import re
import time

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from config import CSV_PATH, POSTGRES


def normalize_column_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def wait_for_postgres(max_attempts: int = 30, delay_seconds: int = 2):
    for attempt in range(1, max_attempts + 1):
        try:
            conn = psycopg2.connect(**POSTGRES)
            conn.close()
            return
        except psycopg2.OperationalError:
            if attempt == max_attempts:
                raise
            time.sleep(delay_seconds)


def get_connection():
    return psycopg2.connect(**POSTGRES)


def load_csv_to_postgres(csv_path: str = CSV_PATH):
    wait_for_postgres()

    df = pd.read_csv(csv_path)
    df.columns = [normalize_column_name(col) for col in df.columns]
    df = df.dropna(how="all")

    expected_columns = [
        "component",
        "region",
        "area_of_responsibility",
        "drug_type",
        "fy",
        "month_abbv",
        "land_filter",
        "count_of_event",
        "sum_qty_lbs",
    ]

    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing expected columns: {missing_columns}")

    df = df[expected_columns]
    df = df.where(pd.notnull(df), None)

    rows = [tuple(row) for row in df.to_numpy()]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE raw_seizures;")
            execute_values(
                cur,
                """
                INSERT INTO raw_seizures (
                    component,
                    region,
                    area_of_responsibility,
                    drug_type,
                    fy,
                    month_abbv,
                    land_filter,
                    count_of_event,
                    sum_qty_lbs
                ) VALUES %s;
                """,
                rows,
            )

    print(f"Loaded {len(rows)} rows into Postgres raw_seizures.")


if __name__ == "__main__":
    load_csv_to_postgres()
