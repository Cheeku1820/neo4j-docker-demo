import psycopg2

from config import POSTGRES
from load_csv_to_postgres import load_csv_to_postgres
from load_postgres_to_neo4j import load_postgres_to_neo4j


def run_sql_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        sql = file.read()

    with psycopg2.connect(**POSTGRES) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def main():
    print("Step 1: loading CSV into Postgres...")
    load_csv_to_postgres()

    print("Step 2: transforming raw Postgres data...")
    run_sql_file("/postgres/transform.sql")

    print("Step 3: loading cleaned Postgres data into Neo4j...")
    load_postgres_to_neo4j()

    print("ETL pipeline complete.")


if __name__ == "__main__":
    main()
