CREATE TABLE IF NOT EXISTS 'country_numbers'(
    'get_datetime' TEXT NOT NULL,
    'country_name' TEXT NOT NULL,
    'cases' INTEGER,
    'deaths' INTEGER,
    'deaths_rate' DECIMAL(10,4),
    'recovery' INTEGER, 
    'recovery_rate' DECIMAL(10,4),
    'original_last_modification' TEXT,
    PRIMARY KEY ('get_datetime', 'country_name')
)