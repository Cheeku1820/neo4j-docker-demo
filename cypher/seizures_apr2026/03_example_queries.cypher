// Count nodes by label
MATCH (n)
RETURN labels(n) AS labels, count(n) AS count
ORDER BY count DESC;


// Top drugs by total seized pounds
MATCH (record:SeizureRecord)-[:FOR_DRUG]->(drug:Drug)
RETURN drug.name AS drug, sum(record.quantityLbs) AS totalPounds
ORDER BY totalPounds DESC
LIMIT 10;


// Top areas by total seized pounds
MATCH (record:SeizureRecord)-[:IN_AREA]->(area:Area)
RETURN area.name AS area, sum(record.quantityLbs) AS totalPounds
ORDER BY totalPounds DESC
LIMIT 10;


// Top regions by total seized pounds
MATCH (record:SeizureRecord)-[:IN_REGION]->(region:Region)
RETURN region.name AS region, sum(record.quantityLbs) AS totalPounds
ORDER BY totalPounds DESC;


// Drug seizures by fiscal year
MATCH (record:SeizureRecord)-[:FOR_DRUG]->(drug:Drug)
RETURN record.fiscalYear AS fiscalYear, drug.name AS drug, sum(record.quantityLbs) AS totalPounds
ORDER BY fiscalYear, totalPounds DESC;


// Visual graph sample
MATCH (area:Area)<-[:IN_AREA]-(record:SeizureRecord)-[:FOR_DRUG]->(drug:Drug)
RETURN area, record, drug
LIMIT 100;


// Component to region graph
MATCH (component:Component)-[:OPERATES_IN]->(region:Region)
RETURN component, region;


// Area to region graph
MATCH (area:Area)-[:PART_OF]->(region:Region)
RETURN area, region
LIMIT 100;