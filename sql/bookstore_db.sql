-- Tabellen erstellen:
CREATE TABLE books 
(
	id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	author VARCHAR(255) NOT NULL,
	publication_year INT NOT NULL,
	publisher VARCHAR(255) NOT NULL,
	pages INT NOT NULL,
	price NUMERIC(10,2) NOT NULL,
	in_stock INT NOT NULL
);

CREATE TABLE ebooks 
(
	id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	author VARCHAR(255) NOT NULL,
	publication_year INT NOT NULL,
	publisher VARCHAR(255) NOT NULL,
	pages INT NOT NULL,
	price NUMERIC(10,2) NOT NULL
);

CREATE TABLE movies
(
	id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	publication_year INT NOT NULL,
	publisher VARCHAR(255) NOT NULL,
	price NUMERIC(10,2) NOT NULL,
	in_stock INT NOT NULL
);

CREATE TABLE logs
(
	id SERIAL PRIMARY KEY,
	table_name VARCHAR(255) NOT NULL,
	item_id INT NOT NULL,
	operation VARCHAR(255) NOT NULL,
	old_data JSONB,
	new_data JSONB,
	timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- sequences auf 30 setzen
SELECT setval(pg_get_serial_sequence('books', 'id'), (SELECT MAX(id) FROM books));
SELECT setval(pg_get_serial_sequence('ebooks', 'id'), (SELECT MAX(id) FROM ebooks));
SELECT setval(pg_get_serial_sequence('movies', 'id'), (SELECT MAX(id) FROM movies));

-- api_user
CREATE USER api_user WITH PASSWORD 'api_user123';

GRANT USAGE ON SCHEMA public TO api_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO api_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO api_user;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO api_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO api_user;


-- trigger function:
CREATE OR REPLACE
FUNCTION log_ops_with_data() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs
    (
	    table_name,
		item_id,
	    operation,
	    old_data,
	    new_data
    )
    VALUES 
    (
        TG_TABLE_NAME,
		CASE
            WHEN TG_OP IN ('INSERT', 'UPDATE') THEN NEW.id
            WHEN TG_OP = 'DELETE' THEN OLD.id
        END,
        TG_OP,
	    CASE
			WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD)
			ELSE NULL
	    END,
	    CASE
			WHEN TG_OP IN ('UPDATE', 'INSERT') THEN to_jsonb(NEW)
			ELSE NULL
	    END
    );

RETURN NEW;
END;

$$ LANGUAGE plpgsql;

-- trigger auf tabellen setzen:
CREATE TRIGGER logs_on_books
AFTER INSERT OR UPDATE OR DELETE ON books
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();

CREATE TRIGGER logs_on_ebooks
AFTER INSERT OR UPDATE OR DELETE ON ebooks
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();

CREATE TRIGGER logs_on_movies
AFTER INSERT OR UPDATE OR DELETE ON movies
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();
