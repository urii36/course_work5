import psycopg2


def create_tables(database_name, params):
    """Создание базы данных и таблиц для сохранения данных."""

    conn = psycopg2.connect(**params)
    conn.autocommit = True

    with conn.cursor() as cur:
        # Проверка существования базы данных
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database_name,))
        database_exists = cur.fetchone()

        if not database_exists:
            cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()
    params.update({'dbname': database_name})

    conn = psycopg2.connect(**params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(id),
                name VARCHAR(255) NOT NULL,
                requirement TEXT,
                salary_from VARCHAR(100),
                salary_to VARCHAR(100),
                description TEXT,
                area VARCHAR(255),
                alternate_url TEXT
            )
        """)
    conn.close()
