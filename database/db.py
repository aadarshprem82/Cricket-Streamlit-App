import sqlite3
from pathlib import Path

# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "cricket.db"

SCHEMA_PATH = BASE_DIR / "schema.sql"

# ==========================================
# SQLITE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(

        DB_PATH,

        check_same_thread=False
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection

# ==========================================
# EXECUTE QUERY
# ==========================================

def execute_query(

    query,
    params=()
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            query,
            params
        )

        connection.commit()

    except Exception as error:

        connection.rollback()

        raise error

    finally:

        connection.close()

# ==========================================
# EXECUTE MANY
# ==========================================

def execute_many(

    query,
    data
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.executemany(
            query,
            data
        )

        connection.commit()

    except Exception as error:

        connection.rollback()

        raise error

    finally:

        connection.close()

# ==========================================
# FETCH ALL
# ==========================================

def fetch_all(

    query,
    params=()
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            query,
            params
        )

        rows = cursor.fetchall()

        return [

            dict(row)
            for row in rows
        ]

    finally:

        connection.close()

# ==========================================
# FETCH ONE
# ==========================================

def fetch_one(

    query,
    params=()
):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            query,
            params
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:

        connection.close()

# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    if not SCHEMA_PATH.exists():

        raise FileNotFoundError(

            "schema.sql not found."
        )

    connection = get_connection()

    cursor = connection.cursor()

    try:

        with open(

            SCHEMA_PATH,

            "r",

            encoding="utf-8"

        ) as schema_file:

            schema_sql = (
                schema_file.read()
            )

        cursor.executescript(
            schema_sql
        )

        connection.commit()

    except Exception as error:

        connection.rollback()

        raise error

    finally:

        connection.close()

# ==========================================
# DATABASE HEALTH CHECK
# ==========================================

def database_health_check():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1"
        )

        connection.close()

        return True

    except:
        return False

# ==========================================
# CLEAR TABLE
# ==========================================

def clear_table(
    table_name
):

    query = (
        f"DELETE FROM {table_name}"
    )

    execute_query(query)

# ==========================================
# TABLE EXISTS
# ==========================================

def table_exists(
    table_name
):

    query = """

    SELECT name

    FROM sqlite_master

    WHERE type='table'

    AND name=?

    """

    result = fetch_one(

        query,

        (table_name,)
    )

    return result is not None

# ==========================================
# GET TABLE ROW COUNT
# ==========================================

def get_row_count(
    table_name
):

    query = (
        f"SELECT COUNT(*) AS count "
        f"FROM {table_name}"
    )

    result = fetch_one(query)

    if not result:
        return 0

    return result["count"]

# ==========================================
# VACUUM DATABASE
# ==========================================

def vacuum_database():

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("VACUUM")

        connection.commit()

    finally:

        connection.close()

# ==========================================
# BACKUP DATABASE
# ==========================================

def backup_database(
    backup_path
):

    source = sqlite3.connect(
        DB_PATH
    )

    destination = sqlite3.connect(
        backup_path
    )

    try:

        source.backup(destination)

    finally:

        source.close()

        destination.close()

# ==========================================
# SQLITE VERSION
# ==========================================

def get_sqlite_version():

    query = (
        "SELECT sqlite_version() "
        "AS version"
    )

    result = fetch_one(query)

    if not result:
        return "Unknown"

    return result["version"]