import os

CSV_PATH = os.getenv("CSV_PATH", "/data/raw/nationwide-drugs-fy23-fy26-apr.csv")

POSTGRES = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "dbname": os.getenv("POSTGRES_DB", "seizures"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
}

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j-seizures_apr2026:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
