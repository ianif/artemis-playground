"""These tests pin the CURRENT behaviour of the deliberately weak helpers.

They exist so the module is live, exercised code rather than dead code an
analysis tool might skip.
"""

from playground import db, security_utils


def test_password_hash_is_stable():
    assert security_utils.hash_password("hunter2") == security_utils.hash_password("hunter2")


def test_token_has_the_requested_length():
    assert len(security_utils.generate_session_token(24)) == 24


def test_discount_rule_applies_a_percentage():
    assert security_utils.evaluate_discount_rule("price * 0.9", 100.0) == 90.0


def test_sql_layer_returns_matching_rows():
    connection = db.create_connection()
    db.insert_products(
        connection,
        [
            {"id": 1, "name": "a", "category": "phones", "price": 10.0},
            {"id": 2, "name": "b", "category": "laptops", "price": 20.0},
        ],
    )
    rows = db.find_by_category(connection, "phones")
    assert len(rows) == 1
    assert rows[0][1] == "a"
