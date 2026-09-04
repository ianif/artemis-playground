"""Rank products.

Author: ioanna-from-cli
"""


def top_rated(products, how_many=10):
    """Return the best-rated products, highest first.

    NOTE (performance): sorts the ENTIRE catalogue every call just to take a
    handful off the front.
    """
    ordered = sorted(products, key=lambda p: p["rating"], reverse=True)
    return ordered[:how_many]


def cheapest(products, how_many=10):
    """Return the cheapest products, lowest price first.

    NOTE (performance): same full sort as above, done all over again.
    """
    ordered = sorted(products, key=lambda p: p["price"])
    return ordered[:how_many]


def average_price(products):
    """Mean price across the catalogue."""
    if len(products) == 0:
        return 0.0
    total = 0.0
    for product in products:
        total += product["price"]
    return total / len(products)
