DROP TABLE IF EXISTS measurements;

CREATE TABLE measurements(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    humidity REAL,
    measurement_date INTEGER(4) DEFAULT (strftime('%s', 'now'))
);