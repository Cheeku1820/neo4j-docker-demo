LOAD CSV WITH HEADERS FROM 'file:///nationwide-drugs-fy23-fy26-apr.csv' AS row

WITH row
WHERE row.Component IS NOT NULL
  AND row.Region IS NOT NULL
  AND row.`Area of Responsibility` IS NOT NULL
  AND row.`Drug Type` IS NOT NULL

MERGE (component:Component {name: row.Component})
MERGE (region:Region {name: row.Region})
MERGE (area:Area {name: row.`Area of Responsibility`})
MERGE (drug:Drug {name: row.`Drug Type`})

MERGE (component)-[:OPERATES_IN]->(region)
MERGE (area)-[:PART_OF]->(region)

CREATE (record:SeizureRecord {
  fiscalYear: row.FY,
  month: row.`Month (abbv)`,
  landFilter: row.`Land Filter`,
  eventCount: toInteger(row.`Count of Event`),
  quantityLbs: toFloat(row.`Sum Qty (lbs)`)
})

CREATE (record)-[:BY_COMPONENT]->(component)
CREATE (record)-[:IN_REGION]->(region)
CREATE (record)-[:IN_AREA]->(area)
CREATE (record)-[:FOR_DRUG]->(drug);