DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'superset') THEN
        CREATE ROLE superset LOGIN PASSWORD 'replace_with_a_database_password';
    END IF;
END
$$;

ALTER ROLE superset WITH PASSWORD 'replace_with_a_database_password';

SELECT 'CREATE DATABASE superset_db OWNER superset'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'superset_db')\gexec

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'examples') THEN
        CREATE ROLE examples LOGIN PASSWORD 'replace_with_an_examples_password';
    END IF;
END
$$;

ALTER ROLE examples WITH PASSWORD 'replace_with_an_examples_password';

SELECT 'CREATE DATABASE example_db OWNER examples'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'example_db')\gexec