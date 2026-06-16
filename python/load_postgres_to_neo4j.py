import time

import psycopg2
from psycopg2.extras import RealDictCursor
from neo4j import GraphDatabase

from config import POSTGRES, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def wait_for_neo4j(max_attempts: int = 30, delay_seconds: int = 2):
    for attempt in range(1, max_attempts + 1):
        try:
            driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD),
            )
            driver.verify_connectivity()
            driver.close()
            return
        except Exception:
            if attempt == max_attempts:
                raise
            time.sleep(delay_seconds)


def fetch_cleaned_rows():
    with psycopg2.connect(**POSTGRES) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    record_id,
                    component,
                    region,
                    area_of_responsibility,
                    drug_type,
                    fy,
                    month_abbv,
                    land_filter,
                    event_count,
                    quantity_lbs,
                    risk_level
                FROM cleaned_seizures;
                """
            )
            return cur.fetchall()


def create_constraints(session):
    constraints = [
        "CREATE CONSTRAINT component_name IF NOT EXISTS FOR (n:Component) REQUIRE n.name IS UNIQUE",
        "CREATE CONSTRAINT region_name IF NOT EXISTS FOR (n:Region) REQUIRE n.name IS UNIQUE",
        "CREATE CONSTRAINT area_name IF NOT EXISTS FOR (n:Area) REQUIRE n.name IS UNIQUE",
        "CREATE CONSTRAINT drug_name IF NOT EXISTS FOR (n:Drug) REQUIRE n.name IS UNIQUE",
        "CREATE CONSTRAINT seizure_record_id IF NOT EXISTS FOR (n:SeizureRecord) REQUIRE n.recordId IS UNIQUE",
    ]
    for query in constraints:
        session.run(query)


def load_rows_to_neo4j(rows):
    wait_for_neo4j()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    cypher = """
    UNWIND $rows AS row
    MERGE (component:Component {name: row.component})
    MERGE (region:Region {name: row.region})
    MERGE (area:Area {name: row.area_of_responsibility})
    MERGE (drug:Drug {name: row.drug_type})
    MERGE (record:SeizureRecord {recordId: row.record_id})
    SET record.fiscalYear = row.fy,
        record.month = row.month_abbv,
        record.landFilter = row.land_filter,
        record.eventCount = row.event_count,
        record.quantityLbs = row.quantity_lbs,
        record.riskLevel = row.risk_level
    MERGE (component)-[:OPERATES_IN]->(region)
    MERGE (area)-[:PART_OF]->(region)
    MERGE (record)-[:BY_COMPONENT]->(component)
    MERGE (record)-[:IN_REGION]->(region)
    MERGE (record)-[:IN_AREA]->(area)
    MERGE (record)-[:INVOLVES_DRUG]->(drug)
    """

    batch_size = 1000
    with driver.session() as session:
        create_constraints(session)
        for start in range(0, len(rows), batch_size):
            batch = rows[start : start + batch_size]
            session.run(cypher, rows=[dict(row) for row in batch])
            print(f"Loaded rows {start + 1}-{start + len(batch)} into Neo4j.")

    driver.close()


def load_postgres_to_neo4j():
    rows = fetch_cleaned_rows()
    load_rows_to_neo4j(rows)
    print(f"Finished loading {len(rows)} cleaned rows into Neo4j.")


if __name__ == "__main__":
    load_postgres_to_neo4j()
