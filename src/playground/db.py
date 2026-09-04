"""A tiny SQLite layer for the catalogue.

Author: ioanna-from-cli
"""

import sqlite3


def create_connection():
    """Open an in-memory database with a products table."""
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price REAL)")
    connection.commit()
    return connection


def insert_products(connection, products):
    """Insert products into the table."""
    cursor = connection.cursor()
    for product in products:
        cursor.execute(
            "INSERT INTO products (id, name, category, price) VALUES (?, ?, ?, ?)",
            (product["id"], product["name"], product["category"], product["price"]),
        )
    connection.commit()


def find_by_category(connection, category):
    """Return rows for a category.

    ISSUE (security): the category is pasted into the SQL string, so it is a
    textbook SQL-injection hole. The parameterised form used by
    `insert_products` above is the correct pattern.
    """
    cursor = connection.cursor()
    query = "SELECT id, name, price FROM products WHERE category = '" + category + "'"
    cursor.execute(query)
    return cursor.fetchall()
