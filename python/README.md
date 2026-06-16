# Python ETL Middleware

This folder contains the Python layer that connects the raw CSV dataset, Postgres, and Neo4j.

## Flow

```text
CSV -> Postgres raw table -> Postgres cleaned table -> Python -> Neo4j graph
```

## Files

- `load_csv_to_postgres.py` reads the CSV, normalizes column names, validates required columns, and inserts rows into `raw_seizures`.
- `run_pipeline.py` runs the full pipeline end-to-end.
- `load_postgres_to_neo4j.py` reads `cleaned_seizures` from Postgres and creates Neo4j nodes/relationships using Cypher through the Neo4j Python driver.
- `config.py` centralizes environment variables.
- `requirements.txt` lists Python dependencies.
- `Dockerfile` builds the ETL container.

## Run

From the repo root:

```bash
docker compose up -d postgres neo4j-seizures_apr2026
docker compose run --rm python-etl
```

By default, the ETL expects the CSV at:

```text
import/seizures_apr2026/nationwide-drugs-fy23-fy26-apr.csv
```

You can override it with `CSV_PATH` in `docker-compose.yml` if needed.
