import unittest
import sqlite3
import os

from database.db import (
    get_connection
)

# ==========================================
# TEST DATABASE
# ==========================================

class TestDatabase(
    unittest.TestCase
):

    # ======================================
    # CONNECTION
    # ======================================

    def test_connection(self):

        conn = get_connection()

        self.assertIsNotNone(
            conn
        )

        conn.close()

    # ======================================
    # DATABASE FILE
    # ======================================

    def test_database_exists(self):

        db_path = (
            "database/cricket.db"
        )

        exists = os.path.exists(
            db_path
        )

        self.assertTrue(exists)

    # ======================================
    # SQLITE VERSION
    # ======================================

    def test_sqlite_version(self):

        conn = sqlite3.connect(
            "database/cricket.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            "SELECT sqlite_version();"
        )

        version = cursor.fetchone()

        self.assertIsNotNone(
            version
        )

        conn.close()

    # ======================================
    # TABLES EXIST
    # ======================================

    def test_tables_exist(self):

        conn = sqlite3.connect(
            "database/cricket.db"
        )

        cursor = conn.cursor()

        tables = [

            "matches",

            "ball_by_ball",

            "players",

            "match_state",

            "tournaments",

            "points_table",

            "users"
        ]

        for table in tables:

            cursor.execute(

                """

                SELECT name

                FROM sqlite_master

                WHERE type='table'

                AND name=?

                """,

                (table,)
            )

            result = cursor.fetchone()

            self.assertIsNotNone(
                result
            )

        conn.close()

    # ======================================
    # INSERT TEST
    # ======================================

    def test_insert_query(self):

        conn = sqlite3.connect(
            "database/cricket.db"
        )

        cursor = conn.cursor()

        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS
            temp_test (

                id INTEGER
            )

            """
        )

        cursor.execute(

            """

            INSERT INTO temp_test
            (id)

            VALUES (1)

            """
        )

        conn.commit()

        cursor.execute(

            "SELECT * FROM temp_test"
        )

        row = cursor.fetchone()

        self.assertEqual(
            row[0],
            1
        )

        cursor.execute(
            "DROP TABLE temp_test"
        )

        conn.commit()

        conn.close()

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    unittest.main()