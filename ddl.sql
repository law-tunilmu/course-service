CREATE TABLE IF NOT EXISTS course (
	id SERIAL PRIMARY KEY,
	title VARCHAR(500) ,
	description TEXT,
	creator VARCHAR(100),
	picture_url VARCHAR(200),
	created_at timestamp,
	last_update_at timestamp,
	price FLOAT,
	tfs tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, ''))) STORED
);

CREATE INDEX tfs_idx ON course USING GIN (tfs);