"""Builds the product catalogue the rest of the package works on.

Author: ioanna-from-cli
"""

import random

# Deterministic on purpose, so two benchmark runs are comparable.
SEED = 42

CATEGORIES = ["laptops", "phones", "tablets", "monitors", "keyboards"]


def build_catalogue(size=4000):
    """Return a list of product dictionaries.

    Each product has an id, a name, a category and a price.
    """
    random.seed(SEED)
    products = []
    for i in range(size):
        products.append(
            {
                "id": i,
                "name": "product-%d" % i,
                "category": CATEGORIES[i % len(CATEGORIES)],
                "price": round(random.uniform(5.0, 2000.0), 2),
                "rating": round(random.uniform(1.0, 5.0), 2),
            }
        )
    return products
