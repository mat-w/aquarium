DROP TABLE IF EXISTS temperatures;

CREATE TABLE temperatures(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	read_datetime TIMESTAMP,
	temperature REAL
)
