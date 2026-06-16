TRUNCATE TABLE cleaned_seizures;

INSERT INTO cleaned_seizures (
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
)
SELECT
    md5(concat_ws('|', id, component, region, area_of_responsibility, drug_type, fy, month_abbv, land_filter)) AS record_id,
    initcap(trim(component)) AS component,
    initcap(trim(region)) AS region,
    initcap(trim(area_of_responsibility)) AS area_of_responsibility,
    initcap(trim(drug_type)) AS drug_type,
    trim(fy) AS fy,
    upper(trim(month_abbv)) AS month_abbv,
    initcap(trim(land_filter)) AS land_filter,
    nullif(regexp_replace(count_of_event, '[^0-9]', '', 'g'), '')::integer AS event_count,
    nullif(regexp_replace(sum_qty_lbs, '[^0-9.]', '', 'g'), '')::numeric AS quantity_lbs,
    CASE
        WHEN nullif(regexp_replace(sum_qty_lbs, '[^0-9.]', '', 'g'), '')::numeric >= 1000 THEN 'High'
        WHEN nullif(regexp_replace(sum_qty_lbs, '[^0-9.]', '', 'g'), '')::numeric >= 100 THEN 'Medium'
        ELSE 'Low'
    END AS risk_level
FROM raw_seizures
WHERE component IS NOT NULL
  AND region IS NOT NULL
  AND area_of_responsibility IS NOT NULL
  AND drug_type IS NOT NULL;
