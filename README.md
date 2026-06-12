# Neo4j Drug Seizures Graph Project

This project uses Docker Compose and Neo4j to build a graph database from a CSV dataset of nationwide drug seizure records.

The graph models seizure records as connected entities such as drugs, regions, components, and areas of responsibility.

## Project Structure

```text
project/
  docker-compose.yml
  README.md
  import/
    seizures_apr2026/
      nationwide-drugs-fy23-fy26-apr.csv
    normal/
  cypher/
    seizures_apr2026/
      01_constraints.cypher
      02_import.cypher
      03_example_queries.cypher
      04_clear_database.cypher
    normal/
      01_constraints.cypher
      02_import.cypher
      03_example_queries.cypher
```

## How the Docker Mounts Work

In `docker-compose.yml`, the seizures Neo4j container has this volume:

```yaml
- ./import/seizures_apr2026:/var/lib/neo4j/import
```

This means the local folder:

```text
./import/seizures_apr2026
```

is mounted inside the Neo4j container as:

```text
/var/lib/neo4j/import
```

So the CSV file:

```text
./import/seizures_apr2026/nationwide-drugs-fy23-fy26-apr.csv
```

is seen by Neo4j as:

```text
/var/lib/neo4j/import/nationwide-drugs-fy23-fy26-apr.csv
```

Inside Cypher, the file is referenced like this:

```cypher
LOAD CSV WITH HEADERS FROM 'file:///nationwide-drugs-fy23-fy26-apr.csv' AS row
```

The Cypher folder is also mounted:

```yaml
- ./cypher/seizures_apr2026:/cypher
```

This means the local folder:

```text
./cypher/seizures_apr2026
```

is available inside the container as:

```text
/cypher
```

That lets us run Cypher scripts from the terminal.

## Start Neo4j

From the project root, run:

```bash
docker compose up -d
```

This starts both Neo4j containers.

The seizures database is available at:

```text
http://localhost:7474
```

Login:

```text
Username: neo4j
Password: password123
```

The normal database is available at:

```text
http://localhost:7475
```

Login:

```text
Username: neo4j
Password: password123
```

## Check That the CSV Is Mounted

Run:

```bash
docker exec -it neo4j-seizures-april2026 ls -l /var/lib/neo4j/import
```

You should see:

```text
nationwide-drugs-fy23-fy26-apr.csv
```

## Check That the Cypher Files Are Mounted

Run:

```bash
docker exec -it neo4j-seizures-april2026 ls -l /cypher
```

You should see files like:

```text
01_constraints.cypher
02_import.cypher
03_example_queries.cypher
04_clear_database.cypher
```

## Build the Graph

First, create the constraints:

```bash
docker exec -it neo4j-seizures-april2026 cypher-shell -u neo4j -p password123 -f /cypher/01_constraints.cypher
```

Then import the CSV data:

```bash
docker exec -it neo4j-seizures-april2026 cypher-shell -u neo4j -p password123 -f /cypher/02_imports.cypher
```

## Run Example Queries

To run the example queries file:

```bash
docker exec -it neo4j-seizures-april2026 cypher-shell -u neo4j -p password123 -f /cypher/03_example_queries.cypher
```

You can also open Neo4j Browser at:

```text
http://localhost:7474
```

and manually run queries from:

```text
cypher/seizures_apr2026/03_example_queries.cypher
```

## Clear the Database

To delete all nodes and relationships:

```bash
docker exec -it neo4j-seizures-april2026 cypher-shell -u neo4j -p password123 -f /cypher/04_clear_database.cypher
```

Then rerun the import:

```bash
docker exec -it neo4j-seizures-april2026 cypher-shell -u neo4j -p password123 -f /cypher/02_imports.cypher
```

## How Someone Else Can Recreate the Graph

After cloning the repository, another person can run:

```bash
docker compose up -d
```

Then:

```bash
docker exec -it neo4j-seizures-april2026 cypher-shell -u neo4j -p password123 -f /cypher/01_constraints.cypher
```

Then:

```bash
docker exec -it neo4j-seizures-april2026 cypher-shell -u neo4j -p password123 -f /cypher/02_imports.cypher
```

After that, they can open:

```text
http://localhost:7474
```

and see the recreated graph in their own local Neo4j instance.

## Important Note

The actual Neo4j database created on one machine is not stored in GitHub.

GitHub stores the files needed to recreate the graph:

```text
CSV data + Cypher scripts + Docker Compose setup
```

When someone clones the repo, Docker creates a fresh Neo4j database on their machine. The Cypher import script rebuilds the graph from the CSV.
