CREATE TABLE IF NOT EXISTS raw_seizures (
    id BIGSERIAL PRIMARY KEY,
    component TEXT,
    region TEXT,
    area_of_responsibility TEXT,
    drug_type TEXT,
    fy TEXT,
    month_abbv TEXT,
    land_filter TEXT,
    count_of_event TEXT,
    sum_qty_lbs TEXT
);

CREATE TABLE IF NOT EXISTS cleaned_seizures (
    record_id TEXT PRIMARY KEY,
    component TEXT NOT NULL,
    region TEXT NOT NULL,
    area_of_responsibility TEXT NOT NULL,
    drug_type TEXT NOT NULL,
    fy TEXT,
    month_abbv TEXT,
    land_filter TEXT,
    event_count INTEGER,
    quantity_lbs NUMERIC,
    risk_level TEXT
);
